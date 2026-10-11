# Scheduled-job reconstruction

`config/automations.json` records sanitized definitions from the current caller-visible inventory, not a full export of the Gateway scheduler. It contains no job IDs, account/session ownership identifiers, execution history, notification destinations, or original private payloads.

| Job | Schedule | Agent | Snapshot state |
| --- | --- | --- | --- |
| Managed main heartbeat | Every 30 minutes | `main` | Enabled; recent run skipped because the local heartbeat task file was empty |
| Sanitized GitHub backup | Tuesday 02:00 America/Los_Angeles | `main` | Enabled |

The managed heartbeat is owned by OpenClaw configuration. Do not create an ordinary cron duplicate. On a reconstructed installation, inspect `openclaw cron list --all --json` and the release's heartbeat settings to confirm the managed interval. Private heartbeat tasks are deliberately absent; leave the local task file empty until checks are authorized.

## Restore the weekly backup job

Inspect the destination scheduler first. If a job with this name/declaration already exists, reconcile it instead of creating a duplicate. An empty caller-scoped inventory does not establish global absence; use the authenticated configured-owner/administrator Automations page if necessary.

From the sanitized checkout root, after installing and reviewing all backup files:

```bash
openclaw cron add --name weekly-sanitized-github-backup \
  --declaration-key backup:weekly-sanitized \
  --agent main --cron '0 2 * * 2' --tz America/Los_Angeles --exact \
  --session isolated --no-deliver --disabled --timeout-seconds 1200 \
  --message "Backup checkout: $PWD. Read and follow docs/BACKUP_UPDATE.md in that checkout. Update only after privacy, secret, and integrity checks pass. Report updated, unchanged, or blocked without private details."
```

This restore command deliberately creates a **disabled, isolated, silent** job. The live source job targets its current conversation and announces there; that private conversation binding cannot be portably exported. Review the new job in the local Automations UI, bind the result to your chosen local conversation if desired, and enable it. No job is installed merely by cloning this repository.

The checkout path is expanded locally and must never be copied into tracked public files. Authentication must be configured locally. The agent needs headless read/exec access to the checkout, GitHub authentication, and Gitleaks.

## Additional jobs

The available scheduler tool reports restricted visibility. This backup cannot claim to include every job. Use a fresh authenticated configured-owner/administrator session or the Automations page for a complete inventory, then publish only reviewed, generalized schedule/task definitions. Mailbox accounts, delivery recipients, private market positions, original private task prompts, and private data-source paths remain local.
