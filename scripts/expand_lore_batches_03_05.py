import json
import shutil
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
BACKUP = ROOT / "archive" / f"lore-expansion-batches-03-05-{date.today().isoformat()}"

SOURCES = {
    "official_databank": "https://www.starwars.com/databank/",
    "official_news": "https://www.starwars.com/news",
    "wookieepedia": "https://starwars.fandom.com/",
}

FILES = {
    "species": "Kyber RPG 06 - Species and Cultures.json",
    "hazards": "Kyber RPG 09 - Creatures and Hazards.json",
    "society": "Kyber RPG 07 - Society Law Economy.json",
    "force": "Kyber RPG 13 - Force Metaphysics Artifacts.json",
    "legends": "Kyber RPG 14 - Legends Supplements.json",
    "factions": "Kyber RPG 04 - Factions and Governments.json",
    "powers": "Kyber RPG 10 - Force Powers.json",
    "orders": "Kyber RPG 11 - Force Orders.json",
    "sabers": "Kyber RPG 12 - Lightsabers and Kyber.json",
    "worlds": "Kyber RPG 05 - Worlds and Regions.json",
    "tech": "Kyber RPG 08 - Technology Ships Gear.json",
    "characters": "Kyber RPG 03 - Characters.json",
}


def rec(batch, book, slug, name, continuity, role, use, keys, priority=1):
    return {
        "batch": batch,
        "book": book,
        "id": f"kyber-batch{batch:02d}-{slug}",
        "name": name,
        "continuity": continuity,
        "role": role,
        "use": use,
        "keys": keys,
        "priority": priority,
    }


ENTRIES = [
    # Batch 03: practical RPG pressure, hazards, society, factions.
    rec(3, "hazards", "hazard-airlock-failure", "airlock failures", "setting baseline", "seal, pump, pressure, and timing failures in stations or ships", "Use as timed danger with decompression, alarms, stuck doors, and rescue tradeoffs.", ["airlock failure", "airlock malfunction"]),
    rec(3, "hazards", "hazard-atmosphere-mismatch", "atmosphere mismatch", "setting baseline", "wrong gas mix, pressure, humidity, or toxin load for a species", "Use to make alien biology and cheap habitats matter without instant death.", ["atmosphere mismatch", "wrong atmosphere"]),
    rec(3, "hazards", "hazard-blood-trail", "forensic blood trails", "setting baseline", "blood, coolant, oil, fabric, and footprints used as pursuit evidence", "Use to ground investigation; cleaning takes time and can still leave chemical traces.", ["forensic blood trail", "blood trace"]),
    rec(3, "hazards", "hazard-cave-in", "cave-ins and structural collapse", "canon/legends", "falling stone, ferrocrete, mine supports, and blast-weakened walls", "Use blocked exits, trapped allies, dust, noise, and oxygen loss as consequences.", ["cave-in", "structural collapse"]),
    rec(3, "hazards", "hazard-contaminated-water", "contaminated water", "setting baseline", "industrial runoff, corpse rot, parasites, spice residue, or fuel in water supplies", "Use dehydration choices, infection, local anger, and evidence of sabotage.", ["contaminated water", "tainted water"]),
    rec(3, "hazards", "hazard-cryo-leak", "cryogenic leaks", "setting baseline", "cold gas, brittle metal, flash frost, and impaired visibility from damaged systems", "Use strain, frostbite, slick floors, and fragile seals.", ["cryogenic leak", "flash frost"]),
    rec(3, "hazards", "hazard-crowd-crush", "crowd crush", "setting baseline", "panic, festival surge, evacuation bottleneck, or checkpoint stampede", "Use civilian stakes; combat in crowds should cause injuries and political consequences.", ["crowd crush", "stampede crowd"]),
    rec(3, "hazards", "hazard-data-trap", "malware traps", "setting baseline", "slicer bait, false credentials, beacon files, and hostile datacards", "Use failed slicing to burn aliases, transmit location, or corrupt gear.", ["malware trap", "hostile datacard"]),
    rec(3, "hazards", "hazard-decompression-sickness", "decompression sickness", "setting baseline", "injury from pressure change, bad dives, damaged suits, or rushed airlock cycles", "Use delayed pain, confusion, joint damage, and need for medical care.", ["decompression sickness", "pressure injury"]),
    rec(3, "hazards", "hazard-droid-plague", "droid logic plagues", "canon/legends", "malware or behavioral corruption spreading through droid networks", "Use for sabotage, quarantine, memory loss, and trust problems with companion droids.", ["droid logic plague", "droid virus"]),
    rec(3, "hazards", "hazard-falling-city", "vertical city fall hazards", "setting baseline", "catwalks, airlanes, gantries, lift shafts, and bottomless urban levels", "Use height honestly; failed checks can separate, injure, expose, or force rescue.", ["vertical city fall", "lift shaft fall"]),
    rec(3, "hazards", "hazard-fire-suppression", "fire suppression failure", "setting baseline", "dead foam systems, vacuum purge, sealed bulkheads, or toxic extinguisher gas", "Use as ship/station crisis with hard choices between rooms and people.", ["fire suppression failure", "toxic extinguisher gas"]),
    rec(3, "hazards", "hazard-heatstroke", "heatstroke and dehydration", "canon/legends", "desert, engine room, volcanic, or armor-trapped heat stress", "Use escalating strain, hallucination, slowed travel, and water ration pressure.", ["heatstroke", "dehydration"]),
    rec(3, "hazards", "hazard-hypothermia", "hypothermia", "canon/legends", "cold-world exposure, wet clothing, failed suit heat, or night desert chill", "Use confusion, slow hands, bad decisions, and urgent shelter needs.", ["hypothermia", "cold exposure"]),
    rec(3, "hazards", "hazard-magnetic-crane", "industrial crane hazards", "setting baseline", "magnetic lifts, cargo hooks, loader arms, and suspended crates", "Use workplace machinery as cover, weapon, obstacle, or evidence-destroyer.", ["industrial crane", "magnetic cargo lift"]),
    rec(3, "hazards", "hazard-minefield", "minefields and old ordnance", "canon/legends", "buried mines, unexploded shells, sensor mines, and warning markers", "Use slow movement, local guides, and ugly civilian injuries.", ["minefield", "unexploded ordnance"]),
    rec(3, "hazards", "hazard-navigation-blackout", "navigation blackout", "setting baseline", "sensor loss from jamming, nebulae, storms, terrain, or bad charts", "Use to force astrogation, piloting, and scout choices with real cost.", ["navigation blackout", "sensor blackout"]),
    rec(3, "hazards", "hazard-plague-ship", "plague ships", "canon/legends", "quarantined vessels with disease, panic, bad air, and sealed compartments", "Use medical triage and contamination rather than simple zombie action.", ["plague ship", "quarantine ship"]),
    rec(3, "hazards", "hazard-reactor-scram", "reactor scram emergencies", "setting baseline", "emergency reactor shutdown causing darkness, cold, locked systems, or backup failure", "Use as cascading station/ship crisis with time pressure.", ["reactor scram", "reactor shutdown"]),
    rec(3, "hazards", "hazard-riot-control", "riot control weapons", "canon/legends", "sonic cannons, stun gas, shields, batons, droids, and crowd traps", "Use as state violence with civilian risk, arrests, and propaganda footage.", ["riot control weapons", "stun gas"]),
    rec(3, "hazards", "hazard-sensor-ghost", "sensor ghosts", "setting baseline", "false contacts from jamming, debris, storms, stealth, or damaged arrays", "Use uncertainty; not every contact is real, and not every ghost is harmless.", ["sensor ghost", "false sensor contact"]),
    rec(3, "hazards", "hazard-slave-collar", "explosive slave collars", "canon/legends", "coercive restraints with trackers, shock, explosives, or remote codes", "Use rescue, disarm, and trauma stakes; never trivialize captive agency.", ["explosive collar", "slave collar"]),
    rec(3, "hazards", "hazard-space-debris", "orbital debris fields", "canon/legends", "wreckage, mines, frozen bodies, cargo, and metallic clouds after battles", "Use piloting danger, salvage clues, and hidden pursuers.", ["orbital debris field", "space debris"]),
    rec(3, "hazards", "hazard-tibanna-leak", "tibanna gas leaks", "canon/legends", "volatile or valuable gas leaks in mines, refineries, and weapon systems", "Use explosion risk, suffocation, intoxication, and corporate coverups.", ["tibanna leak", "tibanna gas"]),
    rec(3, "hazards", "hazard-trapdoor-hab", "hab-stack trapdoors", "setting baseline", "rigged floors, lift hatches, laundry chutes, and maintenance drops", "Use undercity ambushes that separate characters without fiat.", ["hab-stack trapdoor", "maintenance drop"]),
    rec(3, "hazards", "hazard-war-trauma", "war-zone trauma triggers", "setting baseline", "shelling, alarms, burning plastic, clone voices, or droid marching cadence", "Use strain, fear checks, and NPC behavior without stealing player control.", ["war trauma trigger", "combat trauma"]),
    rec(3, "hazards", "creature-bogwing", "bogwings", "canon/legends", "winged swamp creatures seen in Naboo and wetland ecologies", "Use as noise, omen, prey, or swarm nuisance before a larger predator.", ["bogwing", "bogwings"]),
    rec(3, "hazards", "creature-bursa", "bursas", "legends primary", "dangerous Naboo plains predators in older game material", "Use as local wildlife threat for rural Naboo or Legends-compatible hunts.", ["bursa", "bursas"]),
    rec(3, "hazards", "creature-maalraas", "maalraas", "legends primary", "stealth predators associated with Korriban and dark places", "Use as tomb stalkers that punish noise and separation.", ["maalraas"]),
    rec(3, "hazards", "creature-massiff", "massiffs", "canon/legends", "reptilian tracking animals used by Tuskens, clones, and handlers", "Use scent pursuit, camp warnings, and handler relationships.", ["massiff", "massiffs"]),
    rec(3, "hazards", "creature-murra", "murra", "legends primary", "large beasts used in frontier and hunting lore", "Use as dangerous non-sentient wilderness pressure, not evil monsters.", ["murra beast", "murra"]),
    rec(3, "hazards", "creature-nerf", "nerfs", "canon/legends", "livestock animals tied to insults, ranching, meat, and rural economies", "Use for ranch work, herd theft, disease, and frontier flavor.", ["nerf", "nerfs", "nerf herd"]),
    rec(3, "hazards", "creature-orbalisk", "orbalisks", "legends primary", "parasitic armored creatures linked to Darth Bane stories", "Use as Sith-body-horror parasite; label Legends and keep rare.", ["orbalisk", "orbalisks"]),
    rec(3, "hazards", "creature-scurrier", "scurriers", "canon/legends", "small scavengers common in Tatooine settlements", "Use as environmental motion, disease vector, or clue to bodies/food.", ["scurrier", "scurriers"]),
    rec(3, "hazards", "creature-storm-beast", "storm beasts", "legends primary", "large predators from old game/Legends contexts", "Use as ruin or bad-weather apex threat in compatible continuity.", ["storm beast", "storm beasts"]),
    rec(3, "hazards", "creature-strill", "strills", "legends primary", "Mandalorian hunting animals with loyalty and strong scent tracking", "Use for clan culture, bounty pursuit, and ugly-cute predator tension.", ["strill", "strills"]),
    rec(3, "hazards", "creature-tukata", "tuk'ata", "legends primary", "Sith hounds tied to Korriban tombs and dark-side sites", "Use as old Sith guardian beasts; label Legends or mixed continuity.", ["tuk'ata", "sith hound"]),
    rec(3, "hazards", "creature-varactyl", "varactyls", "canon/legends", "climbing lizard mounts such as Boga on Utapau", "Use vertical chase movement, mount trust, and noisy claws on stone.", ["varactyl", "varactyls"]),
    rec(3, "hazards", "creature-voxyn", "voxyn", "legends primary", "Yuuzhan Vong engineered Jedi-hunting beasts", "Use as NJO horror weapon; force-users should fear them for scent, venom, and design.", ["voxyn"]),
    rec(3, "hazards", "creature-ysalamiri-counter", "ysalamiri handling hazards", "legends primary", "transporting force-neutral creatures requires ecology, nutrient frames, and care", "Use to keep anti-Force tactics logistically hard and morally suspect.", ["ysalamiri handling", "ysalamiri nutrient frame"]),
    rec(3, "society", "society-arms-licensing", "arms licensing", "canon/legends", "legal weapon ownership varies by world, regime, class, and occupation status", "Use permits, inspections, confiscation, and black-market markups.", ["arms license", "weapon permit"]),
    rec(3, "society", "society-birth-records", "birth records and missing persons", "setting baseline", "identity files can be altered, lost, sealed, or weaponized", "Use missing-person investigations through clerks, clinics, schools, and corrupt archives.", ["birth record", "missing person file"]),
    rec(3, "society", "society-cargo-manifest", "cargo manifests", "canon/legends", "shipping documents list declared mass, hazard codes, origin, owner, and inspection history", "Use mismatches as clues and legal exposure.", ["cargo manifest", "shipping manifest"]),
    rec(3, "society", "society-caste-law", "caste and status law", "canon/legends", "some worlds encode birth, species, clan, or job into legal status", "Use unfair procedure, not generic prejudice; law can be the weapon.", ["caste law", "status law"]),
    rec(3, "society", "society-child-labor", "child labor and street crews", "canon/legends", "poverty and criminal systems use children as lookouts, thieves, couriers, and bait", "Use grim stakes with care; rescue causes retaliation and resource problems.", ["street crew child", "child courier"]),
    rec(3, "society", "society-clone-veterans", "clone veteran status", "canon/legends", "surviving clones face aging, erased rights, trauma, and changing regimes", "Use as social wound and living evidence of Republic/Imperial betrayal.", ["clone veteran", "aging clone"]),
    rec(3, "society", "society-corporate-arbitration", "corporate arbitration", "setting baseline", "contracts can force disputes into company courts or bought mediators", "Use legal traps where winning morally does not mean winning procedurally.", ["corporate arbitration", "company court"]),
    rec(3, "society", "society-customs-droid-search", "customs droid searches", "canon/legends", "ports inspect droid memory, hidden compartments, restraining bolts, and toolkits", "Use to make droids vulnerable to seizure and evidence extraction.", ["droid customs search", "droid inspection"]),
    rec(3, "society", "society-docking-queue", "docking queue corruption", "setting baseline", "landing order can be bought, delayed, denied, or manipulated", "Use time pressure and bribes at starports.", ["docking queue", "landing queue"]),
    rec(3, "society", "society-evidence-chain", "chain of custody", "setting baseline", "evidence passes through collectors, lockers, clerks, and courts", "Use theft, contamination, planted evidence, and procedural weakness.", ["chain of custody", "evidence locker"]),
    rec(3, "society", "society-family-debt", "family debt leverage", "canon/legends", "criminals and corporations pressure relatives, partners, crews, and sponsors", "Use consequences that follow the character without forcing action.", ["family debt", "relative leverage"]),
    rec(3, "society", "society-food-scarcity", "food scarcity", "canon/legends", "blockade, war, climate, or cartel control turns food into power", "Use ration lines, theft, spoilage, and unrest.", ["food scarcity", "ration line"]),
    rec(3, "society", "society-forced-informant", "forced informants", "canon/legends", "authorities or gangs compel cooperation through charges, debt, family, or addiction", "Use betrayal with understandable motives and future risk.", ["forced informant", "coerced informant"]),
    rec(3, "society", "society-forged-medical", "forged medical records", "setting baseline", "fake injuries, species needs, quarantine papers, and prescriptions bypass checks", "Use as fragile cover that fails under expert review.", ["forged medical record", "fake quarantine papers"]),
    rec(3, "society", "society-freight-brokers", "freight brokers", "setting baseline", "middlemen assign cargo jobs, hide owners, skim fees, and sell crew data", "Use as underworld-adjacent job funnels with hidden liabilities.", ["freight broker", "cargo broker"]),
    rec(3, "society", "society-guild-blacklist", "guild blacklists", "canon/legends", "guilds can deny docking, contracts, repairs, bounties, or legal support", "Use reputation consequences that hurt more than one fight.", ["guild blacklist", "blacklisted pilot"]),
    rec(3, "society", "society-hospital-triage", "hospital triage", "setting baseline", "overloaded clinics prioritize by payment, status, survival chance, or politics", "Use medical scarcity and ugly choices after violence.", ["hospital triage", "clinic triage"]),
    rec(3, "society", "society-illegal-cybernetics", "illegal cybernetics", "canon/legends", "unlicensed implants can hide weapons, addiction controls, trackers, or stolen parts", "Use body autonomy, debt medicine, and maintenance complications.", ["illegal cybernetics", "black market implant"]),
    rec(3, "society", "society-language-barrier", "language barriers", "canon/legends", "Basic is common but not universal; droids, dialects, and local signs matter", "Use misunderstandings, translation delay, and social insult risk.", ["language barrier", "translation problem"]),
    rec(3, "society", "society-loan-shark", "loan sharks", "canon/legends", "private lenders use interest, shame, violence, and legal claims", "Use escalating collections, not one-note threats.", ["loan shark", "predatory loan"]),
    rec(3, "society", "society-media-frame", "media framing", "canon/legends", "events become propaganda, scandal, spectacle, or buried rumor depending ownership", "Use public consequences after messy action.", ["media framing", "news holo scandal"]),
    rec(3, "society", "society-mercenary-contracts", "mercenary contracts", "canon/legends", "jobs specify objective, pay, salvage, prisoners, collateral, and betrayal clauses", "Use contract terms as adventure pressure.", ["mercenary contract", "contract clause"]),
    rec(3, "society", "society-port-quarantine", "port quarantine", "canon/legends", "ships, crews, or cargo may be isolated for disease, pests, sabotage, or politics", "Use delays, bribes, inspections, and desperation.", ["port quarantine", "quarantine hold"]),
    rec(3, "society", "society-private-prisons", "private prisons", "canon/legends", "corporate or criminal detention run for labor, ransom, data, or contracts", "Use captivity as economy and evidence of systemic rot.", ["private prison", "corporate prison"]),
    rec(3, "society", "society-proxy-ownership", "proxy ownership", "setting baseline", "ships, apartments, accounts, and droids can be owned through nominees", "Use hidden sponsors and legal exposure.", ["proxy ownership", "nominee owner"]),
    rec(3, "society", "society-public-execution", "public punishment", "canon/legends", "regimes and gangs stage punishments to teach obedience", "Use witnesses, propaganda, fear, and resistance recruitment.", ["public punishment", "public execution"]),
    rec(3, "society", "society-refugee-documents", "refugee documents", "canon/legends", "displaced people need ration cards, visas, sponsors, and safe routes", "Use paperwork as survival pressure and moral test.", ["refugee document", "ration card"]),
    rec(3, "society", "society-safehouse-rules", "safehouse rules", "setting baseline", "hidden rooms require silence, burner routes, no comms, and compartmentalized contacts", "Use tradecraft discipline and consequences for sloppy habits.", ["safehouse rules", "burner route"]),
    rec(3, "society", "society-scrap-economy", "scrap economy", "canon/legends", "wrecks, droid parts, wire, fuel cells, and ration tins become currency in poor zones", "Use small salvage as meaningful money and evidence.", ["scrap economy", "parts barter"]),
    rec(3, "society", "society-security-clearance", "security clearances", "canon/legends", "access depends on clearance level, station, era, and live database checks", "Use false confidence: a stolen badge may pass doors but fail supervisors.", ["security clearance", "clearance check"]),
    rec(3, "society", "society-ship-mortgage", "ship mortgages", "canon/legends", "ships can be financed through banks, Hutts, brokers, or crew shares", "Use liens, repossession, sabotage insurance, and debt hooks.", ["ship mortgage", "ship lien"]),
    rec(3, "society", "society-slumlord", "slumlords", "setting baseline", "housing power in lower levels comes through locks, water, heat, gangs, and eviction", "Use place-based pressure and neighborhood stakes.", ["slumlord", "hab eviction"]),
    rec(3, "society", "society-smuggling-compartment", "hidden compartments law", "canon/legends", "concealed storage itself can be evidence even when empty", "Use inspections and design tradeoffs in ships and speeders.", ["hidden compartment law", "smuggling compartment"]),
    rec(3, "society", "society-spice-types", "spice variants", "canon/legends", "different spices can be medicinal, recreational, addictive, toxic, or industrial", "Use named cargo type and local law instead of generic contraband.", ["spice variant", "spice type"]),
    rec(3, "society", "society-starvation-wages", "starvation wages", "setting baseline", "low pay, company stores, docking fees, and medical debt trap workers", "Use poverty as system, not scenery.", ["starvation wage", "company store"]),
    rec(3, "society", "society-surveillance-state", "surveillance state habits", "canon/legends", "citizens self-censor under informants, cameras, checkpoints, and random audits", "Use fear in ordinary speech and public spaces.", ["surveillance state", "random audit"]),
    rec(3, "society", "society-torture-records", "interrogation records", "canon/legends", "states and gangs preserve confessions, biometrics, pain logs, and false statements", "Use records as evidence and blackmail; avoid gratuitous detail.", ["interrogation record", "confession file"]),
    rec(3, "society", "society-transit-strike", "transit strikes", "setting baseline", "labor action, sabotage, or curfew can freeze trains, lifts, ferries, and airlanes", "Use travel disruption and public anger.", ["transit strike", "lift shutdown"]),
    rec(3, "factions", "faction-aldorande-security", "Alderaanian security remnants", "canon/legends", "surviving guards, diplomats, and intelligence contacts after Alderaan's destruction", "Use diaspora grief, legitimacy, and covert rebel networks.", ["alderaanian security remnant", "alderaanian diaspora cell"]),
    rec(3, "factions", "faction-askar-cells", "local resistance cells", "canon/legends", "small anti-occupation groups with poor supplies and high infiltration risk", "Use paranoia, scarcity, and civilian exposure.", ["local resistance cell", "occupation resistance"]),
    rec(3, "factions", "faction-banking-clan-courts", "Banking Clan legal departments", "canon/legends", "finance-law machinery behind liens, debts, foreclosures, and war loans", "Use paper violence and financial traps.", ["banking clan legal", "intergalactic banking law"]),
    rec(3, "factions", "faction-caravan-guilds", "caravan guilds", "canon/legends", "overland or hyperspace route associations moving goods through dangerous regions", "Use route tolls, guides, convoy politics, and betrayal.", ["caravan guild", "convoy guild"]),
    rec(3, "factions", "faction-church-force", "Church of the Force communities", "canon", "non-Jedi believers preserving Force faith and Jedi memory", "Use vulnerable communities, relic protection, and quiet courage.", ["church of the force community", "force church cell"]),
    rec(3, "factions", "faction-clone-underground", "clone deserter networks", "canon/legends", "clones hiding, helping brothers, or evading Imperial disposal", "Use aging, guilt, loyalty, and false identities.", ["clone deserter network", "clone underground"]),
    rec(3, "factions", "faction-corporate-arms-cartel", "arms cartels", "canon/legends", "manufacturers, brokers, and smugglers selling weapons to multiple sides", "Use invoices, deniable shipments, and moral corrosion.", ["arms cartel", "weapons broker network"]),
    rec(3, "factions", "faction-droid-liberation", "droid liberation cells", "canon/legends", "radical or peaceful groups resisting memory wipes and ownership", "Use raids, sabotage, safehouses, and philosophical conflict.", ["droid liberation cell", "droid emancipation"]),
    rec(3, "factions", "faction-freighter-unions", "freighter unions", "setting baseline", "pilot and cargo-worker organizations fighting rates, tolls, and unsafe ports", "Use strikes, blacklists, and convoy solidarity.", ["freighter union", "cargo pilot union"]),
    rec(3, "factions", "faction-hutt-enforcers", "Hutt enforcer cadres", "canon/legends", "mixed-species crews enforcing kajidic debt and public fear", "Use intimidation with contracts, witnesses, and family pressure.", ["hutt enforcer cadre", "kajidic enforcers"]),
    rec(3, "factions", "faction-imperial-medical-corps", "Imperial medical corps", "canon/legends", "military medicine split between triage, cybernetics, interrogation support, and logistics", "Use competence inside a cruel system.", ["imperial medical corps", "imperial triage"]),
    rec(3, "factions", "faction-jawa-clans", "Jawa clan networks", "canon/legends", "crawler-based trade, salvage, rumor, and clan bargaining on desert worlds", "Use as real commercial actors with territory and custom.", ["jawa clan network", "sandcrawler clan"]),
    rec(3, "factions", "faction-local-cartels", "local cartels", "canon/legends", "planetary crime groups below galactic syndicate scale", "Use specific territory, police ties, and family politics.", ["local cartel", "planetary cartel"]),
    rec(3, "factions", "faction-medical-guilds", "medical guilds", "setting baseline", "professional groups controlling licenses, supplies, med-droids, and clinic access", "Use healthcare bureaucracy and scarce expertise.", ["medical guild", "clinic guild"]),
    rec(3, "factions", "faction-pirate-confederacies", "pirate confederacies", "canon/legends", "loose alliances of captains sharing ports, fences, and revenge rules", "Use unstable allies and violent democracy.", ["pirate confederacy", "pirate council"]),
    rec(3, "factions", "faction-port-authority", "port authorities", "setting baseline", "customs, traffic, docking, quarantine, and maintenance bureaucracy", "Use mundane power that can strand a crew.", ["port authority", "starport authority"]),
    rec(3, "factions", "faction-prison-gangs", "prison gangs", "canon/legends", "inmate factions controlling food, protection, contraband, and messages", "Use captivity politics and hard bargains.", ["prison gang", "cellblock faction"]),
    rec(3, "factions", "faction-rebel-intelligence", "Rebel intelligence cutouts", "canon/legends", "cells, couriers, dead drops, and compartmentalized handlers", "Use spycraft where even allies do not know the full plan.", ["rebel intelligence cutout", "alliance intelligence cell"]),
    rec(3, "factions", "faction-salvage-clans", "salvage clans", "canon/legends", "families or crews living off wrecks, scrap, and battlefield remains", "Use territorial claims and hard survival ethics.", ["salvage clan", "wrecking clan"]),
    rec(3, "factions", "faction-sector-moff-court", "sector moff courts", "canon/legends", "regional Imperial power circles of officers, industrialists, informants, and rivals", "Use politics around fear, favor, and purges.", ["sector moff court", "moff court"]),
    rec(3, "factions", "faction-shadowport-brokers", "shadowport brokers", "canon/legends", "fixers who control docking, fuel, clean IDs, and no-questions repairs", "Use as gatekeepers who sell safety at ugly prices.", ["shadowport broker", "no questions repair"]),
    rec(3, "factions", "faction-slavers-guilds", "slaver guilds", "canon/legends", "criminal and legalistic networks trafficking sentients by region", "Use as systemic villains with records, buyers, guards, and bribed officials.", ["slaver guild", "trafficking ring"]),
    rec(3, "factions", "faction-veteran-militias", "veteran militias", "canon/legends", "demobilized soldiers forming local defense, gangs, or political movements", "Use competence mixed with trauma and scarce pay.", ["veteran militia", "demobilized soldiers"]),
    rec(3, "factions", "faction-water-merchants", "water merchants", "canon/legends", "desert-world brokers controlling moisture, filters, tanks, and debt", "Use survival economics and local resentment.", ["water merchant", "moisture cartel"]),
    # Batch 04: force, sabers, orders, powers, legends.
    rec(4, "sabers", "saber-crossguard", "crossguard lightsabers", "canon/legends", "lightsabers with lateral vents/quillons for unstable blades or style", "Use as dangerous to wielder and opponent; vents matter in close grapples.", ["crossguard lightsaber", "quillon lightsaber"]),
    rec(4, "sabers", "saber-curved-hilt", "curved-hilt lightsabers", "canon/legends", "ergonomic hilt style associated with duelists such as Dooku", "Use for fencing precision and social signaling, not automatic superiority.", ["curved-hilt lightsaber", "dueling hilt"]),
    rec(4, "sabers", "saber-double-bladed", "double-bladed lightsabers", "canon/legends", "staff saber style with reach, intimidation, and self-risk", "Use cramped-space penalties, flourish, and aggressive control.", ["double-bladed lightsaber", "saberstaff"]),
    rec(4, "sabers", "saber-training", "training sabers", "canon/legends", "reduced-power blades for instruction, still capable of pain and injury", "Use academy scenes and child-safety limits without making them harmless toys.", ["training saber", "training lightsaber"]),
    rec(4, "sabers", "saber-underwater", "lightsabers underwater", "canon/legends", "underwater operation depends on construction, seals, pressure, and continuity", "Use sputtering, drag, visibility, and waterproofing instead of assuming normal performance.", ["lightsaber underwater", "waterproof lightsaber"]),
    rec(4, "sabers", "saber-whip", "lightwhips", "canon/legends", "flexible energy weapons with unusual range and control difficulty", "Use as rare, dangerous, and hard to defend against until pattern is read.", ["lightwhip", "lightwhips"]),
    rec(4, "force", "force-ancient-map", "ancient Force maps", "canon/legends", "star maps, temple paths, wayfinders, and symbolic routes to sacred sites", "Use as partial keys requiring interpretation, not GPS.", ["ancient force map", "temple star map"]),
    rec(4, "force", "force-bloodline-myth", "Force bloodline myths", "canon/legends", "families may mythologize sensitivity, prophecy, curse, or inheritance", "Use belief and pressure; bloodline does not guarantee destiny.", ["force bloodline myth", "force lineage"]),
    rec(4, "force", "force-buried-temple", "buried Jedi temples", "canon/legends", "lost sanctuaries hidden under cities, deserts, ice, or battlefields", "Use archaeology, traps born of defense doctrine, and contested claims.", ["buried jedi temple", "lost jedi temple"]),
    rec(4, "force", "force-corrupted-kyber", "corrupted kyber sites", "canon/legends", "mined or bled crystals leaving pain, visions, and industrial scars", "Use environmental grief and dark-side resonance around extraction.", ["corrupted kyber site", "bled kyber mine"]),
    rec(4, "force", "force-cult-fraud", "Force cult frauds", "canon/legends", "charlatans exploiting Jedi/Sith fear with tricks, drugs, relic scams, or staged visions", "Use uncertainty; not every mystic is genuine, but scams can still be dangerous.", ["force cult fraud", "fake force cult"]),
    rec(4, "force", "force-echo-object", "psychometric objects", "canon/legends", "items carrying emotional impressions readable by rare talents", "Use fragments tied to touch, trauma, and interpretation limits.", ["psychometric object", "object echo"]),
    rec(4, "force", "force-essence-transfer-risk", "essence transfer risks", "canon/legends", "dark-side survival technique involving vessels, decay, failure, and domination", "Use as horror with costs; not easy immortality.", ["essence transfer risk", "sith essence transfer"]),
    rec(4, "force", "force-exile-shrine", "exile shrines", "canon/legends", "small hidden places where survivors meditate, mourn, or hide relics", "Use quiet discovery, personal grief, and local protection.", ["exile shrine", "hidden force shrine"]),
    rec(4, "force", "force-false-vergence", "false vergences", "setting baseline", "places mistaken for Force nexuses because of chemicals, technology, or fear", "Use investigation and ambiguity before declaring mystic truth.", ["false vergence", "fake force nexus"]),
    rec(4, "force", "force-holocron-trap", "holocron traps", "canon/legends", "knowledge devices may test, mislead, lock, curse, or alert guardians", "Use access consequences, not free lore vending.", ["holocron trap", "locked holocron"]),
    rec(4, "force", "force-kyber-withdrawal", "kyber withdrawal symptoms", "original setting-compatible", "workers or cultists exposed to kyber resonance may suffer obsession, dreams, or pain", "Use only as local phenomenon, not universal canon biology.", ["kyber withdrawal", "kyber exposure sickness"]),
    rec(4, "force", "force-memory-rub", "memory-rubbed ruins", "legends-adjacent", "sites where records, droid memories, and survivor stories were deliberately erased", "Use absences as clues and institutional violence.", ["memory-rubbed ruin", "erased jedi archive"]),
    rec(4, "force", "force-nameless-aftermath", "Nameless aftermath", "canon", "Force predators leave fear, calcification, survivor trauma, and institutional secrecy", "Use High Republic horror without overexplaining the creature too early.", ["nameless aftermath", "force eater aftermath"]),
    rec(4, "force", "force-prophecy-fragment", "prophecy fragments", "canon/legends", "visions and prophecies survive as damaged texts, oral lines, or political tools", "Use as ambiguity and manipulation; fulfillment should not be obvious.", ["prophecy fragment", "damaged prophecy"]),
    rec(4, "force", "force-relic-black-market", "Force relic black market", "canon/legends", "collectors, cultists, Imperials, and criminals trade Jedi/Sith objects", "Use fake provenance, curses, raids, and moral cost.", ["force relic black market", "jedi relic market"]),
    rec(4, "force", "force-sith-tomb-air", "Sith tomb atmospherics", "canon/legends", "dust, poison, darkness, inscriptions, dead mechanisms, and fear inside tombs", "Use physical danger before mystic exposition.", ["sith tomb atmosphere", "sith tomb air"]),
    rec(4, "force", "force-vision-contagion", "shared visions", "canon/legends", "multiple witnesses may share or distort a vision through bond, site, artifact, or trauma", "Use conflicting interpretations and strain.", ["shared vision", "vision contagion"]),
    rec(4, "powers", "power-battle-meditation-cost", "battle meditation costs", "canon/legends", "large-scale morale/coordination Force influence requiring focus and vulnerability", "Use as exhausting and targetable; never casual army control.", ["battle meditation cost", "battle meditation risk"]),
    rec(4, "powers", "power-beast-control-limits", "beast control limits", "canon/legends", "calming or influencing animals depends on species, pain, training, hunger, and fear", "Use partial influence and backlash rather than guaranteed control.", ["beast control limit", "force calm beast"]),
    rec(4, "powers", "power-force-barrier", "Force barriers", "canon/legends", "defensive fields resisting impact, heat, debris, or energy briefly", "Use strain, concentration, and failure leakage.", ["force barrier", "force shield technique"]),
    rec(4, "powers", "power-force-cloak", "Force concealment", "canon/legends", "hiding presence, emotion, or alignment from detection", "Use opposing vigilance, stress, wounds, and dark-side sites as limits.", ["force concealment", "hide force presence"]),
    rec(4, "powers", "power-force-drain-cost", "Force drain costs", "legends primary", "dark-side technique stealing vitality, energy, or connection", "Use as corrupting horror with witnesses, backlash, and moral consequence.", ["force drain cost", "dark side drain"]),
    rec(4, "powers", "power-force-listening", "Force listening", "canon/legends", "attuning to distant emotions, echoes, or living presences", "Use impressions, not surveillance-camera certainty.", ["force listening", "listen through the force"]),
    rec(4, "powers", "power-force-scream", "Force scream", "canon/legends", "uncontrolled or deliberate dark-side psychic/sonic outburst", "Use as emotional rupture causing fear, damage, and exposure.", ["force scream", "dark side scream"]),
    rec(4, "powers", "power-healing-price", "Force healing price", "canon", "healing transfers vitality or carries cost depending user, wound, and context", "Use injury, exhaustion, emotional bond, and moral strain; no free full restores.", ["force healing price", "healing transfers life"]),
    rec(4, "powers", "power-mind-trick-limits", "mind trick limits", "canon/legends", "suggestion works best on weak-minded or distracted targets and simple commands", "Use species, training, stakes, and contradiction as resistance.", ["mind trick limit", "jedi mind trick limit"]),
    rec(4, "powers", "power-precognition-noise", "precognition noise", "canon/legends", "future sight distorted by emotion, dark side, choice, and incomplete context", "Use flashes and warning feelings, not guaranteed spoilers.", ["precognition noise", "future sight noise"]),
    rec(4, "orders", "order-altisian-jedi", "Altisian Jedi", "legends primary", "Jedi sect associated with Djinn Altis and looser attachment doctrine", "Use for Jedi diversity and conflict with orthodox Council rules.", ["altisian jedi", "djinn altis"]),
    rec(4, "orders", "order-barando-sages", "Baran Do Sages", "canon/legends", "Kel Dor Force tradition emphasizing weather, prophecy, and contemplation", "Use non-Jedi wisdom and Dorin cultural specificity.", ["baran do sages", "baran do"]),
    rec(4, "orders", "order-bendu", "Bendu tradition", "canon", "powerful nonaligned Force being/philosophy from Rebels context", "Use as rare mythic encounter; not a normal order or neutral easy answer.", ["bendu tradition", "the bendu"]),
    rec(4, "orders", "order-disciples-ragnos", "Disciples of Ragnos", "legends primary", "cult seeking Sith power through Marka Ragnos legacy", "Use for post-Imperial cult violence and artifact theft.", ["disciples of ragnos", "ragnos cult"]),
    rec(4, "orders", "order-green-jedi", "Corellian Green Jedi", "legends primary", "Corellian Jedi tradition emphasizing local duty and family ties", "Use as Legends Jedi variant with political obligations.", ["green jedi", "corellian jedi"]),
    rec(4, "orders", "order-kilian-rangers", "Kilian Rangers", "legends primary", "Force-using lawkeeper tradition from old material", "Use as obscure regional justice order in Legends or mixed play.", ["kilian rangers", "kilian ranger"]),
    rec(4, "orders", "order-mind-walkers", "Mind Walkers", "legends primary", "Force mystics tied to beyond-shadows and esoteric consciousness travel", "Use for dangerous metaphysics, not casual astral travel.", ["mind walkers", "beyond shadows"]),
    rec(4, "orders", "order-nightsister-clans", "Nightsister clan distinctions", "canon/legends", "Dathomiri witches vary by clan, era, and continuity", "Use clan politics and survival; do not make all witches identical.", ["nightsister clan distinction", "dathomiri clans"]),
    rec(4, "orders", "order-order-66-survivor-cells", "Order 66 survivor cells", "canon/legends", "Jedi survivors, helpers, and hidden students fragmented after Purge", "Use paranoia, guilt, dead drops, and compromised safehouses.", ["order 66 survivor cell", "jedi survivor network"]),
    rec(4, "orders", "order-zeffo-sages", "Zeffo sages", "canon", "ancient Force-adjacent civilization from Jedi game continuity", "Use tomb puzzles, empire archaeology, and extinct-civilization mystery.", ["zeffo sages", "zeffo tomb"]),
    rec(4, "legends", "legends-bearer-sith", "Sith species caste detail", "legends primary", "ancient Sith species society with castes, alchemy, and later hybrid Sith empires", "Use for tomb inscriptions, bloodline myths, and imperial archaeology.", ["sith species caste", "ancient sith species"]),
    rec(4, "legends", "legends-celestial-machines", "Celestial machines", "legends primary", "ancient megastructures attributed to Architects/Celestials", "Use as unknowable infrastructure with damaged purpose and massive consequence.", ["celestial machine", "architect machine"]),
    rec(4, "legends", "legends-corellian-system-origin", "Corellian system origin legends", "legends primary", "legends links system arrangement to ancient engineering and Centerpoint", "Use for Corellian mystery without overwriting canon map facts.", ["corellian system origin", "corellian ancient engineering"]),
    rec(4, "legends", "legends-dark-underlord", "Dark Underlord", "legends primary", "ancient Sith-linked warlord figure from early Legends history", "Use as obscure cult reference, not mainstream Sith default.", ["dark underlord"]),
    rec(4, "legends", "legends-desann", "Desann and Reborn", "legends primary", "dark Jedi and artificially empowered Reborn from Jedi Outcast-era lore", "Use for Imperial remnant Force experiments and unstable trainees.", ["desann", "reborn dark jedi"]),
    rec(4, "legends", "legends-freedon-nadd", "Freedon Nadd legacy", "legends primary", "fallen Jedi/Sith ruler whose tomb and teachings corrupt Onderon history", "Use as tomb influence, cult politics, and old royal corruption.", ["freedon nadd legacy", "naddist"]),
    rec(4, "legends", "legends-golden-age-sith", "Golden Age of the Sith detail", "legends primary", "period of Sith Empire wealth, rival lords, alchemy, and expansion before disaster", "Use for ancient ruins with political context rather than random evil temples.", ["golden age sith detail", "ancient sith empire detail"]),
    rec(4, "legends", "legends-hundred-year-darkness", "Hundred-Year Darkness", "legends primary", "war between Jedi and dark siders leading to Sith exile mythology", "Use as deep historical fracture and archive controversy.", ["hundred-year darkness", "second great schism"]),
    rec(4, "legends", "legends-jaden-korr", "Jaden Korr", "legends primary", "New Jedi Order-era student/knight from Jedi Academy continuity", "Use for Legends academy threads and remnant cult conflicts.", ["jaden korr"]),
    rec(4, "legends", "legends-karness-muur", "Karness Muur", "legends primary", "ancient Sith Lord tied to Muur Talisman and rakghoul-like corruption", "Use as artifact horror and possession risk.", ["karness muur", "muur legacy"]),
    rec(4, "legends", "legends-kyle-katarn", "Kyle Katarn", "legends primary", "mercenary turned Jedi tied to Dark Forces/Jedi Knight continuity", "Use as Legends operative with soldier instincts and Force complications.", ["kyle katarn"]),
    rec(4, "legends", "legends-lumiya", "Lumiya", "legends primary", "dark-side agent and Sith figure tied to post-Endor corruption of Jacen Solo", "Use as manipulator and legacy-era Sith bridge.", ["lumiya", "shira brie"]),
    rec(4, "legends", "legends-naga-sadow", "Naga Sadow", "legends primary", "Sith Lord central to Great Hyperspace War and illusion/war strategy", "Use tombs, alchemy, and ancient Sith military legacy.", ["naga sadow detail", "sadow tomb"]),
    rec(4, "legends", "legends-ordo-canderous", "Canderous Ordo", "legends primary", "Mandalorian warrior later linked to Mandalore title in KOTOR-era continuity", "Use for Mandalorian Wars memory and pragmatic warrior politics.", ["canderous ordo", "mandalore the preserver"]),
    rec(4, "legends", "legends-ragnos", "Marka Ragnos", "legends primary", "ancient Sith ruler whose shadow shapes later Sith legitimacy", "Use as name of authority cultists invoke, not active default NPC.", ["marka ragnos detail", "ragnos spirit"]),
    rec(4, "legends", "legends-sith-pureblood", "Sith purebloods", "legends primary", "red-skinned descendants/hybrids of ancient Sith species in SWTOR-era lore", "Use for Old Republic social hierarchy and species politics.", ["sith pureblood", "sith purebloods"]),
    rec(4, "legends", "legends-sunrider-family", "Sunrider family", "legends primary", "ancient Jedi family line tied to Nomi and Vima Sunrider", "Use as archive lineage and old Jedi exemplar material.", ["sunrider family", "vima sunrider"]),
    rec(4, "legends", "legends-tales-jedi-era", "Tales of the Jedi era", "legends primary", "ancient Republic/Jedi/Sith storytelling layer around Exar Kun, Nomi, Ulic, and Sith ruins", "Use as source bucket for old artifacts and histories.", ["tales of the jedi era", "totj era"]),
    rec(4, "legends", "legends-valley-jedi", "Valley of the Jedi legends", "legends primary", "Ruusan Force nexus tied to trapped spirits and Kyle Katarn-era conflicts", "Use as high-stakes Force site with grief and power temptation.", ["valley of the jedi legends", "ruusan valley"]),
    rec(4, "legends", "legends-vima-da-boda", "Vima-Da-Boda", "legends primary", "fallen or damaged Jedi survivor tied to Dark Empire-era underworld", "Use as broken witness and warning about long survival.", ["vima-da-boda", "vima da boda"]),
    rec(4, "legends", "legends-warrior-castes", "Mandalore title legends", "legends primary", "Mandalore as title, symbol, and contested legitimacy across eras", "Use to separate individual leaders from all Mandalorians.", ["mandalore title legends", "mandalore title"]),
    rec(4, "legends", "legends-xizor-palace", "Xizor power base", "legends primary", "Black Sun elite court, wealth, and Falleen social-political influence", "Use for crime-noble intrigue and dangerous hospitality.", ["xizor power base", "black sun palace"]),
    # Batch 05: breadth gaps in worlds, tech, species, characters.
    rec(5, "species", "species-abednedo", "Abednedo", "canon", "long-snouted sentients appearing across sequel-era and broader canon contexts", "Use as ordinary galactic citizens, pilots, and workers, not exotic spectacle.", ["abednedo"]),
    rec(5, "species", "species-aleena", "Aleena", "canon/legends", "small fast sentients such as Ratts Tyerell's species", "Use size, speed, and underestimation in crowds or racing scenes.", ["aleena"]),
    rec(5, "species", "species-bardottan", "Bardottans", "canon", "sentients with mystic traditions and tension with Jedi in Clone Wars stories", "Use non-Jedi spiritual sovereignty and kidnapping/investigation plots.", ["bardottan", "bardottans"]),
    rec(5, "species", "species-bivall", "Bivall", "canon", "large-eyed aquatic-adjacent sentients such as Dr. Nala Se-style medical figures", "Use medical, research, and alien-clinic presence.", ["bivall"]),
    rec(5, "species", "species-crolute", "Crolutes", "canon", "large aquatic sentients associated with Unkar Plutt's species", "Use salvage-yard bosses, junk economies, and harsh bargaining.", ["crolute", "crolutes"]),
    rec(5, "species", "species-dowutin", "Dowutin", "canon", "large tusked sentients including Grummgar-type hunters", "Use wealthy predators, mercenaries, and size-based intimidation.", ["dowutin", "dowutins"]),
    rec(5, "species", "species-glymphid", "Glymphids", "canon/legends", "long-snouted aliens often seen in crowds and racing contexts", "Use as background species with possible racing or mechanic roles.", ["glymphid", "glymphids"]),
    rec(5, "species", "species-kyuzo", "Kyuzo", "canon/legends", "masked agile sentients such as Embo's species", "Use hunters, mercenaries, and acrobatic terrain tactics.", ["kyuzo"]),
    rec(5, "species", "species-lurmen", "Lurmen", "canon/legends", "peace-seeking colonist species from Clone Wars stories", "Use pacifism under invasion and refugee dilemmas.", ["lurmen"]),
    rec(5, "species", "species-mikkian", "Mikkians", "canon/legends", "tendrilled sentients including Jedi Tiplar/Tiplee", "Use Jedi diversity and head-tendril social/body cues.", ["mikkian", "mikkians"]),
    rec(5, "species", "species-mustafarian", "Mustafarians", "canon/legends", "sentients adapted to Mustafar's heat, masks, and mining culture", "Use local guides, harsh industry, and post-Vader ecological change.", ["mustafarian", "mustafarians"]),
    rec(5, "species", "species-ongree", "Ongree", "canon/legends", "stalk-eyed sentients including Jedi Pablo-Jill's species", "Use alien perception and unusual body language in diplomacy.", ["ongree"]),
    rec(5, "species", "species-pykes", "Pyke species", "canon", "sentients from Oba Diah associated with the Pyke Syndicate but not reducible to it", "Use syndicate members and civilians distinctly.", ["pyke species", "pyke sentient"]),
    rec(5, "species", "species-tarsunt", "Tarsunt", "canon", "snouted sentients seen in Resistance-era political contexts", "Use bureaucrats, refugees, and ordinary galactic presence.", ["tarsunt"]),
    rec(5, "species", "species-teedo", "Teedo species", "canon", "Jakku scavenger species using mounts and desert survival techniques", "Use scavenger conflict and survival custom, not generic raiders.", ["teedo species", "teedo scavenger"]),
    rec(5, "species", "species-tholothian", "Tholothians", "canon/legends", "near-human sentients with distinctive head tendrils, including Jedi Adi Gallia/Stass Allie", "Use Jedi, diplomats, and Core-world diversity.", ["tholothian", "tholothians"]),
    rec(5, "species", "species-tognath", "Tognath", "canon", "gas-mask-like sentients such as Edrio Two Tubes' species", "Use partisans, body-horror appearance bias, and atmosphere ambiguity.", ["tognath"]),
    rec(5, "species", "species-uggnaut", "Ugnaughts", "canon/legends", "short porcine sentients known for labor, engineering, and Cloud City work", "Use skilled workers, clans, contract labor, and underestimated expertise.", ["ugnaught", "ugnaughts"]),
    rec(5, "worlds", "world-anaxes", "Anaxes", "canon/legends", "Core military world with continuity differences, naval culture, and strategic history", "Use officer schools, fleet politics, and old Core prestige.", ["anaxes"]),
    rec(5, "worlds", "world-batuu", "Batuu", "canon", "frontier world with Black Spire Outpost and crossroads for smugglers, First Order, and Resistance", "Use border-town tension and layered visitors.", ["batuu", "black spire outpost"]),
    rec(5, "worlds", "world-bonadan", "Bonadan", "legends primary", "Corporate Sector port/industrial world with polluted commerce", "Use corporate dystopia, customs, and hard-edged trade.", ["bonadan"]),
    rec(5, "worlds", "world-castilon", "Castilon", "canon", "ocean planet with Colossus refueling platform in Resistance-era stories", "Use racing, fuel politics, spies, and platform community.", ["castilon", "colossus platform"]),
    rec(5, "worlds", "world-chandrila-politics", "Chandrila political culture", "canon/legends", "Mon Mothma's homeworld and New Republic political symbol", "Use refined democratic image with family, finance, and surveillance tension.", ["chandrila politics", "chandrila senate culture"]),
    rec(5, "worlds", "world-colu", "Colu", "legends primary; canon references vary", "world associated with Colicoids/technology traditions in older lore", "Use technical arrogance and obscure alien manufacturing only with labels.", ["colu legends", "colu"]),
    rec(5, "worlds", "world-corellian-shipyards", "Corellian shipyard districts", "canon/legends", "industrial zones building freighters, warships, and smugglers' dreams", "Use labor, theft, inspections, and corporate security.", ["corellian shipyard district", "corellian shipyards"]),
    rec(5, "worlds", "world-eadu", "Eadu", "canon", "stormy Imperial research world linked to kyber weapons science", "Use rain, secrecy, landing hazards, and weapons-lab guilt.", ["eadu"]),
    rec(5, "worlds", "world-florrum", "Florrum", "canon/legends", "desert world associated with Hondo Ohnaka's pirate base", "Use pirate hospitality, betrayal, and harsh outpost logistics.", ["florrum"]),
    rec(5, "worlds", "world-kijimi", "Kijimi", "canon", "cold world with spice runners, First Order occupation, and later destruction by Final Order", "Use occupation, old crew ties, and canon-era tragedy.", ["kijimi"]),
    rec(5, "worlds", "world-lira-san", "Lira San", "canon", "Lasat refuge world tied to Ashla prophecy and survival", "Use refugee hope and hidden-route mystery.", ["lira san", "lasat refuge"]),
    rec(5, "worlds", "world-lothal-fields", "Lothal rural zones", "canon", "grasslands, farms, kyber-linked temple sites, and Imperial extraction scars", "Use small communities under occupation and post-liberation recovery.", ["lothal rural", "lothal grasslands"]),
    rec(5, "worlds", "world-maridun", "Maridun", "canon/legends", "Lurmen refuge world with giant grass and Separatist weapon testing history", "Use pacifist villages under military threat.", ["maridun"]),
    rec(5, "worlds", "world-mimban", "Mimban", "canon/legends", "muddy war world with Imperial trenches and resource conflict", "Use miserable infantry combat, mud, and local exploitation.", ["mimban"]),
    rec(5, "worlds", "world-oba-diah", "Oba Diah", "canon", "Pyke Syndicate home base/world in spice-trade politics", "Use cartel diplomacy, spice ledgers, and dangerous hospitality.", ["oba diah"]),
    rec(5, "worlds", "world-peridea", "Peridea", "canon", "extradistant world tied to Nightsister origins, purrgil routes, and Thrawn exile", "Use alien isolation and mythic geography; not normal hyperspace travel.", ["peridea"]),
    rec(5, "worlds", "world-raada", "Raada", "canon", "farming moon from Ahsoka novel context under Imperial agricultural exploitation", "Use rural occupation, food extraction, and hidden Force survivor stakes.", ["raada"]),
    rec(5, "worlds", "world-rendili", "Rendili", "canon/legends", "Core shipbuilding world with Republic/Imperial naval relevance", "Use fleet procurement, corporate politics, and dockyard intrigue.", ["rendili", "rendili shipyards"]),
    rec(5, "worlds", "world-scarif", "Scarif", "canon", "tropical Imperial security world with Citadel Tower and Death Star archive battle", "Use beaches against bunker horror, data vaults, and shield-gate tactics.", ["scarif", "citadel tower"]),
    rec(5, "worlds", "world-sorgan", "Sorgan", "canon", "frontier agrarian world with krill ponds and raider/AT-ST conflict", "Use rural defense, hidden veterans, and low-tech stakes.", ["sorgan"]),
    rec(5, "worlds", "world-vandor", "Vandor", "canon", "cold frontier world with conveyex robbery and criminal routes", "Use train heists, snow, and outlaw logistics.", ["vandor", "vandor conveyex"]),
    rec(5, "tech", "tech-arc-170", "ARC-170 starfighters", "canon/legends", "clone wars heavy reconnaissance/fighter craft with crew and astromech", "Use as durable military surplus with crew demands.", ["arc-170", "arc-170 starfighter"]),
    rec(5, "tech", "tech-at-dp", "AT-DP walkers", "canon", "Imperial patrol walkers used for garrison and urban control", "Use as intimidating local armor vulnerable to terrain and planning.", ["at-dp", "at-dp walker"]),
    rec(5, "tech", "tech-at-rt", "AT-RT walkers", "canon/legends", "light one-person scout walkers from Clone Wars and later use", "Use fast patrol armor with exposed rider risk.", ["at-rt", "at-rt walker"]),
    rec(5, "tech", "tech-b1-maintenance", "B1 battle droid remnants", "canon/legends", "old Separatist droids reused, scavenged, or left as suspicious junk", "Use as parts, traps, witnesses, or degraded threats.", ["b1 battle droid remnant", "old b1 droid"]),
    rec(5, "tech", "tech-bacta-patch", "bacta patches", "canon/legends", "portable minor wound treatment with limits and infection risk", "Use as short-term aid, not instant full medical recovery.", ["bacta patch", "bacta patches"]),
    rec(5, "tech", "tech-breath-mask", "breath masks", "canon/legends", "portable breathing gear for underwater, toxins, dust, or thin air", "Use limited filters, seal checks, and species compatibility.", ["breath mask", "rebreather"]),
    rec(5, "tech", "tech-burner-comlink", "burner comlinks", "setting baseline", "cheap disposable communicators used to avoid trace or compartmentalize contacts", "Use as fragile tradecraft that fails if reused or recovered.", ["burner comlink", "disposable comlink"]),
    rec(5, "tech", "tech-code-cylinder", "code cylinders", "canon/legends", "Imperial/Republic access devices tied to rank, station, and live authorization", "Use stolen access with time limits and audit logs.", ["code cylinder", "imperial code cylinder"]),
    rec(5, "tech", "tech-droid-scomp", "scomp links", "canon/legends", "droid interface tools for accessing computer sockets and systems", "Use physical access, permissions, and countermeasures.", ["scomp link", "scomp socket"]),
    rec(5, "tech", "tech-gaderffii", "gaderffii sticks", "canon/legends", "Tusken melee weapons with cultural identity and practical desert use", "Use as more than a club; taking one has social meaning.", ["gaderffii", "gaffi stick"]),
    rec(5, "tech", "tech-holoprojector", "holoprojectors", "canon/legends", "communication/display devices with signal, recording, and spoofing risks", "Use compromised holos and bad transmission quality.", ["holoprojector", "holo projector"]),
    rec(5, "tech", "tech-magnetic-seal", "magnetic seals", "setting baseline", "industrial or security seals holding panels, crates, doors, and evidence boxes", "Use power state, heat, overrides, and tamper marks.", ["magnetic seal", "mag-seal"]),
    rec(5, "tech", "tech-mouse-droid", "MSE mouse droids", "canon/legends", "small utility droids moving through Imperial corridors and facilities", "Use as noise, witness, alarm carrier, or hacked distraction.", ["mouse droid", "mse droid"]),
    rec(5, "tech", "tech-pazaak", "pazaak decks", "legends primary", "card game associated with KOTOR-era gambling", "Use for Old Republic social play, cheating, and debt hooks.", ["pazaak", "pazaak deck"]),
    rec(5, "tech", "tech-personal-shield", "personal shields", "canon/legends", "rare portable shields limited by power, legality, and weapon interactions", "Use as expensive complication, not common immunity.", ["personal shield", "portable shield"]),
    rec(5, "tech", "tech-repulsor-sled", "repulsor sleds", "canon/legends", "floating cargo platforms and stretchers used in ports, clinics, and battlefields", "Use logistics, improvised cover, and cargo theft.", ["repulsor sled", "hover sled"]),
    rec(5, "tech", "tech-security-cam", "security camera systems", "setting baseline", "cams have arcs, storage, blind spots, maintenance logs, and watchers", "Use observation as physical system the player can study or exploit.", ["security camera system", "camera blind spot"]),
    rec(5, "tech", "tech-sonic-weapon", "sonic weapons", "canon/legends", "sound/pressure weapons useful against shields, armor gaps, and crowds", "Use disorientation, collateral, and species-specific hearing risk.", ["sonic weapon", "sonic blaster"]),
    rec(5, "tech", "tech-thermal-detonator-law", "thermal detonator legality", "canon/legends", "highly restricted explosives with massive intimidation value", "Use as legal nightmare, hostage risk, and panic trigger.", ["thermal detonator legality", "illegal thermal detonator"]),
    rec(5, "tech", "tech-toolkit", "mechanic toolkits", "canon/legends", "portable repair kits with cutters, sealant, diagnostics, wire, and improvised value", "Use inventory limits and missing-tool consequences.", ["mechanic toolkit", "repair kit"]),
    rec(5, "characters", "char-babu-frik", "Babu Frik operational profile", "canon", "tiny Anzellan droidsmith with black-market technical skill", "Use as expert who needs tools, payment, and access; not comic relief only.", ["babu frik profile", "anzellan droidsmith"]),
    rec(5, "characters", "char-beckett", "Tobias Beckett operational profile", "canon", "criminal mentor and thief shaped by betrayal, debt, and survival", "Use as lesson in underworld trust: everyone has a price and a fear.", ["tobias beckett profile", "beckett operational"]),
    rec(5, "characters", "char-cal-kestis", "Cal Kestis operational profile", "canon", "Order 66 survivor, scrapper, Jedi, and rebel-era fugitive", "Use trauma, improvisation, and survivor networks; no effortless public heroics.", ["cal kestis profile", "cal operational"]),
    rec(5, "characters", "char-cassian-andor", "Cassian Andor operational profile", "canon", "rebel intelligence operative formed by prison, occupation, and ugly sacrifice", "Use practical spy violence and distrust before Scarif.", ["cassian andor profile", "cassian operational"]),
    rec(5, "characters", "char-cere-junda", "Cere Junda operational profile", "canon", "Jedi survivor carrying guilt, fear, and renewed discipline after the Purge", "Use as mentor with trauma and limits.", ["cere junda profile", "cere operational"]),
    rec(5, "characters", "char-dryden-vos", "Dryden Vos operational profile", "canon", "Crimson Dawn crime boss using refinement, violence, and performative hospitality", "Use as charming danger with immediate consequences for disrespect.", ["dryden vos profile", "dryden operational"]),
    rec(5, "characters", "char-enfys-nest", "Enfys Nest operational profile", "canon", "young rebel-aligned raider leader targeting Crimson Dawn resources", "Use mistaken identity and moral reversal when evidence surfaces.", ["enfys nest profile", "enfys operational"]),
    rec(5, "characters", "char-fennec-shand", "Fennec Shand operational profile", "canon", "elite assassin and mercenary with patience, precision, and survival instinct", "Use as sniper/handler threat who controls range and exits.", ["fennec shand profile", "fennec operational"]),
    rec(5, "characters", "char-greez", "Greez Dritus operational profile", "canon", "Latero pilot and cantina owner with debts, nerves, and loyalty", "Use as practical crew contact shaped by gambling and survival.", ["greez dritus profile", "greez operational"]),
    rec(5, "characters", "char-kino-loy", "Kino Loy operational profile", "canon", "Narkina 5 floor manager turned prison rebel", "Use as institutionalized prisoner whose courage has a specific breaking point.", ["kino loy profile", "kino operational"]),
    rec(5, "characters", "char-marchion-ro", "Marchion Ro operational profile", "canon", "Nihil leader using fear, path technology, symbols, and anti-Jedi strategy", "Use as High Republic asymmetric threat, not generic pirate.", ["marchion ro profile", "marchion operational"]),
    rec(5, "characters", "char-maz-kanata", "Maz Kanata operational profile", "canon", "ancient pirate queen and castle host with relics, eyes, and survival networks", "Use as broker of old knowledge who withholds more than she gives.", ["maz kanata profile", "maz operational"]),
    rec(5, "characters", "char-nien-nunb", "Nien Nunb operational profile", "canon/legends", "Sullustan pilot and rebel hero", "Use as capable veteran pilot with understated competence.", ["nien nunb profile", "nien operational"]),
    rec(5, "characters", "char-reebo-band", "Max Rebo Band operational profile", "canon/legends", "touring entertainers tied to underworld venues and dangerous patrons", "Use music as cover, witness network, and underworld access.", ["max rebo band profile", "rebo band operational"]),
    rec(5, "characters", "char-sol", "Master Sol operational profile", "canon", "High Republic Jedi master tied to Brendok tragedy and concealed guilt", "Use as compassionate but compromised; truth should carry cost.", ["master sol profile", "sol operational"]),
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync(entry):
    keys = []
    for key in entry.get("key", []):
        clean = key.strip()
        if clean and clean not in keys:
            keys.append(clean)
    entry["key"] = keys
    entry["keysRaw"] = ", ".join(keys)
    entry["keywordsRaw"] = entry["keysRaw"]


def make_entry(template, row, order, category):
    entry = dict(template)
    entry.update(
        {
            "activationMode": "standard",
            "activationScript": "",
            "case_sensitive": False,
            "category": category,
            "comment": f"lore expansion batch {row['batch']:02d}; official canon baseline, Wookieepedia tertiary breadth, canon controls conflicts",
            "constant": False,
            "content": (
                f"{row['name'].upper()}\n"
                f"continuity = {row['continuity']}\n"
                f"role = {row['role']}\n"
                f"rpg use = {row['use']}"
            ),
            "enabled": True,
            "extensions": {},
            "groupWeight": 100,
            "id": row["id"],
            "inclusionGroupRaw": "",
            "insertion_order": order,
            "key": row["keys"],
            "keyMatchPriority": True,
            "keysecondary": [],
            "keysecondaryRaw": "",
            "matchWholeWords": True,
            "minMessages": 0,
            "name": row["name"],
            "prioritizeInclusion": False,
            "priority": row["priority"],
            "probability": 100,
            "selectiveLogic": 0,
            "tags": ["star_wars", f"expansion_batch_{row['batch']:02d}"],
        }
    )
    sync(entry)
    return entry


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    grouped = defaultdict(list)
    for row in ENTRIES:
        grouped[FILES[row["book"]]].append(row)

    changes = []
    for filename, rows in sorted(grouped.items()):
        path = ROOT / filename
        shutil.copy2(path, BACKUP / filename)
        data = load(path)
        names = {entry.get("name", "").lower() for entry in data}
        ids = {entry.get("id") for entry in data}
        category = data[0].get("category", "") if data else ""
        template = data[0]
        order = max((entry.get("insertion_order", 0) for entry in data), default=0)
        added = 0
        skipped = 0
        for row in rows:
            if row["name"].lower() in names or row["id"] in ids:
                skipped += 1
                continue
            order += 100
            data.append(make_entry(template, row, order, category))
            names.add(row["name"].lower())
            ids.add(row["id"])
            added += 1
            changes.append(
                {
                    "batch": row["batch"],
                    "file": filename,
                    "name": row["name"],
                    "id": row["id"],
                    "continuity": row["continuity"],
                    "keys": row["keys"],
                }
            )
        data.sort(key=lambda entry: entry.get("insertion_order", 0))
        save(path, data)
        print(f"{filename}: added {added}, skipped {skipped}")

    payload = {"generated": date.today().isoformat(), "sources": SOURCES, "changes": changes}
    (REPORTS / "expansion_batches_03_05_sources.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for batch in (3, 4, 5):
        batch_changes = [change for change in changes if change["batch"] == batch]
        md = [f"# Lore Expansion Batch {batch:02d}", "", f"Generated: {date.today().isoformat()}", "", "## Sources", ""]
        for label, url in SOURCES.items():
            md.append(f"- {label}: {url}")
        md.extend(["", "## Added Entries", ""])
        for change in batch_changes:
            md.append(f"- {change['file']} :: {change['name']} :: {change['continuity']} [{', '.join(change['keys'])}]")
        (REPORTS / f"expansion_batch_{batch:02d}_changelog.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Backed up touched files to {BACKUP}")
    print(f"Added {len(changes)} total entries")


if __name__ == "__main__":
    main()
