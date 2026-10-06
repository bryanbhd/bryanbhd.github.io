# AGENTS.md — rules for any AI agent working in this repo

This is a **public** GitHub Pages site (`bryandebnam.com`). `.nojekyll` is set, so **every
committed file is publicly fetchable** at `bryandebnam.com/<path>`. Treat every commit as
publishing.

## Build
- `portfolio.md` is the source; `index.html` is **generated** — edit the Markdown, then rebuild
  with the project's markdown-enabled Python: `<venv>/bin/python ./build_site.py`.
- Never edit `index.html` by hand. Never overwrite `CNAME`.
- `architecture/` and `model-cards/` are hand-maintained pages; edit them directly.

## Before every push
1. `bash scripts/prepublish-check.sh` must print `OK - safe to publish`.
   It checks for files that must never be public, private IPs, phone numbers, internal
   hostnames and secret-store paths, plus extra patterns in `.disclosure-denylist.local`
   (gitignored — keep specific names there, **never** in a committed file).
2. Stage files **by name**. Never `git add -A` / `git add .`: the working tree can hold
   private drafts.
3. CI (`.github/workflows/security.yml`) re-runs gitleaks (full history), semgrep and the
   disclosure check on every push.

## What must never be published
- Resumes, cover letters or anything tailored to a specific employer or application —
  those live outside this repo.
- `*.local.md` working notes, virtualenvs, env files, credentials of any kind.
- Internal network details: real subnets, hostnames, instance names, VLAN numbers, secret
  paths. Use illustrative values (the architecture deck uses `10.0.x.0/24` and
  `adatum.local` on purpose).
- Vendor names of products being monitored at work, internal system names, or details that
  identify an employer's workloads. Generic platform vocabulary is fine.
- Names of personal side projects that aren't meant to be public — describe them generically.

## Claims
Every project carries a scope tag (Pilot / Reference build / POC). Describe what was built
and verified — say "informational" when a tool reports but doesn't gate, and don't claim
controls that aren't switched on.
