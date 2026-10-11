# Gmail grooming helper

Examines at most 20 selected unread inbox messages from the last 14 days. Uses an explicitly selected OpenAI model through `openclaw infer model run --local --agent main`; that command, provider access, and model must be supported locally.

The only mailbox mutation is marking qualifying messages read. Never deletes, archives, moves, labels, replies, or forwards. Uncertain, truncated, malformed, action-required, or failed classifications stay unread. Gmail OAuth requires the broad `gmail.modify` scope despite the narrower behavior.

## Install

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-gmail-groomer.txt
.venv/bin/python -m unittest discover -s tests -v
```

## Authorize locally

Replace reserved example addresses only in local commands, not tracked files. IMAP login prompts securely for an app password; the account must support Gmail app passwords.

```bash
.venv/bin/python scripts/gmail_groomer.py auth-imap --account you@example.invalid
```

Alternatively create a Google OAuth client supporting the localhost callback and keep its JSON outside this repository:

```bash
.venv/bin/python scripts/gmail_groomer.py auth \
  --account you@example.invalid \
  --client-secret /private/path/to/client_secret.json
```

Credentials are stored under `~/.openclaw/credentials/gmail-groomer/` with restrictive permissions. Never back them up publicly. OAuth URLs/callbacks and terminal output are private.

## Preview

```bash
.venv/bin/python scripts/gmail_groomer.py run \
  --account you@example.invalid --auth imap --dry-run --max 5
```

Use `--auth oauth` for OAuth. The default is `openai/gpt-6-luna`; override with `--model openai/<available-model>` if needed. Email headers/body are sent to the configured model provider. Mail content and digests must remain private.

`--dry-run` prevents mark-read operations and Telegram delivery. Omit it only when you intend mailbox mutations. `--telegram-target` additionally sends a digest outside dry-run mode; leave it unset unless that delivery is intended.

No mailbox accounts, credentials, Telegram destinations, captured emails, or cron jobs are supplied.
