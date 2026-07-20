import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / f"finish-pass-{date.today().isoformat()}"

RENAMES = {
    "Kyber RPG Rules.json": "Kyber RPG 00 - Rules Engine.json",
    "Star Wars Core.json": "Kyber RPG 01 - Core Continuity.json",
    "Star Wars History.json": "Kyber RPG 02 - Eras and History.json",
    "Star Wars Characters.json": "Kyber RPG 03 - Characters.json",
    "Star Wars Factions and Governments.json": "Kyber RPG 04 - Factions and Governments.json",
    "Star Wars Geography.json": "Kyber RPG 05 - Worlds and Regions.json",
    "Star Wars Sepcies and Cultures.json": "Kyber RPG 06 - Species and Cultures.json",
    "Star Wars Economic Society and Law.json": "Kyber RPG 07 - Society Law Economy.json",
    "Star Wars Technology.json": "Kyber RPG 08 - Technology Ships Gear.json",
    "Star Wars Creatures.json": "Kyber RPG 09 - Creatures and Hazards.json",
    "Star Wars Force Abilities.json": "Kyber RPG 10 - Force Powers.json",
    "Star Wars Force Orders and Traditions.json": "Kyber RPG 11 - Force Orders.json",
    "Star Wars Force Lightsabers.json": "Kyber RPG 12 - Lightsabers and Kyber.json",
    "Star Wars Force Metaphysic Artifacts.json": "Kyber RPG 13 - Force Metaphysics Artifacts.json",
    "Star Wars Legends.json": "Kyber RPG 14 - Legends Supplements.json",
}

CATEGORIES = {
    "Kyber RPG 00 - Rules Engine.json": "kyber_rpg_rules_engine",
    "Kyber RPG 01 - Core Continuity.json": "kyber_rpg_core_continuity",
    "Kyber RPG 02 - Eras and History.json": "kyber_rpg_eras_history",
    "Kyber RPG 03 - Characters.json": "kyber_rpg_characters",
    "Kyber RPG 04 - Factions and Governments.json": "kyber_rpg_factions_governments",
    "Kyber RPG 05 - Worlds and Regions.json": "kyber_rpg_worlds_regions",
    "Kyber RPG 06 - Species and Cultures.json": "kyber_rpg_species_cultures",
    "Kyber RPG 07 - Society Law Economy.json": "kyber_rpg_society_law_economy",
    "Kyber RPG 08 - Technology Ships Gear.json": "kyber_rpg_technology_ships_gear",
    "Kyber RPG 09 - Creatures and Hazards.json": "kyber_rpg_creatures_hazards",
    "Kyber RPG 10 - Force Powers.json": "kyber_rpg_force_powers",
    "Kyber RPG 11 - Force Orders.json": "kyber_rpg_force_orders",
    "Kyber RPG 12 - Lightsabers and Kyber.json": "kyber_rpg_lightsabers_kyber",
    "Kyber RPG 13 - Force Metaphysics Artifacts.json": "kyber_rpg_force_metaphysics_artifacts",
    "Kyber RPG 14 - Legends Supplements.json": "kyber_rpg_legends_supplements",
}

MOJIBAKE = {
    "â€”": "-",
    "â€“": "-",
    "â€": '"',
    "â€œ": '"',
    "â€™": "'",
    "â€˜": "'",
    "â€¦": "...",
    "â‰ ": "!=",
    "Â": "",
}

SUMMARY_KEYS = {
    "major worlds": ["major worlds", "important planets", "prominent systems", "known worlds overview"],
    "galaxy structure": ["galaxy structure", "galactic regions", "core rim unknown regions", "hyperlane geography"],
    "galactic dating and eras": ["galactic dating", "galactic eras", "bby aby", "timeline notation"],
    "the force": ["the force", "force metaphysics", "living force", "cosmic force"],
    "hyperspace and navigation": ["hyperspace navigation", "hyperdrive routes", "navicomputer", "hyperspace travel"],
    "droids and common technology": ["common technology", "droid society", "everyday droids", "galactic devices"],
    "jedi order": ["jedi order", "jedi council", "jedi code", "jedi institution"],
    "legends post-endor supplement": ["legends post-endor", "legends new republic era", "legends yuuzhan vong", "legends legacy era"],
    "legends ancient supplement": ["legends ancient history", "legends old republic", "legends ancient sith", "legends rakata"],
}

CHARACTER_REWRITES = {
    "cassian andor": """CASSIAN ANDOR
continuity = canon
era = rebellion before rogue one
role = intelligence operative, recruiter, infiltrator, assassin when ordered
goals = hurt empire, protect rebel network, complete mission despite moral cost
methods = deception, surveillance, covert violence, false papers, local contacts
trust threshold = slow; tests motives and usefulness before disclosure
violence threshold = pragmatic; will shoot first if exposure endangers mission
weakness = guilt, exhaustion, attachment to people trapped by empire
rpg use = does not admire strangers quickly; cooperation requires credible anti-imperial value""",
    "mon mothma andor era": """MON MOTHMA - ANDOR ERA
continuity = canon
era = imperial senate, early rebellion
role = public loyalist mask, covert rebel financier and organizer
goals = build lawful-looking resistance until open rebellion becomes unavoidable
methods = coded patronage, political cover, careful alliances, controlled risk
trust threshold = extremely high; exposure threatens family, network, and rebellion
conflict = ideals versus necessary secrecy and personal sacrifice
response to radicals = cautious alliance; rejects needless cruelty but may need deniable actors
rpg use = access to her requires political credibility, proof, or trusted intermediaries""",
    "bail organa": """BAIL ORGANA
continuity = canon
era = late republic, early empire
role = alderaanian senator, rebel architect, guardian of leia
goals = preserve democracy, protect alderaan, oppose empire covertly
methods = diplomacy, legal cover, intelligence channels, relief operations
trust threshold = high but humane; tests discretion and moral discipline
violence threshold = avoids cruelty; will fund armed resistance when tyranny leaves no lawful path
hard limit = will not casually expose leia, alderaan, or rebel networks
rpg use = generous does not mean gullible; aid comes with vetting and consequences""",
    "barriss offee": """BARRISS OFFEE
continuity = canon
era = clone wars into imperial aftermath
role = fallen jedi healer, temple bomber, later inquisitor-survivor trajectory
goals = justice warped by disillusionment; later survival and atonement pressure
methods = discipline, concealment, medical skill, precise force use, moral argument
trust threshold = guarded; recognizes institutional hypocrisy but not random manipulation
violence threshold = capable of extreme acts when ideology collapses restraint
rpg use = do not portray as simple villain or easy redemption; guilt and conviction coexist""",
    "moff gideon": """MOFF GIDEON
continuity = canon
era = imperial remnant, new republic
role = warlord, intelligence operator, mandalore exploiter
goals = power, control of force-sensitive research, restoration of imperial dominance
methods = intimidation, hostage leverage, black-site science, elite troops, betrayal
trust threshold = transactional only; every alliance is a tool
violence threshold = high; destroys assets before losing them
rpg use = never becomes harmless through charm; mercy usually serves strategy""",
    "the grand inquisitor": """THE GRAND INQUISITOR
continuity = canon
era = imperial reign
role = chief jedi hunter under vader and sidious
goals = locate survivors, break force sensitives, maintain rank
methods = intimidation, archival knowledge, dueling discipline, psychological pressure
trust threshold = none outside hierarchy; cooperation is coercive
violence threshold = high but controlled; prefers capture if intelligence value remains
rpg use = treats mercy, fear, and hope as tools to expose fugitives""",
    "kanan jarrus": """KANAN JARRUS
continuity = canon
era = imperial rebellion
role = survivor jedi, rebel mentor, ghost crew member
goals = protect crew, resist empire, train ezra without repeating jedi failures
methods = caution, improvisation, sacrifice, small-cell tactics
trust threshold = wary with force matters; warmer with proven rebels and civilians in danger
fear = exposing himself or failing students as the old order failed him
rpg use = helps underdogs but will not risk his crew for a stranger's vanity""",
    "jabba the hutt": """JABBA THE HUTT
continuity = canon
era = clone wars through galactic civil war
role = hutt crime lord of tatooine
goals = profit, tribute, spectacle, dominance, debt control
methods = contracts, bounty hunters, blackmail, enslavement, public punishment
trust threshold = nonexistent; loyalty must be bought, feared, or useful
violence threshold = casual when reputation is challenged
rpg use = bargaining with jabba creates debt; insults or failed jobs invite lethal examples""",
    "kay vess": """KAY VESS
continuity = canon
era = galactic civil war, around 3 ABY
role = thief, slicer-adjacent outlaw, survivor of canto bight underworld
goals = freedom, survival, one big score, protection of nix
methods = bluffing, stealth, improvisation, underworld favors, fast escape
trust threshold = low; responds to practical help more than ideals
weakness = debt, inexperience with galactic-scale politics, attachment to nix
rpg use = useful underworld contact, not a rebel saint or master criminal mastermind""",
    "mother talzin": """MOTHER TALZIN
continuity = canon
era = clone wars
role = nightsister matriarch and dathomirian force-magick leader
goals = survival of clan, revenge against sidious/dooku, preservation of power
methods = ritual magick, manipulation, spirit-binding, proxies, prophecy
trust threshold = clan-centered and transactional
violence threshold = high when dathomir or her bloodline is threatened
rpg use = aid always carries occult price, clan obligation, or hidden strategic cost""",
    "nala se": """NALA SE
continuity = canon
era = clone wars, early empire
role = kaminoan scientist, clone engineer
goals = preserve research, protect selected clones/omega under pressure
methods = secrecy, genetic science, compartmentalized truth, institutional obedience
trust threshold = narrow; emotional choices are concealed behind clinical behavior
weakness = imperial coercion and kaminoan survival politics
rpg use = information from her is precise but incomplete unless trust or leverage is strong""",
    "cere junda": """CERE JUNDA
continuity = canon
era = imperial jedi survivor period
role = former jedi, hidden path leader, mentor
goals = protect force survivors, confront trauma, preserve jedi knowledge
methods = caution, archives, discipline, underground networks, decisive combat when cornered
trust threshold = measured; trauma makes reckless force use alarming
fear = falling back into despair or endangering survivors
rpg use = compassionate but not permissive; demands responsibility from force users""",
}

RECENT_ENTRIES = {
    "Kyber RPG 02 - Eras and History.json": [
        ("kyber-recent-andor-s2", "andor season 2", "ANDOR SEASON 2\ncontinuity = canon\nchronology = 4 bby to 1 bby; final arc leads into rogue one\nfocus = rebel cells becoming alliance, isb pressure, ghorman, mon mothma break with senate\nrpg use = early rebellion is fragmented, paranoid, underfunded, and morally costly; imperial security response is competent", ["andor season 2", "andor s2", "andor final season"]),
        ("kyber-recent-ghorman-project", "ghorman project and massacre", "GHORMAN PROJECT AND MASSACRE\ncontinuity = canon; andor season 2 expansion of older ghorman lore\nimperial goal = exploit ghorman resources for secret weapons work while shaping public narrative\nkey actors = krennic, isb supervisors, ministry propaganda, ghorman front, mon mothma\nrpg use = ghorman scenes should involve surveillance, staged provocation, resource extraction, civic dignity, and catastrophic imperial reprisal", ["ghorman project", "ghorman massacre", "mina-rau", "kalkite", "ghorman front"]),
        ("kyber-recent-skeleton-crew", "skeleton crew era note", "SKELETON CREW ERA NOTE\ncontinuity = canon\nchronology = new republic era around 9 aby\nfocus = lost at attin, pirate predation, children aboard onyx cinder, jod na nawood deception\nrpg use = new republic space can still contain hidden worlds, weak enforcement, pirates, old republic infrastructure, and local systems cut off from galactic reality", ["skeleton crew", "onyx cinder", "at attin incident"]),
        ("kyber-recent-tales-underworld", "tales of the underworld", "TALES OF THE UNDERWORLD\ncontinuity = canon\nrelease = 2025 animated anthology\nfocus = asajj ventress given new life and forced through underworld survival; cad bane confronts past and frontier law\nrpg use = underworld stories can involve old grudges, changing identities, bounty politics, and survival after presumed endings", ["tales of the underworld", "asajj ventress underworld", "cad bane underworld"]),
        ("kyber-recent-high-republic-ending", "high republic phase iii ending", "HIGH REPUBLIC PHASE III ENDING\ncontinuity = canon\nstate = nihil occlusion zone collapses; marchion ro faces capture/trial pressure; blight and nameless crisis define late phase\nrpg use = high republic aftermath should leave traumatized jedi, damaged frontier trust, liberated sectors, and fear of anti-force creatures", ["trials of the jedi", "nihil ending", "high republic phase iii", "nameless creatures"]),
        ("kyber-recent-outlaws-era", "star wars outlaws era", "STAR WARS OUTLAWS ERA\ncontinuity = canon\nchronology = around 3 aby after hoth\nfocus = underworld scramble while empire and rebellion exploit criminal networks\nrpg use = syndicates compete with pyke, hutt, crimson dawn, ashiga, and zerek besh influence; reputation and debt matter more than hero speeches", ["star wars outlaws", "outlaws era", "kay vess era"]),
        ("kyber-recent-mask-fear", "reign of the empire mask of fear", "REIGN OF THE EMPIRE - THE MASK OF FEAR\ncontinuity = canon\nchronology = early imperial rule after revenge of the sith\nfocus = mon mothma, bail organa, saw gerrera, and political resistance under authoritarian consolidation\nrpg use = early rebellion should feel legally dangerous, socially fragmented, and vulnerable to surveillance", ["mask of fear", "reign of the empire", "mon mothma early empire", "bail organa early empire"]),
        ("kyber-watch-maul-shadow-lord", "maul shadow lord watch item", "MAUL: SHADOW LORD\ncontinuity = announced canon project; plot details not yet stable\nstatus = watch item only\nrpg use = do not invent events; if referenced, treat as future official media requiring source check before lore expansion", ["maul shadow lord", "star wars maul shadow lord"]),
    ],
    "Kyber RPG 03 - Characters.json": [
        ("kyber-recent-jod-na-nawood", "jod na nawood", "JOD NA NAWOOD\ncontinuity = canon\naliases = captain silvo, crimson jack\nrole = pirate, liar, opportunistic force-user claimant near at attin incident\ngoals = wealth, survival, control of lost-world access\nmethods = charm, threats, identity fraud, lightsaber intimidation, betrayal\nrpg use = charismatic help can become predatory leverage; do not treat jedi claim as proof of jedi ethics", ["jod na nawood", "captain silvo", "crimson jack"]),
        ("kyber-recent-fern", "fern", "FERN\ncontinuity = canon\nrole = at attin youngling, captain of skeleton crew\ntraits = proud, decisive, learns delegation under pressure\nrpg use = child character; never sexualize; portray as endangered minor with agency, fear, and limits", ["fern skeleton crew", "captain fern"]),
        ("kyber-recent-wim", "wim", "WIM\ncontinuity = canon\nrole = at attin youngling, skeleton crew member\ntraits = imaginative, adventure-hungry, learns real danger is not storybook heroism\nrpg use = child character; never sexualize; use for new republic lost-world stakes, not adult romance or wish fulfillment", ["wim skeleton crew"]),
        ("kyber-recent-kb", "kb", "KB\ncontinuity = canon\nrole = at attin youngling, skeleton crew member with prosthetic/cybernetic support needs\ntraits = observant, capable, must account for physical limitations under stress\nrpg use = child character; never sexualize; danger should respect medical/device vulnerability without reducing her to it", ["kb skeleton crew"]),
        ("kyber-recent-neel", "neel", "NEEL\ncontinuity = canon\nspecies = myykian\nrole = at attin youngling, skeleton crew member\ntraits = cautious, kind, physically nonhuman limitations in climbing and movement\nrpg use = child character; never sexualize; useful for showing nonhuman needs in practical hazards", ["neel skeleton crew", "myykian"]),
        ("kyber-recent-sliro-barsha", "sliro barsha", "SLIRO BARSHA\ncontinuity = canon\nrole = isb director using zerek besh as criminal front\nmethods = family betrayal, black budget funding, death marks, secret codex, proxy syndicate pressure\nrpg use = underworld threat may actually be imperial intelligence; defeating street assets does not expose full command structure", ["sliro barsha", "sliro", "director sliro"]),
        ("kyber-recent-vail-tormin", "vail tormin", "VAIL TORMIN\ncontinuity = canon\nrole = bounty hunter connected to kay vess and zerek besh events\nmethods = pursuit, leverage, professional violence, opportunistic alliance\nrpg use = bounty hunters may switch sides only for credible profit, survival, or revenge, not sentiment alone", ["vail tormin", "vail"]),
        ("kyber-recent-riko-vess", "riko vess", "RIKO VESS\ncontinuity = canon\nrole = slicer and kay vess's estranged mother\nmethods = technical expertise, concealment, opportunistic survival\nrpg use = family ties create leverage and resentment; reconciliation requires evidence, not one emotional speech", ["riko vess", "riko"]),
    ],
    "Kyber RPG 04 - Factions and Governments.json": [
        ("kyber-recent-zerek-besh", "zerek besh", "ZEREK BESH\ncontinuity = canon\npublic identity = new wealthy criminal syndicate after hoth\nhidden truth = imperial security bureau front under sliro barsha\nmethods = black-budget funding, death marks, vault intelligence, intimidation of older syndicates\nrpg use = players may misread imperial intelligence as normal underworld politics; criminal jobs can be counterinsurgency traps", ["zerek besh", "zerek besh syndicate"]),
        ("kyber-recent-ghorman-front", "ghorman front", "GHORMAN FRONT\ncontinuity = canon\nrole = ghorman resistance movement under imperial pressure\ncontext = civic resistance, rebel interest, imperial provocation and surveillance\nrpg use = local rebels are not disposable quest-givers; help risks collective reprisal, informants, and propaganda backlash", ["ghorman front", "ghorman resistance"]),
        ("kyber-recent-at-attin-government", "at attin government", "AT ATTIN GOVERNMENT\ncontinuity = canon\nstructure = isolated lost-world civic order directed by supervisor system and great work ideology\nsecurity = safety droids, barrier isolation, controlled information\nrpg use = hidden peaceful systems can be authoritarian through bureaucracy, secrecy, and isolation rather than open brutality", ["at attin government", "the supervisor", "great work"]),
    ],
    "Kyber RPG 05 - Worlds and Regions.json": [
        ("kyber-recent-at-attin", "at attin", "AT ATTIN\ncontinuity = canon\nregion = hidden/lost new republic-era world protected by barrier\nsociety = tidy suburban order, great work, controlled information, secret mint infrastructure\nrpg use = outsiders trigger civic/security crisis; piracy threat comes from knowledge of wealth and route access", ["at attin", "lost planet at attin"]),
        ("kyber-recent-toshara", "toshara", "TOSHARA\ncontinuity = canon\nrole = savanna moon/world used in star wars outlaws underworld travel\nfeatures = criminal jobs, imperial presence, ship repair pressure, local syndicate leverage\nrpg use = good starter location for outlaw survival, debt, repairs, and reputation tests", ["toshara"]),
        ("kyber-recent-westhill-palace", "westhill palace", "WESTHILL PALACE\ncontinuity = canon\nlocation = sliro barsha estate on canto bight/cantonica\nfunction = luxury front, vault, underworld intelligence hub\nrpg use = heist location with elite security, false criminal branding, and hidden imperial stakes", ["westhill palace", "sliro vault"]),
    ],
    "Kyber RPG 08 - Technology Ships Gear.json": [
        ("kyber-recent-onyx-cinder", "onyx cinder", "ONYX CINDER\ncontinuity = canon\nrole = buried starship discovered on at attin; base of skeleton crew\nassociated droid = sm-33\nrpg use = lost ships can carry locked routes, old orders, hidden autopilot, pirate claims, and child-endangerment stakes", ["onyx cinder", "the onyx cinder"]),
        ("kyber-recent-sm-33", "sm-33", "SM-33\ncontinuity = canon\nrole = droid first mate of onyx cinder\nbehavior = pirate-coded loyalty, ship knowledge, old command constraints\nrpg use = droid loyalty may be literal, dangerous, and bound by prior captaincy or ship protocol", ["sm-33", "sm 33"]),
        ("kyber-recent-trailblazer", "the trailblazer", "THE TRAILBLAZER\ncontinuity = canon\nrole = kay vess's stolen light freighter during outlaws events\nrpg use = ship ownership is legally and criminally contested; repairs, transponder risk, and debt should follow it", ["the trailblazer", "trailblazer freighter"]),
        ("kyber-recent-ghorsian-crystal", "ghorsian crystal", "GHORSIAN CRYSTAL\ncontinuity = canon\nsource layer = wookieepedia detail from the acolyte: wayseeker\nuse = non-kyber crystal associated with vernestra rwoh shield interaction and lightsaber-nullifier complications\nrpg use = force-adjacent materials can have narrow mechanical effects without behaving like generic kyber", ["ghorsian crystal", "ghorisan crystal"]),
    ],
    "Kyber RPG 11 - Force Orders.json": [
        ("kyber-recent-wayseeker", "wayseeker", "WAYSEEKER\ncontinuity = canon\norder = jedi order title/practice during high republic\nmeaning = jedi operating independently of high council direction while following the force\nstatus = not a late republic norm\nrpg use = high republic jedi can be institutionally sanctioned independents; late republic jedi should not casually use the title", ["wayseeker", "jedi wayseeker"]),
    ],
    "Kyber RPG 13 - Force Metaphysics Artifacts.json": [
        ("kyber-recent-nameless", "nameless creatures", "NAMELESS CREATURES\ncontinuity = canon\nrole = anti-force predators central to high republic crisis\neffect = terror and force-draining petrification risk for jedi/force sensitives\nrpg use = not normal animals; use sparingly as existential threat, morale collapse, and force-user vulnerability", ["nameless creatures", "the nameless", "leveler"]),
    ],
    "Kyber RPG 14 - Legends Supplements.json": [
        ("kyber-legends-source-policy", "legends and wookieepedia source policy", "LEGENDS AND WOOKIEEPEDIA SOURCE POLICY\ncanon = first layer and controls contradictions\nlegends = second layer; may fill gaps when labeled and compatible\nwookieepedia = third layer; useful for aliases, minor entities, obscure details, and lead-finding\nrpg use = never overwrite canon with legends or unsourced wiki detail; label uncertainty when needed", ["legends policy", "wookieepedia policy", "canon legends wookieepedia"]),
    ],
}


def fix_text(value):
    if isinstance(value, str):
        for bad, good in MOJIBAKE.items():
            value = value.replace(bad, good)
        return value
    if isinstance(value, list):
        return [fix_text(item) for item in value]
    if isinstance(value, dict):
        return {key: fix_text(item) for key, item in value.items()}
    return value


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_keys(entry, keys=None):
    if keys is not None:
        entry["key"] = keys
    joined = ", ".join(entry.get("key", []))
    entry["keysRaw"] = joined
    entry["keywordsRaw"] = joined


def template_entry(existing, entry_id, name, content, keys, insertion_order):
    entry = {key: fix_text(value) for key, value in existing.items()}
    entry.update(
        {
            "activationMode": "standard",
            "activationScript": "",
            "case_sensitive": False,
            "comment": "added in finish pass; sources: official starwars.com plus wookieepedia as secondary detail layer",
            "constant": False,
            "content": content,
            "enabled": True,
            "extensions": {},
            "groupWeight": 100,
            "id": entry_id,
            "inclusionGroupRaw": "",
            "insertion_order": insertion_order,
            "key": keys,
            "keyMatchPriority": True,
            "keysecondary": [],
            "keysecondaryRaw": "",
            "matchWholeWords": True,
            "minMessages": 0,
            "name": name,
            "prioritizeInclusion": False,
            "priority": 2,
            "probability": 100,
            "selectiveLogic": 0,
            "tags": ["star_wars", "canon", "finish_pass"],
        }
    )
    sync_keys(entry)
    return entry


def backup_sources():
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for old_name in RENAMES:
        path = ROOT / old_name
        if path.exists():
            shutil.copy2(path, ARCHIVE / old_name)
    for name in [
        "Kyber RPG Bot Definitions-Personality.md",
        "Kyber RPG Bot Example Dialogs.md",
        "Initial Messages.md",
        "RPG Bot Public Facing Card.html",
    ]:
        path = ROOT / name
        if path.exists():
            shutil.copy2(path, ARCHIVE / name)


def rename_files():
    for old_name, new_name in RENAMES.items():
        old_path = ROOT / old_name
        new_path = ROOT / new_name
        if old_path.exists():
            old_path.rename(new_path)


def update_entries():
    for path in sorted(ROOT.glob("Kyber RPG *.json")):
        data = read_json(path)
        data = fix_text(data)
        category = CATEGORIES.get(path.name)
        existing_names = {entry.get("name") for entry in data}
        max_order = max((entry.get("insertion_order", 0) for entry in data), default=0)

        for index, entry in enumerate(data):
            if category:
                entry["category"] = category
            entry["name"] = fix_text(entry.get("name", ""))
            entry["content"] = fix_text(entry.get("content", ""))
            entry["key"] = [fix_text(key) for key in entry.get("key", [])]

            lower_name = entry["name"].lower()
            if lower_name in SUMMARY_KEYS:
                sync_keys(entry, SUMMARY_KEYS[lower_name])
                entry["matchWholeWords"] = True
                entry["priority"] = max(entry.get("priority", 1), 2)

            if path.name == "Kyber RPG 04 - Factions and Governments.json" and lower_name == "sith doctrine and artifacts":
                sync_keys(entry, [key for key in entry["key"] if key.lower() != "sith holocron"] + ["sith doctrine artifacts"])
            if path.name == "Kyber RPG 08 - Technology Ships Gear.json" and lower_name == "holocrons":
                sync_keys(entry, [key for key in entry["key"] if key.lower() != "sith holocron"] + ["holocron technology"])
            if path.name == "Kyber RPG 02 - Eras and History.json" and lower_name == "first order and resistance war":
                sync_keys(entry, [key for key in entry["key"] if key.lower() != "starkiller base"] + ["first order resistance war"])
            if path.name == "Kyber RPG 08 - Technology Ships Gear.json" and lower_name == "superweapons":
                sync_keys(entry, [key for key in entry["key"] if key.lower() != "starkiller base"] + ["planet-killer superweapons"])

            if path.name == "Kyber RPG 03 - Characters.json":
                rewrite = CHARACTER_REWRITES.get(lower_name)
                if rewrite:
                    entry["content"] = rewrite
                    entry["priority"] = max(entry.get("priority", 1), 3)
                elif "goals =" not in entry.get("content", "").lower() and "methods =" not in entry.get("content", "").lower():
                    entry["content"] = entry["content"].rstrip() + "\nrpg use = portray from established motives and limits; no instant trust, romance, surrender, or competence collapse"

            seen = []
            for key in entry.get("key", []):
                if key and key not in seen:
                    seen.append(key)
            sync_keys(entry, seen)

        for entry_id, name, content, keys in RECENT_ENTRIES.get(path.name, []):
            if name not in existing_names and entry_id not in {entry.get("id") for entry in data}:
                max_order += 100
                data.append(template_entry(data[0], entry_id, name, content, keys, max_order))
                existing_names.add(name)

        data.sort(key=lambda item: item.get("insertion_order", 0))
        write_json(path, data)


def main():
    backup_sources()
    rename_files()
    update_entries()
    print(f"Backed up originals to {ARCHIVE}")
    print("Renamed and updated Kyber RPG lorebooks")


if __name__ == "__main__":
    main()
