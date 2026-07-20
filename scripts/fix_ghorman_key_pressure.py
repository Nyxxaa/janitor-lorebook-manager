import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"ghorman-key-pressure-{date.today().isoformat()}"

TARGETS = [
    ROOT / "Kyber RPG 02 - Eras and History.json",
    ROOT / "Kyber RPG 05 - Worlds and Regions.json",
]


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
    for path in TARGETS:
        shutil.copy2(path, BACKUP / path.name)
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        for entry in data:
            name = entry.get("name", "")
            if path.name.startswith("Kyber RPG 02") and name == "ghorman project and massacre":
                entry["key"] = [key for key in entry.get("key", []) if key != "ghorman front"]
                entry["key"].append("ghorman crisis")
                entry["key"].append("ghorman imperial project")
                sync(entry)
            if path.name.startswith("Kyber RPG 05") and name == "ghorman":
                entry["key"] = [key for key in entry.get("key", []) if key != "ghorman front"]
                entry["key"].append("ghorman world")
                sync(entry)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Backed up touched files to {BACKUP}")
    print("Resolved ghorman front duplicate key pressure")


if __name__ == "__main__":
    main()
