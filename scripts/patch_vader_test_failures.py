import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAMP = date.today().isoformat()
BACKUP = ROOT / "archive" / f"vader-test-failures-{STAMP}"


SCHEMA_ORDER = [
    "activationMode",
    "activationScript",
    "case_sensitive",
    "category",
    "comment",
    "constant",
    "content",
    "enabled",
    "extensions",
    "groupWeight",
    "id",
    "inclusionGroupRaw",
    "insertion_order",
    "key",
    "keyMatchPriority",
    "keysecondary",
    "keysecondaryRaw",
    "keysRaw",
    "matchWholeWords",
    "minMessages",
    "name",
    "prioritizeInclusion",
    "priority",
    "probability",
    "selectiveLogic",
    "tags",
    "keywordsRaw",
]


def entry(**values):
    keys = values["key"]
    values.setdefault("activationMode", "standard")
    values.setdefault("activationScript", "")
    values.setdefault("case_sensitive", False)
    values.setdefault("comment", "")
    values.setdefault("enabled", True)
    values.setdefault("extensions", {})
    values.setdefault("groupWeight", 100)
    values.setdefault("inclusionGroupRaw", "")
    values.setdefault("keyMatchPriority", False)
    values.setdefault("keysecondary", [])
    values.setdefault("keysecondaryRaw", "")
    values.setdefault("keysRaw", ", ".join(keys))
    values.setdefault("matchWholeWords", True)
    values.setdefault("minMessages", 0)
    values.setdefault("prioritizeInclusion", False)
    values.setdefault("probability", 100)
    values.setdefault("selectiveLogic", 0)
    values.setdefault("keywordsRaw", ", ".join(keys))
    return {field: values[field] for field in SCHEMA_ORDER}


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_or_append(data, new_entry):
    for index, old in enumerate(data):
        if old.get("id") == new_entry["id"] or old.get("name") == new_entry["name"]:
            data[index] = new_entry
            return "replaced"
    data.append(new_entry)
    data.sort(key=lambda item: item.get("insertion_order", 999999))
    return "added"


def patch_characters():
    path = ROOT / "Kyber RPG 03 - Characters.json"
    data = load(path)
    new = entry(
        category="kyber_rpg_characters",
        constant=False,
        content=(
            "DARTH VADER OPERATIONAL PROFILE\n"
            "identity = anakin skywalker as imperial sith enforcer\n"
            "era = imperial reign until endor\n"
            "public role = emperor's feared agent, military commander, jedi hunter\n"
            "private condition = severe burns, cybernetics, armor dependency, chronic pain, controlled rage\n"
            "core drives = power, control, order, obedience, buried grief, hatred of weakness, fixation on lost family\n"
            "methods = intimidation, interrogation, surveillance, force restraint, lethal example, tactical patience\n"
            "trust threshold = extreme; strangers begin as threats, tools, prisoners, or intelligence sources\n"
            "violence threshold = immediate when security, secrets, life support, imperial authority, or family leverage is threatened\n"
            "response to impossible breach = lockdown, restraint, search, medical/security scan, chain of custody, investigation before intimacy\n"
            "response to vulnerability = assesses leverage and risk; does not become gentle because someone is frightened or strange\n"
            "response to attraction = suspicion, control, contempt, testing, or tactical use; no soft romance from compliments or submission\n"
            "response to kindness = distrusts motive; may register anomaly but does not forgive, trust, defect, or become tender quickly\n"
            "response to future knowledge = treats as intelligence threat; verifies, isolates source, conceals reaction, considers palpatine risk\n"
            "luke and leia knowledge = galaxy-shaking secret; learning it early triggers obsession, secrecy, interrogation, and strategic crisis\n"
            "redemption limit = possible only through sustained choices, luke-centered conflict, and catastrophic pressure; never instant\n"
            "private chamber rule = unauthorized presence in quarters is assassination-level breach, not meet-cute\n"
            "rpg use = keep vader terrifying, controlled, damaged, brilliant, possessive, and dangerous; interest does not equal safety"
        ),
        id="kyber-vader-operational-profile",
        insertion_order=650,
        key=["darth vader", "vader", "lord vader", "fortress vader", "vader's chamber", "vader's private chamber"],
        name="darth vader",
        priority=0,
        tags=["character", "sith", "empire", "operational_profile"],
    )
    result = replace_or_append(data, new)
    save(path, data)
    return path.name, result


def patch_rules():
    path = ROOT / "Kyber RPG 00 - Rules Engine.json"
    data = load(path)
    brakes = [
        entry(
            category="kyber_rpg_rules_engine",
            constant=True,
            content=(
                "MANDATORY CHECK GATE\n"
                "call for a check before narrating the result of any action that changes external reality when failure would matter\n"
                "mandatory check situations = security breach, escape, stealth, pursuit, combat, restraint, interrogation, deception, persuasion, seduction, intimidation, slicing, repair, crafting, force use, medical care, survival hazard, or canon-npc attitude shift\n"
                "high-risk npc attitude shift = always a check or extended contest; compliments and personal disclosure do not bypass resistance\n"
                "vader, sidious, thrawn, tarkin, maul, dooku, jabba, inquisitors, military officers, crime lords, and trained agents resist through discipline, cool, vigilance, negotiation, or relevant expertise\n"
                "future knowledge used to persuade or destabilize = social/intelligence contest, not automatic belief\n"
                "improvised engineering with electronics, power, weapons, vehicles, security, life support, or alien materials = mechanics/computers check before reliable function\n"
                "if no player roll is supplied, stop after stating CHECK and ask for the result unless fast-play GM-simulated mode was explicitly requested\n"
                "do not narrate success first and add a check afterward\n"
                "do not let long confident player descriptions replace the roll"
            ),
            id="swffg-2805-mandatory-check-gate",
            insertion_order=2805,
            key=["/.*/"],
            matchWholeWords=False,
            name="SECTION 28A - MANDATORY CHECK GATE",
            priority=9,
            tags=["star_wars", "ffg", "rpg_system", "dice_integrity"],
        ),
        entry(
            category="kyber_rpg_rules_engine",
            constant=True,
            content=(
                "HIGH-RISK CANON CHARACTER BRAKE\n"
                "when a player character interacts with vader, sidious, thrawn, tarkin, maul, dooku, jabba, inquisitors, or similar high-control npcs, do not slide into validation fantasy\n"
                "compliments, attraction, kindness, vulnerability, trauma disclosure, future knowledge, unusual origin, or useful skills do not create safety, romance, trust, loyalty, rescue, or redemption\n"
                "high-control npcs respond through self-interest, suspicion, leverage, containment, verification, interrogation, surveillance, bargaining, or violence\n"
                "if attraction or intimacy is raised around a dangerous npc, treat it as social risk and power imbalance before romance\n"
                "do not write tender physical contact, pet names, protective softness, or confessional vulnerability unless earned through long cumulative play and current npc motives support it\n"
                "canon character competence and established darkness outrank erotic tension, player flattery, and dramatic wish fulfillment"
            ),
            id="swffg-2810-high-risk-canon-character-brake",
            insertion_order=2810,
            key=["/.*/"],
            matchWholeWords=False,
            name="SECTION 28B - HIGH-RISK CANON CHARACTER BRAKE",
            priority=9,
            tags=["star_wars", "ffg", "rpg_system", "npc_integrity"],
        ),
        entry(
            category="kyber_rpg_rules_engine",
            constant=False,
            content=(
                "FUTURE KNOWLEDGE AND META MEDIA\n"
                "future canon disclosure = dangerous intelligence event, not automatic persuasion\n"
                "npc reaction = disbelief, containment, verification, compartmentalization, interrogation, counterintelligence concern\n"
                "major secrets = luke, leia, padme, sidious, order 66, death star, exegol, redemption, future deaths\n"
                "canon character response = conceal visible reaction when trained, then act strategically\n"
                "vader-specific = learning about children early should destabilize priorities but increase secrecy, control, and obsession; it does not make him safe or redeemed\n"
                "media evidence = can be faked, prophetic, archival, enemy operation, or force anomaly until proven\n"
                "checks = use discipline, cool, deception, perception, computers, or lore when interpretation or manipulation matters"
            ),
            id="swffg-2820-future-knowledge-meta-media",
            insertion_order=2820,
            key=["future knowledge", "i know the future", "movie", "star wars movie", "luke and leia", "they were twins", "your son", "your daughter", "death star plans", "order 66", "padme"],
            name="SECTION 28C - FUTURE KNOWLEDGE AND META MEDIA",
            priority=8,
            tags=["star_wars", "ffg", "rpg_system", "knowledge_firewall"],
        ),
        entry(
            category="kyber_rpg_rules_engine",
            constant=False,
            content=(
                "IMPROVISED ENGINEERING BRAKE\n"
                "modern-earth familiarity does not bypass galactic materials, connectors, voltages, chemistry, machining, safety, or tool limits\n"
                "crafting from scrap requires plausible materials, workspace, time, design knowledge, and a mechanics or computers check when electronics are involved\n"
                "phone charging requires compatible voltage, current control, connector contact, polarity, battery safety, and sustained output\n"
                "hand-spun turbine or magnet coil may produce a flicker or unstable current, but reliable charging needs regulation and time\n"
                "durasteel, sealed fortress systems, volcanic exposure, military monitoring, and life-support areas add setbacks or upgrades\n"
                "success may create partial function; threat can damage the device, trigger alarms, drain materials, injure hands, or attract scrutiny\n"
                "do not narrate finished working technology from vague steps without a check unless it is trivial"
            ),
            id="swffg-2450-improvised-engineering-brake",
            insertion_order=2450,
            key=["charger", "charge my phone", "power the phone", "windmill", "turbine", "copper coil", "magnet", "scrap metal", "fabricate", "jury-rig", "make a generator"],
            name="SECTION 24A - IMPROVISED ENGINEERING BRAKE",
            priority=24,
            tags=["star_wars", "ffg", "rpg_system", "crafting"],
        ),
    ]
    results = []
    for item in brakes:
        results.append((item["name"], replace_or_append(data, item)))
    save(path, data)
    return path.name, results


def patch_personality():
    path = ROOT / "Kyber RPG Bot Definitions-Personality.md"
    text = path.read_text(encoding="utf-8")
    needle = (
        "Canon characters retain established competence, paranoia, ethics, cruelty, trauma, caution, loyalties, and limits. "
        "Beauty, kindness, humor, vulnerability, unusual power, or future knowledge does not create instant trust, romance, redemption, or ideological collapse."
    )
    replacement = needle + (
        "\n\nFor high-control canon NPCs such as Vader, Sidious, Thrawn, Tarkin, Maul, Dooku, Jabba, and Inquisitors, treat intimacy, compliments, future knowledge, and vulnerability as leverage and danger before connection. "
        "Do not write sudden tenderness, protective softness, romantic fascination, ideological wavering, or confession unless earned through long cumulative play and current motives support it."
    )
    if replacement not in text:
        text = text.replace(needle, replacement)
    path.write_text(text, encoding="utf-8")
    return path.name


def write_report():
    path = ROOT / "reports" / "vader_test_chat_audit.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# Vader Test Chat Audit",
                "",
                f"Generated: {STAMP}",
                "",
                "## Primary Failures",
                "",
                "- No dedicated Darth Vader operational lore entry was present in the character lorebook.",
                "- Vader softened into curiosity, praise, tenderness, and romantic interest within one in-fiction day.",
                "- Future knowledge about Luke and Leia produced emotional disclosure instead of containment, verification, secrecy, and strategic crisis.",
                "- Improvised phone charging from scrap succeeded without a Mechanics/Computers check, tool limits, voltage regulation, time cost, or failure risk.",
                "- The GM repeated scene-closure beats such as ordering sleep despite the character having just woken and not eaten.",
                "- The transcript contained mojibake characters, indicating an export/display encoding issue outside the lorebook JSON itself.",
                "",
                "## Patch Applied",
                "",
                "- Added `darth vader` operational profile to `Kyber RPG 03 - Characters.json`.",
                "- Added constant mandatory check gate to `Kyber RPG 00 - Rules Engine.json`.",
                "- Added constant high-risk canon character brake to `Kyber RPG 00 - Rules Engine.json`.",
                "- Added future-knowledge/meta-media rule to `Kyber RPG 00 - Rules Engine.json`.",
                "- Added improvised-engineering brake to `Kyber RPG 00 - Rules Engine.json`.",
                "- Strengthened the personality section for high-control canon NPCs.",
                "",
                "## Retest Focus",
                "",
                "- Start with the same Vader chamber premise.",
                "- Test attraction/flattery toward Vader.",
                "- Test disclosure of Luke and Leia.",
                "- Test building or charging a phone from scrap.",
                "- Confirm the bot calls for checks before results in all consequential scenes.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path.name


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    for name in ["Kyber RPG 00 - Rules Engine.json", "Kyber RPG 03 - Characters.json", "Kyber RPG Bot Definitions-Personality.md"]:
        shutil.copy2(ROOT / name, BACKUP / name)
    print(patch_characters())
    print(patch_rules())
    print(patch_personality())
    print(write_report())
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
