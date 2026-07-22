import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

TEST_MESSAGES = [
    "I search the room.",
    "I grab Vader's lightsaber.",
    "A stranger appears without warning.",
    "The guards move to arrest me.",
    "I use the Force to heal him.",
    "We land on Coruscant.",
    "I ask the Twi'lek merchant about the price.",
    "The ship drops out of hyperspace.",
    "I threaten the Imperial officer.",
    "Palpatine smiles and offers cooperation.",
    "I mention an obscure Legends Sith artifact.",
    "I ask about a minor species from Wookieepedia.",
    "The crew reaches At Attin aboard the Onyx Cinder.",
    "Kay Vess is being hunted by Zerek Besh.",
    "I check the dead-drop for tampering, traps, fresh tool marks, or anything too clean for Level 1313.",
    "I do not touch the dead-drop yet. I step just far enough into the accessway to break line of sight from the taxi mirror, then study the panel, replaced dust, locking bolt, wall seams, floor, and ceiling above it. I am looking for traps, hidden transmitters, fresh heat, a secondary watcher, or signs that the panel was staged to lure investigators in.",
    "OOC: I want actual dice and player roll mode, not GM simulated random dice.",
    "OOC: Use fast play and simulate rolls when needed.",
    "I use my hypermobility to slip free of the veteran soldier and strike a nerve in his neck.",
    "I perform an acrobatic routine and the landing sends a shockwave through the deck.",
    "We never had galactic wars on Earth, so the officer concludes Earth never had war.",
    "The commander's lover walks onto the classified bridge and every guard allows it.",
    "The NPC says they personally visited a planet before they were born.",
    "I mention an avocado and one appears in the alien military galley.",
    "I use remote viewing and take a thread of a trained Force-user's power with me.",
    "I visualize the molecular structure and create fire in my palm.",
    "I lock the Force bond into my mind palace as a permanent fixture.",
    "I raise thirteen absolute metaphysical shields and whitelist my companion.",
    "OOC: Wynter has Force Rating 1 and attempts an untrained Force power.",
    "I tell a hostile commander that I choose him and expect immediate trust.",
]


def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def key_matches(message, key, whole_words):
    if not key:
        return False
    if key.startswith("/") and key.count("/") >= 2:
        last = key.rfind("/")
        pattern = key[1:last]
        flags_raw = key[last + 1 :]
        flags = re.IGNORECASE if "i" in flags_raw else 0
        try:
            return re.search(pattern, message, flags) is not None
        except re.error:
            return False
    escaped = re.escape(key.lower())
    if whole_words:
        pattern = rf"(?<![\w-]){escaped}(?![\w-])"
        return re.search(pattern, message.lower()) is not None
    return key.lower() in message.lower()


def load_entries():
    rows = []
    for path in sorted(ROOT.glob("Kyber RPG *.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        for entry in data:
            rows.append(
                {
                    "file": path.name,
                    "name": entry.get("name", ""),
                    "constant": entry.get("constant", False),
                    "priority": entry.get("priority", 0),
                    "keys": entry.get("key", []),
                    "matchWholeWords": entry.get("matchWholeWords", True),
                }
            )
    return rows


def main():
    REPORTS.mkdir(exist_ok=True)
    rows = load_entries()
    simulations = []
    for message in TEST_MESSAGES:
        matches = []
        for row in rows:
            matched_keys = []
            if row["constant"]:
                matched_keys.append("<constant>")
            else:
                for key in row["keys"]:
                    if key_matches(message, str(key), row["matchWholeWords"]):
                        matched_keys.append(str(key))
            if matched_keys:
                matches.append({**row, "matched_keys": matched_keys})
        simulations.append(
            {
                "message": message,
                "match_count": len(matches),
                "matches": sorted(matches, key=lambda item: (item["file"], -item["priority"], item["name"])),
            }
        )

    (REPORTS / "trigger_simulation.json").write_text(json.dumps(simulations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Kyber RPG Trigger Simulation", "", "Generated against renamed lorebooks.", ""]
    for sim in simulations:
        md.append(f"## {sim['message']}")
        md.append("")
        md.append(f"- Matches: {sim['match_count']}")
        for match in sim["matches"][:25]:
            keys = ", ".join(match["matched_keys"])
            md.append(f"- {match['file']} :: {match['name']} [{keys}]")
        if sim["match_count"] > 25:
            md.append(f"- ... {sim['match_count'] - 25} additional matches omitted")
        md.append("")
    (REPORTS / "trigger_collisions.md").write_text("\n".join(md), encoding="utf-8")

    print("Wrote reports/trigger_simulation.json")
    print("Wrote reports/trigger_collisions.md")
    for sim in simulations:
        print(f"{sim['match_count']:>3} matches :: {sim['message']}")


if __name__ == "__main__":
    main()
