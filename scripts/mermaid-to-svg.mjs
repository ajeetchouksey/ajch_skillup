/**
 * Converts ```mermaid blocks in notes to static, AaryaAI-branded SVG files.
 *
 *   node scripts/mermaid-to-svg.mjs [--exam <id>] [--file <notes.md>] [--dry]
 *   python scripts/embed-svg-fonts.py --fonts <dir> <svg>...   (then embed fonts)
 *
 * Why: notes used to render Mermaid live in the browser, which clipped labels
 * and looked different from the hand-built brand diagrams. Each block becomes
 *   content/skillup/{exam}/images/{note}-m{n}.svg       (the picture)
 *   scripts/diagrams/mermaid/{exam}/{note}-m{n}.mmd      (its source, to re-render)
 * and the block is replaced by an image with alt text built from its labels.
 *
 * Rendering uses Playwright + the mermaid package from the sibling ajch_platform
 * checkout (PLATFORM_DIR, default ../ajch_platform), so this repo needs no deps.
 * Labels are SVG <text> (htmlLabels off) because notes load diagrams through
 * <img>, which can't render HTML labels or see web fonts — embed-svg-fonts.py
 * adds subset Barlow afterwards. Palette: scripts/build-svg-diagrams.py header.
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'fs';
import { join, dirname, basename } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SKILLUP = join(ROOT, 'content/skillup');
const PLATFORM = process.env.PLATFORM_DIR ?? join(ROOT, '../ajch_platform');
const FONTS = process.env.FONTS_DIR;
const MERMAID_RE = /```mermaid\r?\n([\s\S]*?)```/g;

const arg = (k) => { const i = process.argv.indexOf(k); return i === -1 ? null : process.argv[i + 1]; };
const DRY = process.argv.includes('--dry');
const onlyExam = arg('--exam');
const onlyFile = arg('--file');

const require = createRequire(join(PLATFORM, 'package.json'));
const { chromium } = require('playwright');
const mermaidJs = readFileSync(join(PLATFORM, 'node_modules/mermaid/dist/mermaid.min.js'), 'utf8');

// Decorative emoji in labels: the brand diagrams don't use them, and <img> SVGs
// fall back to whatever emoji font the viewer's system has.
const EMOJI = /(?:\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}])(?:\u{FE0F}|\u{200D}|\u{20E3})*\s?/gu;

const THEME = {
  background: '#0e1a2d',
  fontFamily: 'Barlow, sans-serif',
  fontSize: '15px',
  primaryColor: '#1a2a42', primaryTextColor: '#e2e8f0', primaryBorderColor: '#334155',
  secondaryColor: '#162236', secondaryTextColor: '#e2e8f0', secondaryBorderColor: '#5ec8f2',
  tertiaryColor: '#111f35', tertiaryTextColor: '#e2e8f0', tertiaryBorderColor: '#334155',
  lineColor: '#64748b', textColor: '#e2e8f0', mainBkg: '#1a2a42', nodeBorder: '#334155',
  edgeLabelBackground: '#162236', clusterBkg: '#111f35', clusterBorder: '#334155', titleColor: '#ffffff',
  noteBkgColor: '#2a1a22', noteTextColor: '#e2e8f0', noteBorderColor: '#f5b94a',
  actorBkg: '#1a2a42', actorBorder: '#A99BFF', actorTextColor: '#e2e8f0', actorLineColor: '#475569',
  signalColor: '#94a3b8', signalTextColor: '#e2e8f0', labelBoxBkgColor: '#162236', labelBoxBorderColor: '#334155',
  labelTextColor: '#e2e8f0', loopTextColor: '#e2e8f0', activationBkgColor: '#5B4BD6', activationBorderColor: '#A99BFF',
  sequenceNumberColor: '#ffffff',
  // state / class / pie / journey
  labelColor: '#e2e8f0', altBackground: '#162236', compositeBackground: '#111f35', compositeTitleBackground: '#1a2a42',
  // pie slices follow the SkillUp colour code's domain order (colour-code.json), indigo first
  pie1: '#5B4BD6', pie2: '#5EC8F2', pie3: '#3DD9B3', pie4: '#F5B94A', pie5: '#FF8A7A', pie6: '#E58AE8', pie7: '#A99BFF',
  pieTitleTextColor: '#ffffff', pieSectionTextColor: '#ffffff', pieLegendTextColor: '#e2e8f0', pieStrokeColor: '#0e1a2d',
  cScale0: '#5B4BD6', cScale1: '#1a2a42', cScale2: '#162236', cScale3: '#111f35',
};

const KIND = [
  [/^\s*(graph|flowchart)\b/, 'Flow diagram'], [/^\s*sequenceDiagram/, 'Sequence diagram'],
  [/^\s*stateDiagram/, 'State diagram'], [/^\s*classDiagram/, 'Class diagram'], [/^\s*mindmap/, 'Mind map'],
  [/^\s*timeline/, 'Timeline'], [/^\s*pie/, 'Pie chart'], [/^\s*quadrantChart/, 'Quadrant chart'],
  [/^\s*journey/, 'Journey'], [/^\s*erDiagram/, 'Entity diagram'], [/^\s*gantt/, 'Timeline'],
];

function fontFace() {
  if (!FONTS) return '';
  const face = (file, weight) => {
    const p = join(FONTS, file);
    return existsSync(p) ? `@font-face{font-family:Barlow;font-weight:${weight};src:url(data:font/ttf;base64,${readFileSync(p).toString('base64')})}` : '';
  };
  return face('Barlow-Regular.ttf', '100 450') + face('Barlow-Medium.ttf', '451 900');
}

/** Pad the viewBox, size the SVG to it and lay a rounded brand plate behind it. */
function finish(svg) {
  const vb = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);
  if (!vb) return svg;
  const P = 16;
  const [x, y, w, h] = vb.slice(1).map(Number);
  const nx = x - P, ny = y - P, nw = Math.ceil(w + 2 * P), nh = Math.ceil(h + 2 * P);
  return svg
    .replace(vb[0], `viewBox="${nx} ${ny} ${nw} ${nh}"`)
    .replace(/\swidth="[^"]*"/, ` width="${nw}"`)
    .replace(/style="max-width:[^"]*"/, `height="${nh}"`)
    .replace(/(<svg[^>]*>)/, `$1<rect x="${nx}" y="${ny}" width="${nw}" height="${nh}" rx="16" fill="#0e1a2d"/>`);
}

function nearestHeading(md, index) {
  const before = md.slice(0, index).split('\n').reverse();
  const h = before.find((l) => /^#{2,3}\s/.test(l));
  return h ? h.replace(/^#+\s*/, '').replace(EMOJI, '').replace(/[*_`]/g, '').trim() : null;
}

function altText(code, labels, heading) {
  const kind = (KIND.find(([re]) => re.test(code)) ?? [null, 'Diagram'])[1];
  const uniq = [...new Set(labels.map((l) => l.replace(/\s+/g, ' ').trim()).filter((l) => l.length > 1))].slice(0, 10);
  const head = heading ? `${kind} for "${heading.replace(/"/g, "'")}"` : kind;
  return `${head}${uniq.length ? `: ${uniq.join(', ')}` : ''}`.replace(/[[\]()]/g, '').slice(0, 400);
}

const files = [];
for (const exam of readdirSync(SKILLUP, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name)) {
  if (onlyExam && exam !== onlyExam) continue;
  const notesDir = join(SKILLUP, exam, 'notes');
  if (!existsSync(notesDir)) continue;
  for (const f of readdirSync(notesDir).filter((n) => n.endsWith('.md'))) {
    if (onlyFile && f !== onlyFile) continue;
    files.push({ exam, path: join(notesDir, f) });
  }
}

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent(`<!doctype html><html><head><style>${fontFace()} body{margin:0;background:#0e1a2d;font-family:Barlow,sans-serif}</style></head><body><div id="c"></div><script>${mermaidJs}</script></body></html>`);
await page.evaluate(async (theme) => {
  await document.fonts.ready;
  window.mermaid.initialize({
    startOnLoad: false, theme: 'base', securityLevel: 'strict', themeVariables: theme, fontFamily: theme.fontFamily,
    htmlLabels: false, markdownAutoWrap: true,
    flowchart: { htmlLabels: false, curve: 'basis', padding: 12, nodeSpacing: 30, rankSpacing: 42, useMaxWidth: true, wrappingWidth: 180 },
    sequence: { useMaxWidth: true, mirrorActors: false, actorMargin: 24, messageMargin: 30, boxMargin: 8, noteMargin: 8, wrap: true, width: 130, messageFontSize: 15, actorFontSize: 15, noteFontSize: 14 },
  });
}, THEME);

const written = [];
let converted = 0, failed = 0;
for (const { exam, path } of files) {
  let md = readFileSync(path, 'utf8');
  const blocks = [...md.matchAll(MERMAID_RE)];
  if (!blocks.length) continue;
  const slug = basename(path, '.md');
  // Continue after diagrams this note already has, so a re-run never overwrites one.
  const imgDir = join(SKILLUP, exam, 'images');
  const taken = existsSync(imgDir) ? readdirSync(imgDir).map((f) => f.match(new RegExp(`^${slug}-m(\\d+)\\.svg$`))?.[1]).filter(Boolean).map(Number) : [];
  let n = taken.length ? Math.max(...taken) : 0;
  const replacements = [];
  for (const m of blocks) {
    n += 1;
    const code = m[1].replace(EMOJI, '').replace(/\r/g, '');
    const name = `${slug}-m${n}`;
    try {
      const out = await page.evaluate(async ({ code, id }) => {
        const { svg } = await window.mermaid.render(id, code);
        const doc = new DOMParser().parseFromString(svg, 'image/svg+xml');
        const labels = [...doc.querySelectorAll('g.node text, g.nodes text, text.actor, .messageText, g.label text, text.taskText, .mindmap-node text, text')]
          .map((t) => t.textContent ?? '');
        return { svg, labels };
      }, { code, id: `d${converted + failed}` });
      const alt = altText(code, out.labels, nearestHeading(md, m.index));
      const svgFile = join(SKILLUP, exam, 'images', `${name}.svg`);
      const srcFile = join(ROOT, 'scripts/diagrams/mermaid', exam, `${name}.mmd`);
      if (!DRY) {
        mkdirSync(dirname(svgFile), { recursive: true });
        mkdirSync(dirname(srcFile), { recursive: true });
        writeFileSync(svgFile, finish(out.svg));
        writeFileSync(srcFile, m[1].replace(/\r/g, ''));
      }
      written.push(svgFile);
      replacements.push({ from: m[0], to: `![${alt}](/content/skillup/${exam}/images/${name}.svg)\n<!-- diagram source: scripts/diagrams/mermaid/${exam}/${name}.mmd -->` });
      converted += 1;
    } catch (e) {
      failed += 1;
      console.error(`FAIL ${exam}/${slug} #${n}: ${String(e?.message ?? e).split('\n')[0]}`);
    }
  }
  for (const r of replacements) md = md.replace(r.from, r.to);
  if (!DRY && replacements.length) writeFileSync(path, md);
  console.log(`${exam}/${slug}: ${replacements.length}/${blocks.length}`);
}
await browser.close();
writeFileSync(join(ROOT, '.mermaid-svg-written.txt'), written.join('\n'));
console.log(`converted ${converted}, failed ${failed}`);
