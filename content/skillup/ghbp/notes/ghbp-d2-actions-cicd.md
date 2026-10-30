# D2: GitHub Actions & CI/CD

> **Exam weight**: 33% · **Questions**: ~30 in the bank

## Overview

GitHub Actions runs your code, often with your secrets and a token that can write to your repository. This domain covers how to make that safe: least-privilege tokens, secrets and OIDC instead of long-lived keys, pinned dependencies, and treating untrusted input as data. It also covers making pipelines fast and maintainable, with caching, reusable workflows, composite actions, environments and deployment gates, concurrency and timeouts.

> 💡 **Human Angle**: Automation is only as trustworthy as the controls around it. A misconfigured workflow isn't a safety net; it's a door with your keys hanging in the lock.

---

## 2.1 Apply least-privilege GITHUB_TOKEN permissions

### Key Concept

**Give every job the smallest token that still works; when you list one permission, all unlisted ones drop to none.**

At the start of each job GitHub creates a `GITHUB_TOKEN` scoped to the workflow's repository, which expires when the job ends. Its default permissions come from the repository or organization setting: *permissive* or *restricted* (read-only contents and packages), and restricted is the recommended default. The `permissions` key overrides it per workflow or job, and `permissions: {}` disables everything.

**Think of the token like a hotel key card**: it opens only the rooms you were assigned, and it stops working at checkout.

![A workflow defaults to contents read, the test job keeps that, the comment job adds pull-requests write and the release job adds contents write, while fork pull requests are downgraded to read-only with no secrets.](/content/skillup/ghbp/images/ghbp-2-1-token-permissions.svg)

### Real use

An npm library's workflow defaults to `contents: read`. Only the release job gets `contents: write` and `id-token: write`, so when a third-party changelog action turns malicious, the job it runs in can't push to branches or move tags.

### How it works

With `permissions: write-all`, one compromised action in any job can push to branches, rewrite releases and move tags: every dependency's blast radius becomes the whole repository.

- Listing any scope sets every unlisted scope to `none`.
- `pull_request` runs from forks get a read-only token and no repository secrets.
- Events created with `GITHUB_TOKEN` generally don't start new workflow runs, and the token can't reach other repositories.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Workflow default `contents: read`, elevate per job | Almost always | A few more lines of YAML |
| GitHub App installation token | You must act on other repositories or trigger workflows | An app to register and manage |
| `permissions: write-all` | Never in shared workflows | Every step gets everything |

### How to do it

```yaml
permissions:
  contents: read              # workflow default
jobs:
  comment:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write    # post PR comments only
```

### Exam Trap ⚠️

<div class="note-trap">"Fork PRs get the write-all token" is false: <code>pull_request</code> runs from forks are read-only and get no secrets. The real danger is trusted runs (push, <code>pull_request_target</code>, <code>workflow_run</code>, schedules) where a compromised action inherits the full token.</div>

### Go deeper

- [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)

---

## 2.2 Store secrets and variables at the right scope

### Key Concept

**Secrets hold credentials, variables hold configuration, and the most specific scope wins when names collide.**

Secrets exist at organization, repository and environment level, and the lowest level takes precedence: environment over repository, repository over organization. Environment secrets reach only jobs that name the environment, and only after its required reviewers approve. Configuration variables (`vars`) are for non-sensitive values and aren't masked.

**Think of the hierarchy like dress codes**: the company sets a default, the department can override it, and the specific event's rule beats both.

![Organization, repository and environment secrets are stacked with the environment level winning name collisions, environment secrets unlock only after reviewer approval, and non-sensitive values live in variables.](/content/skillup/ghbp/images/ghbp-2-2-secret-scopes.svg)

### Real use

A team keeps the production database password as a `production` environment secret behind two reviewers, the staging password as a repository secret, and the region and hostnames as variables. Test workflows can't read production credentials at all.

### How it works

A production password stored as a repository secret is readable by every workflow in the repo, including a test workflow someone can edit in a branch PR.

- Redaction can fail for structured secrets (a JSON blob), and values derived from a secret aren't masked automatically; use `::add-mask::`.
- Dependabot-triggered runs read **Dependabot secrets**, not Actions secrets.
- Workflow YAML is committed, so `env:` blocks are never a place for credentials.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Environment secret | Only deploy jobs need it, ideally after approval | Jobs must declare the environment |
| Repository secret | Every workflow in one repo needs it | Readable by all of that repo's workflows |
| Organization secret | Many repos share one credential | Wider blast radius |
| Variable (`vars`) | The value isn't sensitive | Shown in logs |
| OIDC (2.3) | The target is a cloud that can federate | Store nothing at all |

### Exam Trap ⚠️

<div class="note-trap">Precedence is environment → repository → organization: the most specific wins, not "organization always wins" or "the most recent wins".</div>

### Go deeper

- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)

---

## 2.3 Deploy to the cloud with OpenID Connect instead of stored keys

### Key Concept

**OIDC swaps stored cloud keys for a short-lived token the cloud provider issues to one job, on conditions you define.**

A job with `permissions: id-token: write` asks GitHub's OIDC provider for a signed JWT describing the run (repository, ref, environment). The cloud provider checks its claims against a role's trust conditions and returns a short-lived access token for that job only. `id-token: write` only lets the job *request* the JWT; it grants no write access to the repository.

**Think of it like a guest list at a venue**: the ID card (JWT) proves who you are, but the bouncer (trust policy) still decides whether you're on tonight's list.

![A deploy job requests a JWT from GitHub's OIDC provider, the cloud checks the audience and the subject claim against the role's trust policy, and only a matching job receives short-lived credentials.](/content/skillup/ghbp/images/ghbp-2-3-oidc.svg)

### Real use

A retailer deletes its `AWS_ACCESS_KEY_ID` secret. The deploy job declares `environment: production`, and the IAM role trusts only `sub = repo:retail/web:environment:production`, so only an approved production deploy from that repository can assume it.

### How it works

A stored cloud key keeps working for an attacker until someone notices and rotates it. Even with OIDC, a trust policy that checks only `aud` lets *any* GitHub workflow that requests that audience assume your role.

- Default `sub` with an environment: `repo:ORG/REPO:environment:NAME`; for a branch: `repo:ORG/REPO:ref:refs/heads/BRANCH`.
- Always add a `sub` condition, ideally the environment form, so the approval gate and the credential gate coincide.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| OIDC with an environment `sub` | The cloud supports federation | Trust policy must be kept precise |
| Customized `sub` template (e.g. `job_workflow_ref`) | Trust should follow one reusable workflow | Update the cloud condition first |
| Environment secret | The target can't federate | A long-lived key to rotate |

### How to do it

```yaml
deploy:
  runs-on: ubuntu-latest
  environment: production            # sub = repo:my-org/my-repo:environment:production
  permissions:
    id-token: write                  # request the OIDC JWT
    contents: read
  steps:
    - uses: aws-actions/configure-aws-credentials@<full-sha>  # vX.Y.Z
      with:
        role-to-assume: arn:aws:iam::123456789012:role/deploy-prod
        aws-region: eu-west-1
```

### Exam Trap ⚠️

<div class="note-trap">"Move the keys to an environment secret" still leaves a long-lived key; OIDC removes it. There is no <code>id-token: read</code>; the permission is <code>id-token: write</code>. A trust policy without a <code>sub</code> condition is the classic misconfiguration.</div>

### Go deeper

- [OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect)

---

## 2.4 Pin and govern third-party actions

### Key Concept

**A tag is a pointer someone else can move; a full-length commit SHA is not.**

Every `uses:` runs someone else's code with your token and secrets in reach. GitHub's guidance is to pin actions to a **full-length commit SHA** from the action's own repository. Organizations can enforce it: the allowed-actions policy can require SHA pinning and allow or block specific actions. Workflow dependency lockfiles (`.github/workflows/actions.lock`, public preview in 2026) record every action's exact commit, including transitive ones.

**Think of a tag like a street address and a SHA like a fingerprint**: anyone can move into the house at an address, but nobody else has your fingerprint.

![An action referenced by tag runs whatever the tag points to after a maintainer is compromised, while an action pinned to a full SHA keeps running the reviewed commit and Dependabot proposes updates as reviewable pull requests.](/content/skillup/ghbp/images/ghbp-2-4-pinning.svg)

### Real use

An organization turns on SHA-pinning enforcement in its allowed-actions policy and adds `github-actions` to every `dependabot.yml`. When a popular action is later compromised and its tags moved, none of its repositories run the new code; they keep the pinned commit until a reviewed Dependabot PR updates it.

### How it works

When a maintainer's account is compromised and `v2` is moved to malicious code, every repository using `@v2` runs it on the next trigger, and nothing changes in your own history.

- Pin with a version comment so humans and Dependabot can read it.
- Protect `.github/workflows/` with CODEOWNERS so workflow changes get a qualified reviewer.
- Local actions (`uses: ./.github/actions/setup`) change only with your own commits.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full SHA + Dependabot | Any third-party action | Bumps arrive as PRs to review |
| Org SHA-pinning enforcement | Many repos and teams | Unpinned workflows fail until fixed |
| Workflow lockfile (preview) | You want transitive actions pinned too | Preview feature |
| Tag reference | You fully trust the creator | Code can change under you |

### How to do it

```yaml
# ❌ The tag can be moved to different code at any time
- uses: actions/checkout@v4
# ✅ SHA-pinned; the comment keeps it readable and lets Dependabot update it
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

### Exam Trap ⚠️

<div class="note-trap">"Use <code>@latest</code>" or "use a verified creator" don't make a reference immutable. The answer is a full-length SHA with a version comment, kept current by Dependabot and enforced org-wide by the allowed-actions SHA-pinning option.</div>

### Go deeper

- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

---

## 2.5 Prevent script injection from untrusted input

### Key Concept

**Never interpolate untrusted `${{ }}` values into a script; pass them through an environment variable.**

Expressions are expanded into the script text *before* the shell runs, so `run: echo "${{ github.event.issue.title }}"` with a crafted title executes the attacker's command. Issue and PR titles and bodies, branch names, commit messages and comments are all attacker-controllable. Triggers matter too: `pull_request_target` and `workflow_run` run in the base repository's context with secrets and a write-capable token.

**Think of `${{ }}` like pasting a stranger's text into your terminal**: the shell can't tell which part you typed and which part they did.

![An issue title interpolated into run becomes part of the shell command and executes, while the same title passed through an environment variable arrives as plain data.](/content/skillup/ghbp/images/ghbp-2-5-injection.svg)

### Real use

An open-source project's "triage new issues" workflow passes the issue title through `env: TITLE` and quotes `"$TITLE"` in the script. When someone files an issue titled with a shell payload, the bot simply labels it.

### How it works

Interpolating an issue title into `run:` lets anyone on the internet execute commands on your runner with that job's token and secrets.

| Trigger | Runs in | Fork PRs get secrets? | Safe use |
|---|---|---|---|
| `pull_request` | Merge of PR into base | No | Build and test untrusted code |
| `pull_request_target` | Base branch | Yes | Label or comment; never run PR code |
| `workflow_run` | Default branch | Yes | Post-process; treat artifacts as untrusted |

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Pass via `env:` and quote | Any value outsiders can influence | None worth mentioning |
| Pass as an action input | The logic lives in an action | Action must handle it safely |
| Interpolate directly | Trusted values like `github.sha` or your own computed outputs | Only safe for trusted data |

### How to do it

```yaml
# ✅ Safe: the title arrives as data in an environment variable
- env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "Triaging $TITLE"
```

### Exam Trap ⚠️

<div class="note-trap">Wrapping the expression in quotes doesn't help; the attacker brings their own quote. Masking only hides logs, and read-only permissions reduce impact but the command still runs. <code>pull_request_target</code> plus checking out the PR head is the classic critical misconfiguration.</div>

### Go deeper

- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

---

## 2.6 Choose and secure GitHub-hosted and self-hosted runners

### Key Concept

**Self-hosted runners should almost never run public-repository workflows.**

GitHub-hosted runners give each job a fresh, isolated VM that is discarded afterwards. Self-hosted runners are your machines: they can keep state between jobs and often sit inside your network. On a public repository, anyone can open a PR that runs code on them. The safe pattern is ephemeral, just-in-time runners in runner groups restricted to specific private or internal repositories.

**Think of a self-hosted runner as lending someone your office for an hour**: fine for a colleague, reckless for a stranger, and either way you want the room reset afterwards.

![A public repository's fork pull request reaches a persistent self-hosted runner that keeps state and sits inside the network, while ephemeral runners in a restricted group serve only private repositories and are destroyed after each job.](/content/skillup/ghbp/images/ghbp-2-6-runners.svg)

### Real use

An ML team needs GPUs for packaging jobs. It runs ephemeral GPU runners, one job each and then destroyed, in a runner group available only to its two private repositories, while everything else stays on GitHub-hosted runners.

### How it works

A fork PR to an open-source project runs on a shared persistent runner, plants a modified tool in the toolcache, and steals credentials from the next private job on that machine.

- Ask who can make a job run on the machine and what the machine can reach.
- Ephemeral or just-in-time runners remove persistence; runner groups limit which repositories can use them.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| GitHub-hosted (standard or larger) | Most workloads, and all public repos | Less hardware choice |
| Ephemeral self-hosted in a restricted group | Private repos needing GPUs, special hardware or on-prem access | You run the infrastructure |
| Persistent self-hosted | Avoid; only for trusted private repos you fully control | State leaks between jobs |

### Exam Trap ⚠️

<div class="note-trap">GitHub doesn't <em>forbid</em> self-hosted runners on public repos; it strongly advises against them. The risk the exam wants is persistence plus network access plus untrusted code.</div>

### Go deeper

- [Self-hosted runners](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners)

---

## 2.7 Configure Dependabot alerts, security updates and version updates

### Key Concept

**Dependabot alerts tell you, security updates fix what's vulnerable, version updates keep everything current.**

**Alerts** fire when the dependency graph contains a package with a known advisory. **Security updates** open PRs raising a vulnerable dependency to the minimum patched version; they need the dependency graph and alerts, but no `dependabot.yml`. **Version updates** open scheduled PRs for any newer version and *are* configured in `.github/dependabot.yml`. Dependabot never auto-merges on its own.

**Think of it like a car's service light, a recall notice and a maintenance schedule**: three different triggers, and confusing them is how cars go unserviced.

![A dependency graph feeds Dependabot alerts, alerts lead to security update pull requests with no config file, and dependabot.yml schedules version update pull requests, including the github-actions ecosystem.](/content/skillup/ghbp/images/ghbp-2-7-dependabot.svg)

### Real use

A team enables alerts and security updates organization-wide and adds weekly, grouped version updates for npm, Docker and `github-actions`. A critical CVE in a library they use arrives as a ready-to-merge PR the next morning, not in a customer's audit months later.

### How it works

Without it, a service runs a vulnerable library for 14 months because nothing is watching.

- Grouped security updates combine fixes per ecosystem; version-update groups can bundle, say, all patch bumps.
- Route Dependabot PRs to reviewers with CODEOWNERS (the `reviewers` option was removed in 2025).
- Auto-merge is something you build with a workflow and `dependabot/fetch-metadata`.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Alerts + security updates | Everywhere | PRs only when something is vulnerable |
| Version updates with groups | The team can absorb steady update PRs | More PRs to review |
| Auto-merge patch updates | Strong tests and low-risk ecosystems | Trusts the test suite |
| Security updates only | Frozen, end-of-life services | Falls behind on versions |

### How to do it

```yaml
# .github/dependabot.yml (version updates)
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule: { interval: "weekly" }
    groups:
      npm-patch: { update-types: ["patch"] }
  - package-ecosystem: "github-actions"   # keeps SHA-pinned actions current
    directory: "/"
    schedule: { interval: "weekly" }
```

### Exam Trap ⚠️

<div class="note-trap">"Security updates require dependabot.yml" is false; only version updates do. Dependabot doesn't auto-merge by default, and <code>open-pull-requests-limit: 0</code> means "don't open version-update PRs", not "needs review".</div>

### Go deeper

- [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
- [About Dependabot security updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates)

---

## 2.8 Cache dependencies safely and effectively

### Key Concept

**Key the cache on a hash of the lockfile, and remember that branches can read their parents' caches but not their siblings'.**

`actions/cache` (or the `cache:` option of `setup-*` actions) saves a path under a key and restores it on later runs. The key should include `hashFiles('**/package-lock.json')` so the cache changes exactly when dependencies do; `restore-keys` give prefix fallbacks, and `cache-hit` is true only for an exact match. Caches are immutable, evicted after 7 days unused, and limited to 10 GB per repository by default.

**Think of the cache like a family recipe box**: children can borrow from their parents' box, but nobody can slip a card into their sibling's.

![A feature branch can restore caches from itself and the default branch, and a pull request also from its base branch, but nothing flows from a sibling branch or back up to main.](/content/skillup/ghbp/images/ghbp-2-8-cache-scope.svg)

### Real use

A Node team caches `~/.npm` keyed on `runner.os` plus the lockfile hash. Installs drop from about three minutes to ten seconds, and the cache refreshes exactly when someone changes a dependency.

### How it works

A cache keyed on branch name keeps restoring old packages after an upgrade; one keyed on `github.run_id` never hits.

- Scope is a security boundary: a run restores caches from its own branch or the default branch, and PR runs also from the base branch.
- Cache the package manager's download cache, not `node_modules/`, which is fragile across OS and Node versions.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| `setup-*` built-in `cache:` | Standard language setups | Less control over the key |
| `actions/cache` with a lockfile hash | Custom paths or tools | You maintain the key |
| No cache restore | Release builds that must be reproducible | Slower builds |

### How to do it

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Exam Trap ⚠️

<div class="note-trap">Caches flow <em>down</em> (default branch → feature branch, base branch → PR), never sideways or up, which prevents cache poisoning across branches. "Branch name as key" and "run ID as key" are both distractors.</div>

### Go deeper

- [Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)

---

## 2.9 Run code scanning with CodeQL and make it a merge gate

### Key Concept

**Code scanning finds vulnerabilities in your code; it only blocks merges once you make it a required gate.**

Code scanning analyses source for issues such as SQL injection, command injection and path traversal, and raises alerts in the Security tab and on PRs. **Default setup** enables CodeQL without a workflow file; **advanced setup** uses a workflow you control. Third-party tools feed the same alerts by uploading SARIF with `github/codeql-action/upload-sarif`. Code scanning is free on public repositories; private ones need GitHub Code Security.

**Think of code scanning like a smoke detector**: essential, but it only stops a fire if it's wired to the sprinklers.

![CodeQL or a third-party tool's SARIF upload produces alerts on the pull request, and only a ruleset's code scanning rule or a required check turns those alerts into a blocked merge.](/content/skillup/ghbp/images/ghbp-2-9-code-scanning.svg)

### Real use

A bank turns on CodeQL default setup across its repositories, then adds a ruleset rule that blocks merges on high or higher security alerts. A SQL injection found on a PR now stops the merge instead of sitting in a report.

### How it works

CodeQL flags a SQL injection on a PR and the PR merges anyway, because the result was informational: a security report, not a security gate.

- Block merges with a ruleset's **Require code scanning results** rule (by severity, or when a tool hasn't run), or make the check required.
- `upload-sarif` needs `security-events: write`.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Default setup | Breadth across many repositories | Less customisation |
| Advanced setup | Custom builds, extra query packs, monorepos | A workflow to maintain |
| Third-party SARIF upload | You already use another SAST tool | Results quality depends on the tool |

### Exam Trap ⚠️

<div class="note-trap">"There's a <code>block: true</code> parameter" is a distractor; blocking comes from a required check or the ruleset code scanning rule. The SARIF action is <code>github/codeql-action/upload-sarif</code>, not <code>actions/upload-sarif</code>.</div>

### Go deeper

- [CodeQL code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning)

---

## 2.10 Reuse automation with reusable workflows and composite actions

### Key Concept

**Reuse whole jobs with reusable workflows; reuse steps with composite actions.**

A **reusable workflow** has `on: workflow_call` with typed `inputs` and `secrets`; callers use it at *job* level (`jobs.x.uses: org/repo/.github/workflows/file.yml@ref`) and it runs as its own job. A **composite action** is an `action.yml` with `runs.using: composite`; it's used as a *step* and runs inline on the caller's runner. Both turn one fix into a fix everywhere, so pin or protect their `@ref` like any dependency.

**Think of a reusable workflow as a franchise kitchen and a composite action as a house spice blend**: one is the whole operation run to a standard, the other is a component you mix into your own cooking.

![A reusable workflow is called at job level and runs as its own job on its own runner, a composite action is called at step level and runs inline in the caller's job, and a workflow template is copied once and then diverges.](/content/skillup/ghbp/images/ghbp-2-10-reuse.svg)

### Real use

A platform team keeps one reusable deploy workflow with environments and OIDC in a central repository, and twelve services call it by SHA. A security fix lands once and every service picks it up on its next pinned bump.

### How it works

Five repositories each carry a copy of the deploy workflow; a security fix lands in two and the other three keep the vulnerable step for months.

| | Reusable workflow | Composite action | Template |
|---|---|---|---|
| Used at | Job level | Step level | Copied at creation |
| Runs | Own job and runner | Inline, caller's runner | N/A |
| A fix propagates? | Yes | Yes | No, copies diverge |

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Reusable workflow | Reusing a whole stage with its own runner, environment and secrets | Job-level only |
| Composite action | Reusing a few setup steps inside a job | Shares the caller's runner |
| Workflow template | Teams should diverge after day one | Fixes don't propagate |

### How to do it

```yaml
jobs:
  test:   # reusable workflows are used at JOB level
    uses: your-org/shared-workflows/.github/workflows/reusable-test.yml@<sha-or-protected-tag>
    with:
      node-version: '22'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Exam Trap ⚠️

<div class="note-trap">"A reusable, parameterized multi-step sequence used inside a job" is a composite action, not a reusable workflow. Environments share secrets and protection rules, not steps.</div>

### Go deeper

- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Create a composite action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action)

---

## 2.11 Protect deployments with environments

### Key Concept

**An environment's rules only guard jobs that name the environment, and its secrets stay locked until those rules pass.**

A job opts in with `environment: production`. Before it reaches a runner, every protection rule must pass: **required reviewers** (up to six users or teams, any one can approve, with an option to prevent self-review), a **wait timer** (up to 43,200 minutes), **deployment branches and tags**, and custom protection rules from GitHub Apps. Admins can bypass unless that's turned off. Private repositories need GitHub Enterprise for required reviewers and wait timers.

**Think of an environment like a bank vault with a time lock and two keyholders**: the cash is inside, and the door opens only when the clock and the people agree.

![A merged change deploys to staging automatically, then the production job waits for an approved reviewer, the wait timer and a main-only branch rule before production secrets unlock and the deploy runs.](/content/skillup/ghbp/images/ghbp-2-11-environments.svg)

### Real use

A team's production environment needs one approval from `@team-leads`, blocks self-review, waits five minutes and accepts deployments only from `main`. A bad Friday-evening merge reaches staging but waits at the production gate until someone looks.

### How it works

A bad merge auto-deploys to production and the only stop button is disabling the workflow. With a required-reviewer environment, the deploy waits for a person, and production credentials aren't readable until they approve.

- Protection rules don't apply to a job that doesn't declare the environment, even if it deploys to production.
- The `environment:` name must match the environment in Settings exactly.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Required reviewers | A human should approve production | Waits for people |
| Wait timer | You want a short window to cancel | Slower deploys |
| Deployment branch rules | Only `main` or tags may deploy | Hotfix branches need a rule |
| Custom protection rule (App) | Mature teams gate on monitoring signals | An app to build or buy |

### Exam Trap ⚠️

<div class="note-trap">Branch protection's deployment requirement gates <em>merging</em>; environments gate <em>deploying</em>. And a job that doesn't name the environment skips all of its rules and can't read its secrets.</div>

### Go deeper

- [Managing environments for deployment](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)

---

## 2.12 Control workflow runs with concurrency, timeouts, matrices and outputs

### Key Concept

**Most pipeline problems have a built-in key; reach for it before writing glue code.**

`concurrency` allows one run per group, and `cancel-in-progress: true` cancels the older run. `timeout-minutes` exists at job level (default 360) and step level, never workflow level. `strategy.matrix` fans one job out into every combination, and jobs without `needs:` run in parallel. Values pass between jobs through `outputs` set via `$GITHUB_OUTPUT`, because each job runs on a fresh runner.

**Think of these keys as the switches on a fuse board**: each one controls exactly one circuit, and knowing which does what beats rewiring the house.

![Four built-in keys solve four problems: concurrency queues or cancels overlapping runs, timeout-minutes ends hung jobs, a matrix fans one job across operating systems and versions, and outputs pass values to dependent jobs.](/content/skillup/ghbp/images/ghbp-2-12-workflow-control.svg)

### Real use

A team's PR CI cancels superseded runs, its deploy workflow queues runs without cancelling, a 2×3 matrix tests every OS and Node version in parallel, and a 30-minute job timeout means a hung test never holds a runner for six hours again.

### How it works

Three merges in two minutes start three deploys that race each other, and a hung test fixture holds a runner for six hours because nobody set a timeout.

- `on: push: branches:` filters the whole workflow; a job-level `if:` skips one job.
- `workflow_dispatch` with typed `inputs` (`choice`, `string`, `boolean`, `environment`) gives a manual run form.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Concurrency with cancel-in-progress | PR CI, where only the latest commit matters | Interrupts runs |
| Concurrency without cancel | Deploys, which should queue | Waits for the earlier run |
| Matrix | The same job across OS or version combinations | More runner minutes |
| Outputs or artifacts | A later job needs data from an earlier one | Explicit wiring |

### How to do it

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false        # queue deploys; use true for PR CI
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    outputs:
      image-tag: ${{ steps.tag.outputs.image-tag }}
    steps:
      - id: tag
        run: echo "image-tag=sha-${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"
```

### Exam Trap ⚠️

<div class="note-trap"><code>timeout-minutes</code> at the workflow level doesn't exist; it's a job or step key. Jobs can't share a workspace; use outputs or artifacts. And a trigger branch filter stops every job, so limit one job with <code>if:</code>.</div>

### Go deeper

- [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
- [Run job variations](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)

---

## Deep Dive: Making Actions Security Click

### 1. The connective narrative

Every workflow run is a small, temporary computer that holds three valuable things: a **token** that can act on your repository, **secrets** that can act on other systems, and **network access** from wherever the runner lives. Every control in this domain shrinks one of those, or controls *whose code* gets to run next to them.

Least-privilege `permissions` shrink the token. Environment secrets and OIDC shrink the secrets: environment secrets by hiding them until approval, OIDC by removing them entirely and issuing a per-job credential that the cloud provider grants only when the trust policy's `sub` matches. Ephemeral runners and runner groups shrink the network exposure. On the other side, SHA pinning, allowed-actions policies, lockfiles and Dependabot control *whose code* runs; the env-var pattern and careful use of `pull_request_target` keep *attacker-supplied text* from becoming code.

The performance and maintainability features (caching, reusable workflows, composite actions, concurrency, timeouts) follow the same logic. A shared, reviewed reusable workflow is one place to get security right instead of fifty. Cache scope rules exist so a feature branch can't poison main's builds. Environments are both the deployment gate and the secret vault.

### 2. Worked scenario

> **Scenario.** An open-source project's release workflow runs on `push` to main with `permissions: write-all`, uses `third-party/changelog@v3`, reads `NPM_TOKEN` and `AWS_SECRET_ACCESS_KEY` from repository secrets, and has a triage workflow with `run: echo "${{ github.event.issue.title }}"`.
>
> **Step 1: Shrink the token.** Set the workflow default to `permissions: contents: read`. The release job alone gets `contents: write` (to create the GitHub Release) and `id-token: write` (for OIDC). The triage job gets `issues: write` only.
>
> **Step 2: Remove the AWS key.** Create an IAM OIDC identity provider for `token.actions.githubusercontent.com`. The role trust policy requires `aud = sts.amazonaws.com` **and** `sub = repo:proj/proj:environment:release`. The release job declares `environment: release` with one required reviewer and deployment branches limited to `main`. Delete `AWS_SECRET_ACCESS_KEY`.
>
> **Step 3: Contain the npm token.** npm publishing still needs a credential here, so move `NPM_TOKEN` from repository secrets to the `release` environment. Now no other workflow can read it, and the release job can't read it until the reviewer approves.
>
> **Step 4: Pin the supply chain.** Replace `@v3` with the full commit SHA plus a `# v3.x.y` comment, add a `github-actions` entry to dependabot.yml, and add `/.github/workflows/ @maintainers` to CODEOWNERS.
>
> **Step 5: Fix the injection.** Move the title into `env: TITLE: ${{ github.event.issue.title }}` and use `"$TITLE"`.
>
> **Outcome:** A compromised changelog action can no longer change code that runs (pinned), and if a malicious SHA were ever merged it would find a read-only token and no secrets outside the approved release job. The AWS credential no longer exists to steal.

### 3. Memory aid

**PINS-OE**: the questions to ask of every workflow:

- **P**ermissions: minimal, per job; `contents: read` default
- **I**nput: untrusted `${{ }}` goes through `env:`
- **N**o tags: actions pinned to full SHAs (enforced by policy, kept fresh by Dependabot)
- **S**ecrets: scoped to environments, never in YAML
- **O**IDC: federate to cloud; `sub` condition pinned
- **E**nvironments: reviewers, branch rules and secrets on the deploy job

### 4. Exam strategy for this domain

- **Watch the trigger.** `pull_request` from a fork means a read-only token and no secrets; `pull_request_target` and `workflow_run` mean a privileged context. Many questions hinge on this one distinction.
- **"Most secure" means least privilege plus removing the secret,** not "rotate more often" or "encrypt it yourself".
- **Native keys beat glue code:** concurrency, `timeout-minutes` (job/step), matrix, outputs, environments, allowed-actions policy.
- **Look-alikes:** reusable workflow (job level) vs composite action (step level) vs template (copy); Dependabot security updates (no config file) vs version updates (dependabot.yml); `id-token: write` (request JWT) vs write access (none).
- Five minutes before the exam: *Shrink the token, remove the secret, pin the code, and never let a stranger's text become a command.*

---

## Cheat Sheet 📋

| Control | Check | Key rule |
|---|---|---|
| Token permissions | `permissions:` at workflow and job level | Listing any scope sets the rest to `none`; default org/repo to restricted |
| Fork PRs | `pull_request` from forks | Read-only token, no secrets |
| Privileged triggers | `pull_request_target`, `workflow_run` | Never check out and run PR code |
| Script injection | `run:` steps | Untrusted `${{ }}` goes into `env:` |
| Secrets precedence | Env > repo > org | Env secrets locked until reviewers approve |
| OIDC | `id-token: write` + cloud trust policy | Always add a `sub` condition |
| Action pinning | Full-length SHA + version comment | Org allowed-actions policy can enforce; lockfiles (preview) go further |
| Dependabot | alerts / security updates / version updates | Only version updates need `dependabot.yml`; include `github-actions` |
| Caching | `actions/cache` keyed on lockfile hash | Own branch, default branch, PR base branch only; 7-day eviction; 10 GB |
| Code scanning | CodeQL default or advanced setup | Block via ruleset "Require code scanning results" or required check |
| SARIF upload | `github/codeql-action/upload-sarif` | Needs `security-events: write` |
| Reuse | `workflow_call` (job) / composite (step) | Pin `@ref` of shared workflows |
| Environments | `environment:` on the job | Up to 6 reviewers; wait timer up to 30 days; admin bypass can be disabled |
| Concurrency | `concurrency.group` + `cancel-in-progress` | Queue deploys, cancel PR CI |
| Timeouts | `jobs.<id>.timeout-minutes` (default 360) | No workflow-level timeout |
| Self-hosted runners | Private repos only, ephemeral | Never for public fork PRs |
