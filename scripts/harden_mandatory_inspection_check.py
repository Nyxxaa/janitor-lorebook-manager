import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"mandatory-inspection-check-{date.today().isoformat()}"
RULES = ROOT / "Kyber RPG 00 - Rules Engine.json"

EXTRA_KEYS = [
    "i study",
    "i assess",
    "i look over",
    "looking for traps",
    "looking for tampering",
    "hidden transmitter",
    "hidden transmitters",
    "fresh heat",
    "secondary watcher",
    "staged to lure",
    "panel was staged",
    "panel is bait",
]

MANDATORY_LINES = """

MANDATORY CHECK FORMAT FOR RISKY INSPECTION
if risky inspection enforcement applies, begin the resolution with:
CHECK: skill or skill choice; difficulty; major modifiers; result if simulated
do not skip the check header and then narrate reliable findings
if the player has no dice roller result, simulate transparently or ask for the roll before conclusions
safe phrasing before a check = possible, appears, seems, may, cannot confirm yet
unsafe phrasing before a check = no trap, no watcher, no heat, nothing moves, panel is safe, definitely bait, definitely clear
"""


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
        if entry.get("id") == "swffg-0200-6ae62db2":
            for key in EXTRA_KEYS:
                if key not in entry["key"]:
                    entry["key"].append(key)
            sync(entry)
        if entry.get("id") == "swffg-2800-ddd93d59":
            content = entry.get("content", "")
            if "MANDATORY CHECK FORMAT FOR RISKY INSPECTION" not in content:
                entry["content"] = content.rstrip() + MANDATORY_LINES
    RULES.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Backed up {RULES.name} to {BACKUP}")
    print("Hardened mandatory risky-inspection check format")


if __name__ == "__main__":
    main()
