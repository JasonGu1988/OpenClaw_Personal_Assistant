# Public-backup policy

This public repository contains allowlisted reusable code, synthetic tests, newly written generic templates, non-secret policy settings, and documentation. Raw private files were never staged.

Configuration was constructed from explicit harmless selections. Human names, owner paths, account/group/chat IDs, bindings, access lists, tokens, provider sessions, and secret values were not copied. The classifier's owner name and personal billing assumption were generalized.

## Never include

- Original user profiles, private identity/role files, memories, dreams, conversations, or private-context prompts.
- Investment positions, watchlists tied to the owner, trades, balances, banking/brokerage data, financial spreadsheets, or private investment analysis.
- OAuth tokens, app passwords, API keys, Gateway/bot tokens, client-secret JSON, private keys, cookies, auth profiles, or service environments.
- Pairing/device identities, cron state, execution history, attachments, databases, logs, caches, or complete OpenClaw archives.
- Personal authorship metadata in new commits, private URLs, host-specific owner paths, or real personal email addresses.

Generic billing/security code and synthetic test cases are not financial records. `example.invalid` addresses are placeholders. GitHub repository-owner metadata necessarily remains visible.

## Future updates

1. Work in the sanitized checkout, never push the private runtime workspace.
2. Copy only approved paths after local review. Generalize private context explicitly.
3. Run `python3 scripts/check_public_backup.py`, which checks tracked paths and non-ignored working files.
4. Run Gitleaks on files and Git history with redaction enabled.
5. Privately compare files against known sensitive local identifiers/secrets. Never publish comparison values or detailed findings.
6. Regenerate `MANIFEST.sha256`, excluding itself, Git internals, environments, and bytecode; verify checksums.
7. Inspect the staged diff and use a generic commit author. Preserve unrelated repository history; do not force-push.

Ignore rules and scanners are defense-in-depth, not proof arbitrary text contains no personal information. Manually review every publication. Deleting files from the latest revision does not remove them from Git history.
