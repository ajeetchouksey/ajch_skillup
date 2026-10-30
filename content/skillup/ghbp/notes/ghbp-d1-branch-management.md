# D1: Branch Management & Protection

> **Exam weight**: 33% · **Questions**: ~31 in the bank

## Overview

This domain covers how a team keeps its important branches trustworthy: which changes are allowed in, who has to look at them first, and what evidence must exist before a merge. On GitHub that means two enforcement systems, classic **branch protection rules** and **repository rulesets**. Around them sit CODEOWNERS for routing reviews, required checks and deployments as merge gates, and a branching strategy that keeps branches short-lived enough for all of this to stay cheap.

> 💡 **Human Angle**: Protect main like a production server. Every unreviewed commit to main is a change to production that nobody signed for.

---

## 1.1 Configure branch protection rules that require review, checks and an up-to-date branch

### Key Concept

**A protected branch only accepts changes that arrive the way you said they must: reviewed, tested and current.**

A branch protection rule matches branches by name pattern and attaches requirements to them. Only one classic rule applies to a branch at a time, so the most specific match wins. Force pushes and deletions are blocked on protected branches by default.

**Think of each requirement as a separate lock on the same door**: adding locks makes the door harder to open, and the lock you leave off is exactly where someone gets through.

![A direct push to main is rejected, while a pull request passes required approvals, fresh approval after new commits, required checks and resolved conversations before it can merge.](/content/skillup/ghbp/images/ghbp-1-1-protection-gate.svg)

### Real use

A payments team protects `main` with a required pull request, two approvals, required `build` and `test` checks and conversation resolution. When an engineer tries a Friday-night hotfix straight to main, the push is rejected, and the fix ships an hour later through a reviewed PR instead of causing a weekend incident.

### How it works

Without protection, any collaborator, or anyone holding a stolen credential, can push straight to production. The most common gap auditors find is stale approval: a PR approved on Monday picks up fifteen commits on Tuesday, and Monday's approval still counts for code nobody reviewed.

- **Require a pull request**, with 1–2 approvals from people with write access.
- **Dismiss stale approvals** when new commits change the diff.
- **Require approval of the most recent reviewable push**: someone other than the last pusher must approve.
- **Require status checks** (strict mode also requires the branch to be up to date) and **conversation resolution**.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Full rule: PR, approvals, stale dismissal, checks | The branch deploys or releases to users | More steps per change |
| Add most-recent-push approval | Regulated repos, or reviewers who also push fixes | Needs a second reviewer after every push |
| Light rule: PR and checks, zero approvals | One-person sandboxes and prototypes | No second pair of eyes |

### How to do it

1. Go to **Settings → Branches → Add branch protection rule** (or use a ruleset, see 1.3) and target `main`.
2. Turn on **Require a pull request before merging** with 1–2 approvals and **Dismiss stale pull request approvals**.
3. Turn on **Require status checks to pass** and select your CI checks.
4. Turn on **Require conversation resolution** and leave force pushes and deletions blocked.

### Exam Trap ⚠️

<div class="note-trap">"Dismiss stale approvals" forces a re-review after new commits, but the person who pushed them can still re-approve. Only "Require approval of the most recent reviewable push" demands someone other than the last pusher.</div>

### Go deeper

- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

## 1.2 Control who can bypass branch protection and design break-glass access

### Key Concept

**By default, repository admins are not bound by classic branch protection; you have to opt them in.**

Classic rules don't apply to repository admins, or to custom roles with "bypass branch protections", unless you enable **Do not allow bypassing the above settings**. Rulesets work the other way round: nobody bypasses a ruleset unless they're on its **bypass list**, and each entry can be "Always allow" or "For pull requests only".

**Think of the bypass list as the building's master-key register**: master keys exist, but the register says exactly who holds one.

![Classic protection lets every admin skip the rules unless no-bypass is enabled, while a ruleset binds everyone except a named bypass list whose entries can be limited to pull requests.](/content/skillup/ghbp/images/ghbp-1-2-bypass.svg)

### Real use

An incident team at a SaaS company holds the only bypass entry on the production ruleset, set to "For pull requests only". During an outage they merge a fix without waiting for two approvals, and the change still leaves a PR, a diff and an audit trail.

### How it works

When admin bypass is left at its default, a compromised admin token can push a backdoor straight to main, or an admin can force-push over three days of merged work during a "quick cleanup", without a single review.

- Classic protection: one on/off switch for admins ("Do not allow bypassing").
- Rulesets: an explicit list of roles, teams, GitHub Apps or Dependabot that may bypass.
- "For pull requests only" means even a bypass has to go through a PR.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Classic rule with no-bypass on | A single repo where nobody should skip the rules | No sanctioned emergency path |
| Ruleset bypass, "For pull requests only" | You need a break-glass path that still leaves a trail | Bypassers can skip approvals, so keep the list small |
| Ruleset bypass, "Always allow" | A release app must push tags or commits directly | Direct pushes leave no PR |

### How to do it

1. Create a branch ruleset on `main` (**Settings → Rules → Rulesets**).
2. Under **Bypass list**, add only the incident team or release app.
3. Set each entry to **For pull requests only** unless it must push directly.
4. On remaining classic rules, enable **Do not allow bypassing the above settings**.

### Exam Trap ⚠️

<div class="note-trap">"Temporarily disable branch protection" or "add the on-call engineer to the admin team" widen access for everyone or forever. The exam rewards a scoped ruleset bypass entry, ideally "For pull requests only".</div>

### Go deeper

- [Creating rulesets for a repository](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)

---

## 1.3 Choose between repository rulesets and classic branch protection rules

### Key Concept

**Rulesets stack; classic branch protection rules don't, so with rulesets the strictest requirement always wins.**

Multiple rulesets can apply to one branch at once. They have no priority order: GitHub aggregates them, and where the same rule is defined differently the most restrictive version applies. Rulesets also layer with any classic rule on the same branch, and organization rulesets (Team and Enterprise plans) can target all repositories, name patterns or **custom properties**.

**Think of rulesets like building codes from city, state and federal authorities**: a building must meet the strictest of them, not the one issued last.

![An organization ruleset requiring two approvals and a repository ruleset requiring one approval plus code owner review combine into two approvals and code owner review.](/content/skillup/ghbp/images/ghbp-1-3-rulesets-stack.svg)

### Real use

A fintech with 180 repositories sets one organization ruleset on the default branch of every repo whose custom property is `tier=production`. New production repos are protected the moment they get the property, and teams can still add stricter repository rules on top.

### How it works

Per-repository settings drift: every new repo starts unprotected until someone remembers it, and API scripts only fix the repos that existed when they last ran. Rulesets fix this and add capabilities classic rules lack:

- Several rulesets per branch, aggregated, most restrictive wins.
- Organization-wide targeting by name or custom property; Active, Disabled or Evaluate status.
- Tag rulesets, push rulesets (path, extension, size) and metadata rules (branch names, commit messages).
- An explicit bypass list instead of an admin switch.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Organization ruleset by custom property | A requirement applies to a class of repos | Needs Team or Enterprise and well-kept properties |
| Repository ruleset | One repo needs extra rules or tag protection | Managed per repo |
| Classic branch protection rule | A single small repo that already works | One rule per branch; no tags, no org scope |

### Exam Trap ⚠️

<div class="note-trap">"The repository rule overrides the organization ruleset" and "the newer rule wins" are both false: everything that applies is combined and the most restrictive version wins. Organization rulesets target repos by name or custom property, not by topic.</div>

### Go deeper

- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Creating rulesets for repositories in your organization](https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization)

---

## 1.4 Route and require expert review with CODEOWNERS

### Key Concept

**CODEOWNERS routes reviews automatically; "Require review from Code Owners" is what turns routing into a gate.**

A `CODEOWNERS` file maps path patterns to users or teams, and GitHub requests them as reviewers when a PR touches matching files. **The last matching pattern wins**, so broad defaults go first. The PR uses the CODEOWNERS file **on its base branch**, so editing CODEOWNERS in a PR doesn't change who must review that PR.

**Think of CODEOWNERS like a hospital's on-call rota**: it pages the right specialist automatically, but surgery only waits for them if policy says sign-off is mandatory.

![A pull request touching migrations and payments files is matched against CODEOWNERS from top to bottom, the last matching line names the owner, and the merge waits for that owner only when code owner review is required.](/content/skillup/ghbp/images/ghbp-1-4-codeowners.svg)

### Real use

A payments company maps `/migrations/` to the DBA team and `/src/payments/` to the payments team. A frontend developer's PR that touches a migration automatically requests the DBAs, and with code owner review required it can't merge on a frontend approval alone.

### How it works

Without it, a migration merges with an approval from whoever was free first, or a catch-all `*` line at the bottom silently overrides every specific rule above it.

- GitHub looks in `.github/`, then the root, then `docs/`, and uses the first file it finds (under 3 MB).
- Owners need write access; draft PRs request owners only when marked ready.
- Large owner teams can use automatic review assignment (round robin or load balance) so one or two people are requested, not fifteen.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| CODEOWNERS + "Require review from Code Owners" | A mistake in some path is expensive and only certain people can judge it | Owners can become a bottleneck |
| CODEOWNERS without the requirement | You want routing but not a hard gate | Owners can be ignored |
| Required approvals only | Small, high-trust teams where everyone reviews everything | No expertise routing |

### How to do it

```
# .github/CODEOWNERS: broad default first, specific paths later (last match wins)
*                     @team-lead
/terraform/           @team-devops
/src/payments/        @security-lead
/migrations/          @dba-team
/.github/CODEOWNERS   @security-lead
```

### Exam Trap ⚠️

<div class="note-trap">Last match wins, not first match and not "most specific". Owners are only required when "Require review from Code Owners" is on. And the base branch's CODEOWNERS applies, so a PR that adds its author as owner still needs the existing owners.</div>

### Go deeper

- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

## 1.5 Gate merges on status checks, deployments and the merge queue

### Key Concept

**A check that isn't marked required is only advice; it never blocks a merge.**

Required status checks name the checks that must succeed before a merge. **Strict** mode ("Require branches to be up to date") also makes the PR contain the latest base commit. **Require deployments to succeed** gates the merge on a deployment to named environments such as `staging`. A **merge queue** gives busy branches strict-mode safety without endless rebasing, and **auto-merge** merges a PR once every requirement is met, without bypassing any.

**Think of required checks like a pre-flight checklist**: the plane can technically take off without it, which is why it has to be mandatory.

![Merge is allowed only when required checks pass on an up-to-date branch and the required staging deployment succeeded; optional checks are shown but never block, and auto-merge waits for the same gates.](/content/skillup/ghbp/images/ghbp-1-5-merge-gates.svg)

### Real use

An e-commerce team marks `build`, `test` and `security-scan` as required, requires a successful `staging` deployment, and uses a merge queue on main. Authors enable auto-merge and move on; PRs land only after they've been tested together with everything queued ahead of them.

### How it works

Without required checks, CI goes red and someone merges anyway because the button was still green. Without strict mode or a queue, two PRs that each pass alone break main together.

- The workflow must trigger on `pull_request` (and `merge_group` with a merge queue), and its check name must be selected as required.
- Renaming a job renames its check; the old required check then waits forever as "Expected".

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Required checks, loose mode | Low-traffic repos | PRs aren't tested against each other |
| Strict mode | PRs often interact and traffic is modest | Authors keep updating branches |
| Merge queue | Busy branches where strict mode becomes a treadmill | Needs `merge_group` triggers |
| Require deployments | A real staging environment should prove the change first | Slower merges; needs an environment |

### Exam Trap ⚠️

<div class="note-trap">"Require deployments to succeed before merging" is a separate setting from required status checks; it is the native answer for gating a merge on a staging deployment. And auto-merge never bypasses requirements.</div>

### Go deeper

- [About status checks](https://docs.github.com/en/pull-requests/reference/status-checks)
- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)

---

## 1.6 Enforce centrally owned workflows with organization rulesets

### Key Concept

**A required status check trusts any workflow that reports the right name; a required workflow makes GitHub run one centrally owned file itself.**

"Require workflows to pass before merging" is a rule in **organization or enterprise rulesets**. You choose a source repository, branch and workflow file, and GitHub runs it on pull requests in every targeted repository; a PR can't merge until it passes. With an ordinary required check, the workflow lives in the target repo, so anyone who can edit its `.github/workflows/` can weaken it.

**Think of it like a building inspector the city sends**: a contractor can fire an inspector they hired, but not the city's.

![A team edits its own copy of a dependency-review workflow to always pass, so its required check goes green, while a ruleset-required workflow runs from the central repository and still blocks the vulnerable pull request.](/content/skillup/ghbp/images/ghbp-1-6-required-workflow.svg)

### Real use

A security team requires one dependency-review workflow, stored in a central `security-workflows` repository, on every production repo through an organization ruleset. Service teams can change their own CI freely, but none of them can switch the security gate off.

### How it works

When a gate lives as a copy in each repository, one team adds `continue-on-error: true` and the check passes regardless of findings.

- The source repo must be at least as visible as the targets: a private workflow can run on private repos only.
- Ruleset workflows run on `pull_request`, `pull_request_target` and `merge_group` and **ignore** `paths:` and `branches:` filters.
- Roll out in **Evaluate** mode first; the rule also blocks direct pushes, so target only PR-only branches.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Ruleset "Require workflows to pass" | The gate must hold even if the repo's maintainers change their workflows | Org or enterprise ruleset; filters ignored |
| Ordinary required status check | Team-owned CI that varies by repository | Teams can weaken their own workflow |
| "Require code scanning results" rule | The gate is code scanning | Uses the code scanning rule, not a workflow |

### Exam Trap ⚠️

<div class="note-trap">If teams must not be able to remove or edit the gate, "make it a required status check" is the distractor. And adding <code>paths:</code> to a ruleset workflow doesn't skip it, because its event filters are ignored.</div>

### Go deeper

- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

---

## 1.7 Choose a branching strategy and merge method

### Key Concept

**Short-lived branches make every other control cheap; long-lived branches make every merge an incident.**

**GitHub flow** is one long-lived branch (main) with short-lived feature branches merged by PR. **Trunk-based development** pushes that further: branches live for hours and unfinished work ships dark behind feature flags. **GitFlow** adds `develop`, `release/*` and `hotfix/*`, which suits scheduled, versioned releases. Merge method shapes history: merge commits keep everything, squash gives one commit per PR, rebase replays commits linearly.

**Think of a long-lived branch like a letter written over three months**: by the time you post it, half the addresses have changed.

![Trunk-based development with hour-long branches, GitHub flow with days-long branches and GitFlow with weeks-long release branches are compared by branch lifetime and release style, alongside the merge, squash and rebase merge methods.](/content/skillup/ghbp/images/ghbp-1-7-branching.svg)

### Real use

A SaaS team deploying several times a day uses trunk-based development with feature flags and squash merging, so every PR becomes one Conventional Commit on main and release notes generate themselves.

### How it works

A three-month feature branch diverges so far from main that the final merge takes a week of conflict resolution, and integration bugs that would have shown in week one show in month three.

- "Require linear history" allows only squash or rebase merges.
- Draft PRs are GitHub's way to share unfinished work: they can't be merged and don't request code owners until marked ready.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Trunk-based | You deploy many times a day with strong CI | Needs feature flags and discipline |
| GitHub flow | Most web services and SaaS teams | Release from main only |
| GitFlow-style release branches | You ship versioned releases and support old lines | Slower; more branches to protect |
| Squash merging | You want one clean commit per PR | Loses the PR's individual commits |

### Exam Trap ⚠️

<div class="note-trap">"Require linear history" blocks merge commits; it doesn't enforce review or lock tags. And "WIP:" title prefixes aren't a GitHub feature; Draft pull requests are.</div>

### Go deeper

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [About merge methods on GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)

---

## 1.8 Enforce branch naming conventions

### Key Concept

**A naming convention is only real when something rejects names that break it.**

Prefixes such as `feature/`, `fix/`, `hotfix/` and `release/` make intent visible and let rules target patterns like `release/**`. There are two enforcement points: a ruleset **restrict branch names** metadata rule rejects the branch at push time, and a required PR check that validates `github.head_ref` blocks the merge instead.

**Think of the convention as a dress code**: posting it on the door informs people, but only the doorman checking names enforces it.

![A push of a branch named Release-2.4 is rejected by a ruleset branch-name rule at push time, while a required check catches the same name later, at merge time.](/content/skillup/ghbp/images/ghbp-1-8-naming.svg)

### Real use

A platform team's ruleset requires branch names to match `(feature|fix|hotfix|release|chore|docs)/*`. Because the protected-branch pattern `release/*` is now reliable, no release branch escapes protection by being called `Release-2.4`.

### How it works

When names aren't enforced, pattern-based protection silently misses branches: a rule on `release/*` doesn't protect `Release-2.4`, and nobody notices until a force push lands on it.

- Ruleset metadata restriction: rejects bad names when the branch is pushed.
- Required check on `pull_request`: pass the name through `env:`, because branch names from forks are attacker-controllable (see 2.5).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Ruleset "restrict branch names" | Rules or automation depend on names | Needs rulesets |
| Required naming check | You also want a friendly CI message | Catches names at merge, not at push |
| No enforcement | Trunk-based teams whose branches live for hours | Names drift |

### How to do it

```yaml
- name: Validate branch name
  env:
    BRANCH: ${{ github.head_ref }}   # pass via env: never interpolate into run
  run: |
    echo "$BRANCH" | grep -qE '^(feature|fix|hotfix|release|chore|docs)/.+' \
      || { echo "Branch '$BRANCH' breaks the naming convention"; exit 1; }
```

### Exam Trap ⚠️

<div class="note-trap">Classic branch protection patterns choose <em>which</em> branches are protected; they don't validate new branch names. Name validation is a ruleset metadata restriction or a required check.</div>

### Go deeper

- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

---

## 1.9 Manage the branch lifecycle and protect release tags

### Key Concept

**Delete branches when they merge, lock branches you must keep, and protect the tags you release from.**

"Automatically delete head branches" removes PR branches as they merge. **Lock branch** makes a branch you must keep, such as an end-of-life `v1.x`, read-only. A **tag ruleset** on `refs/tags/v*` that restricts updates and deletions stops anyone outside its bypass list from moving `v1.0.0`; it replaced the old tag protection rules, sunset in 2024.

**Think of a locked branch as a museum exhibit**: everyone can look at it, but nobody gets to rearrange it.

![Merged feature branches are deleted automatically, end-of-life release branches are locked read-only, release tags are protected by a tag ruleset, and a whole retired repository is archived instead.](/content/skillup/ghbp/images/ghbp-1-9-lifecycle.svg)

### Real use

A library maintainer enables auto-delete, locks `v1.x` when its support ends, and adds a tag ruleset on `refs/tags/v*` with the release app as the only bypass actor. Downstream builds pinned to `v2.3.0` always get the code that was published.

### How it works

Merged branches left behind hide active work. A blunt "delete everything older than 90 days" job deletes a `release/2023-lts` branch customers still get patches from, or someone moves a release tag and builds silently pick up different code.

- Auto-delete for merged branches; a scheduled report for stale ones, excluding `release/*`.
- Lock branch for "keep but freeze"; archive for a whole retired repository.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Auto-delete head branches | Always, for merged PR branches | Restore needed if deleted by mistake |
| Lock branch | A branch must stay but never change | Read-only for that branch only |
| Tag ruleset | Released versions must never move | Release tooling needs a bypass entry |
| Archive repository | The whole repository is retired | Issues and PRs become read-only too |

### Exam Trap ⚠️

<div class="note-trap">"Tag protection rules" are the retired feature; prefer a tag ruleset targeting <code>refs/tags/...</code>. And "lock branch" is read-only for one branch, while "archive" is read-only for the whole repository.</div>

### Go deeper

- [Managing the automatic deletion of branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

## 1.10 Require signed commits and map branch risks to controls

### Key Concept

**Signing proves who made a commit; it says nothing about whether anyone reviewed it.**

"Require signed commits" accepts only commits signed and verified with a GPG, SSH or S/MIME key on the committer's GitHub account. Git otherwise trusts whatever name and email a developer configures, so anyone can author commits "as" a colleague. Vigilant mode only *labels* unsigned commits as Unverified; it enforces nothing.

**Think of a signature on a cheque**: it proves who wrote it, but someone still has to check the amount.

![Each branch risk maps to its control: direct pushes to a required pull request, unreviewed merges to approvals and code owners, rewritten history to blocked force pushes, moved tags to a tag ruleset, and forged authorship to required signed commits.](/content/skillup/ghbp/images/ghbp-1-10-risk-matrix.svg)

### Real use

A company under SOC 2 requires signed commits on `main` and release branches. When an auditor asks for proof that a change attributed to a senior engineer was really theirs, the Verified badge and the signing key answer it in seconds.

### How it works

Git metadata is self-asserted: without signing, you can't prove a commit's author. Compliance regimes usually want both signing (who) and review (what was checked).

- Developers add a signing key and set `commit.gpgsign true`.
- Bots sign by creating commits through the GitHub API, which GitHub signs.
- Unsigned commits on a PR's head branch can block a squash merge even though GitHub signs the squash commit.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Require signed commits | You need non-repudiation (SOC 2, FedRAMP, supply-chain attestations) | Every contributor and bot must sign |
| Signing on release branches only | Open-source projects with casual contributors | Main stays unsigned |
| Vigilant mode only | You want visibility, not enforcement | Nothing is blocked |

### How to do it

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
# Add the key to GitHub as a *signing* key, then require signed commits on the branch or ruleset
```

### Exam Trap ⚠️

<div class="note-trap">"A CI workflow that checks signatures" finds unsigned commits only after they're pushed; the native rule rejects them at the door. "Vigilant mode" is a display setting, and "add GPG keys to accounts" is a prerequisite, not enforcement.</div>

### Go deeper

- [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)

---

## Deep Dive: Making Branch Management Click

### 1. The connective narrative

Every control in this domain answers one question: *what has to be true before a change becomes part of main?* Requiring a PR says the change must be visible. Approvals, stale dismissal and most-recent-push approval say a person other than the author must have seen the *final* version. Required checks and deployments say machines must have tested it. Signed commits say we know who made it. Force-push and deletion blocks say that once something is in, the record of it can't be erased.

The two enforcement systems are two generations of the same idea. Classic branch protection is per-repository, one rule per branch, with an on/off admin bypass. Rulesets are layered, can be organization-wide, can target tags and pushes, and replace the admin switch with an explicit bypass list. Because they aggregate (most restrictive wins), an organization can set a floor and repositories can only raise it.

CODEOWNERS and branching strategy are what make the controls sustainable. CODEOWNERS sends each review to someone qualified, so requiring approvals doesn't become rubber-stamping. Short-lived branches keep PRs small enough to review properly and keep strict mode affordable. Lifecycle hygiene (auto-delete, lock, tag rulesets) keeps the set of things you have to protect small and well defined.

### 2. Worked scenario

> **Scenario.** A fintech organization has 180 repositories. An audit finds: 40 repos with no protection on main; several repos where admins pushed directly; release tags moved twice last year; and a payments PR approved by a frontend engineer.
>
> **Step 1: Set a floor across the organization.** Create an organization ruleset targeting the default branch of every repository with the custom property `tier=production`. Rules: require a pull request with 2 approvals, dismiss stale approvals, require approval of the most recent reviewable push, require conversation resolution, require status checks `build` and `test` (strict), block force pushes, restrict deletions. This fixes the 40 unprotected repos and every repo created later, because new production repos get the property and inherit the ruleset.
>
> **Step 2: Close admin bypass.** Rulesets don't exempt admins unless they're on the bypass list. Add only an `incident-response` team, with bypass mode "For pull requests only", so even emergency changes leave a PR. Existing classic rules stay in place and layer with the ruleset; where they're weaker, the ruleset's stricter rules apply anyway.
>
> **Step 3: Route expert review.** In the payments repo, add `/src/payments/ @payments-team` *after* the catch-all line in CODEOWNERS, protect `/.github/CODEOWNERS` with `@security-lead`, and add "Require review from Code Owners" through a repository ruleset. The frontend engineer's approval still counts toward the two approvals, but the PR can't merge without a payments-team approval.
>
> **Step 4: Freeze releases.** Add an organization tag ruleset on `refs/tags/v*` that restricts updates and deletions, with the release GitHub App as the only bypass actor.
>
> **Outcome:** Four configurations (one branch ruleset, one tag ruleset, CODEOWNERS edits, one repo ruleset) replace 180 hand-maintained settings pages, and every finding maps to a specific rule.

### 3. Memory aid

**PROTECT**: the questions to ask of any important branch:

- **P**ull request required: no direct pushes
- **R**eviews: approvals, stale dismissal, most-recent-push approval
- **O**wners: CODEOWNERS, with code owner review required
- **T**ests: required status checks (strict or merge queue), required workflows and deployments
- **E**veryone bound: no admin bypass; explicit ruleset bypass list
- **C**an't rewrite: force pushes and deletions blocked, signed commits, tag rulesets
- **T**argeted at scale: org rulesets by name or custom property

### 4. Exam strategy for this domain

- **Look-alike settings** are the main trap: stale dismissal vs most-recent-push approval; required checks vs required deployments; required status checks vs ruleset required workflows; lock branch vs archive; classic "do not allow bypassing" vs ruleset bypass list.
- **"Overrides" language is usually wrong** for rulesets. They aggregate, and the most restrictive rule wins.
- **Native beats custom.** When a native setting exists (auto-merge, team review assignment, require signed commits), the exam prefers it over webhooks or homemade workflows. The exception is branch-name validation, where a required check is a legitimate answer alongside ruleset metadata restrictions.
- **Watch scope words**: "all 200 repositories" points to an organization ruleset; "this one branch must never change" points to lock branch; "tags" points to a tag ruleset.
- Five minutes before the exam: *A rule only protects what it targets, binds only who it doesn't exempt, and requires only what is marked required.*

---

## Cheat Sheet 📋

| Control | Where | Key rule |
|---|---|---|
| Branch protection on `main` | Settings → Branches (classic) or Settings → Rules → Rulesets | One classic rule per branch; rulesets layer |
| Require PR + approvals | Branch rule / ruleset "Require a pull request" | Approvals come from people with write access |
| Dismiss stale approvals | Branch rule / ruleset | New commits that change the diff dismiss approvals |
| Most recent push approval | Branch rule / ruleset | Approver must differ from the last pusher |
| Required status checks | Branch rule / ruleset | Strict = must be up to date; check must run on `pull_request` |
| Required workflows | Org/enterprise ruleset: "Require workflows to pass before merging" | Central workflow file; event filters ignored; source repo at least as visible as targets |
| Require deployments | Branch rule / ruleset | Gate merge on environment deployment |
| Admin bypass disabled | "Do not allow bypassing the above settings" | Admins bypass classic rules by default |
| Ruleset bypass | Bypass list | "Always allow" vs "For pull requests only" |
| Org-wide enforcement | Organization rulesets (Team/Enterprise) | Target by name pattern or custom property |
| CODEOWNERS | `.github/`, root, or `docs/` | Last match wins; base branch's file applies; < 3 MB |
| Code owner review | "Require review from Code Owners" | Without it, owners are only requested |
| Force push / deletion | Blocked by default on protected branches | Leave blocked on main |
| Tag immutability | Tag ruleset on `refs/tags/v*` | Tag protection rules were sunset in 2024 |
| Freeze a branch | Lock branch | Read-only; optional fork syncing |
| Auto-delete merged branches | Settings → General | Removes head branches on merge |
| Signed commits | Branch rule / ruleset | Verified GPG, SSH or S/MIME signatures only |
