# Janitor Lorebook Manager

Tools and lorebook exports for managing large Janitor AI lorebook sets without a Janitor API.

## What Is Here

- `lorebooks/janitor_upload/` contains the current Janitor-ready lorebook JSON files.
- `janitor_sync_manifest.json` is the public sync manifest consumed by the Chrome extension.
- `chrome-extension/` contains the unpacked Chrome extension.
- `scripts/generate_janitor_sync_manifest.py` rebuilds the sync manifest and validates lorebook file size, hashes, and basic schema.
- `reports/` contains audits and upload summaries.

## Chrome Extension

Load `chrome-extension/` as an unpacked extension from `chrome://extensions`.

The extension can:

- fetch a public GitHub raw sync manifest,
- verify lorebook SHA-256 hashes,
- load lorebooks from local files,
- detect likely Janitor lorebook fields,
- back up current page content,
- dry-run or apply matched lorebook JSON into page fields.

It does not click Janitor save or publish buttons. Review changes in Janitor and save manually.

## GitHub Raw Manifest URL

After this repo is pushed to GitHub, use this pattern in the extension:

```text
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/janitor_sync_manifest.json
```

The manifest uses relative paths, so the extension will fetch the lorebooks from the same branch.

## Rebuild Manifest

```powershell
python -m scripts.generate_janitor_sync_manifest --project "Kyber RPG" --version "YYYY-MM-DD-label"
```

Then commit and push `janitor_sync_manifest.json` and the changed lorebook files.
