import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PATCHES = {
    "Kyber RPG 08 - Technology Ships Gear.json": {
        "armor materials": {
            "cortosis": "cortosis armor material",
            "phr ik": "phrik armor material",
        },
        "lightsaber resistant materials": {
            "cortosis": "cortosis resistant material",
            "phrik": "phrik resistant material",
        },
    },
    "Kyber RPG 02 - Eras and History.json": {
        "clone wars campaigns": {
            "umbara": "umbara clone wars overview",
        },
    },
    "Kyber RPG 06 - Species and Cultures.json": {
        "umbarans": {
            "umbara": "umbaran homeworld context",
        },
    },
}


def sync(entry):
    keys = entry.get("key", [])
    entry["keysRaw"] = ", ".join(keys)
    entry["keywordsRaw"] = entry["keysRaw"]


def main():
    changed = 0
    for filename, by_name in PATCHES.items():
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        for entry in data:
            replacements = by_name.get(entry.get("name", "").lower())
            if not replacements:
                continue
            keys = [replacements.get(key, key) for key in entry.get("key", [])]
            if keys != entry.get("key", []):
                entry["key"] = keys
                sync(entry)
                changed += 1
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {changed} entries")


if __name__ == "__main__":
    main()
