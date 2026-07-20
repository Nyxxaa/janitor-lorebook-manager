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


def main():
    parser = argparse.ArgumentParser(description="Generate a portable Janitor Lorebook Manager sync manifest.")
    parser.add_argument("--project", default="Kyber RPG", help="Project/profile name.")
    parser.add_argument("--version", default=date.today().isoformat(), help="Manifest version label.")
    parser.add_argument(
        "--base-url",
        default="",
        help="Optional public raw GitHub base URL ending at the repository root.",
    )
    args = parser.parse_args()

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
        if issues or item["overCap"]:
            all_issues.append({"file": path.name, "issues": issues, "overCap": item["overCap"]})
        files.append(item)

    manifest = {
        "schema": "janitor-lorebook-manager/v1",
        "project": args.project,
        "version": args.version,
        "generated": date.today().isoformat(),
        "warningBytes": WARN_BYTES,
        "capBytes": CAP_BYTES,
        "sourceMode": "github-raw" if args.base_url else "relative",
        "files": files,
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
    print(f"Issues: {len(all_issues)}")


if __name__ == "__main__":
    main()
