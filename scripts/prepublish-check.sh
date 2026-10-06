#!/usr/bin/env bash
# prepublish-check.sh - run before every push. This repo is PUBLIC and served raw
# (.nojekyll): every committed file is fetchable at bryandebnam.com/<path>.
#
# Checks (exit 1 on any finding):
#   1. staged/committed files that should never be public (cover letters, resumes,
#      *.local.md, virtualenvs, env files);
#   2. disclosure patterns in tracked text files: private IPs/subnets, phone numbers,
#      internal hostnames (*.incus), secret-store paths;
#   3. optional extra patterns from .disclosure-denylist.local (gitignored, one
#      extended regex per line) - keep specific vendor/system/employer names THERE,
#      never in this public file;
#   4. gitleaks (full history) and semgrep ERROR-level, if installed.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
FAIL=0
hit() { echo "  ✗ $1"; FAIL=1; }

echo "1. files that must not be published"
git ls-files --cached | grep -iE '(cover[_-]?letter|resume.*\.(pdf|docx|md)$|\.local\.md$|(^|/)\.venv/|(^|/)\.env$)' \
  | while read -r f; do echo "  ✗ tracked: $f"; done | grep . && FAIL=1

echo "2. disclosure patterns"
mapfile -t FILES < <(git ls-files | grep -vE '\.(png|jpe?g|gif|svg|ico|pdf|woff2?)$|^scripts/prepublish-check\.sh$')
PATTERNS=(
  '\b10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b'                                   # RFC1918 10/8
  '\b172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3}\b'                     # RFC1918 172.16/12
  '\b192\.168\.[0-9]{1,3}\.[0-9]{1,3}\b'                                         # RFC1918 192.168/16
  '\(?\b[0-9]{3}\)?[-. ][0-9]{3}[-. ][0-9]{4}\b'                                 # phone numbers
  '\b[a-z0-9-]+\.incus\b'                                                        # internal Incus DNS
  '\b(kv|secret)/data/'                                                          # Vault KV paths
)
# Illustrative sample ranges used on purpose in the architecture deck.
ALLOW='\b10\.0\.(1|10|30|40|50)\.0/24\b'
[ -f .disclosure-denylist.local ] && mapfile -t -O "${#PATTERNS[@]}" PATTERNS < <(grep -vE '^\s*(#|$)' .disclosure-denylist.local)
for p in "${PATTERNS[@]}"; do
  grep -nHiE "$p" "${FILES[@]}" 2>/dev/null | grep -vE "$ALLOW" | while read -r h; do echo "  ✗ ${h:0:160}"; done | grep . && FAIL=1
done

echo "3. gitleaks / semgrep"
if command -v gitleaks >/dev/null; then
  gitleaks detect --source . --redact --no-banner >/dev/null 2>&1 || hit "gitleaks found secrets (run: gitleaks detect --source . -v)"
else echo "  - gitleaks not installed (CI runs it)"; fi
if command -v semgrep >/dev/null; then
  # Count real findings; a semgrep engine crash (seen locally) is a warning, not a finding.
  n="$(semgrep scan --config auto --severity ERROR --json --quiet . 2>/dev/null \
       | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d["results"]), len(d.get("errors",[])))' 2>/dev/null || echo "? ?")"
  case "$n" in
    "0 0") ;;
    "0 "*) echo "  - semgrep: 0 findings, but the engine reported errors (CI re-runs it)";;
    *)     hit "semgrep ERROR findings: ${n%% *} (run: semgrep scan --config auto --severity ERROR .)";;
  esac
else echo "  - semgrep not installed (CI runs it)"; fi

[ "$FAIL" -eq 0 ] && echo "OK - safe to publish" || { echo "FAIL - fix the above before pushing"; exit 1; }
