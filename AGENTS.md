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

<!-- BEGIN agent-standards:baseline v=fc4d2520fd - managed by agent-standards; edit baseline.md there and run `agentstd sync`, not this block -->
## Shared rules (all agents, all projects)

These rules come from real incidents: an agent once took a one-word reply as approval,
its backup attempt failed, and it wiped a secrets store anyway; a later sweep found live
passwords in unit files, `.env` files, container config and process arguments.

### Destructive actions — hard rules
1. **Explicit yes to the exact action.** Before deleting, wiping, re-initialising,
   force-pushing, dropping or overwriting anything stateful, state the exact command and
   what will be lost, then wait for an unambiguous "yes" to *that* command. A vague,
   one-word or frustrated reply is **not** approval — ask again.
2. **Safety net first, or stop.** Take a snapshot/backup before the destructive step. If it
   fails, **stop and report** — never proceed without it. Check that the snapshot actually
   covers the data (separate volumes are often not in a container snapshot).
3. **Move aside, don't delete.** Prefer `mv x x.bak-<date>` over `rm -rf`.
4. **Never wipe or re-initialise a secrets store or identity system.** Lost access means
   asking the owner to unseal / recover — not starting over.
5. **"Blocked" is an answer.** If you lack access or permission, say what is blocked and
   what the user can do. Don't find a workaround that destroys state or bypasses a control.

### Secrets
1. **Secrets live in the secret store** (e.g. Vault) and services read them at start. Never
   put a secret in a repo file, `.env`, unit file, compose file, container config, chat,
   log or command-line argument.
2. **Never display secret values**, even while debugging: print variable *names* only and
   compare secrets by hash or equality. Never ask the user to paste a secret into chat —
   have them run the command, or read it from a file inside the command.
3. **Pass secrets via stdin or files, never argv** — argv is readable by every process
   (`/proc/<pid>/cmdline`, `ps`). With curl:
   - body: `--data @<(printf '{"secret_id":"%s"}' "$SID")` or `--data @-`
   - headers: `-K <(printf 'header = "Authorization: Bearer %s"\n' "$TOKEN")`
   - CI secret variables: map them through the step's `env:`; never inline a secret
     variable macro (e.g. `$(SECRET)`) into script text.
   - **Never trace a shell that holds a secret.** `set -x` / `bash -x` prints every
     expanded argument, so a secret held in a variable is printed even though it never
     reaches argv (`printf 'header = "X-Vault-Token: %s"' "$TOKEN"` leaks the token under
     `-x`). Debug with fingerprints or hashes, not with a trace - and have a script that
     handles secrets refuse to run under one: `case "$-" in *x*) exit 1;; esac`.
4. **Rotating = change the store, restart the consumer.** If a rotation needs editing files
   on the consumer, wire the consumer to the store first.
5. **Don't echo secrets through tools, docs or exports.** Most leaks here were not committed
   on purpose - a command printed a value and it was copied on. So:
   - commands that dump values (`incus config show`, `docker inspect`, `env`, `printenv`,
     `cat` of `.env`/unit files, `set -x`, `vault kv get` without `-field`) only with the
     values filtered out - list names, or use a hash/length check;
   - docs, findings and Markdown get placeholders (`<redacted>`, `kv/<path>`), never the
     value - not even a rotated or "dead" one;
   - app exports (Flowise, n8n, Grafana, …) are scrubbed before they are saved to a repo:
     `~/agent-standards/checks/scrub-export.py`;
   - masking matches the value's shape (`user:PASS@host`, `[A-Za-z0-9]+`), not just names.
   The pre-commit hook (`~/agent-standards/hooks/pre-commit`) blocks the commit if one slips.
6. **Never pipe a whole config/env dump to stdout — allowlist the shape, don't denylist.**
   A filter that does not match the tool's real output format leaks the secret with extra
   steps. Real leaks here came from exactly that: a `sed` written for `value: ` applied to
   `incus config show`'s `key: value` YAML, and `grep -i secret` on a dump whose secrets did
   not contain the word "secret".
   - **Allowlist**: print the keys you need, never the whole dump. `incus config get <inst>
     <key>` · `vault kv get -field=<f> <path>` · `jq -r 'keys[]'` · `systemctl show -p
     Environment | tr ' ' '\n' | cut -d= -f1` · `~/agent-standards/checks/config-names.py`
     for a names-only view of any dump.
   - **Never mix**: if one command returns both secret and non-secret lines, split it — a
     name-based filter cannot tell `NEXTAUTH_SECRET=x` from `DATABASE_URL=y`.
   - **Prove the filter fired**: a redaction count of 0 means the pattern did not match. Stop,
     read the tool's real output shape, fix the filter. Do not print it again to "check".
7. **The transcript is the leak.** Anything printed lands in a chat log, a session file and
   provider telemetry. Treat a printed value as published:
   - a value printed once is exposed and must be **rotated** — not "redacted afterwards";
   - never verify a secret by printing it; compare by hash (`sha256sum | cut -c1-12`) or by
     equality;
   - if a secret was printed, say so immediately, name every copy of it (secret-store path,
     container config, env file, repo), and propose rotation. Do not quietly move on.

### Git and publishing
- **Stage files by name.** Never `git add -A` / `git add .` — working trees hold private
  drafts. Never force-push or rewrite shared history without rule 1 of Destructive actions.
- **Public repos: every commit is publishing.** No internal hostnames, IPs, subnets,
  instance names, secret-store paths, employer-identifying details, or job-application
  material. Run the repo's pre-publish/security checks before pushing.
- Keep commits scoped to the request; never commit `.env` or credentials, even "temporarily".

### Working style
- Read only what the task needs; ignore `node_modules`, `dist`, `build`, `target`, `.git`,
  virtualenvs. Prefer the project's own scripts over new toolchains.
- Close stdin on commands that could prompt or block — `incus exec`, `docker exec`, `ssh`,
  `vault`, `psql`, `kubectl`: end them with `</dev/null`. An open stdin can hang the call
  indefinitely, and a hung call tempts a retry that repeats a side effect.
- Match existing style, layout and naming. Keep changes scoped; preserve public interfaces
  unless asked to break them.
- Validate external input; no SQL/command injection. Never disable auth, TLS verification
  or sandboxing for convenience — fix the trust chain instead.
- Report outcomes faithfully: say what was verified and how, and say plainly when something
  failed or was skipped.
- After changes, summarize the paths changed and how to verify them.
<!-- END agent-standards:baseline -->
