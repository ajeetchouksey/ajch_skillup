# D3: Repository Security & Governance

> **Exam weight**: 34% · **Questions**: ~30 in the bank

## Overview

A repository is more than a code store. It is an access-control boundary, an audit trail and a collaboration protocol. This domain covers the security features that watch it (secret scanning and push protection, dependency review, and how GitHub packages them as Secret Protection and Code Security), how to enforce them at scale with security configurations, and the governance files and settings that make collaboration predictable: templates, security policy and private vulnerability reporting, commit conventions, visibility, machine identities and the audit log.

> 💡 **Human Angle**: Governance gaps compound like interest. No template, no owner, no policy: each looks minor on its own, and together they add up to a compliance failure.

---

## 3.1 Set up the essential repository files

### Key Concept

**The files in a repository's root and `.github/` folder are its operating manual and its first line of defence.**

A production repository needs a README, a LICENSE, a `.gitignore`, CONTRIBUTING.md, SECURITY.md, CODEOWNERS, and `dependabot.yml` if it uses version updates. GitHub surfaces several of them automatically, and organization-wide defaults for community files can live in a public repository named `.github`. A missing `.gitignore` is a security issue: once a secret is committed it stays in history even if the next commit deletes it.

**Think of `.gitignore` like a "do not pack" list for airport security**: it's far easier to leave the knife at home than to explain it at the gate.

![A repository's root and .github folder hold the README, LICENSE, .gitignore, CONTRIBUTING, SECURITY, CODEOWNERS and dependabot.yml, grouped by what each one protects: people, legal terms, secrets, reviews and dependencies.](/content/skillup/ghbp/images/ghbp-3-1-repo-files.svg)

### Real use

A platform team ships a repository template with a stack-specific `.gitignore` (`.env`, `*.pem`, `*.key`), CODEOWNERS and `dependabot.yml`, and keeps SECURITY.md, CONTRIBUTING.md and issue templates in the organization's `.github` repository. Every new service starts with the essentials on day one.

### How it works

A developer runs `git add .` with a `.env` file present, and production credentials go into a commit every clone now carries forever.

- Ask: could a new contributor set up, contribute and report a security problem using only what's in the repo?
- `.gitignore` must exist per repository, because it's specific to the stack.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Files in each repository | Stack-specific files like `.gitignore` and CODEOWNERS | Copies to maintain |
| Organization `.github` defaults | Community files (SECURITY, CONTRIBUTING, templates) shared by many repos | A repo's own file overrides them |
| Repository template | New repos should start complete | Existing repos aren't updated |

### Exam Trap ⚠️

<div class="note-trap">Deleting the file in the next commit doesn't remove a committed secret; the earlier commit still holds it. The first response is to revoke and rotate the secret, and only then, if needed, rewrite history.</div>

### Go deeper

- [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)

---

## 3.2 Stop leaked secrets with secret scanning and push protection

### Key Concept

**Secret scanning finds leaked secrets after the fact; push protection stops supported secrets before they land.**

**Secret scanning** scans history, issues, PRs and discussions for known secret formats, custom patterns and AI-detected generic secrets, and raises alerts. **Push protection** checks content at push time (command line, web UI, uploads, REST API) and rejects pushes containing supported secrets. By default a contributor can bypass with a reason; **delegated bypass** turns that into a request designated reviewers must approve.

**Think of push protection as a metal detector at the door and secret scanning as the CCTV**: one stops things coming in, the other shows what's already inside.

![A push containing a secret is stopped by push protection before it reaches the repository, a secret already in history is found by secret scanning, and the remediation order is rotate first, check logs, then optionally rewrite history.](/content/skillup/ghbp/images/ghbp-3-2-push-protection.svg)

### Real use

A cloud team enables push protection with delegated bypass on its infrastructure repositories. When an engineer pastes an AWS key into a Terraform file, the push is rejected with the exact line, and the key never reaches GitHub.

### How it works

An AWS key pushed to a public repo is found by automated scrapers within minutes, long before the next day's review.

- Bypass reasons "used in tests" and "false positive" create *closed* alerts; "I'll fix it later" creates an *open* alert. Every bypass is logged and emailed.
- After a leak: revoke and rotate, check the provider's logs, then optionally rewrite with `git-filter-repo` and ask GitHub Support to clear cached views.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Push protection, self-service bypass | Most repositories | Contributors decide their own bypasses |
| Push protection with delegated bypass | High-value credentials | Bypasses wait for a reviewer |
| Secret scanning alerts | Always, to catch what's already in history | Detects after the fact |

### Exam Trap ⚠️

<div class="note-trap">"Secret scanning blocked the push" is wrong: push protection blocks, secret scanning alerts. Bypass needs approval only with delegated bypass. And a history rewrite is clean-up; rotation is the fix.</div>

### Go deeper

- [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)
- [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

---

## 3.3 Choose GitHub Secret Protection or Code Security and enforce them with security configurations

### Key Concept

**GitHub Advanced Security is sold as two products, Secret Protection and Code Security, and enforced at scale with security configurations.**

**Secret Protection** covers secret scanning, push protection, AI-detected secrets, custom patterns and delegated bypass. **Code Security** covers code scanning, Copilot Autofix, dependency review and security campaigns. Both need GitHub Team or Enterprise for private repositories. **Security configurations** apply a chosen set of features to many repositories, and a custom configuration with **Enforce configuration** blocks owners from changing what it sets.

**Think of security configurations as a building's fire code**: tenants can decorate as they like, but they can't remove the sprinklers.

![Secret Protection groups secret scanning, push protection and custom patterns, Code Security groups code scanning, Autofix and dependency review, and an enforced security configuration applies the chosen features to a class of repositories.](/content/skillup/ghbp/images/ghbp-3-3-security-products.svg)

### Real use

A 300-repository organization applies a custom security configuration with push protection, secret scanning and Dependabot to every `tier=critical` and `tier=standard` repository, with Enforce on. Sixty repositories whose owners had switched scanning off are back on, and stay on.

### How it works

A team disables secret scanning on a noisy repository "temporarily", and nobody notices for a year because each repository's settings were managed by hand.

- Security overview *reports* coverage and alerts; configurations with Enforce *enforce*.
- Features a configuration leaves unset aren't enforced.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Secret Protection only | The need is credentials and leaks | No code scanning on private repos |
| Code Security | You need code scanning, Autofix and dependency review | Separate purchase |
| Enforced custom configuration | Many repo admins and a non-negotiable baseline | Owners can't opt out |
| GitHub-recommended configuration | A small organization getting started | Less tailored |

### Exam Trap ⚠️

<div class="note-trap">"Push protection is part of Code Security" is wrong; it's in Secret Protection. "Security overview enforces settings" is wrong; it reports, and enforced configurations enforce.</div>

### Go deeper

- [About GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)
- [Organization security at scale](https://docs.github.com/en/code-security/concepts/security-at-scale/organization-security)

---

## 3.4 Block vulnerable and non-compliant dependencies with dependency review

### Key Concept

**Dependabot tells you about vulnerable dependencies you already have; dependency review stops a PR from adding new ones.**

The **dependency review action** (`actions/dependency-review-action`) compares a PR's dependency changes against the GitHub Advisory Database and fails when a change introduces a vulnerability at or above `fail-on-severity`. It can scope failures with `fail-on-scopes` and enforce licenses with **either** `allow-licenses` **or** `deny-licenses`, using SPDX identifiers. Like every gate, it blocks only when the check is required.

**Think of dependency review as customs at the border, and Dependabot alerts as recall notices for goods already in the country.**

![A pull request's dependency changes are checked against the advisory database and the license allow list, and a required dependency review check blocks the merge on a high-severity vulnerability or a disallowed license.](/content/skillup/ghbp/images/ghbp-3-4-dependency-review.svg)

### Real use

A software vendor requires dependency review on every PR to `main` with `fail-on-severity: high` and an allow list of MIT, Apache-2.0, BSD-3-Clause and ISC. A PR that pulls in a GPL-licensed package fails before legal ever has to find it.

### How it works

A PR adds a package with a known critical CVE, CI is green because the tests pass, and it reaches production before Dependabot raises an alert on main the next morning.

- Prevention at the PR is dependency review as a required check; learning about existing risk is Dependabot alerts.
- To make the gate tamper-proof across repos, require it with an organization ruleset (1.6).

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Dependency review as a required check | You must stop new risk at the PR | A check to maintain |
| Ruleset-required dependency review workflow | Teams must not be able to weaken the gate | Org ruleset needed |
| Dependabot alerts | Always, to watch merged code as new advisories appear | Detects after merge |

### How to do it

```yaml
# .github/workflows/dependency-review.yml
on: pull_request
permissions:
  contents: read
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-sha>  # vX.Y.Z
      - uses: actions/dependency-review-action@<full-sha>  # vX.Y.Z
        with:
          fail-on-severity: high
          allow-licenses: MIT, Apache-2.0, BSD-3-Clause, ISC
```

### Exam Trap ⚠️

<div class="note-trap">Dependabot alerts don't block PRs, and code scanning analyses your code, not your dependency manifests. License gating comes from dependency review (or a ruleset license rule), not from Dependabot.</div>

### Go deeper

- [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review)

---

## 3.5 Structure contributions with pull request and issue templates

### Key Concept

**Templates move the questions reviewers and triagers always ask to the moment the author is filling in the form.**

A PR template (`.github/pull_request_template.md`, or several under `.github/PULL_REQUEST_TEMPLATE/`) pre-fills the PR description. **Issue forms** (`.github/ISSUE_TEMPLATE/*.yml`) render real form fields with validation, so "Steps to reproduce" can be required. A `config.yml` in the same folder can turn off blank issues and link to discussions or the security policy.

**Think of a template as the pre-flight checklist for authors**: it doesn't fly the plane, but it makes skipping a step a conscious choice.

![A bug report opened through an issue form must fill required fields before it can be submitted, a PR template prompts for what, why and how it was tested, and config.yml turns off blank issues and sends security reports to private reporting.](/content/skillup/ghbp/images/ghbp-3-5-templates.svg)

### Real use

An open-source project replaces its Markdown bug template with an issue form that requires version and steps to reproduce, and disables blank issues. First replies stop being "which version?", and triage time drops noticeably.

### How it works

A 2,000-line PR titled "Fix stuff" with no description gets a tired "LGTM", and a week later nobody can tell why the authentication flow changed.

- Issue forms can make fields required; Markdown templates can't.
- A PR template's checklist makes an omission visible, though it doesn't enforce code quality.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Issue forms (YAML) | Fields must be required | More setup than Markdown |
| Markdown issue or PR template | Light prompts are enough | Authors can delete the text |
| A three-line PR template | Small teams | Less context captured |

### How to do it

```yaml
# .github/ISSUE_TEMPLATE/bug-report.yml
name: Bug Report
description: Report a reproducible bug
labels: [bug, triage]
body:
  - type: textarea
    id: reproduction
    attributes: { label: Steps to reproduce }
    validations: { required: true }
```

### Exam Trap ⚠️

<div class="note-trap">A "word-count check on PR descriptions" or a "PR size limit" is the distractor when the problem is missing context; the native answer is a PR template. Only issue forms can make fields required.</div>

### Go deeper

- [About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)

---

## 3.6 Handle vulnerability reports privately with a security policy

### Key Concept

**Private vulnerability reporting gives researchers a confidential channel; SECURITY.md tells them how you'll handle what they send.**

When owners or admins enable **private vulnerability reporting** on a public repository, reporters submit details privately from the Security tab as a draft security advisory, and maintainers are notified at once. It doesn't depend on a SECURITY.md file. **SECURITY.md** is the policy: supported versions, how to report and expected response times. Maintainers then fix privately in a **repository security advisory**, optionally request a CVE, and publish with the release.

**Think of private reporting as the hospital's side entrance for emergencies**: the urgent case doesn't have to queue through the public waiting room.

![A researcher's report goes privately through the Security tab into a draft advisory seen only by maintainers, who fix it in a private fork, request a CVE and publish the advisory with the release, instead of the report appearing as a public issue.](/content/skillup/ghbp/images/ghbp-3-6-private-reporting.svg)

### Real use

A popular parsing library enables private reporting and publishes a SECURITY.md promising a reply within 48 hours. A researcher reports a SQL injection privately, the fix and the advisory ship together, and users learn about the bug with the patch already available.

### How it works

Without either, a researcher posts "SQL injection with a working exploit" as a public issue, it's indexed within the hour, and every user is exposed before a patch exists.

- If it already happened: lock or hide the issue, contact the reporter privately, fix and release, then publish an advisory.
- Deleting the issue doesn't undo indexing; making the repository private breaks every user.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Private reporting + SECURITY.md | Any public repository | Maintainers must respond |
| SECURITY.md pointing to a bug bounty | An established external programme exists | Researchers leave GitHub |
| Neither | Never for public projects | Reports arrive in public |

### Exam Trap ⚠️

<div class="note-trap">"Private vulnerability reporting requires a SECURITY.md" is false, and reports go to the repository's maintainers, not GitHub's security team. The harm of having neither is premature public disclosure.</div>

### Go deeper

- [Configuring private vulnerability reporting for a repository](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
- [Adding a security policy to your repository](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy)

---

## 3.7 Standardize commit messages with Conventional Commits

### Key Concept

**Conventional Commits turn commit messages into machine-readable release instructions.**

The format is `<type>(<scope>): <description>` with an optional body and footers. `feat` maps to a MINOR bump and `fix` to a PATCH; a breaking change, marked with `!` (`feat!:`) or a `BREAKING CHANGE:` footer, maps to MAJOR in tools such as semantic-release. Enforce it with commitlint as a required check, or with a ruleset metadata rule that requires commit messages to match a pattern.

**Think of commit types as shipping labels**: the warehouse robot can't read your handwriting, but it can read a barcode.

![Commit types map to version bumps: fix to a patch, feat to a minor release, and an exclamation mark or BREAKING CHANGE footer to a major release, feeding an automatic changelog.](/content/skillup/ghbp/images/ghbp-3-7-commit-types.svg)

### Real use

A component library squash-merges every PR with its Conventional Commit title and runs semantic-release on `main`. Version numbers, the changelog and release notes generate themselves, and a `feat!:` change can never sneak out in a minor release.

### How it works

Release notes written by hand from "fix", "wip" and "stuff" mean version numbers stop meaning anything, and consumers get breaking changes in minor releases.

- Squash merging pairs well: each PR becomes one well-formed commit on main.
- Lint PR titles or commits as a required check, or reject bad messages at push with a ruleset commit-message pattern.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Conventional Commits + release tooling | You publish versions and changelogs | Contributors learn the format |
| Ruleset commit-message pattern | Messages must be rejected at push | Needs rulesets |
| Imperative summary + issue link | Apps that deploy continuously without versions | No automatic versioning |

### Exam Trap ⚠️

<div class="note-trap"><code>feat!:</code> is MAJOR, not MINOR, because the <code>!</code> overrides the type, and a <code>BREAKING CHANGE:</code> footer does the same. Watch for distractors that read only the type prefix.</div>

### Go deeper

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

---

## 3.8 Govern visibility, archiving, topics and custom properties

### Key Concept

**Visibility controls who can see a repository; archiving freezes it; topics and custom properties make it findable and governable.**

Repositories are **public**, **private**, or **internal** (GitHub Enterprise: visible to every enterprise member, not to the public or outside collaborators). **Archiving** makes the whole repository read-only, including issues, PRs and the wiki. **Topics** are free-form labels for discovery; **custom properties** are organization-defined, typed metadata (`tier: critical`) that rulesets and security configurations can target.

**Think of topics as hashtags and custom properties as the fields on an asset register**: one helps people find things, the other lets policy act on them.

![Public, internal and private visibility are compared by who can see the repository, archiving freezes a retired repository, topics help people find repositories, and custom properties let rulesets and security configurations target them.](/content/skillup/ghbp/images/ghbp-3-8-visibility.svg)

### Real use

An enterprise makes shared libraries internal so every engineer can read and reuse them, tags them with topics like `terraform` and `payments`, and sets a required `tier` property that its organization rulesets and security configuration target.

### How it works

An internal tool is made public "so everyone can see it" and is exposed to the internet, or kept private so every team must request access. Meanwhile "protect every production service" is impossible because nothing records which repos are production services.

- Use topics for discovery and custom properties for governance.
- Retire one branch with lock branch; retire a whole repository with archive.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Internal visibility | Inner-source code for the whole enterprise | Needs GitHub Enterprise |
| Archive | The repository is retired but must stay readable | Everything becomes read-only |
| Custom properties | A policy must select a group of repositories | Properties must be kept accurate |
| Topics | People need to find repositories | Policies can't target topics |

### Exam Trap ⚠️

<div class="note-trap">"Private with an Everyone team" isn't internal, and "lock all branches" isn't archive, because issues and PRs stay open. Organization rulesets target repositories by name or custom property, not by topic.</div>

### Go deeper

- [Archiving repositories](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories)
- [Managing custom properties for repositories in your organization](https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization)

---

## 3.9 Choose the right machine identity for automation

### Key Concept

**Automation should authenticate as itself, with short-lived and narrowly scoped credentials, never as a person.**

A **GitHub App** is the recommended identity for organization automation: not tied to a user, no seat, fine-grained permissions on selected repositories, and installation tokens that expire after one hour. A **deploy key** is an SSH key for one repository, read-only unless you grant write, and it doesn't expire. **Personal access tokens** act as a person and break when that person leaves. **OIDC** removes stored cloud credentials (2.3).

**Think of a GitHub App as a company car with a fuel card limited to work routes**: it belongs to the organization, not to whoever is driving.

![Each automation need maps to its identity: GitHub API work across repositories to a GitHub App with one-hour tokens, a server pulling one repository to a read-only deploy key, cloud deploys to OIDC, and personal scripts to a short-lived fine-grained token.](/content/skillup/ghbp/images/ghbp-3-9-machine-identities.svg)

### Real use

A company replaces a departed engineer's PAT in its release pipeline with a "release-bot" GitHub App that has `contents: write` on the release repositories only. Releases keep working through staff changes, and every token the bot uses expires within the hour.

### How it works

A release pipeline running on a departed engineer's PAT stops when their account is deactivated, or keeps working from their laptop after they've left.

- One deploy key per server, read-only by default.
- GitHub Packages with a classic PAT needs `read:packages` to install and `write:packages` to publish; in Actions, prefer `GITHUB_TOKEN` with `packages: write`.
- Machine accounts are allowed, but they use a seat and need a responsible human owner.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| GitHub App | Cross-repo automation, bots, release tooling | An app to register |
| Deploy key (read-only) | A server only needs to `git pull` one repo | No expiry; rotate manually |
| OIDC | Deploying to AWS, Azure or GCP | Cloud trust policy to maintain |
| Fine-grained PAT | Personal or one-off scripts | Tied to a person |

### Exam Trap ⚠️

<div class="note-trap">"A bot account is against GitHub's Terms" is false. A deploy key "with write access shared across servers" combines two risks: excess privilege and key reuse. A 401 from GitHub Packages usually means the PAT lacks <code>read:packages</code>.</div>

### Go deeper

- [About creating GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps)
- [Managing deploy keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)

---

## 3.10 Audit changes and verify webhook deliveries

### Key Concept

**The audit log records who changed what in your organization; webhook signatures prove a payload really came from GitHub.**

The organization **audit log** records security-relevant events with actor and timestamp: membership and permission changes, repository visibility and deletion, branch protection and ruleset changes, secrets, app authorizations and push protection bypasses. On GitHub Enterprise Cloud it can be **streamed** to a SIEM. Webhooks configured with a secret are signed with HMAC-SHA256 in `X-Hub-Signature-256`, and the receiver verifies it over the raw body in constant time.

**Think of the audit log as the building's sign-in book and the webhook signature as the wax seal on a letter**: one tells you who came in, the other that the message wasn't forged.

![Organization events flow into the audit log and on to a SIEM for alerting, while a webhook receiver recomputes the HMAC signature over the raw body and rejects any payload whose signature doesn't match.](/content/skillup/ghbp/images/ghbp-3-10-audit-webhooks.svg)

### Real use

A bank streams its audit log to its SIEM and alerts on ruleset and branch protection changes, and its deploy service verifies `X-Hub-Signature-256` on every webhook. When someone relaxes a ruleset at 2 am, the security team knows by 2:01.

### How it works

After a breach, nobody can say who turned off a protection rule, because the log was never retained. Separately, a deploy service that accepts any POST claiming to be a push event can be triggered by anyone who can reach it.

- TLS protects the payload in transit but doesn't prove the sender; `X-GitHub-Event` can be set by anyone.
- IP allowlisting is an extra layer, never a substitute for signatures.

### Choose when

| Option | Choose it when | Trade-off |
|---|---|---|
| Audit log streaming to a SIEM | You need retention and real-time alerts | Enterprise Cloud; SIEM costs |
| Audit log in the UI or API | Occasional investigations | Shorter retention |
| Webhook secret + signature check | Any webhook receiver | A secret to manage |

### How to do it

```python
import hmac, hashlib

def verify(secret: bytes, body: bytes, header: str) -> bool:
    expected = "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header)
```

### Exam Trap ⚠️

<div class="note-trap">Only the HMAC signature authenticates the sender; TLS and the <code>X-GitHub-Event</code> header don't. And the git log records commits, not access or permission events; for those, use the audit log.</div>

### Go deeper

- [Reviewing the audit log for your organization](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)
- [Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)

---

## Deep Dive: Making Repository Governance Click

### 1. The connective narrative

Repository governance has two halves that people often treat separately: **security features that watch the code** and **conventions that shape how people work**. They solve the same problem from two directions. Push protection, dependency review and code scanning catch dangerous changes mechanically. Templates, CODEOWNERS, commit conventions and security policy make sure the humans in the loop have the context to catch what machines can't.

The security features line up along a time axis. **Before the commit**: `.gitignore` and local pre-commit scanners. **At push**: push protection and push rulesets. **At the PR**: dependency review, code scanning results and required reviews. **After merge**: secret scanning alerts, Dependabot alerts and security updates, and scheduled code scanning. **After disclosure**: private vulnerability reporting and security advisories. A mature repository has something at every point, and the exam often asks which point a given control acts at.

Scale is the final piece. One well-configured repo is easy; four hundred are not. Custom properties describe repositories, security configurations (with Enforce) and organization rulesets act on those descriptions, security overview measures the result, and the audit log records every exception. GitHub Apps and OIDC keep the automation that does all this from depending on any one person's credentials.

### 2. Worked scenario

> **Scenario.** A 300-repository organization on GitHub Enterprise Cloud has these findings: secret scanning disabled on 60 private repos by their owners; an AWS key pushed to a private repo last month; two public libraries with no way to report vulnerabilities privately; a release pipeline using a departed engineer's PAT; and nobody can say who disabled branch protection on `billing-api`.
>
> **Step 1: Describe the estate.** Define a custom property `tier` (`critical`, `standard`, `sandbox`) and set it on every repository.
>
> **Step 2: Enforce the baseline.** Create a custom security configuration: dependency graph, Dependabot alerts and security updates, secret scanning, push protection, and private vulnerability reporting (which applies to public repos). Apply it to `tier=critical` and `tier=standard`, with policy **Enforce configuration**. The 60 repos are re-enabled, and owners can no longer turn the features off.
>
> **Step 3: Handle the leaked key correctly.** Revoke and rotate the AWS key first, then check CloudTrail for use during the exposure window. Only then decide whether rewriting history is worth the disruption. The rotation is the fix; the rewrite is hygiene. Configure delegated bypass for push protection on critical repos, so the next bypass needs a security reviewer.
>
> **Step 4: Open a private channel.** On the two public libraries, enable private vulnerability reporting and add SECURITY.md files listing supported versions and response times.
>
> **Step 5: Replace the human credential.** Register a "release-bot" GitHub App with `contents: write` on the release repositories only. Its one-hour installation tokens are minted per run, and the departed engineer's PAT is revoked.
>
> **Step 6: Make changes attributable.** Stream the audit log to the SIEM and alert on `protected_branch` and ruleset changes. The `billing-api` question is answered from the log, and the next such change raises an alert in real time.
>
> **Outcome:** Each finding maps to one mechanism: properties describe, configurations enforce, rotation remediates, private reporting channels disclosure, Apps replace people, and the audit log attributes changes.

### 3. Memory aid

**SHIELD**: the layers of repository governance:

- **S**ecrets: `.gitignore`, push protection, secret scanning; rotate first
- **H**ygiene files: README, LICENSE, CONTRIBUTING, templates
- **I**dentities: GitHub Apps, read-only deploy keys, OIDC, no personal PATs
- **E**nforcement at scale: custom properties, security configurations (Enforce), org rulesets
- **L**ogs: audit log streaming, signed webhooks
- **D**isclosure and dependencies: private vulnerability reporting, SECURITY.md, Dependabot, dependency review

### 4. Exam strategy for this domain

- **Place the control on the timeline.** "Before it reached GitHub" means push protection. "Before the PR merged" means dependency review or code scanning as a required gate. "After it's already in the repo" means secret scanning alerts or Dependabot alerts.
- **Know which product a feature belongs to.** Secret Protection covers secrets and push protection; Code Security covers code scanning, Autofix and dependency review. Questions about buying "just enough" hinge on this.
- **Report vs enforce.** Security overview, the dependency graph and Dependabot alerts *report*; security configurations with Enforce, rulesets and required checks *enforce*.
- **Remediation order.** For leaked secrets, rotate first; history rewriting is clean-up, never the fix.
- **Absolute-language distractors.** "GitHub requires SECURITY.md for private reporting", "bot accounts violate the Terms", "deleting the issue removes the disclosure" are all wrong.
- Five minutes before the exam: *Detect early, enforce centrally, rotate first, and never let automation borrow a person's identity.*

---

## Cheat Sheet 📋

| Item | Location / setting | Key rule |
|---|---|---|
| `.gitignore` with secrets/artifacts excluded | Root | Critical; prevents the commit entirely |
| Push protection | Security settings / security configuration | Blocks at push; bypass reasons create closed or open alerts |
| Secret scanning | Security settings | Alerts on secrets already in history |
| Leaked secret | Provider + repo | Rotate first, then optionally `git-filter-repo` + GitHub Support |
| Secret Protection vs Code Security | Billing / licensing | Secrets + push protection vs code scanning + Autofix + dependency review |
| Security configurations | Org settings → Code security | "Enforce configuration" blocks owner changes |
| Dependency review | `actions/dependency-review-action` | Required check; `fail-on-severity`; `allow-licenses` or `deny-licenses` |
| SARIF from third-party tools | `github/codeql-action/upload-sarif` | `security-events: write` |
| PR template | `.github/pull_request_template.md` | Structures context |
| Issue forms | `.github/ISSUE_TEMPLATE/*.yml` | Can require fields; `config.yml` disables blank issues |
| Security policy | `SECURITY.md` | Recommended; not required for private reporting |
| Private vulnerability reporting | Repo settings (public repos) | Reports go privately to maintainers as draft advisories |
| Conventional Commits | commitlint / ruleset metadata | `feat!` or `BREAKING CHANGE:` = MAJOR |
| Visibility | Public / private / internal | Internal = enterprise members only |
| Archive | Repo settings → Danger zone | Whole repo read-only, including issues/PRs |
| Custom properties | Org settings | Targets for rulesets and security configurations |
| GitHub Apps | Org-owned app | 1-hour installation tokens; no seat; fine-grained |
| Deploy keys | Repo settings | One per server, read-only by default; no expiry |
| Packages auth | Classic PAT scopes | `read:packages` / `write:packages` |
| Audit log | Org / enterprise settings | Stream to SIEM on Enterprise Cloud |
| Webhooks | Webhook secret | Verify `X-Hub-Signature-256` HMAC-SHA256 |
