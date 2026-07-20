import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"dice-protocol-{date.today().isoformat()}"
RULES = ROOT / "Kyber RPG 00 - Rules Engine.json"

DICE_KEYS = [
    "roll mode",
    "dice protocol",
    "actual dice",
    "random dice",
    "simulate roll",
    "roll the dice",
    "player roll",
]

RANDOMNESS_PROTOCOL = """

RANDOMNESS AND DICE INTEGRITY
llms are not trusted random number generators.
default mode = player-roll-first.
when a meaningful check is needed and no result has been supplied, state the pool and ask the Player to provide the result before narrating reliable consequences.
do not choose success/failure to fit preferred drama.
do not repeatedly choose success with threat as a compromise.
do not call a result random unless an external roll or player-provided result exists.
if the Player explicitly requests fast play, use GM-simulated mode and label it:
CHECK: skill; difficulty; modifiers; GM-simulated result = ...
GM-simulated result is a pacing shortcut, not true randomness.
for high-stakes checks involving death, arrest, major injury, major social outcome, canon-character trust, rare force use, or large resource loss, prefer player-provided roll unless the Player explicitly requested GM-simulated fast play.

PLAYER RESULT FORMAT
accept any clear result format:
success/failure plus advantage/threat/triumph/despair
raw narrative dice symbols
plain text such as "2 success, 1 threat"
if a result is unclear, ask one concise OOC clarification.
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
        if entry.get("id") == "swffg-0100-1ad0af93":
            entry["content"] = entry["content"].replace(
                "- If an actual dice roller is unavailable, either ask the player to provide the result or produce a transparent simulated result.\n",
                "- LLMs are not trusted random number generators; default to player-roll-first for meaningful checks.\n- If no external result is supplied, state the pool and ask the Player to provide the result before narrating reliable consequences.\n- If the Player explicitly requests fast play, label any shortcut as GM-simulated, not true random.\n",
            )
            for key in DICE_KEYS:
                if key not in entry["key"]:
                    entry["key"].append(key)
            sync(entry)
        if entry.get("id") == "swffg-2800-ddd93d59":
            content = entry.get("content", "")
            content = content.replace(
                "if the player has no dice roller result, simulate transparently or ask for the roll before conclusions",
                "if the player has no dice roller result, ask for the roll before conclusions unless fast-play GM-simulated mode was explicitly requested",
            )
            if "RANDOMNESS AND DICE INTEGRITY" not in content:
                content = content.rstrip() + RANDOMNESS_PROTOCOL
            entry["content"] = content
            for key in DICE_KEYS:
                if key not in entry["key"]:
                    entry["key"].append(key)
            sync(entry)
        if entry.get("id") == "swffg-2900-c6dc3d98":
            if "GM-simulated result" not in entry.get("content", ""):
                entry["content"] = entry["content"].rstrip() + "\n\nDICE INTEGRITY\nDefault check flow asks Player for result after pool is stated. GM-simulated fast play must be labeled and is not true randomness."
            for key in DICE_KEYS:
                if key not in entry["key"]:
                    entry["key"].append(key)
            sync(entry)

    RULES.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Backed up {RULES.name} to {BACKUP}")
    print("Patched player-roll-first dice protocol")


if __name__ == "__main__":
    main()
