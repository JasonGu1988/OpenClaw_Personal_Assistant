#!/usr/bin/env python3
"""Conservative publication guard; not a substitute for manual review/Gitleaks."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    '.gitignore', 'README.md', 'MANIFEST.sha256',
    'config/openclaw.patch.json', 'config/telegram-disabled.patch.json',
    'docs/INITIALIZATION.md', 'docs/GMAIL.md', 'docs/PRIVACY.md',
    'scripts/gmail_groomer.py', 'scripts/requirements-gmail-groomer.txt',
    'scripts/check_public_backup.py', 'tests/test_gmail_groomer.py',
} | {
    f'workspace/{agent}/{name}.md'
    for agent in ('main', 'developer', 'specialist')
    for name in ('AGENTS', 'SOUL', 'IDENTITY', 'USER', 'HEARTBEAT')
}
PATTERNS = {
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'provider token': r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
    'bot token': r'\b[0-9]{6,}:[A-Za-z0-9_-]{30,}\b',
    'owner home path': r'(?:/Users/|/home/)[A-Za-z0-9_.-]+/',
}
EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b')


def main() -> int:
    result = subprocess.run(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        cwd=ROOT, check=True, capture_output=True,
    )
    paths = sorted(set(result.stdout.decode().split('\0')) - {''})
    failures = []
    for name in paths:
        path = ROOT / name
        if name not in ALLOWED:
            failures.append(f'{name}: path not allowlisted')
            continue
        if path.is_symlink() or not path.is_file():
            failures.append(f'{name}: must be a regular file')
            continue
        try:
            value = path.read_text(encoding='utf-8')
        except UnicodeError:
            failures.append(f'{name}: must be UTF-8 text')
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, value):
                failures.append(f'{name}: {label} detected (value omitted)')
        if any(not m.group(1).lower().endswith('.invalid') for m in EMAIL.finditer(value)):
            failures.append(f'{name}: non-placeholder email detected (value omitted)')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print(f'PASS: {len(paths)} files checked against public allowlist/content rules.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
