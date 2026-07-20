import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "lorebooks" / "source"
UPLOAD_DIR = ROOT / "lorebooks" / "janitor_upload"
REPORTS = ROOT / "reports"
DEFAULT_WARN_BYTES = 400 * 1024
DEFAULT_CAP_BYTES = 450 * 1024


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_entry_schema(data):
    expected = None
    issues = []
    for path in sorted(ROOT.glob("Kyber RPG *.json")):
        entries = load_json(path)
        if not isinstance(entries, list):
            issues.append({"file": path.name, "issue": "root is not array"})
            continue
        for index, entry in enumerate(entries):
            keys = set(entry.keys())
            if expected is None:
                expected = keys
            elif keys != expected:
                issues.append({"file": path.name, "index": index, "issue": "schema mismatch"})
            joined = ", ".join(entry.get("key", []))
            if entry.get("keysRaw", "") != joined:
                issues.append({"file": path.name, "index": index, "issue": "keysRaw mismatch"})
            if entry.get("keywordsRaw", "") != joined:
                issues.append({"file": path.name, "index": index, "issue": "keywordsRaw mismatch"})
    return issues


def write_source_and_upload():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(exist_ok=True)

    manifest = {
        "generated": date.today().isoformat(),
        "default_warning_bytes": DEFAULT_WARN_BYTES,
        "default_cap_bytes": DEFAULT_CAP_BYTES,
        "files": [],
    }

    for path in sorted(ROOT.glob("Kyber RPG *.json")):
        data = load_json(path)
        source_path = SOURCE_DIR / path.name
        upload_path = UPLOAD_DIR / path.name

        shutil.copy2(path, source_path)
        minified = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        upload_path.write_text(minified, encoding="utf-8")

        source_bytes = source_path.stat().st_size
        upload_bytes = upload_path.stat().st_size
        manifest["files"].append(
            {
                "file": path.name,
                "entries": len(data),
                "source_bytes": source_bytes,
                "upload_bytes": upload_bytes,
                "upload_kb": round(upload_bytes / 1024, 1),
                "warning": upload_bytes >= DEFAULT_WARN_BYTES,
                "over_default_cap": upload_bytes >= DEFAULT_CAP_BYTES,
            }
        )

    issues = validate_entry_schema([])
    manifest["schema_issues"] = issues
    (REPORTS / "janitor_upload_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Janitor Upload Manifest", "", f"Generated: {manifest['generated']}", ""]
    md.append(f"Default warning: {DEFAULT_WARN_BYTES} bytes")
    md.append(f"Default cap: {DEFAULT_CAP_BYTES} bytes")
    md.append("")
    md.append("| File | Entries | Source KB | Minified Upload KB | Warning | Over Cap |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for item in manifest["files"]:
        md.append(
            f"| {item['file']} | {item['entries']} | {round(item['source_bytes'] / 1024, 1)} | {item['upload_kb']} | {item['warning']} | {item['over_default_cap']} |"
        )
    md.append("")
    md.append("## Schema Issues")
    md.append("")
    if issues:
        for issue in issues:
            md.append(f"- {issue}")
    else:
        md.append("- None.")
    (REPORTS / "janitor_upload_manifest.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("Wrote lorebooks/source")
    print("Wrote lorebooks/janitor_upload")
    print("Wrote reports/janitor_upload_manifest.md")
    print("Wrote reports/janitor_upload_manifest.json")


def main():
    write_source_and_upload()


if __name__ == "__main__":
    main()
