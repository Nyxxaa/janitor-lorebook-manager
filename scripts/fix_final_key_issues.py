import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"final-key-fixes-{date.today().isoformat()}"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
    touched = [
        ROOT / "Kyber RPG 02 - Eras and History.json",
        ROOT / "Kyber RPG 03 - Characters.json",
    ]
    for path in touched:
        shutil.copy2(path, BACKUP / path.name)

    history = load(touched[0])
    for entry in history:
        if entry.get("name") == "galactic dating and eras":
            entry["constant"] = False
            entry["keyMatchPriority"] = True
            entry["priority"] = max(entry.get("priority", 1), 2)
            sync(entry)
    save(touched[0], history)

    characters = load(touched[1])
    for entry in characters:
        if entry.get("name") == "jod na nawood":
            entry["name"] = "jod na nawood"
            entry["content"] = entry["content"].replace("JOD NA NAWOOD", "JOD NA NAWOOD")
            entry["key"] = [
                "jod na nawood",
                "jod na nawwood",
                "captain silvo",
                "crimson jack",
            ]
            sync(entry)
    save(touched[1], characters)

    print(f"Backed up touched files to {BACKUP}")
    print("Fixed final key issues")


if __name__ == "__main__":
    main()
