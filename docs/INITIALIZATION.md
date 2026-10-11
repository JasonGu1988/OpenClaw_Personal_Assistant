# Initialization and reconstruction

Use a fresh machine/profile. Do not replace a populated configuration or workspace wholesale. Back up existing state privately, inspect it first, and merge only intended changes.

## 1. Install prerequisites and clone

Install a supported Node.js release, Git, and Python 3.13 or compatible newer Python. The observed Node.js version is a snapshot, not a minimum requirement.

```bash
npm install -g openclaw@2026.9.9
openclaw --version
git clone https://github.com/JasonGu1988/OpenClaw_Personal_Assistant.git
cd OpenClaw_Personal_Assistant
shasum -a 256 -c MANIFEST.sha256
python3 scripts/check_public_backup.py
```

The exact observed build may not be available from the public npm registry. If unavailable, install the release distributed by your OpenClaw provider, inspect `openclaw --help`, and validate the patch before applying it. Commands, plugins, and model IDs may differ across releases.

## 2. Initialize authentication and service locally

```bash
openclaw onboard --install-daemon
```

Choose a local loopback Gateway, port 18790, token authentication, and an OpenAI login available to your account. Skip optional messaging initially. Generate fresh credentials locally; never publish the previous machine's tokens. Prefer secret-reference storage when supported. Return here after any first-run conversation to install the templates.

## 3. Review and merge public configuration

```bash
openclaw config file
openclaw config patch --file config/openclaw.patch.json --dry-run
openclaw config patch --file config/openclaw.patch.json
openclaw config patch --file config/telegram-disabled.patch.json --dry-run
openclaw config patch --file config/telegram-disabled.patch.json
openclaw config validate
```

These patches contain no credentials or machine-specific paths. Objects merge recursively; the model-policy allow-array replaces that setting. The auth-mode setting preserves the token created by onboarding. Review the allowlist before merging into an existing installation.

If validation reports unavailable plugins/models, edit a local copy for your release. Select an available default with `openclaw models set <provider/model>` and update the allowlist and heartbeat model consistently. Keep login state outside Git.

## 4. Initialize agent workspaces

Run from the repository root. The copy commands refuse to overwrite existing files; reconcile an existing installation manually.

```bash
mkdir -p "$HOME/.openclaw/workspace"
cp -n workspace/main/*.md "$HOME/.openclaw/workspace/"
openclaw config set agents.entries.main.workspace "$HOME/.openclaw/workspace"

openclaw agents add tom --workspace "$HOME/.openclaw/workspace-tom" --non-interactive
openclaw agents add etienne --workspace "$HOME/.openclaw/workspace-etienne" --non-interactive
cp -n workspace/developer/*.md "$HOME/.openclaw/workspace-tom/"
cp -n workspace/specialist/*.md "$HOME/.openclaw/workspace-etienne/"
openclaw agents set-identity --agent main --name Adam
openclaw agents set-identity --agent tom --name Tom
openclaw agents set-identity --agent etienne --name Pierre
```

Agent creation/onboarding may seed default files. Inspect those files and replace only generated identity/role templates with the corresponding repository templates after review; `cp -n` intentionally leaves them unchanged. Do not overwrite customized files without merging. `config/agents.json` preserves actual software-agent IDs/names; template folder labels `developer` and `specialist` are role labels, not runtime IDs. Pierre deliberately retains the internal ID `etienne` and its existing workspace path to preserve schedule/routing compatibility. Each `CONTEXT.md` restores sanitized operating context rather than private memory.

Edit `USER.md` only in runtime workspaces. Create memory locally only when there is concrete information to record. No private memory is recoverable here.

Check agent auth visibility using `openclaw models status --agent tom` and `--agent etienne`; configure missing credentials through the installed local CLI. Do not copy credential files into Git.

## 5. Optional Gmail helper

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-gmail-groomer.txt
.venv/bin/python -m unittest discover -s tests -v
mkdir -p "$HOME/.openclaw/workspace/scripts"
cp -n scripts/gmail_groomer.py scripts/requirements-gmail-groomer.txt "$HOME/.openclaw/workspace/scripts/"
```

Follow [GMAIL.md](GMAIL.md). A scheduler should use the absolute virtual-environment Python path and the runtime script path. Keep that environment available or create one in the runtime workspace. These commands install no schedules.

## 6. Optional Telegram and scheduling

Use the installed channel setup wizard to authenticate a fresh bot. Define approved users/groups and routing locally; previous allowlists and bindings are excluded. Configure secrets through supported secret-store/reference flows. Enable Telegram only after testing local access policy.

The Gmail helper expects `TELEGRAM_BOT_TOKEN` or a string token in local configuration. It does not resolve SecretRef objects; supply a local environment value when your channel uses a SecretRef. Never commit service-environment files.

Restore the included sanitized job definitions using [SCHEDULES.md](SCHEDULES.md). They preserve verified schedules and generic task intent, not private prompts, data, or destinations. Inspect existing jobs first, create user jobs disabled, and bind delivery locally before enabling. The current export is caller-scoped rather than a complete Gateway inventory. Start any locally configured mailbox jobs in dry-run mode before enabling mutations or notifications.

## 7. Verify

```bash
openclaw config validate
openclaw agents list
openclaw models status
openclaw gateway restart
openclaw gateway status --require-rpc
```

The final command verifies the fresh local Gateway, not every remote integration. Test integrations with your own local accounts. Backup validation itself does not contact mailboxes or restore live schedules.
