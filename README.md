# OpenClaw Personal Assistant — Sanitized Backup

Public-safe backup of reusable configuration, agent templates, and mail automation.
This is a **reconstruction kit**, not a full copy of the live installation. Private state must be recreated locally.

## Setup snapshot

Observed on 2026-10-10:

| Component | Current architecture |
| --- | --- |
| Runtime | OpenClaw 2026.9.9 (`bcfc888`), macOS, Node.js 26.3.0 |
| Python | Python 3.13.12; isolated virtual environment recommended |
| Gateway | Local, loopback-only, port 18790, token authentication |
| Agents | Main coordinator plus coding and specialist workspaces; public templates use generic identities |
| Default model | `openai/gpt-6.1-sol` |
| Additional allowed models | `openai/gpt-6-astra`, `openai/gpt-6-sol`, `openai/gpt-6-luna` |
| Heartbeat model | `openai/gpt-6-luna`, coordinated by `main` |
| Provider login | OpenAI OAuth; login/session data excluded |
| Plugins | `openai`, `codex`, `telegram`, `parallel` enabled |
| Messaging | Telegram; token, destinations, bindings, and group policy excluded |
| Tools / sessions | Coding tool profile; DMs isolated per channel/peer |
| Optional skills | Existing disabled-skill choices retained in the configuration patch |
| Local automation | Gmail grooming helper supporting IMAP app passwords or Gmail OAuth |

Model names reflect this installation's catalog, not guaranteed availability in every account or release. Select available equivalents when restoring elsewhere.

## Contents

- `config/openclaw.patch.json`: allowlisted non-secret settings, merged into a freshly initialized configuration.
- `config/telegram-disabled.patch.json`: messaging stays off until local setup is complete.
- `workspace/`: newly written generic agent templates, not copies of private profiles.
- `scripts/gmail_groomer.py`: reusable source with owner-specific instructions generalized.
- Python dependencies and synthetic tests.
- [Initialization guide](docs/INITIALIZATION.md), [mail setup](docs/GMAIL.md), and [privacy policy](docs/PRIVACY.md).
- `scripts/check_public_backup.py`: strict file allowlist and basic sensitive-content checks.
- `MANIFEST.sha256`: artifact checksums, excluding the manifest itself.

## Start here

Follow [docs/INITIALIZATION.md](docs/INITIALIZATION.md) to install OpenClaw, authenticate locally, merge configuration, and initialize workspaces.

No scheduled jobs are automatically installed. Existing prompts, cron payloads, timing, recipients, and execution history are intentionally excluded; recreate only the jobs you need locally.

## Excluded

No human-owner profiles, personal email addresses, investment holdings, balances, transactions, financial records, private notes, memories, transcripts, credentials, tokens, pairing identities, logs, caches, attachments, or raw configuration backups are included. The GitHub repository URL and repository-owner attribution are inherently public platform metadata, not exported assistant data.

## Validate before publishing changes

```bash
python3 scripts/check_public_backup.py
shasum -a 256 -c MANIFEST.sha256
# Install Gitleaks separately; scan working files and Git history.
gitleaks dir . --redact
gitleaks git . --redact
```

See [docs/PRIVACY.md](docs/PRIVACY.md) for the curated backup process and its limitations.
