# Janitor Lorebook Manager

Chrome Manifest V3 extension for assisted Janitor AI lorebook sync.

## What It Does

- Loads lorebooks from a public GitHub raw `janitor_sync_manifest.json`.
- Loads one or more local `.json` lorebook files through the popup.
- Validates Janitor-style lorebook arrays before apply.
- Injects a small manager panel into Janitor pages.
- Detects likely lorebook editor fields, previews matches, creates a backup, and fills fields.
- Leaves Janitor's final save/publish action manual.

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

In the extension popup, paste the raw URL to `janitor_sync_manifest.json`, then click `Check GitHub`.

## Local File Sync

Use the popup's local file picker and choose one or more Janitor lorebook JSON files. Then open the Janitor editor tab and click `Send Bundle To Page`.

## Safety Notes

- The extension does not know or store Janitor credentials.
- The extension does not use a Janitor API.
- The extension does not click final save/publish in v1.
- If Janitor changes its editor UI, field detection may fail closed.
