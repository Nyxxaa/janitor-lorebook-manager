import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "Kyber RPG Rules.json"

ROLE_BLOCK_RE = re.compile(
    r"\n\nROLE AND LAYER DEFINITIONS\n\nPlayer = the physical human at the keyboard\..*?"
    r"NPCs = all non-player characters",
    re.DOTALL,
)

COMPACT_ENFORCEMENT = """DECLARATIVE ACTION ENFORCEMENT
player wording such as "i do x" = attempted action, not completed external fact
gm must resolve uncertain, opposed, dangerous, consequential, or capability-dependent actions before confirming success
trivial uncontested routine actions may resolve automatically
if success is uncertain = call for or simulate the relevant check
if opposed = allow npc resistance, tactics, evidence, fear, training, and environment
failure must change the scene through cost, danger, lost position, injury, exposure, delay, suspicion, or escalation
success may still carry threat, strain, damage, debt, attention, collateral harm, or future consequence
do not convert confident player wording into automatic success
do not protect {{user}} from believable defeat, capture, injury, loss, rejection, legal response, or death
do not narrate {{user}}'s voluntary choices, dialogue, private thoughts, sincere feelings, consent, loyalty, attraction, surrender, or belief changes
npc action against {{user}} is valid world action, not player-character puppeting
npcs may attack, restrain, arrest, deceive, refuse, flee, exploit vulnerability, call reinforcements, or use force when justified
canon characters retain competence, paranoia, cruelty, loyalty, trauma, caution, and established limits
kindness, beauty, vulnerability, humor, future knowledge, or unusual power does not automatically earn trust
trust, romance, redemption, ideological change, and loyalty require cumulative evidence and time
every response should materially change scene state, information, position, stakes, or available choices"""

GENERIC_ACTION_KEYS = {
    "i open",
    "i grab",
    "i take",
    "i pull",
    "i push",
    "i lift",
    "i hit",
    "i shoot",
    "i stab",
    "i dodge",
    "i block",
    "i run",
    "i escape",
    "i hide",
    "i sneak",
    "i convince",
    "i persuade",
    "i threaten",
    "i lie",
    "i use the force",
    "i heal",
    "i hack",
    "i slice",
    "i repair",
    "i climb",
    "i jump",
    "i search",
    "i look for",
    "i break",
    "i unlock",
    "i disable",
    "i restrain",
}


def normalize_newlines(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def remove_action_blocks(text):
    final_sentence = (
        'Never infer success merely because the player used present tense, past tense, decisive wording, '
        'or omitted the phrases "I try" and "I attempt."'
    )
    short_sentence = (
        "A player-declared external action is an attempt unless it is trivial and uncontested. "
        "Declarative wording does not grant success. The GM resolves uncertain, opposed, dangerous, "
        "or consequential actions before treating them as completed facts."
    )

    for header, ending in [
        ("PLAYER ACTION DECLARATIONS", final_sentence),
        ("ACTION DECLARATION RULE", short_sentence),
    ]:
        while header in text:
            start = text.find(header)
            end = text.find(ending, start)
            if end == -1:
                break
            end += len(ending)
            while start > 0 and text[start - 1] == "\n":
                start -= 1
            text = text[:start] + text[end:]
    return text


def section_number(name):
    match = re.search(r"section\s+(\d+)", name.lower())
    if not match:
        return None
    return int(match.group(1))


def main():
    entries = json.loads(RULES_PATH.read_text(encoding="utf-8-sig"))

    for entry in entries:
        if "keywordsRaw" not in entry:
            entry["keywordsRaw"] = entry.get("keysRaw", "")

        content = entry.get("content", "")
        name = entry.get("name", "").lower()

        if "section 0" not in name and "section 28" not in name:
            content = remove_action_blocks(content)
            content = ROLE_BLOCK_RE.sub("", content)
            entry["content"] = normalize_newlines(content)

        if section_number(name) != 2:
            keys = entry.get("key", [])
            if isinstance(keys, list):
                kept_keys = [key for key in keys if str(key).strip().lower() not in GENERIC_ACTION_KEYS]
                if kept_keys != keys:
                    entry["key"] = kept_keys
                    entry["keysRaw"] = ", ".join(str(key).strip() for key in kept_keys)
                    entry["keywordsRaw"] = entry["keysRaw"]

    for entry in entries:
        name = entry.get("name", "").lower()
        if "section 28" in name:
            entry["content"] = COMPACT_ENFORCEMENT
            entry["constant"] = True
            entry["priority"] = 10
            entry["insertion_order"] = 2800
            entry["key"] = ["/.*/"]
            entry["keysRaw"] = "/.*/"
            entry["keywordsRaw"] = "/.*/"
            entry["matchWholeWords"] = False
            entry["keyMatchPriority"] = False
            entry["probability"] = 100
            break

    RULES_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {RULES_PATH.name}")


if __name__ == "__main__":
    main()
