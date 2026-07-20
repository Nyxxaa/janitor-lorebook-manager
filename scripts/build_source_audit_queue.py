import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CLASSIFICATION = REPORTS / "entry_classification.json"
QUEUE_JSON = REPORTS / "source_audit_queue.json"
QUEUE_MD = REPORTS / "source_audit_queue.md"


def main() -> None:
    entries = json.loads(CLASSIFICATION.read_text(encoding="utf-8"))
    queue = [entry for entry in entries if entry.get("classification") == "source_audit"]
    queue.sort(key=lambda entry: (entry["file"], entry.get("index", 0)))

    by_file = Counter(entry["file"] for entry in queue)
    QUEUE_JSON.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Source Audit Queue",
        "",
        "Purpose: track lore entries that should be checked against current canon/Legends source layering before further expansion.",
        "",
        f"Entries queued: {len(queue)}",
        "",
        "## Counts By File",
        "",
    ]
    for filename, count in sorted(by_file.items()):
        lines.append(f"- {filename}: {count}")

    lines.extend(["", "## Queue", ""])
    for entry in queue:
        reasons = "; ".join(entry.get("reasons") or ["source audit"])
        lines.append(f"- {entry['file']} :: {entry['name']} :: {reasons}")

    QUEUE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {QUEUE_JSON}")
    print(f"Wrote {QUEUE_MD}")
    print(f"Queued {len(queue)} entries")


if __name__ == "__main__":
    main()
