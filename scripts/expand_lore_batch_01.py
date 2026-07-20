import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"lore-expansion-batch-01-{date.today().isoformat()}"
REPORTS = ROOT / "reports"

BASE_SOURCES = {
    "official_databank": "https://www.starwars.com/databank/",
    "official_news": "https://www.starwars.com/news",
    "wookieepedia_species": "https://starwars.fandom.com/wiki/Species",
    "wookieepedia_species_legends": "https://starwars.fandom.com/wiki/Species/Legends",
    "wookieepedia_droid": "https://starwars.fandom.com/wiki/Droid",
    "wookieepedia_droid_legends": "https://starwars.fandom.com/wiki/Droid/Legends",
}


def entry(entry_id, name, content, keys, tags=None, priority=1, source="wookieepedia tertiary; canon/legends labels retained"):
    return {
        "id": entry_id,
        "name": name,
        "content": content,
        "key": keys,
        "tags": tags or [],
        "priority": priority,
        "source": source,
    }


EXPANSION = {
    "Kyber RPG 06 - Species and Cultures.json": [
        entry("kyber-species-anzati", "anzati", "ANZATI\ncontinuity = legends primary; canon-adjacent only if separately sourced\nbiology = near-human predators with cheek proboscises; feed on life essence or brain-soup concept in legends\nrpg use = social predator, assassin, ancient threat; charm may mask feeding danger\nlimits = do not treat as common public knowledge", ["anzati", "anzat"]),
        entry("kyber-species-barabel", "barabels", "BARABELS\ncontinuity = legends prominent; limited canon checks required\ntraits = reptilian hunters, heat-loving, direct, clan/pride driven\nculture = respect strength, courage, survival skill, and clear speech\nrpg use = dangerous trackers, mercenaries, survival guides; insults can escalate quickly", ["barabel", "barabels"]),
        entry("kyber-species-besalisk", "besalisks", "BESALISKS\ncontinuity = canon\nbiology = large multi-armed sentients from ojoj-style traditions in canon/legends material\nsocial use = extra arms useful for cooks, mechanics, laborers, brawlers\nrpg use = avoid comic-only portrayal; size and arms affect cramped spaces, restraints, tools, and intimidation", ["besalisk", "besalisks"]),
        entry("kyber-species-caamasi", "caamasi", "CAAMASI\ncontinuity = legends primary\ntraits = pacifist-leaning, empathic reputation, strong memory culture\nhistory = caamas devastation creates refugee/grievance politics\nrpg use = witnesses, diplomats, moral pressure, anti-genocide memory; not every caamasi is harmless", ["caamasi"]),
        entry("kyber-species-celegian", "celegians", "CELEGIANS\ncontinuity = legends primary\nbiology = floating tentacled sentients from high-pressure cyanogen atmosphere\naccess needs = life-support chamber or atmosphere containment in standard environments\nrpg use = alien scholar/diplomat with logistical vulnerability; sabotage of tank = lethal threat", ["celegian", "celegians"]),
        entry("kyber-species-defel", "defel", "DEFEL\ncontinuity = legends primary; canon check required per use\nbiology = light-bending fur creates shadowlike appearance under many spectra\nculture/use = stealth specialists, scouts, assassins, miners\nrpg use = detection should depend on lighting, sensors, scent, sound, and preparation, not invisibility handwave", ["defel", "wraith species"]),
        entry("kyber-species-draethos", "draethos", "DRAETHOS\ncontinuity = legends primary\nbiology = long-lived predatory-looking sentients, often telepathic in legends depictions\nculture = reputation for scholarship, force traditions, and severe discipline\nrpg use = alien mentor, archivist, or austere mystic; appearance may provoke fear or prejudice", ["draethos"]),
        entry("kyber-species-falleen", "falleen", "FALLEEN\ncontinuity = canon/legends compatible with caution\nbiology = reptilian near-humanoids; legends emphasizes pheromonal influence and emotional discipline\nculture = controlled presentation, pride, hierarchy, political subtlety\nrpg use = social manipulation, court intrigue, Black Sun ties; pheromones are influence, not mind control", ["falleen"]),
        entry("kyber-species-fosh", "fosh", "FOSH\ncontinuity = legends primary\nbiology = avian sentients; rare and often obscure\nnotable = vergere in legends continuity\nrpg use = rare species for mystic, diplomat, or biological oddity; most NPCs may misidentify them", ["fosh"]),
        entry("kyber-species-givin", "givin", "GIVIN\ncontinuity = canon/legends\nbiology = skeletal-looking sentients adapted to vacuum/low pressure tolerance in many sources\nculture = mathematics, shipbuilding, probability, formal logic\nrpg use = navigators, engineers, eerie negotiators; vacuum tolerance is useful but not universal invulnerability", ["givin"]),
        entry("kyber-species-herglic", "herglics", "HERGLICS\ncontinuity = legends primary; canon check per use\nbiology = large whale-like sentients, amphibious/aquatic heritage\nculture = trade, gambling, gregarious public presence in many legends sources\nrpg use = size affects seating, armor, ships, medical care, and intimidation; avoid flattening into comic relief", ["herglic", "herglics"]),
        entry("kyber-species-iktotchi", "iktotchi", "IKTOTCHI\ncontinuity = canon/legends\nbiology = horned sentients from iktotchon; legends often links to limited precognition\nsocial issue = others may distrust perceived future-sight\nrpg use = pilots, seers, investigators; foresight should be symbolic/fragmentary, not omniscience", ["iktotchi", "iktotch"]),
        entry("kyber-species-killik", "killiks", "KILLIKS\ncontinuity = canon ancient references; legends major expansion\nbiology = insectoid hive species with joiner phenomenon in legends\nrisk = hive memory, pheromone/social assimilation, collective motives\nrpg use = unsettling colony encounters; individual consent and identity can become central stakes", ["killik", "killiks", "joiner"]),
        entry("kyber-species-neti", "neti", "NETI\ncontinuity = legends primary\nbiology = sentient plant species; extreme longevity and shape/growth themes in legends\nrpg use = ancient witness, patient strategist, hard-to-read nonhuman priorities; fire/drought/environment matter", ["neti"]),
        entry("kyber-species-noghri", "noghri", "NOGHRI\ncontinuity = legends primary\nbiology = compact lethal hunters from honoghr\nculture = clan honor, debt, service, deception by empire in legends\nrpg use = terrifying close-range commandos; loyalty can be absolute until betrayal is proven", ["noghri", "honoghr"]),
        entry("kyber-species-selkath", "selkath", "SELKATH\ncontinuity = legends primary; canon check per use\nhomeworld = manaan\nculture = kolto trade neutrality, aquatic city law, formal diplomacy\nrpg use = medical-resource politics, underwater access, neutrality violations, old republic scenarios", ["selkath", "manaan"]),
        entry("kyber-species-ssi-ruu", "ssi-ruu", "SSI-RUU\ncontinuity = legends primary\nbiology = saurian extragalactic/unknown regions species tied to entechment threat\nculture = caste, technology, religious fear of dying away from consecrated worlds\nrpg use = horror-tech enemy; entechment = identity/energy violation, not normal droid control", ["ssi-ruu", "ssiruuk", "entechment"]),
        entry("kyber-species-verpine", "verpine", "VERPINE\ncontinuity = canon/legends\nbiology = insectoid sentients; radio/comm-style communication themes in legends\nculture = engineering, hive cooperation, asteroid colonies\nrpg use = starship repair, custom weapons, sensor logic; social cues may not map to humanoid norms", ["verpine"]),
        entry("kyber-species-vurk", "vurk", "VURK\ncontinuity = canon\nbiology = reptilian/amphibious sentients; notable jedi coleman trebor\nrpg use = underused species for diplomats, jedi, laborers, water-adjacent communities; do not assume aggression from reptilian appearance", ["vurk"]),
        entry("kyber-species-yuuzhan-vong", "yuuzhan vong species", "YUUZHAN VONG SPECIES\ncontinuity = legends\norigin = extragalactic invaders from new jedi order era\nculture = pain, sacrifice, caste, biotechnology, religious conquest\nforce status = famously difficult for jedi to sense in legends context\nrpg use = major legends war threat; use only in legends/mixed games unless explicitly imported", ["yuuzhan vong", "vong"]),
    ],
    "Kyber RPG 09 - Creatures and Hazards.json": [
        entry("kyber-creature-acklay", "acklay", "ACKLAY\ncontinuity = canon\nrole = arena predator; crustacean/reptilian traits; dangerous claws and reach\nrpg use = open terrain melee hazard; threat can sunder gear, pin limbs, or force movement", ["acklay"]),
        entry("kyber-creature-nexu", "nexu", "NEXU\ncontinuity = canon\nrole = agile arena predator with multiple eyes and quilled back\nrpg use = ambush/leaping threat; setbacks in darkness/jungle; threat results can cause bleeding, panic, or lost footing", ["nexu"]),
        entry("kyber-creature-reek", "reek", "REEK\ncontinuity = canon\nrole = horned arena beast, charger, mountable with risk\nrpg use = crowd-control hazard; failed checks may knock prone, gore, trample, or break cover", ["reek"]),
        entry("kyber-creature-mynock", "mynocks", "MYNOCKS\ncontinuity = canon\nhabitat = space/asteroid environments; attach to ships and chew power cables\nrpg use = starship complication, hullwalk hazard, hyperspace delay; not a combat boss unless in swarm", ["mynock", "mynocks"]),
        entry("kyber-creature-dianoga", "dianoga", "DIANOGA\ncontinuity = canon\nhabitat = garbage, sewage, dark water, compact industrial spaces\nrpg use = hidden grappler hazard; detection depends on smell, water movement, trash shift, and sensors", ["dianoga", "trash compactor monster"]),
        entry("kyber-creature-exogorth", "exogorth", "EXOGORTH\ncontinuity = canon\nrole = giant space slug living in asteroids\nrpg use = environmental setpiece; ship-scale hazard, false cave, sudden bite, atmosphere pocket uncertainty", ["exogorth", "space slug"]),
        entry("kyber-creature-kouhun", "kouhun", "KOUHUN\ncontinuity = canon\nrole = venomous segmented assassination creature\nrpg use = stealth poison threat; detection through container residue, thermal movement, or local animal silence", ["kouhun", "kouhuns"]),
        entry("kyber-creature-gundark", "gundarks", "GUNDARKS\ncontinuity = canon\nrole = powerful aggressive cave/rocky-world predators\nrpg use = brute creature fight; confined terrain, grappling, thrown bodies, and fear checks matter", ["gundark", "gundarks"]),
        entry("kyber-creature-fyrnock", "fyrnocks", "FYRNOCKS\ncontinuity = canon\nhabitat = dark places; vulnerable to strong light in rebels-era depiction\nrpg use = swarm ambush, darkness hazard, improvised light tactics; threat can separate party", ["fyrnock", "fyrnocks"]),
        entry("kyber-creature-krykna", "krykna", "KRYKNA\ncontinuity = canon\nrole = large webbing/spiderlike lothal predators; hostile to many energy weapons in rebels context\nrpg use = tunnel hazard, web restraint, pack pressure; force/empathy may matter by scene", ["krykna"]),
        entry("kyber-creature-rathtar", "rathtar", "RATHTAR\ncontinuity = canon\nrole = tentacled rolling predator, contraband beast\nrpg use = shipboard containment disaster; threat destroys doors, cargo, limbs, or escape route", ["rathtar", "rathtars"]),
        entry("kyber-creature-vornskr", "vornskr", "VORNSKR\ncontinuity = legends\nrole = myrkr predator that hunts force-sensitive prey\nrpg use = legends anti-jedi wilderness threat; force concealment and animal handling may matter more than stealth alone", ["vornskr", "myrkr predator"]),
        entry("kyber-creature-ysalamir", "ysalamiri", "YSALAMIRI\ncontinuity = legends\nrole = myrkr creatures projecting force-neutral bubble in legends\nrpg use = anti-force tactical terrain; do not use in canon-only games unless imported as legends element", ["ysalamir", "ysalamiri"]),
        entry("kyber-creature-terentatek", "terentatek", "TERENTATEK\ncontinuity = legends\nrole = dark-side altered predator that hunts force users\nrpg use = old republic/sith ruin boss hazard; resistant to normal force assumptions, not unbeatable", ["terentatek"]),
        entry("kyber-creature-leviathan-kotor", "sithspawn leviathan", "SITHSPAWN LEVIATHAN\ncontinuity = legends\nrole = alchemical war beast/dark-side monstrosity in old republic legends\nrpg use = horror relic, laboratory failure, sith tomb guardian; moral cost and contamination matter", ["sithspawn leviathan", "leviathan sithspawn"]),
        entry("kyber-hazard-kolto-contamination", "kolto contamination", "KOLTO CONTAMINATION\ncontinuity = legends primarily\ncontext = manaan/old republic medical economy\nrpg use = healing-resource hazard; contaminated kolto can create infection, political liability, or supply crisis", ["kolto contamination", "tainted kolto"]),
        entry("kyber-hazard-spice-addiction", "spice addiction hazards", "SPICE ADDICTION HAZARDS\ncontinuity = canon/legends\nrisk = dependency, withdrawal, debt, exploitation, cartel leverage, impaired judgment\nrpg use = treat as social/medical/criminal pressure, not free power-up; cure requires time, care, and resources", ["spice addiction", "spice withdrawal"]),
        entry("kyber-hazard-vacuum-exposure", "vacuum exposure", "VACUUM EXPOSURE\ncontinuity = setting baseline\nrisk = decompression, freezing, hypoxia, embolism, panic, suit breach\nrpg use = immediate timed hazard; armor is not vacuum gear unless sealed and supplied", ["vacuum exposure", "hard vacuum", "suit breach"]),
    ],
    "Kyber RPG 14 - Legends Supplements.json": [
        entry("kyber-legends-rakata", "rakata and infinite empire", "RAKATA AND INFINITE EMPIRE\ncontinuity = legends\nera = pre-republic ancient history\ntraits = force-using conquerors, star forge, slave empire, technological brutality\nrpg use = ancient ruins, predatory artifacts, hyperspace anomalies, species trauma; canon games require explicit legends import", ["rakata", "infinite empire", "star forge"], priority=2),
        entry("kyber-legends-celestials", "celestials and architects", "CELESTIALS AND ARCHITECTS\ncontinuity = legends\nrole = ancient supercivilization linked to impossible megastructures and cosmic engineering\nrpg use = mystery scale; use fragments, machines, and consequences rather than omnipotent exposition", ["celestials", "architects", "centerpoint station"], priority=2),
        entry("kyber-legends-kwa-gree", "kwa and gree", "KWA AND GREE\ncontinuity = legends\nrole = ancient civilizations with hypergate/infinity gate and alien technology themes\nrpg use = ancient sites, unstable portals, nonhuman interfaces, archaeology danger", ["kwa", "gree enclave", "infinity gate", "hypergate"]),
        entry("kyber-legends-pius-dea", "pius dea crusades", "PIUS DEA CRUSADES\ncontinuity = legends\nera = early galactic republic dark age\ntraits = theocratic humanocentric crusades, political corruption, anti-alien violence\nrpg use = ancient institutional shame, relic cults, legal archives, sectarian villains", ["pius dea", "pius dea crusades"]),
        entry("kyber-legends-great-hyperspace-war", "great hyperspace war", "GREAT HYPERSPACE WAR\ncontinuity = legends\nera = old republic/sith empire conflict\nfigures = naga sadow, ludo kressh, marka ragnos legacy\nrpg use = sith ruins, old battlefields, cursed artifacts, republic historical blind spots", ["great hyperspace war", "naga sadow", "ludo kressh", "marka ragnos"]),
        entry("kyber-legends-exar-kun", "exar kun and ulic qel-droma war", "EXAR KUN AND ULIC QEL-DROMA WAR\ncontinuity = legends\ncontext = great sith war\ntraits = fallen jedi, massassi temples, corrupted students, mandalorian involvement\nrpg use = temptation arcs, yavin ruins, sith spirit hazards, jedi institutional trauma", ["exar kun", "ulic qel-droma", "great sith war"]),
        entry("kyber-legends-mandalorian-wars", "mandalorian wars", "MANDALORIAN WARS\ncontinuity = legends\nera = old republic before revan's fall\ntraits = republic hesitation, jedi schism, mandalorian crusade, mass shadow generator at malachor v\nrpg use = veterans, war crimes, mando honor, jedi guilt, unexploded superweapon consequences", ["mandalorian wars", "malachor v", "mass shadow generator"]),
        entry("kyber-legends-revan-malak", "revan and malak", "REVAN AND MALAK\ncontinuity = legends\nroles = jedi war heroes turned sith lords; memory manipulation and redemption/tyranny arcs\nrpg use = identity, brainwashing, old republic politics, sith fleet remnants; avoid canonizing in canon-only play", ["darth revan", "revan", "darth malak"]),
        entry("kyber-legends-sith-triumvirate", "sith triumvirate", "SITH TRIUMVIRATE\ncontinuity = legends\nmembers = darth traya, darth nihilus, darth sion\ntraits = wound in force, hunger, pain, betrayal, anti-force philosophy\nrpg use = metaphysical horror and trauma, not normal dark jedi villains", ["sith triumvirate", "darth traya", "darth nihilus", "darth sion"]),
        entry("kyber-legends-vitiate", "vitiate and eternal empire", "VITIATE AND ETERNAL EMPIRE\ncontinuity = legends\naliases = tenebrae, valkorion\ntraits = immortal sith emperor archetype, ritual consumption, zakuul, eternal fleet\nrpg use = extreme old republic threat; use sparingly because scale overwhelms street-level play", ["vitiate", "tenebrae", "valkorion", "eternal empire", "zakuul"]),
        entry("kyber-legends-darth-bane", "darth bane legends", "DARTH BANE - LEGENDS\ncontinuity = legends; canon has rule of two existence but details differ\nrole = sith reformer after new sith wars\nlegacy = rule of two, apprentice zannah, secrecy over armies\nrpg use = distinguish canon rule from legends biography", ["darth bane legends", "bane trilogy", "darth zannah"]),
        entry("kyber-legends-abeloth", "abeloth", "ABELOTH\ncontinuity = legends\nrole = beyond-mortal force entity tied to mortis-adjacent legends mythology\ntraits = chaos, possession, impossible identity, galactic-scale threat\nrpg use = cosmic horror only; do not use as casual antagonist or canon fact", ["abeloth"]),
        entry("kyber-legends-hapes", "hapes consortium", "HAPES CONSORTIUM\ncontinuity = legends\nregion = hapes cluster\ntraits = matriarchal monarchy, isolation, court intrigue, powerful fleet, dynastic danger\nrpg use = diplomacy, assassination, noble marriage politics, restricted foreign access", ["hapes", "hapan", "hapes consortium", "tenel ka"]),
        entry("kyber-legends-corporate-sector", "corporate sector authority legends", "CORPORATE SECTOR AUTHORITY - LEGENDS\ncontinuity = legends\nrole = corporate-run region with exploitive law, security police, profit sovereignty\nrpg use = corporate dystopia, debt labor, private prisons, deniable imperial commerce", ["corporate sector authority", "espos", "corporate sector"]),
        entry("kyber-legends-yevetha", "yevetha and black fleet crisis", "YEVETHA AND BLACK FLEET CRISIS\ncontinuity = legends\ntraits = xenophobic militarist species/state, captured imperial ships, post-endor crisis\nrpg use = brutal regional war, ethnic cleansing themes, new republic intervention politics", ["yevetha", "black fleet crisis", "duskhan league"]),
        entry("kyber-legends-warlord-zsinj", "warlord zsinj", "WARLORD ZSINJ\ncontinuity = legends\nrole = post-endor imperial warlord with major fleet and intelligence apparatus\nrpg use = warlord politics, false flags, mercenary work, new republic task forces", ["warlord zsinj", "zsinj"]),
        entry("kyber-legends-thrawn-campaign", "thrawn campaign legends", "THRAWN CAMPAIGN - LEGENDS\ncontinuity = legends\ncontext = heir to the empire era, different from canon thrawn return\ntraits = katana fleet, ysalamiri tactics, clone pressure, mara jade linkage\nrpg use = label clearly; do not merge with canon ahsoka-era thrawn", ["thrawn campaign legends", "heir to the empire", "katana fleet"]),
        entry("kyber-legends-mara-jade", "mara jade", "MARA JADE\ncontinuity = legends\nroles = emperor's hand, smuggler, later jedi and partner to luke in legends\ntraits = lethal, suspicious, disciplined, independent, not easily impressed\nrpg use = high-value legends NPC; do not insert into canon unless mixed-continuity game requested", ["mara jade", "emperor's hand"]),
        entry("kyber-legends-njo", "new jedi order legends", "NEW JEDI ORDER - LEGENDS\ncontinuity = legends\nrole = luke's rebuilt jedi institution after endor\ntraits = looser doctrine, family lines, war trauma, political suspicion\nrpg use = supports legends post-endor games; do not replace canon luke's academy fate", ["new jedi order legends", "luke jedi order legends"]),
        entry("kyber-legends-zonama-sekot", "zonama sekot", "ZONAMA SEKOT\ncontinuity = legends\nrole = living planet tied to yuuzhan vong origins/resolution\ntraits = bioships, consciousness, moral diplomacy, alien ecology\nrpg use = high-mystery endpoint for vong-era campaigns, not ordinary travel stop", ["zonama sekot"]),
        entry("kyber-legends-fel-empire", "fel empire", "FEL EMPIRE\ncontinuity = legends legacy era\nrole = imperial successor state with fel dynasty and imperial knights\ntraits = order, monarchy, gray morality, anti-sith imperial identity\nrpg use = post-njo/legacy politics; not same as palpatine's empire", ["fel empire", "roan fel", "fel dynasty"]),
        entry("kyber-legends-darth-krayt", "darth krayt and one sith", "DARTH KRAYT AND ONE SITH\ncontinuity = legends legacy era\nrole = a'sharad hett reborn as sith ruler; one sith replaces rule of two with collective obedience\nrpg use = distinguish from canon sith eternal and rule-of-two sith", ["darth krayt", "a'sharad hett", "one sith"]),
        entry("kyber-legends-dark-empire", "dark empire palpatine", "DARK EMPIRE PALPATINE\ncontinuity = legends\nrole = cloned palpatine return, byss, world devastators, eclipse dreadnought\nrpg use = legends-only resurrection branch; do not merge with canon exegol without explicit mixed-continuity premise", ["dark empire", "byss", "world devastators", "eclipse dreadnought"]),
        entry("kyber-legends-dathomir-witches", "witches of dathomir legends", "WITCHES OF DATHOMIR - LEGENDS\ncontinuity = legends\nrole = force-using clans beyond canon nightsister framing\ntraits = rancor riding, clan spells, diverse light/dark traditions\nrpg use = distinguish canon nightsisters from broader legends dathomiri force cultures", ["witches of dathomir legends", "singing mountain clan"]),
        entry("kyber-legends-jensaarai", "jensaarai", "JENSAARAI\ncontinuity = legends\nrole = hidden force tradition blending jedi and sith misunderstandings\ntraits = armor, secrecy, defenders, nonstandard doctrine\nrpg use = force sect contact; not automatically dark side despite sith-derived elements", ["jensaarai"]),
    ],
    "Kyber RPG 08 - Technology Ships Gear.json": [
        entry("kyber-tech-yvh-droid", "yvh battle droids", "YVH BATTLE DROIDS\ncontinuity = legends\nrole = yuuzhan-vong-hunter droids developed for vong war\ntraits = anti-vong tactics, aggressive combat programming, specialized sensors\nrpg use = legends war asset; can create postwar danger if autonomous or repurposed", ["yvh droid", "yvh battle droid"]),
        entry("kyber-tech-world-devastator", "world devastators", "WORLD DEVASTATORS\ncontinuity = legends\nrole = dark empire superweapons that consume matter and manufacture war machines\nrpg use = planetary-scale industrial horror; not canon unless mixed/legends game", ["world devastator", "world devastators"]),
        entry("kyber-tech-eclipse-dreadnought", "eclipse-class dreadnought", "ECLIPSE-CLASS DREADNOUGHT\ncontinuity = legends\nrole = palpatine dark empire flagship class with superlaser-scale terror symbolism\nrpg use = campaign-scale threat; ordinary PCs survive by infiltration, sabotage, intelligence, not fair combat", ["eclipse-class", "eclipse dreadnought"]),
        entry("kyber-tech-interdictor", "interdictor cruisers", "INTERDICTOR CRUISERS\ncontinuity = canon/legends\nfunction = gravity-well projection prevents hyperspace escape or pulls ships from hyperspace\nrpg use = makes retreats fail, traps smugglers, creates blockade pressure; destroying generators may open escape", ["interdictor cruiser", "gravity well projector", "interdiction field"]),
        entry("kyber-tech-cloaking-device", "cloaking devices", "CLOAKING DEVICES\ncontinuity = canon/legends rare\nlimits = expensive, power-hungry, often sensor/communication tradeoffs\nrpg use = stealth ship plots should still involve emissions, wakes, patrol patterns, and blind spots", ["cloaking device", "stygium cloak", "hibridium cloak"]),
        entry("kyber-tech-basilisk-war-droid", "basilisk war droids", "BASILISK WAR DROIDS\ncontinuity = legends; canon visual/concept may vary\nrole = mandalorian rider war machines in old republic legends\nrpg use = terror cavalry, relic mount, clan prestige; not normal astromech-style droid", ["basilisk war droid", "basilisk droid"]),
        entry("kyber-tech-kolto", "kolto", "KOLTO\ncontinuity = legends primary\nrole = pre-bacta healing substance, especially manaan old republic economy\nrpg use = medical scarcity, neutrality politics, contaminated supply, underwater trade routes", ["kolto"]),
        entry("kyber-tech-bacta-scarcity", "bacta scarcity", "BACTA SCARCITY\ncontinuity = canon/legends\nconstraint = healing tanks and refined bacta are valuable, regulated, and logistics-dependent\nrpg use = severe injury should create debt, delay, triage, black-market risk, or faction bargaining", ["bacta scarcity", "bacta shortage", "bacta black market"]),
        entry("kyber-tech-slicer-ice", "slicer ice and countermeasures", "SLICER ICE AND COUNTERMEASURES\ncontinuity = setting operational\nconcept = intrusion countermeasures, trace routines, lockouts, alert daemons, physical access limits\nrpg use = slicing failures should trigger alarms, tracebacks, false data, burned credentials, or security dispatch", ["slicer ice", "intrusion countermeasures", "trace routine"]),
        entry("kyber-tech-restraints", "restraint technologies", "RESTRAINT TECHNOLOGIES\ncontinuity = canon/legends\nexamples = binders, stun cuffs, mag cuffs, shock collars, restraining bolts for droids\nrpg use = capture can be playable; restraints limit options but do not require PC thought control", ["binders", "mag cuffs", "shock collar", "restraining tech"]),
        entry("kyber-tech-tracking-devices", "tracking devices", "TRACKING DEVICES\ncontinuity = canon/legends\nforms = homing beacon, tracker fob, transponder tag, probe relay, slicing marker\nrpg use = pursuit should follow evidence, range, signal quality, interference, and counter-surveillance", ["tracking device", "homing beacon", "transponder tag"]),
        entry("kyber-tech-medical-droids-extra", "specialist medical droids", "SPECIALIST MEDICAL DROIDS\ncontinuity = canon/legends\nroles = surgical, diagnostic, midwife, cybernetic, battlefield triage, interrogation-adjacent abuse\nrpg use = medical care quality depends on model, supplies, ethics, owner orders, and memory wipe status", ["specialist medical droid", "diagnostic droid", "surgical droid"]),
    ],
    "Kyber RPG 04 - Factions and Governments.json": [
        entry("kyber-faction-corporate-sector", "corporate sector authority", "CORPORATE SECTOR AUTHORITY\ncontinuity = legends primary\nrole = corporate state with private security and profit-first law\nmethods = contracts, debt, imprisonment, labor exploitation, trade leverage\nrpg use = good setting for corporate dystopia and legal traps; canon-only games require import", ["corporate sector authority", "corporate sector", "espos"]),
        entry("kyber-faction-hapes", "hapes consortium", "HAPES CONSORTIUM\ncontinuity = legends\nrole = isolated matriarchal monarchy in hapes cluster\nmethods = court intrigue, fleet deterrence, noble assassination, restricted diplomacy\nrpg use = social danger and political marriages; outsiders lack context and legal protection", ["hapes consortium", "hapan court", "hapes cluster"]),
        entry("kyber-faction-chiss-ascendancy", "chiss ascendancy", "CHISS ASCENDANCY\ncontinuity = canon/legends with differences\nrole = unknown regions power governed by aristocra families and military doctrine\nmethods = secrecy, border control, merit, political exile, sky-walker navigators in canon\nrpg use = disciplined non-imperial state; do not make all chiss thrawn clones", ["chiss ascendancy", "csilla", "chiss families"]),
        entry("kyber-faction-imperial-security-bureau", "isb operational culture", "ISB OPERATIONAL CULTURE\ncontinuity = canon\nrole = imperial internal security and counterinsurgency bureaucracy\nmethods = surveillance, informants, sector files, interdepartmental rivalry, disappearances\nrpg use = arrests should create paperwork, interrogation, leverage, and network risk, not only gunfights", ["isb operations", "imperial security bureau culture", "isb surveillance"]),
        entry("kyber-faction-sector-rangers", "sector rangers", "SECTOR RANGERS\ncontinuity = canon/legends\nrole = law enforcement operating across remote sectors where local law is thin\nmethods = warrants, pursuit, informants, local cooperation, limited resources\nrpg use = frontier law can be persistent and competent without imperial scale", ["sector rangers", "sector ranger"]),
        entry("kyber-faction-bounty-guild-politics", "bounty guild politics", "BOUNTY GUILD POLITICS\ncontinuity = canon/legends\nrole = contracts, reputation, posting rights, guild protection, rival hunters\nrpg use = bounties create legal/criminal ambiguity; killing a target may reduce pay or anger sponsor", ["bounty guild politics", "bounty contract", "guild posting"]),
        entry("kyber-faction-crimson-dawn-cells", "crimson dawn cells", "CRIMSON DAWN CELLS\ncontinuity = canon\nrole = syndicate network built through fronts, blackmail, artifacts, and elite criminal patronage\nrpg use = local cell may not know full leadership; betrayal and leverage matter more than open war", ["crimson dawn cell", "crimson dawn cells"]),
        entry("kyber-faction-pyke-logistics", "pyke syndicate logistics", "PYKE SYNDICATE LOGISTICS\ncontinuity = canon\nrole = spice transport, protection rackets, mining exploitation, cartel bargaining\nrpg use = spice jobs involve routes, bribes, loaders, pilots, local addicts, and violent debt collection", ["pyke logistics", "pyke spice route"]),
        entry("kyber-faction-hutt-clan-law", "hutt clan law", "HUTT CLAN LAW\ncontinuity = canon/legends\nrole = kajidic power, debt custom, slave markets, cartel courts, patronage\nrpg use = hutt deals bind families, crews, ships, and future favors; insult costs are often public", ["hutt clan law", "kajidic law", "hutt debt"]),
        entry("kyber-faction-mandalorian-clans", "mandalorian clan politics", "MANDALORIAN CLAN POLITICS\ncontinuity = canon/legends varies\nrole = clans, houses, foundlings, armor legitimacy, old grudges\nrpg use = armor, oaths, rescue, betrayal, and lineage create consequences beyond ordinary payment", ["mandalorian clan politics", "mandalorian houses", "mandalorian foundlings"]),
    ],
    "Kyber RPG 05 - Worlds and Regions.json": [
        entry("kyber-world-manaan", "manaan", "MANAAN\ncontinuity = legends primary\nrole = ocean world, selkath home, kolto source in old republic\nlaw = neutrality and strict export politics\nrpg use = underwater access, medical trade, diplomatic danger, ancient ruins", ["manaan", "ahto city"]),
        entry("kyber-world-myrkr", "myrkr", "MYRKR\ncontinuity = legends primary\nfeatures = vornskr predators and ysalamiri force-neutral bubbles\nrpg use = anti-force wilderness, smuggler refuge, thrawn-era tactics; canon import required", ["myrkr"]),
        entry("kyber-world-honoghr", "honoghr", "HONOGHR\ncontinuity = legends primary\nrole = noghri homeworld devastated/ecologically manipulated by empire\nrpg use = clan debt, imperial deception, poisoned land, lethal commando culture", ["honoghr"]),
        entry("kyber-world-bilbringi", "bilbringi", "BILBRINGI\ncontinuity = legends prominent; canon check per use\nrole = shipyards and major thrawn campaign battle site in legends\nrpg use = military shipyard infiltration, fleet politics, salvage, imperial remnant security", ["bilbringi", "bilbringi shipyards"]),
        entry("kyber-world-borleias", "borleias", "BORLEIAS\ncontinuity = legends prominent\nrole = strategic world near core routes, rebel/new republic staging in legends\nrpg use = contested base, siege logistics, starfighter operations, medical evacuation", ["borleias"]),
        entry("kyber-world-dromund-kaas", "dromund kaas", "DROMUND KAAS\ncontinuity = legends primary\nrole = sith imperial capital in old republic legends\nfeatures = jungle, storms, dark-side temples, imperial bureaucracy\nrpg use = oppressive sith politics and hostile archaeology", ["dromund kaas"]),
        entry("kyber-world-korriban-moraband", "korriban moraband distinction", "KORRIBAN / MORABAND DISTINCTION\ncontinuity = moraband canon name; korriban common legends/older name\nrole = ancient sith tomb world\nrpg use = label by continuity; tombs contain ideology, traps, spirits, and rival seekers, not simple loot rooms", ["korriban", "moraband", "sith tomb world"]),
        entry("kyber-world-ziost", "ziost", "ZIOST\ncontinuity = legends primary\nrole = ancient sith world and imperial center in old republic legends\nrpg use = dead cities, imperial archives, dark-side devastation, sith history", ["ziost"]),
        entry("kyber-world-ord-mantell", "ord mantell", "ORD MANTELL\ncontinuity = canon/legends\nrole = scrapyards, mercenaries, smugglers, separatist/new republic/postwar conflict in different eras\nrpg use = dirty jobs, old military salvage, bounty trouble, unreliable authorities", ["ord mantell"]),
        entry("kyber-world-nar-shaddaa-depth", "nar shaddaa lower levels", "NAR SHADDAA LOWER LEVELS\ncontinuity = canon/legends\nfeatures = vertical poverty, cartel zones, failing utilities, undocumented tunnels, bought police\nrpg use = every shortcut has owner, toll, gang, camera, or debt; no clean anonymity", ["nar shaddaa lower levels", "vertical city moon", "smuggler's moon depths"]),
        entry("kyber-world-telos", "telos iv legends", "TELOS IV\ncontinuity = legends primary\nrole = devastated/restored world tied to old republic and kotor-era history\nrpg use = restoration politics, old war scars, hidden facilities, exiles returning to broken homes", ["telos iv", "telos"]),
        entry("kyber-world-ossus", "ossus", "OSSUS\ncontinuity = canon/legends\nrole = ancient jedi world, library ruins, later jedi refuge in multiple continuities\nrpg use = archaeology, refugee enclave, knowledge recovery, sith/imperial raids", ["ossus"]),
    ],
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync(entry_obj):
    keys = []
    for key in entry_obj.get("key", []):
        if key and key not in keys:
            keys.append(key)
    entry_obj["key"] = keys
    entry_obj["keysRaw"] = ", ".join(keys)
    entry_obj["keywordsRaw"] = entry_obj["keysRaw"]


def make_entry(template, item, order, category):
    keys = item["key"]
    new_entry = dict(template)
    new_entry.update(
        {
            "activationMode": "standard",
            "activationScript": "",
            "case_sensitive": False,
            "category": category,
            "comment": f"lore expansion batch 01; source layer: {item['source']}",
            "constant": False,
            "content": item["content"],
            "enabled": True,
            "extensions": {},
            "groupWeight": 100,
            "id": item["id"],
            "inclusionGroupRaw": "",
            "insertion_order": order,
            "key": keys,
            "keyMatchPriority": True,
            "keysecondary": [],
            "keysecondaryRaw": "",
            "matchWholeWords": True,
            "minMessages": 0,
            "name": item["name"],
            "prioritizeInclusion": False,
            "priority": item["priority"],
            "probability": 100,
            "selectiveLogic": 0,
            "tags": ["star_wars", "expansion_batch_01"] + item["tags"],
        }
    )
    sync(new_entry)
    return new_entry


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    changes = []

    for filename, items in EXPANSION.items():
        path = ROOT / filename
        shutil.copy2(path, BACKUP / filename)
        data = load(path)
        names = {entry.get("name", "").lower() for entry in data}
        ids = {entry.get("id") for entry in data}
        category = data[0].get("category", "") if data else ""
        order = max((entry.get("insertion_order", 0) for entry in data), default=0)
        template = data[0]
        added = 0
        skipped = 0
        for item in items:
            if item["name"].lower() in names or item["id"] in ids:
                skipped += 1
                continue
            order += 100
            data.append(make_entry(template, item, order, category))
            names.add(item["name"].lower())
            ids.add(item["id"])
            added += 1
            changes.append(
                {
                    "file": filename,
                    "name": item["name"],
                    "id": item["id"],
                    "keys": item["key"],
                    "source_layer": item["source"],
                }
            )
        data.sort(key=lambda entry_obj: entry_obj.get("insertion_order", 0))
        save(path, data)
        print(f"{filename}: added {added}, skipped {skipped}")

    sources_path = REPORTS / "expansion_batch_01_sources.json"
    sources_path.write_text(json.dumps({"generated": date.today().isoformat(), "base_sources": BASE_SOURCES, "changes": changes}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Lore Expansion Batch 01", "", f"Generated: {date.today().isoformat()}", "", "## Base Sources", ""]
    for label, url in BASE_SOURCES.items():
        md.append(f"- {label}: {url}")
    md.append("")
    md.append("## Added Entries")
    md.append("")
    for change in changes:
        md.append(f"- {change['file']} :: {change['name']} [{', '.join(change['keys'])}]")
    (REPORTS / "expansion_changelog.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Backed up touched files to {BACKUP}")
    print(f"Added {len(changes)} total entries")


if __name__ == "__main__":
    main()
