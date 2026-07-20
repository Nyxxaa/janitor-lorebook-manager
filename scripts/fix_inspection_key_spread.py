import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"inspection-key-spread-fix-{date.today().isoformat()}"
RULES = ROOT / "Kyber RPG 00 - Rules Engine.json"

INSPECTION_KEYS = {
    "i inspect",
    "i check",
    "i examine",
    "i scan",
    "i listen",
    "check for traps",
    "check for tampering",
    "look for traps",
    "look for tampering",
    "fresh tool marks",
    "too clean",
    "dead-drop",
    "dead drop",
}


def sync(entry):
    seen = []
    for key in entry.get("key", []):
        if key and key not in seen:
            seen.append(key)
    entry["key"] = seen
    entry["keysRaw"] = ", ".join(seen)
    entry["keywordsRaw"] = entry["keysRaw"]


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RULES, BACKUP / RULES.name)

    data = json.loads(RULES.read_text(encoding="utf-8-sig"))
    for entry in data:
        is_check_construction = entry.get("id") == "swffg-0200-6ae62db2"
        if not is_check_construction:
            entry["key"] = [key for key in entry.get("key", []) if key not in INSPECTION_KEYS]
            sync(entry)

    RULES.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Backed up {RULES.name} to {BACKUP}")
    print("Removed inspection keys from unrelated rules entries")


if __name__ == "__main__":
    main()
