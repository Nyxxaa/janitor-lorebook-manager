import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"remaining-recent-gaps-{date.today().isoformat()}"

ADDITIONS = {
    "Kyber RPG 02 - Eras and History.json": [
        (
            "kyber-recent-bad-batch-sanctuary",
            "bad batch sanctuary",
            "BAD BATCH: SANCTUARY\ncontinuity = canon\nrelease = 2025 novel\nfocus = post-clone-wars clone survival, pabu-era refuge pressure, imperial aftermath\nrpg use = clone stories after order 66 should include medical scarcity, identity trauma, imperial pursuit, and fragile safe havens",
            ["bad batch sanctuary", "sanctuary bad batch"],
        ),
        (
            "kyber-recent-ghost-agents",
            "ghost agents",
            "GHOST AGENTS\ncontinuity = canon\nrelease = 2025 comic series\nfocus = imperial-era covert survival and asajj ventress-linked underworld/force continuity\nrpg use = presumed-dead characters and covert agents should create evidence trails, hunters, and identity risk instead of clean resets",
            ["ghost agents", "asajj ventress ghost agents"],
        ),
        (
            "kyber-recent-vader-master-evil",
            "darth vader master of evil",
            "DARTH VADER: MASTER OF EVIL\ncontinuity = canon\nrelease = 2025 novel\nfocus = vader during early imperial consolidation\nrpg use = vader scenes should emphasize terror, obedience, imperial mythmaking, and tactical brutality; do not use unsourced plot specifics without source check",
            ["darth vader master of evil", "master of evil"],
        ),
        (
            "kyber-recent-acolyte-publishing",
            "the acolyte publishing",
            "THE ACOLYTE PUBLISHING\ncontinuity = canon\nworks = the acolyte: wayseeker; the acolyte: the crystal crown\nfocus = high republic jedi independence, vernestra rwoh context, and acolyte-era force politics\nrpg use = use as targeted continuity support for high republic/acolyte scenes, not as proof of late-republic jedi norms",
            ["the acolyte wayseeker", "the crystal crown", "acolyte publishing"],
        ),
        (
            "kyber-recent-krennic-andor-s2",
            "krennic andor season 2",
            "KRENNIC - ANDOR SEASON 2\ncontinuity = canon\nrole = imperial advanced weapons administrator tied to ghorman/resource exploitation and death star secrecy\nmethods = bureaucratic menace, project compartmentalization, political pressure, disposable local populations\nrpg use = krennic-facing plots should involve security clearance, propaganda, resource extraction, and lethal secrecy",
            ["krennic andor season 2", "director krennic andor", "orson krennic andor"],
        ),
    ],
    "Kyber RPG 03 - Characters.json": [
        (
            "kyber-recent-skeleton-kids-group",
            "fern wim neel kb",
            "FERN WIM NEEL KB\ncontinuity = canon\nrole = at attin children aboard onyx cinder during skeleton crew events\nshared risk = minors outside controlled homeworld facing pirates, deception, survival hazards, and adult exploitation\nrpg use = group key for skeleton crew children; never sexualize; danger should preserve child status and limited competence",
            ["fern wim neel kb", "skeleton crew kids", "at attin children"],
        ),
    ],
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def make_entry(template, entry_id, name, content, keys, order):
    entry = dict(template)
    entry.update(
        {
            "activationMode": "standard",
            "activationScript": "",
            "case_sensitive": False,
            "comment": "added to clear recent-canon gap audit; verify against official sources before expanding plot specifics",
            "constant": False,
            "content": content,
            "enabled": True,
            "extensions": {},
            "groupWeight": 100,
            "id": entry_id,
            "inclusionGroupRaw": "",
            "insertion_order": order,
            "key": keys,
            "keyMatchPriority": True,
            "keysecondary": [],
            "keysecondaryRaw": "",
            "keysRaw": ", ".join(keys),
            "matchWholeWords": True,
            "minMessages": 0,
            "name": name,
            "prioritizeInclusion": False,
            "priority": 2,
            "probability": 100,
            "selectiveLogic": 0,
            "tags": ["star_wars", "canon", "recent"],
            "keywordsRaw": ", ".join(keys),
        }
    )
    return entry


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    for filename, additions in ADDITIONS.items():
        path = ROOT / filename
        shutil.copy2(path, BACKUP / filename)
        data = load(path)
        names = {entry.get("name") for entry in data}
        ids = {entry.get("id") for entry in data}
        order = max(entry.get("insertion_order", 0) for entry in data)
        template = data[0]
        for entry_id, name, content, keys in additions:
            if name in names or entry_id in ids:
                continue
            order += 100
            data.append(make_entry(template, entry_id, name, content, keys, order))
        data.sort(key=lambda entry: entry.get("insertion_order", 0))
        save(path, data)
    print(f"Backed up touched files to {BACKUP}")
    print("Filled remaining recent-canon audit gaps")


if __name__ == "__main__":
    main()
