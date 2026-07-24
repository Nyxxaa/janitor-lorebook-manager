# Janitor Manager

Chrome Manifest V3 extension for assisted Janitor AI lorebook and character production.

## Recommended Character Workflow

1. Click **Refresh Production Batch**.
2. Confirm the batch summary shows the expected character count.
3. Click **Test First Character** and review the result.
4. Only then click **Update Verified Characters**.

The character queue is isolated from lorebook publishing. Local-file, lorebook, comparison, and repository controls are kept in separate expandable sections.

## What It Does

- Loads lorebooks from a public GitHub raw `janitor_sync_manifest.json`.
- Loads one or more local `.json` lorebook files through the popup.
- Validates Janitor-style lorebook arrays before apply.
- Injects a small manager panel into Janitor pages.
- Shows the floating panel only on `/scripts`, `/scripts/...`, `/create_character`, and `/edit_character/...` routes; it stays hidden on ordinary browsing and chat pages.
- Detects likely lorebook editor fields, including Janitor's CodeMirror JSON editor.
- Previews matches, creates a backup, and fills fields.
- Downloads a self-contained HTML backup of visible Janitor character fields, including the character card, personality/definition, scenario, initial message, and example dialogs when present.
- Keeps manual single-record fills review-first; the explicit project updater can save existing records unattended.
- Loads character packages from a GitHub manifest, including avatars, and fills Janitor character creation/edit forms.
- **Update Verified Characters** updates only packages with exact Janitor `editUrl` values.
- Packages without verified edit URLs are skipped, never auto-created. This prevents duplicates when an existing Janitor character has not yet been reconciled with the repository.
- Existing-character updates preserve their current visibility. Release scheduling runs only for newly created characters.
- **Stop Run** safely finishes the character currently being saved/released, then prevents the next queue item from starting.
- **Compare My Characters** reads every page of an open Janitor **My Characters** library, matches repository records by Janitor UUID, and performs a read-only field comparison in matched editors.
- Updates an existing project unattended when manifest lorebooks and characters include exact Janitor `editUrl` values: backup, fill, save, verify, and continue past individual failures.
- Compares repository character fields with the live Janitor form and writes only changed fields; already-current characters are not unnecessarily saved.
- Supports project profiles and arbitrary Janitor lorebook arrays; Kyber RPG is only the default profile.
- Backs up every lorebook from Janitor's Scripts/Lorebooks list in one operation by auto-scrolling the list and processing temporary background tabs.

## Repository Manifest

The manifest may contain `lorebooks` (or the legacy `files` array), `characters`, or both. Character field paths are resolved relative to the raw manifest URL.

```json
{
  "project": "Example Series",
  "version": "2026-07-22",
  "lorebooks": [
    { "name": "World Lore", "path": "lorebooks/world.json" }
  ],
  "characters": [
    {
      "id": "example-character",
      "name": "Example Character",
      "group": "Example Group",
      "editUrl": "https://janitorai.com/edit_character/00000000-0000-0000-0000-000000000000",
      "fields": {
        "characterName": { "text": "Example Character" },
        "characterCard": "bots/example-character/character-card.txt",
        "personalityDefinition": "bots/example-character/personality-definition.txt",
        "scenario": "bots/example-character/scenario.txt",
        "initialMessage": "bots/example-character/initial-message.txt",
        "exampleDialogs": "bots/example-character/example-dialogs.txt"
      }
    }
  ]
}
```

Field values can use a relative/absolute path string, `{ "path": "..." }`, `{ "url": "..." }`, or inline `{ "text": "..." }`. Bulk updates require an exact Janitor `editUrl`. New characters must be opened and reviewed individually from the popup.

## Workspace Compiler

Generate compatible project manifests, immutable build copies, hashes, and validation reports with:

```powershell
python Bots\tools\build_bot.py
```

Each owned project receives `janitor-manager-manifest.json` and `.janitor-build/`. Commit those artifacts to the project's GitHub repository, then use the raw manifest URL as the Janitor Manager profile source.

For local testing, choose the project directory under **Local compiled project folder** and click **Load Local Project Build**. The browser resolves generated field and lorebook paths from that selected directory; no GitHub push is required.

## Local Install

1. Open `chrome://extensions`.
2. Enable `Developer mode`.
3. Click `Load unpacked`.
4. Select this `chrome-extension` folder.

## GitHub Sync

Generate a repo manifest first:

```powershell
python -m scripts.generate_janitor_sync_manifest --project "Kyber RPG" --version "2026-07-20-b06" --base-url "https://raw.githubusercontent.com/OWNER/REPO/BRANCH"
```

Commit `janitor_sync_manifest.json` and `lorebooks/janitor_upload/*.json`.

In the extension popup, paste the raw URL to `janitor_sync_manifest.json`, then choose **Load From GitHub**.

## Local File Sync

Use the popup's local file picker and choose one or more Janitor lorebook JSON files. Then open the Janitor editor tab and choose **Load Lorebooks In Panel**.

## Janitor Editor Notes

Janitor's lorebook JSON editor currently uses CodeMirror. Backups read the full CodeMirror document from Janitor's page context so virtualized off-screen content is preserved. The extension tries to update CodeMirror through its editor state first, then falls back to browser text insertion for contenteditable editors.

Character backups are read-only: open a character editor and choose **Backup Current Character** in the page panel. The file preserves exact field text in readable sections and embeds a `janitor-character-backup/v1` JSON payload for future restore/import tooling. It ignores passwords, tokens, file inputs, and hidden fields.

For a complete account lorebook backup, open any Janitor script editor with the lorebook sidebar visible and choose **Backup Entire Library** in the page panel. Keep that tab open while it runs. Janitor Manager scrolls the sidebar, discovers reactive script items and IDs, opens each in an inactive temporary tab, reads the full editor document, closes that tab, and downloads one `janitor-lorebook-batch-backup/v1` bundle. It reports any individual failures without discarding successful backups.

If only one lorebook editor is open, the extension can match it by the existing JSON category, such as `kyber_rpg_core_continuity`. If multiple editors are visible at once, choose **Preview Repository Fill** and confirm each match before **Fill Lorebook Editors**.

## Safety Notes

- The extension does not know or store Janitor credentials.
- The extension does not use a Janitor API.
- Automatic bulk saving happens only after the explicit **Update Verified Characters** click. Bulk creation is disabled.
- If Janitor changes its editor UI, field detection may fail closed.
