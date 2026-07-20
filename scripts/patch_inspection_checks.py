import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"inspection-checks-{date.today().isoformat()}"
RULES = ROOT / "Kyber RPG 00 - Rules Engine.json"


SECTION_28_APPEND = """

RISKY INSPECTION ENFORCEMENT
searching, inspecting, scanning, listening, checking for traps, checking for tampering, testing locks, reading a scene for danger, or assessing a suspicious object under time pressure, surveillance, poor visibility, hostile territory, hidden threats, incomplete tools, or enemy access = uncertain action
resolve with an appropriate check before giving reliable conclusions
common checks = perception, vigilance, mechanics, skulduggery, computers, streetwise, knowledge, survival, medicine, discipline
do not state "no trap", "no danger", "nothing moves", or equally confident safety conclusions unless a check succeeds or the uncertainty is stated
success may reveal true details while threat spends time, exposes position, creates noise, leaves evidence, worsens countdown, or misses a secondary danger
failure may still reveal partial information, but it must leave ambiguity, false confidence, danger, or escalation

SCENE ENDING RULE
avoid ending every reply with "what do you do?"
prefer ending on live pressure, countdown, changed circumstance, npc action, visible consequence, unresolved danger, or a concrete window of opportunity
use direct questions only when out-of-character clarification is needed or the scene has no immediate pressure
"""


NEW_SECTION_2_KEYS = [
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
    shutil.copy2(RULES, BACKUP / RULES.name)

    data = json.loads(RULES.read_text(encoding="utf-8-sig"))
    for entry in data:
        name = entry.get("name", "")
        if entry.get("id") == "swffg-0200-6ae62db2":
            for key in NEW_SECTION_2_KEYS:
                if key not in entry["key"]:
                    entry["key"].append(key)
            sync(entry)
        if name.startswith("SECTION 28") and "RISKY INSPECTION ENFORCEMENT" not in entry.get("content", ""):
            entry["content"] = entry["content"].rstrip() + SECTION_28_APPEND
    RULES.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Backed up {RULES.name} to {BACKUP}")
    print("Patched inspection checks and scene ending rule")


if __name__ == "__main__":
    main()
