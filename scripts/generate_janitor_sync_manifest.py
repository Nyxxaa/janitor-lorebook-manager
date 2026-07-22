import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPLOAD_DIR = ROOT / "lorebooks" / "janitor_upload"
OUTPUT = ROOT / "janitor_sync_manifest.json"
REPORT = ROOT / "reports" / "janitor_sync_manifest.md"
WARN_BYTES = 400 * 1024
CAP_BYTES = 450 * 1024


def load_entries(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def validate_entries(entries):
    issues = []
    if not isinstance(entries, list):
        return ["root is not an array"]
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(f"entry {index} is not an object")
            continue
        for field in ("name", "content", "key", "keysRaw", "keywordsRaw"):
            if field not in entry:
                issues.append(f"entry {index} missing {field}")
        keys = entry.get("key", [])
        if isinstance(keys, list):
            joined = ", ".join(keys)
            if entry.get("keysRaw") != joined:
                issues.append(f"entry {index} keysRaw mismatch")
            if entry.get("keywordsRaw") != joined:
                issues.append(f"entry {index} keywordsRaw mismatch")
        else:
            issues.append(f"entry {index} key is not an array")
    return issues


def make_url(base_url, relative_path):
    if not base_url:
        return relative_path
    return f"{base_url.rstrip('/')}/{relative_path.replace('\\', '/')}"


def load_characters(source_path, base_url):
    if not source_path.exists():
        return []
    characters = json.loads(source_path.read_text(encoding="utf-8-sig"))
    if not isinstance(characters, list):
        raise ValueError(f"{source_path} root must be an array")
    for character in characters:
        if not character.get("name") or not isinstance(character.get("fields"), dict):
            raise ValueError("Each character requires name and fields")
        edit_url = character.get("editUrl") or character.get("sourceUrl")
        if edit_url:
            character["editUrl"] = edit_url
        for field_name, source in character["fields"].items():
            if isinstance(source, dict) and "text" in source:
                continue
            path_value = source if isinstance(source, str) else source.get("path") if isinstance(source, dict) else None
            if not path_value:
                raise ValueError(f"{character['name']} field {field_name} has no path or inline text")
            local_path = ROOT / path_value
            if not local_path.is_file():
                raise ValueError(f"Missing character field file: {path_value}")
            if base_url:
                character["fields"][field_name] = make_url(base_url, Path(path_value).as_posix())
    return characters


def main():
    parser = argparse.ArgumentParser(description="Generate a portable Janitor Manager sync manifest.")
    parser.add_argument("--project", default="Kyber RPG", help="Project/profile name.")
    parser.add_argument("--version", default=date.today().isoformat(), help="Manifest version label.")
    parser.add_argument(
        "--base-url",
        default="",
        help="Optional public raw GitHub base URL ending at the repository root.",
    )
    parser.add_argument(
        "--characters",
        type=Path,
        default=ROOT / "character_sync_sources.json",
        help="Optional JSON registry of repository character packages.",
    )
    parser.add_argument(
        "--lorebook-urls",
        type=Path,
        default=ROOT / "lorebook_edit_urls.json",
        help="Optional JSON object mapping lorebook filename or stem to its existing Janitor edit URL.",
    )
    args = parser.parse_args()

    lorebook_urls = {}
    if args.lorebook_urls.exists():
        lorebook_urls = json.loads(args.lorebook_urls.read_text(encoding="utf-8-sig"))
        if not isinstance(lorebook_urls, dict):
            raise ValueError(f"{args.lorebook_urls} root must be an object")

    files = []
    all_issues = []
    for path in sorted(UPLOAD_DIR.glob("*.json")):
        raw = path.read_bytes()
        entries = load_entries(path)
        issues = validate_entries(entries)
        relative_path = path.relative_to(ROOT).as_posix()
        item = {
            "name": path.stem,
            "filename": path.name,
            "path": relative_path,
            "url": make_url(args.base_url, relative_path),
            "sha256": sha256_bytes(raw),
            "bytes": len(raw),
            "entries": len(entries) if isinstance(entries, list) else 0,
            "warning": len(raw) >= WARN_BYTES,
            "overCap": len(raw) >= CAP_BYTES,
            "issues": issues,
        }
        edit_url = lorebook_urls.get(path.name) or lorebook_urls.get(path.stem)
        if edit_url:
            item["editUrl"] = edit_url
        if issues or item["overCap"]:
            all_issues.append({"file": path.name, "issues": issues, "overCap": item["overCap"]})
        files.append(item)

    characters = load_characters(args.characters, args.base_url)
    manifest = {
        "schema": "janitor-manager/v2",
        "project": args.project,
        "version": args.version,
        "generated": date.today().isoformat(),
        "warningBytes": WARN_BYTES,
        "capBytes": CAP_BYTES,
        "sourceMode": "github-raw" if args.base_url else "relative",
        "files": files,
        "characters": characters,
        "issues": all_issues,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# Janitor Sync Manifest",
        "",
        f"Project: {args.project}",
        f"Version: {args.version}",
        f"Generated: {manifest['generated']}",
        "",
        "| File | Entries | KB | Warning | Over Cap | Issues |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for item in files:
        lines.append(
            f"| {item['filename']} | {item['entries']} | {round(item['bytes'] / 1024, 1)} | {item['warning']} | {item['overCap']} | {len(item['issues'])} |"
        )
    if all_issues:
        lines.extend(["", "## Issues", ""])
        for issue in all_issues:
            lines.append(f"- {issue}")
    else:
        lines.extend(["", "## Issues", "", "- None."])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {REPORT}")
    print(f"Files: {len(files)}")
    print(f"Characters: {len(characters)}")
    print(f"Issues: {len(all_issues)}")


if __name__ == "__main__":
    main()
