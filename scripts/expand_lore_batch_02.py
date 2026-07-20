import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "archive" / f"lore-expansion-batch-02-{date.today().isoformat()}"
REPORTS = ROOT / "reports"

BASE_SOURCES = {
    "official_databank": "https://www.starwars.com/databank/",
    "official_news": "https://www.starwars.com/news",
    "wookieepedia_species": "https://starwars.fandom.com/wiki/Species",
    "wookieepedia_species_legends": "https://starwars.fandom.com/wiki/Species/Legends",
    "wookieepedia_starship_legends": "https://starwars.fandom.com/wiki/Starship/Legends",
    "wookieepedia_galaxy_legends": "https://starwars.fandom.com/wiki/The_galaxy/Legends",
}


def item(slug, name, continuity, role, use, keys, tags=None, priority=1):
    return {
        "id": f"kyber-batch02-{slug}",
        "name": name,
        "continuity": continuity,
        "role": role,
        "use": use,
        "key": keys,
        "tags": tags or [],
        "priority": priority,
    }


DATA = {
    "Kyber RPG 06 - Species and Cultures.json": [
        item("species-aqualish", "aqualish", "canon/legends", "tusked sentients with many subgroups and a reputation for rough work, gangs, labor, and pilots", "Use as dock muscle, separatist veterans, mercenaries, or civilians; do not make every aqualish stupid or violent.", ["aqualish"]),
        item("species-arcona", "arcona", "canon/legends", "desert-adapted reptilian sentients often vulnerable to salt addiction in legends", "Use for addiction pressure, mining towns, debt, and alien body needs; salt abuse should have consequences.", ["arcona"]),
        item("species-balosar", "balosar", "canon/legends", "near-human sentients with retractable antennae and strong underworld associations in common media", "Use for addicts, informants, dealers, or survivors; avoid treating a whole species as inherently criminal.", ["balosar"]),
        item("species-bith", "bith", "canon/legends", "large-headed sentients known for music, science, and precision work", "Use as musicians, analysts, surgeons, mathematicians, and witnesses who notice acoustic or technical detail.", ["bith"]),
        item("species-bothan", "bothans", "canon/legends", "furred sentients famous in Legends for intelligence networks and clan politics", "Use for espionage, information brokerage, reputation traps, and political blackmail; canon-only use should stay cautious.", ["bothan", "bothans"]),
        item("species-cerean", "cereans", "canon/legends", "tall-headed sentients associated with binary-brain processing and Ki-Adi-Mundi", "Use for analysis, tradition-vs-modernity conflict, council politics, and logistical reasoning.", ["cerean", "cereans"]),
        item("species-chagrian", "chagrians", "canon/legends", "horned amphibious sentients including Mas Amedda's species", "Use for bureaucrats, senators, diplomats, and aquatic-environment cultural detail.", ["chagrian", "chagrians"]),
        item("species-clawdite", "clawdites", "canon/legends", "shapeshifting sentients able to mimic humanoid appearance within limits", "Use for infiltration plots with stress, injury, mass, clothing, voice, and behavioral tells limiting disguise.", ["clawdite", "clawdites"]),
        item("species-dashade", "dashade", "canon/legends", "large predatory sentients with legends associations to force resistance and assassin work", "Use as terrifying bodyguards or old Sith-era survivors; force resistance is continuity-dependent, not automatic.", ["dashade"]),
        item("species-dug", "dugs", "canon/legends", "limb-inverted sentients from Malastare with strong climbing and mechanical mobility", "Use as racers, mechanics, tough negotiators, or local power brokers; avoid lazy comic caricature.", ["dug", "dugs"]),
        item("species-echani", "echani", "legends primary", "near-human martial culture reading intent through combat and movement", "Use for duel etiquette, body-language insight, mercenary philosophy, and intimate but dangerous training scenes.", ["echani"]),
        item("species-elomin", "elomin", "legends primary", "ordered, analytical sentients who value pattern and structure", "Use for administrators, surveyors, archivists, and people unsettled by chaos or improvisation.", ["elomin"]),
        item("species-ewok", "ewoks", "canon/legends", "forest moon hunter-gatherers with traps, courage, and strong local terrain knowledge", "Use as competent locals; primitive technology does not mean helplessness or innocence.", ["ewok", "ewoks"]),
        item("species-felucian", "felucians", "canon/legends", "fungal-jungle native culture with strong environmental and force-adjacent depictions", "Use for hostile ecology, local guides, shamans, and colonial harm without flattening them into monsters.", ["felucian", "felucians"]),
        item("species-gand", "gand", "canon/legends", "ammonia-breathing or lunged insectoid sentients with findsman traditions in Legends", "Use for trackers, mystics, bounty hunters, and life-support constraints in standard atmospheres.", ["gand", "findsman"]),
        item("species-geonosian-castes", "geonosian castes", "canon/legends", "hive society with workers, warriors, aristocrats, engineers, and queen-centered reproduction", "Use caste and pheromone/social hierarchy in Geonosian scenes; surviving hives after imperial sterilization should be rare and haunted.", ["geonosian caste", "geonosian queen"]),
        item("species-gotal", "gotals", "canon/legends", "horned sentients whose head cones sense energy/emotion in many depictions", "Use for lie pressure, crowded-room overload, bounty work, and discomfort around droids or heavy electronics.", ["gotal", "gotals"]),
        item("species-gran", "gran", "canon/legends", "three-eyed sentients from Kinyen and colonies such as Malastare", "Use for municipal politics, merchants, podracing worlds, and colonial identity differences.", ["gran", "kinyen"]),
        item("species-ishi-tib", "ishi tib", "canon/legends", "beaked amphibious sentients often seen in finance, rebellion, and bureaucracy", "Use water needs and ecological values as practical constraints in travel, prisons, or negotiations.", ["ishi tib", "ishi-tib"]),
        item("species-jenet", "jenet", "legends primary", "small rodentlike sentients known for memory and information brokerage", "Use as data brokers, witnesses, smugglers, and people who remember dangerous debts.", ["jenet"]),
        item("species-kaleesh", "kaleesh", "canon/legends", "warrior culture from Kalee, associated with Grievous before cybernetics", "Use for vendetta, ritual masks, anti-Huk history, and proud martial NPCs.", ["kaleesh", "kalee"]),
        item("species-kaminoan", "kaminoans", "canon/legends", "tall cloners from Kamino with elegant manner and severe utilitarian science", "Use for bioethics, clone politics, medical arrogance, and sterile facilities hiding ugly choices.", ["kaminoan", "kaminoans"]),
        item("species-karkarodon", "karkarodons", "canon/legends", "sharklike aquatic sentients including Separatist commander Riff Tamson", "Use as aquatic soldiers, predators, or officials; water dominance changes encounter geometry.", ["karkarodon", "karkarodons"]),
        item("species-kel-dor", "kel dor", "canon/legends", "Dorin natives requiring masks and goggles in oxygen-rich atmospheres", "Use atmosphere vulnerability, Jedi traditions, and pressure on life-support gear as real stakes.", ["kel dor", "kel-dor", "dorin"]),
        item("species-kiffar", "kiffar", "canon/legends", "near-human culture from Kiffu/Kiffex with clan markings and psychometry in some bloodlines", "Use for guardians, prison-world politics, memory clues, and clan obligations.", ["kiffar", "kiffu", "kiffex"]),
        item("species-klatooinian", "klatooinians", "canon/legends", "Nikto-adjacent Hutt client species with long servitude history", "Use as guards, debt soldiers, emancipated workers, or people caught in Hutt legal customs.", ["klatooinian", "klatooinians"]),
        item("species-korun", "korunnai", "canon/legends", "Haruun Kal human population with strong jungle warfare and force-sensitive traditions in Legends", "Use for partisan warfare, trauma, and local force culture; label Legends details clearly.", ["korunnai", "haruun kal"]),
        item("species-kubaz", "kubaz", "canon/legends", "long-snouted sentients often used as spies, scouts, or insectivorous travelers", "Use for surveillance, informants, xenophobic suspicion, and unusual dietary needs.", ["kubaz"]),
        item("species-lannik", "lannik", "canon/legends", "short tough sentients including Jedi Even Piell", "Use for underestimated fighters, stubborn negotiators, and compact-size tactical details.", ["lannik"]),
        item("species-lasat", "lasat", "canon", "large strong sentients from Lasan, nearly destroyed by Imperial violence", "Use for survivor grief, honor guards, refugee identity, and the Ashla/prophecy thread only where relevant.", ["lasat", "lasan"]),
        item("species-lorrdian", "lorrdians", "legends primary", "near-human culture famous for kinetic communication after historic oppression", "Use for body-language expertise, trauma-coded etiquette, and silent communication under surveillance.", ["lorrdian", "lorrdians"]),
        item("species-massassi", "massassi", "canon/legends", "Sith species warrior caste or descendants tied to Yavin temples in Legends", "Use for ancient Sith ruins, mutated guardians, and history; canon-only treatment should stay vague.", ["massassi"]),
        item("species-miraluka", "miraluka", "legends primary", "near-human force-seeing sentients without normal eyes", "Use in Legends/mixed games for force perception, blindness assumptions, and worlds wounded by Sith violence.", ["miraluka"]),
        item("species-muun", "muuns", "canon/legends", "tall Banking Clan species associated with finance, law, and long institutional memory", "Use for bankers, creditors, economic villains, or precise neutral professionals.", ["muun", "muuns", "banking clan species"]),
        item("species-nagai", "nagai", "legends primary", "near-human extragalactic/unknown-region-associated warriors and infiltrators", "Use for obscure Legends threats, elegant violence, and postwar displacement.", ["nagai"]),
        item("species-nautolan", "nautolans", "canon/legends", "amphibious sentients with head tendrils sensitive to chemicals/emotions in water", "Use underwater competence, social scent reads, and vulnerability in dry or polluted environments.", ["nautolan", "nautolans"]),
        item("species-neimoidian", "neimoidians", "canon/legends", "Duros-related trade culture central to Trade Federation leadership", "Use for merchants, separatist politics, fear of liability, and post-war prejudice.", ["neimoidian", "neimoidians"]),
        item("species-nikto-subgroups", "nikto subgroups", "canon/legends", "multiple Nikto peoples shaped by harsh Kintan history and Hutt servitude", "Use subgroup differences for guards, pilgrims, laborers, and people escaping cartel expectation.", ["nikto subgroups", "kajain'sa'nikto", "kadas'sa'nikto"]),
        item("species-omwati", "omwati", "legends primary", "blue-skinned avian near-humans exploited for scientific aptitude in Legends", "Use for Imperial science abuse, genius pressure, and survivors of weapon projects.", ["omwati"]),
        item("species-pauan-utai", "pauans and utai", "canon/legends", "Utapau's tall administrators and small laboring Utai with sinkhole-city culture", "Use for class tension, vertical cities, creature stables, and occupation memories.", ["pauan", "utai", "utapau species"]),
        item("species-phindian", "phindians", "canon/legends", "thin-faced sentients from Phindar with trade and memory-wipe plot history in Legends", "Use for old Republic intrigue, biotech crime, and merchant networks.", ["phindian", "phindians"]),
        item("species-quermian", "quermians", "canon/legends", "long-necked multi-limbed sentients related in some sources to Xexto", "Use for diplomats, Jedi, and alien body-plan constraints in chairs, armor, and restraints.", ["quermian", "quermians"]),
        item("species-rakata-survivors", "rakata survivors", "legends primary", "descendants of ancient Infinite Empire reduced after losing force-linked technology", "Use as ruin keepers, dangerous isolationists, or victims of their own ancestral empire.", ["rakata survivors", "rakatan survivors"]),
        item("species-rattataki", "rattataki", "legends primary; canon-adjacent designs vary", "pale near-humans associated with gladiatorial warfare and Asajj-style visual confusion", "Use for arena culture and warlords; do not conflate automatically with Dathomiri Nightsisters.", ["rattataki"]),
        item("species-skakoan", "skakoans", "canon/legends", "pressure-suited sentients from Skako, associated with Techno Union leadership", "Use life-support suits, industrial politics, and corporate engineering power.", ["skakoan", "skakoans"]),
        item("species-sluissi", "sluissi", "legends primary", "serpentine starship engineers known for careful work", "Use shipyard repair, slow precision, and logistical constraints in humanoid-designed spaces.", ["sluissi"]),
        item("species-sullustan", "sullustans", "canon/legends", "subterranean sentients known for piloting, navigation, and SoroSuub corporate power", "Use tunnels, corporate towns, rebel pilots, and low-light technical scenes.", ["sullustan", "sullustans", "sullust"]),
        item("species-talortai", "talortai", "canon", "avian sentients with long lives and warrior figures like Lord Maul's era contacts", "Use as rare veteran duelists or scouts; scarcity should make recognition uncertain.", ["talortai"]),
        item("species-talz", "talz", "canon/legends", "four-eyed furred sentients from cold environments and colonial conflict stories", "Use for oppressed frontier communities, cold-weather survival, and language barriers.", ["talz"]),
        item("species-thakwaash", "thakwaash", "legends primary", "large equine sentients with compartmentalized personality traits in Legends", "Use carefully for alien cognition and pilot/warrior roles without reducing them to a gimmick.", ["thakwaash"]),
        item("species-toydarian", "toydarians", "canon/legends", "winged sentients with strong will and resistance to some mind tricks in film portrayal", "Use merchants and practical negotiators; force resistance is not universal immunity.", ["toydarian", "toydarians"]),
        item("species-tusken-culture", "tusken raider culture", "canon/legends", "Indigenous Tatooine cultures with clans, sign language, sacred customs, raids, and survival law", "Use as people with territory and history, not disposable raiders; outsiders trigger risk through ignorance.", ["tusken culture", "sand people customs", "tusken clans"], priority=2),
        item("species-umbaran", "umbarans", "canon/legends", "pale shadow-world sentients with advanced technology and political complexity", "Use for clone wars trauma, low-light tactics, social subtlety, and tech unease.", ["umbaran", "umbarans", "umbara"]),
        item("species-voss", "voss", "legends primary", "mystic society from SWTOR-era Voss with commandos and interpreters of visions", "Use for Old Republic prophecy politics and outsider restriction; not default canon.", ["voss species", "voss mystics"]),
        item("species-whiphid", "whiphids", "canon/legends", "large tusked cold-world sentients often used as hunters or enforcers", "Use for survival guides, mercenaries, or migrants; size and cold adaptation matter.", ["whiphid", "whiphids"]),
        item("species-yarkora", "yarkora", "canon/legends", "long-necked, trunked sentients rarely encountered", "Use as obscure aliens, sages, or quiet observers in crowded ports.", ["yarkora"]),
        item("species-yinchorri", "yinchorri", "legends primary", "aggressive reptilian sentients resistant to some force influence in Legends", "Use for prequel-era military crises or anti-Jedi encounters; label as Legends when needed.", ["yinchorri"]),
        item("species-zeltron", "zeltrons", "legends primary; some canon usage varies", "near-human empathic culture associated with pleasure, hospitality, and pheromones", "Use for emotional intelligence, diplomacy, trauma masking, and social consent; pheromones are not mind control.", ["zeltron", "zeltrons", "zeltros"]),
    ],
    "Kyber RPG 09 - Creatures and Hazards.json": [
        item("hazard-acid-rain", "acid rain and caustic weather", "setting baseline", "industrial or exotic-weather hazard that degrades armor, skin, optics, and exposed gear", "Use as countdown pressure; threat damages seals, optics, packs, or evidence.", ["acid rain", "caustic weather"]),
        item("creature-aiwha", "aiwha", "canon/legends", "large flying/aquatic Kaminoan mount creature", "Use for storm flight, ocean recovery, and exposed rider checks in bad weather.", ["aiwha"]),
        item("creature-anooba", "anoobas", "canon/legends", "pack predators used by hunters such as Embo", "Use for pursuit scenes, scent tracking, and perimeter pressure.", ["anooba", "anoobas"]),
        item("creature-bando-gora-horror", "bando gora biohazards", "legends primary", "cult and chemical horror tied to death sticks, madness, and body modification in Bounty Hunter-era lore", "Use for underworld horror, addiction, and occult-crime scenes; keep continuity labeled.", ["bando gora biohazard", "bando gora"]),
        item("creature-bantha", "banthas", "canon/legends", "large herd mounts central to Tusken and desert travel", "Use as culture-bearing animals, transport, scent/noise complications, and survival resource.", ["bantha", "banthas"]),
        item("creature-blurrg", "blurrgs", "canon/legends", "stout reptilian mounts used on harsh frontier worlds", "Use as rugged transport with handling checks, smell, feeding, and panic under fire.", ["blurrg", "blurrgs"]),
        item("hazard-boiling-coolant", "boiling coolant leaks", "setting baseline", "industrial leak hazard with steam burns, slick floors, toxic additives, and visibility loss", "Use in undercity/substation scenes; threat damages skin, optics, breath masks, or stealth.", ["boiling coolant", "coolant leak"]),
        item("creature-boma", "bomas", "legends primary", "Onderon/Dxun reptilian predators and war beasts", "Use for jungle ambush, beast-rider cultures, and disease from bites.", ["boma", "bomas"]),
        item("creature-bordok", "bordoks", "canon/legends", "Endor pack/ride animals associated with Ewoks", "Use for forest travel, gentle mounts, or scared herd complications.", ["bordok", "bordoks"]),
        item("creature-cannok", "cannoks", "legends primary", "Dxun scavenger creatures known for eating gear in KOTOR", "Use as nuisance that becomes serious when it destroys power packs, ration seals, or evidence.", ["cannok", "cannoks"]),
        item("hazard-carbon-freeze", "carbon-freezing trauma", "canon/legends", "medical and neurological danger from carbonite freezing, especially rushed or improvised freezes", "Use hibernation sickness, blindness, panic, and equipment failure as consequences.", ["carbon-freezing trauma", "hibernation sickness"]),
        item("creature-colo-claw-fish", "colo claw fish", "canon/legends", "large Naboo core predator", "Use as underwater scale threat; survival depends on vehicles, sensors, and bigger predators.", ["colo claw fish"]),
        item("creature-condor-dragon", "condor dragon", "canon", "large winged predator of the Endor moon", "Use for forest canopy danger and sudden aerial extraction risk.", ["condor dragon"]),
        item("creature-corridor-ghoul", "undercity feral packs", "original setting-compatible", "feral sentients or animals living in abandoned urban service levels", "Use as moral hazard; hunger, sickness, and territory make violence messy, not heroic.", ["undercity feral pack", "feral lower levels"]),
        item("creature-cyborg-spider", "bt-16 perimeter droids", "setting baseline", "small security droids, crawler mines, or improvised perimeter bots in industrial spaces", "Use as traps that mark, shock, follow, or call guards rather than simply explode.", ["perimeter droid", "crawler mine"]),
        item("creature-dewback", "dewbacks", "canon/legends", "large Tatooine reptilian mounts used by locals and Imperial patrols", "Use for desert patrol signs, scent, tracks, and low-speed pursuit.", ["dewback", "dewbacks"]),
        item("hazard-dioxin-smog", "toxic smog pockets", "setting baseline", "localized chemical fog in factories, lower cities, crash sites, or war zones", "Use as strain, coughing, sensor distortion, and forced mask decisions.", ["toxic smog", "chemical fog"]),
        item("creature-dragonsnake", "dragonsnakes", "canon/legends", "Dagobah swamp predator capable of drowning or dragging prey", "Use as waterline ambush; mud, visibility, and panic matter.", ["dragonsnake", "dragonsnakes"]),
        item("hazard-electrical-arc", "exposed power arcs", "setting baseline", "damaged conduits throwing lethal arcs through wet metal or cramped corridors", "Use as positioning hazard; threat shorts gear, seals exits, or reveals position.", ["power arc", "exposed conduit", "electrical arc"]),
        item("creature-fambaa", "fambaa", "canon/legends", "massive Gungan shield-bearing beasts", "Use as battlefield terrain and living logistical asset, not normal mount.", ["fambaa", "fambaa shield"]),
        item("creature-fathier", "fathiers", "canon", "large racing animals exploited at Canto Bight", "Use for rich-world cruelty, racing debt, stampedes, and animal liberation complications.", ["fathier", "fathiers"]),
        item("hazard-flash-fire", "flash fires", "setting baseline", "fuel vapor, tibanna leaks, dust, or chemical aerosol causing sudden fires", "Use to punish blaster shots in bad environments and force hard rescue/escape choices.", ["flash fire", "fuel vapor ignition"]),
        item("creature-gorax", "gorax", "canon/legends", "giant Endor predator from Ewok lore", "Use as mythic-scale local threat; villagers know terrain and taboos better than offworlders.", ["gorax"]),
        item("creature-gralloc", "grallocs", "legends primary", "large dangerous herd/predator creatures used in wilderness material", "Use for stampedes, hunting scenes, and non-evil animal danger.", ["gralloc", "grallocs"]),
        item("creature-ikopi", "ikopi", "canon/legends", "Naboo herd animal seen in open grassland ecology", "Use as prey, herd movement clue, or hunting-law issue.", ["ikopi"]),
        item("hazard-ion-storm", "ion storms", "canon/legends", "space or atmospheric storm interfering with shields, sensors, droids, and comms", "Use to isolate parties and make navigation rolls consequential.", ["ion storm", "ion storms"]),
        item("creature-keeradak", "keeradaks", "canon", "winged Skako Minor creatures used by locals in Clone Wars scenes", "Use for vertical terrain travel and fragile alliances with native handlers.", ["keeradak", "keeradaks"]),
        item("creature-krayt-dragon", "krayt dragons", "canon/legends", "massive Tatooine apex predators with pearls and deep cultural meaning", "Use as territory-scale threat; killing one has ecological and cultural consequences.", ["krayt dragon", "krayt dragons"]),
        item("hazard-mynock-infestation", "mynock infestation", "canon/legends", "ship parasite problem that drains systems, damages cables, and delays travel", "Use as maintenance crisis that can expose smugglers to patrol timing.", ["mynock infestation", "mynocks on hull"]),
        item("creature-narglatch", "narglatches", "canon/legends", "large feline predators used as mounts or beasts on Orto Plutonia and elsewhere", "Use cold-world pursuit, beast handling, and intimidating cavalry.", ["narglatch", "narglatches"]),
        item("hazard-neurotoxin-darts", "neurotoxin darts", "setting baseline", "assassin or hunter toxin delivery through darts, needles, or microinjectors", "Use delayed symptoms, antidote scarcity, and forensic clues rather than instant death.", ["neurotoxin dart", "poison dart"]),
        item("creature-opee-sea-killer", "opee sea killer", "canon/legends", "Naboo deep-water predator with long tongue and huge jaws", "Use vehicle-scale underwater chase; bigger-fish ecology can alter stakes.", ["opee sea killer"]),
        item("creature-porg", "porgs", "canon", "Ahch-To seabirds that are curious, edible, loud, and intrusive", "Use as local ecology and nuisance clues, not combat threats.", ["porg", "porgs"]),
        item("creature-rancor-culture", "rancor handling", "canon/legends", "rancors are dangerous predators but can be bonded, trained, or culturally important", "Use handlers, grief, feeding, restraints, and terrain; not every rancor is just a pit monster.", ["rancor handling", "trained rancor"]),
        item("hazard-radiation-hot-zone", "radiation hot zones", "setting baseline", "reactor leaks, crashed ships, orbital bombardment scars, or exotic mineral exposure", "Use ticking injury, sensor warnings, suit checks, and long-term consequences.", ["radiation hot zone", "reactor radiation"]),
        item("creature-roggwart", "roggwarts", "canon/legends", "large predatory beast used by Separatists/Geonosians", "Use as arena or guard-beast threat with reach, smell, and handler weakness.", ["roggwart", "roggwarts"]),
        item("creature-sando-aqua", "sando aqua monster", "canon/legends", "enormous Naboo sea predator", "Use as a scale reminder: some threats are environmental, not enemies to defeat.", ["sando aqua monster"]),
        item("creature-sarlacc", "sarlaccs", "canon/legends", "pit predator with tentacles, beak, digestive horror, and local myth", "Use as terrain hazard, execution site, and salvage/cult location after death.", ["sarlacc", "sarlaccs"]),
        item("hazard-sewer-gas", "sewer gas and low oxygen", "setting baseline", "methane, rot gas, coolant vapor, or oxygen displacement in lower levels", "Use explosions, hallucination, unconsciousness, and bad sensor readings.", ["sewer gas", "low oxygen", "oxygen displacement"]),
        item("creature-shyrack", "shyracks", "legends primary", "batlike cave swarms from Korriban in KOTOR-era lore", "Use sith tomb noise, swarm panic, and fragile footing.", ["shyrack", "shyracks"]),
        item("creature-tauntaun", "tauntauns", "canon/legends", "Hoth riding animals vulnerable to cold, predators, and panic", "Use as survival transport; injured mounts create hard moral/logistical choices.", ["tauntaun", "tauntauns"]),
        item("hazard-vacuum-ice", "vacuum frost and seal failure", "setting baseline", "rapid freezing, brittle seals, and oxygen loss during hard-vacuum exposure", "Use for hullwalks and suit breaches; threat marks suit damage or lost tools.", ["vacuum frost", "seal failure"]),
        item("creature-wampa", "wampas", "canon/legends", "Hoth apex predator with ambush tactics and lair behavior", "Use as stealth predator; tracks, smell, and missing patrols foreshadow danger.", ["wampa", "wampas"]),
        item("creature-wraid", "wraids", "legends primary", "large desert predators hunted on Tatooine/Korriban in game lore", "Use as old RPG wilderness threat; hide, ambush, and heat matter.", ["wraid", "wraids"]),
    ],
    "Kyber RPG 07 - Society Law Economy.json": [
        item("society-bail-bonds", "bail bonds and legal surety", "setting baseline", "local courts, sector posts, and private sureties can release suspects for money or collateral", "Use to convert arrest into debt, leverage, missed court dates, and bounty authorization.", ["bail bond", "legal surety"]),
        item("society-black-market-medicine", "black market medicine", "canon/legends", "illegal clinics sell bacta, cybernetics, organs, forged records, and quiet deaths", "Use with infection risk, debt, predatory doctors, and law-enforcement traces.", ["black market medicine", "illegal clinic"]),
        item("society-bounty-paperwork", "bounty paperwork", "canon/legends", "bounty legality depends on issuer, jurisdiction, capture terms, proof, and delivery condition", "Use to stop murderhobo play; wrong body, wrong world, or dead target can void payment.", ["bounty paperwork", "bounty license", "capture terms"]),
        item("society-chain-codes", "chain codes and identity records", "canon", "Imperial and later systems track identity through official codes, documents, and databases", "Use records checks, aliases, stolen identities, and exposure through bureaucracy.", ["chain code", "identity record"]),
        item("society-checkpoint-bribes", "checkpoint bribes", "setting baseline", "low-level officials may accept money, favors, contraband, or future leverage", "Use bribes as risky, priced, and recordable; a bribe can become blackmail.", ["checkpoint bribe", "inspection bribe"]),
        item("society-civilian-curfew", "civilian curfews", "canon/legends", "occupation forces restrict movement after attacks, unrest, or political incidents", "Use curfews to make timing, forged passes, and local shelter meaningful.", ["civilian curfew", "sector curfew"]),
        item("society-contraband-grades", "contraband grades", "setting baseline", "items vary from taxed goods to restricted tech, weapons, spice, artifacts, and military hardware", "Use graduated consequences instead of binary legal/illegal treatment.", ["contraband grade", "restricted cargo"]),
        item("society-credit-tracing", "credit tracing", "canon/legends", "digital credits, bank transfers, marked chits, and exchange logs can expose movement", "Use money as evidence; laundering costs time and fees.", ["credit tracing", "marked credits"]),
        item("society-customs-seizure", "customs seizure", "setting baseline", "ports can impound cargo, ships, droids, animals, weapons, or documents pending review", "Use seizure as a nonlethal consequence that still hurts badly.", ["customs seizure", "impounded cargo"]),
        item("society-debt-peonage", "debt peonage", "canon/legends", "criminal and corporate systems convert debt into forced work, ship liens, or family pressure", "Use debt as brutal continuing consequence, not background flavor.", ["debt peonage", "debt labor", "ship lien"]),
        item("society-droid-rights", "droid rights and restraining bolts", "canon/legends", "droids range from property to companions depending on owner, region, and era", "Use memory wipes, restraining bolts, labor exploitation, and emancipation conflicts.", ["droid rights", "restraining bolt law"]),
        item("society-forged-permits", "forged permits", "setting baseline", "false permits pass only the checks they were built for", "Use cursory pass, database failure, supervisor challenge, and burned identity consequences.", ["forged permit", "fake work permit"]),
        item("society-front-companies", "front companies", "canon/legends", "criminals and intelligence services hide payments, cargo, and property behind shell businesses", "Use paper trails, false manifests, and accountants as adventure clues.", ["front company", "shell company"]),
        item("society-gang-protection", "gang protection rackets", "canon/legends", "local gangs charge businesses for safety from the gang itself or from rivals", "Use weekly payments, public examples, informants, and impossible neutrality.", ["protection racket", "gang tax"]),
        item("society-holonet-censorship", "holonet censorship", "canon/legends", "governments and corporations throttle news, flag keywords, and flood channels with propaganda", "Use misinformation and message delay; public truth needs proof and distribution.", ["holonet censorship", "propaganda filter"]),
        item("society-impound-fees", "impound fees", "setting baseline", "ports and authorities charge escalating fees while holding vehicles or cargo", "Use to drain credits and force favors without needing a firefight.", ["impound fee", "docking impound"]),
        item("society-informant-economy", "informant economy", "setting baseline", "tips are bought with credits, favors, fear, ideology, revenge, or legal mercy", "Use informants as unreliable assets with motives and exposure risk.", ["informant economy", "paid informant"]),
        item("society-insurance-salvage", "insurance and salvage fraud", "canon/legends", "ship losses, cargo theft, and battlefield salvage generate claims and scams", "Use auditors, fake pirates, staged wrecks, and angry underwriters.", ["salvage fraud", "insurance scam"]),
        item("society-jurisdiction-conflict", "jurisdiction conflicts", "setting baseline", "local police, sector forces, Imperials, guilds, and private security may all claim authority", "Use overlapping authority to create delay, corruption, and loopholes.", ["jurisdiction conflict", "sector jurisdiction"]),
        item("society-labor-contracts", "indenture and labor contracts", "canon/legends", "legal language can trap workers short of open slavery", "Use contract debt, dock fees, medical charges, and family remittances as grim pressure.", ["indenture contract", "labor contract"]),
        item("society-local-currency", "local currency and barter", "canon/legends", "credits are not always trusted; worlds may require pegged currency, barter, or hard goods", "Use conversion loss, counterfeit risk, and emergency barter.", ["local currency", "barter economy"]),
        item("society-military-requisition", "military requisition", "canon/legends", "armies seize ships, food, fuel, medical supplies, or buildings under emergency authority", "Use as lawful theft with paperwork and intimidation.", ["military requisition", "emergency requisition"]),
        item("society-noble-hostage", "noble hostage customs", "canon/legends", "courts and clans may use wards, hostages, marriages, and sworn guests to enforce deals", "Use formal hospitality as danger; breaking custom can start feuds.", ["noble hostage", "guest right"]),
        item("society-prison-transport", "prison transports", "canon/legends", "captives move through shuttles, cages, records, guards, med checks, and transfer windows", "Use capture as playable logistics with escape windows and surveillance.", ["prison transport", "prisoner transfer"]),
        item("society-refugee-camps", "refugee camps", "canon/legends", "war, planetary disaster, and occupation produce camps with aid politics and black markets", "Use scarcity, family separation, recruitment, disease, and exploitation.", ["refugee camp", "displaced civilians"]),
        item("society-reputation-ledger", "underworld reputation ledgers", "canon/legends", "criminal networks track favors, betrayals, prices, and protection status", "Use consequences across sessions; one betrayal changes access and prices.", ["underworld reputation", "reputation ledger"]),
        item("society-salvage-rights", "salvage rights", "canon/legends", "ownership of wrecks depends on jurisdiction, war status, beacon claims, and corporate contracts", "Use legal salvage vs theft as a live problem.", ["salvage rights", "wreck claim"]),
        item("society-sector-post", "sector post procedure", "setting baseline", "arrests lead to booking, search, interrogation, chain-code checks, and evidence intake", "Use procedure to ground Imperial/local law scenes and give players windows to act.", ["sector post", "booking procedure"]),
        item("society-slavery-legal-zones", "slavery legal zones", "canon/legends", "slavery is illegal in some governments and openly practiced or disguised elsewhere", "Use jurisdiction and hypocrisy; rescue creates retaliation and paperwork problems.", ["slavery legal zone", "slave market law"]),
        item("society-spice-economy", "spice economy", "canon/legends", "spice ranges from medicine to narcotic to industrial precursor depending type and law", "Use type, purity, route, cartel, and enforcement rather than generic drug language.", ["spice economy", "spice route"]),
        item("society-starport-rating", "starport ratings", "canon/legends", "ports differ in repair, fuel, customs, docking, medical, law, and black-market access", "Use starport quality to shape travel consequences and available gear.", ["starport rating", "port rating"]),
        item("society-tariffs", "tariffs and port fees", "setting baseline", "legal trade bleeds money through docking, customs, cargo inspection, and local taxes", "Use to keep crews poor and make smuggling economically tempting.", ["tariff", "port fee", "docking fee"]),
        item("society-war-profiteers", "war profiteers", "canon/legends", "merchants, nobles, corporations, and criminals profit from both sides of a conflict", "Use moral rot, double contracts, and evidence trails.", ["war profiteer", "war profiteers"]),
        item("society-witness-protection", "witness protection and extraction", "setting baseline", "informants need relocation, new documents, medical disguise, and silence", "Use extraction as hard logistics; leaks create pursuit.", ["witness protection", "informant extraction"]),
    ],
    "Kyber RPG 13 - Force Metaphysics Artifacts.json": [
        item("force-amulet", "sith amulets", "canon/legends", "dark-side artifacts storing fear, authority, memory, poison, or ritual focus", "Use as corrupting leverage and clue object; never just a stat bonus.", ["sith amulet", "sith amulets"]),
        item("force-dark-side-cave", "dark side cave tests", "canon/legends", "vergences or tainted places that confront fear, memory, and temptation", "Use visions as pressure and symbolic truth, not perfect prophecy.", ["dark side cave", "cave vision"]),
        item("force-dathomir-ichor", "nightsister ichor", "canon", "green magickal energy used in Nightsister rituals, illusions, conjurations, and transformations", "Use as culturally specific magick, not generic Jedi/Sith power.", ["nightsister ichor", "green ichor"]),
        item("force-dyad", "force dyad", "canon", "rare bond between two beings with extreme connection and transfer effects", "Use only for major plot-scale characters; do not hand out casually.", ["force dyad", "dyad in the force"]),
        item("force-echoes", "force echoes", "canon/legends", "impressions of past events, emotions, or objects perceived through the Force", "Use for fragments, sensory flashes, and ambiguity; echoes should not solve mysteries alone.", ["force echo", "force echoes"]),
        item("force-exegol-rituals", "exegol sith rituals", "canon", "Sith Eternal rites involving cloning, essence, cult labor, and fleet-scale hidden industry", "Use body horror, failed vessels, cult logistics, and secrecy rather than simple resurrection magic.", ["exegol ritual", "sith eternal ritual"]),
        item("force-holocron-gatekeeper", "holocron gatekeepers", "canon/legends", "interactive persona/interface preserving knowledge with bias and access tests", "Use as unreliable teacher with agenda, limits, and security protocols.", ["holocron gatekeeper", "gatekeeper persona"]),
        item("force-jedi-beacon", "jedi emergency beacons", "canon/legends", "signals, caches, or coded calls that can summon survivors or traps after the Purge", "Use as moral bait: calling for help may expose hidden Jedi.", ["jedi beacon", "emergency jedi signal"]),
        item("force-kyber-singing", "kyber resonance", "canon/legends", "crystals resonate with living Force, trauma, alignment, and construction contexts", "Use subtle sound, heat, pressure, and emotion; avoid making kyber a vending-machine gem.", ["kyber resonance", "kyber singing"]),
        item("force-living-planet", "living planets", "legends primary", "rare worlds with consciousness or force/ecological identity such as Zonama Sekot", "Use as campaign-scale mystery; communication should be indirect and alien.", ["living planet", "sentient planet"]),
        item("force-malachor-wound", "malachor wound", "canon/legends", "ancient Sith/Jedi catastrophe sites carry weapons, echoes, and spiritual damage", "Use as oppressive terrain that worsens fear, rivalry, and temptation.", ["malachor wound", "malachor echo"]),
        item("force-mortis-symbolism", "mortis symbolism", "canon", "Father, Son, Daughter imagery represents cosmic balance, temptation, and sacrifice", "Use as mythic signal, not easy exposition or regular travel destination.", ["mortis symbolism", "father son daughter"]),
        item("force-nexus-corruption", "force nexus corruption", "canon/legends", "strong sites can amplify emotion, visions, healing, rage, or despair", "Use mechanical pressure through fear, strain, conflict, and distorted perception.", ["force nexus corruption", "dark side nexus"]),
        item("force-possessed-mask", "possessed masks", "canon/legends", "helmets or masks may carry identity, memory, cult authority, or dark-side imprint", "Use for obsession and influence; player agency should erode through choices, not instant control.", ["possessed mask", "haunted mask"]),
        item("force-sith-alchemy-lab", "sith alchemy laboratories", "canon/legends", "places of altered beasts, preserved organs, poisons, kyber abuse, and ritual apparatus", "Use hazards, evidence, and moral cost; labs should feel clinical and profane.", ["sith alchemy lab", "sith laboratory"]),
        item("force-spirit-anchor", "spirit anchors", "canon/legends", "objects, tombs, places, or unfinished vows can bind an imprint or spirit-like presence", "Use as haunting rule: remove anchor, resolve vow, or survive temptation.", ["spirit anchor", "force haunting"]),
        item("force-temple-guardian", "temple guardian constructs", "canon/legends", "droids, beasts, puzzles, illusions, or bound spirits protecting sacred sites", "Use guardian logic tied to doctrine, not random dungeon traps.", ["temple guardian", "jedi temple guardian"]),
        item("force-vergences", "vergences in the force", "canon/legends", "places or beings where the Force concentrates unusually", "Use as rare plot gravity with risk, visions, attention, and competing claims.", ["vergence", "vergences in the force"]),
        item("force-vision-cost", "vision cost", "setting baseline", "visions can exhaust, mislead, tempt, or reveal only emotionally framed fragments", "Use to stop prophecy from becoming perfect scouting.", ["vision cost", "force vision consequence"]),
        item("force-world-between-worlds-access", "world between worlds access", "canon", "mystic pathways connected to portals, voices, and time-adjacent perception", "Use only with major canon-aware restraint; access is rare, guarded, and dangerous.", ["world between worlds access", "lothal portal"]),
    ],
    "Kyber RPG 14 - Legends Supplements.json": [
        item("legends-adumar", "adumar and starfighter diplomacy", "legends", "post-Endor world where starfighter honor culture intersects diplomacy", "Use for fighter-ace politics, absurd formal duels, and diplomatic pressure in Legends campaigns.", ["adumar", "starfighters of adumar"]),
        item("legends-alsakan", "alsakan conflicts", "legends", "Core World rival to Coruscant in ancient Republic political-military disputes", "Use as deep-history Core politics and old grudges in archives or noble claims.", ["alsakan conflicts", "alsakan"]),
        item("legends-caamas-document", "caamas document crisis", "legends", "New Republic political crisis over Bothan involvement in Caamas devastation", "Use for evidence politics, guilt, riots, and intelligence blackmail.", ["caamas document", "caamas crisis"]),
        item("legends-centerpoint", "centerpoint station legends", "legends", "ancient megastructure linked to Corellian system and gravity-scale power", "Use as impossible archaeology and political deterrent; not casual superweapon loot.", ["centerpoint station legends", "centerpoint"]),
        item("legends-courtship", "courtship of princess leia crisis", "legends", "Hapes, Dathomir, warlord politics, and marriage diplomacy intersecting after Endor", "Use as Hapan/Dathomiri political background only in Legends continuity.", ["courtship crisis", "courtship of princess leia"]),
        item("legends-crimson-empire", "crimson empire", "legends", "post-Endor Royal Guard power struggle and Imperial succession violence", "Use for red-armored assassins, loyalty cults, and remnant intrigue.", ["crimson empire", "kir kanos", "carnor jax"]),
        item("legends-daala", "natasi daala campaigns", "legends", "Imperial admiral linked to Maw Installation and later remnant politics", "Use for secret weapons facilities, hardline strategy, and Imperial faction conflict.", ["natasi daala", "admiral daala"]),
        item("legends-empires-end", "empire's end legends", "legends", "Dark Empire aftermath involving Palpatine clone failure and Sith-related endgame", "Use only in Legends resurrection branch; do not mix with canon Exegol without label.", ["empire's end legends", "empires end"]),
        item("legends-galactic-alliance", "galactic alliance legends", "legends", "successor government formed after New Republic collapse during Yuuzhan Vong War", "Use for postwar politics, military fatigue, and legitimacy problems.", ["galactic alliance legends", "gffa"]),
        item("legends-hand-of-thrawn", "hand of thrawn crisis", "legends", "Thrawn-related deception, Imperial peace, and information warfare crisis", "Use for fake returns, document scandals, and peace negotiations.", ["hand of thrawn", "nirauan"]),
        item("legends-jedi-academy-yavin", "jedi academy trilogy crisis", "legends", "Luke's Yavin academy faces Exar Kun's spirit, students, and Imperial weapons", "Use for early academy vulnerability and haunted training grounds.", ["jedi academy trilogy", "yavin academy crisis"]),
        item("legends-katana-fleet", "katana fleet", "legends", "lost dreadnaught fleet central to Thrawn-era military race", "Use for salvage war, old automation, and competing claims.", ["katana fleet", "dark force fleet"]),
        item("legends-kessel-run-detail", "kessel run legends detail", "legends/canon varies", "route through dangerous spatial hazards around Kessel with smuggling reputation", "Use as dangerous navigation and bragging-rights lore; avoid exact-detail conflicts by era.", ["kessel run legends", "maw kessel route"]),
        item("legends-killik-crisis", "dark nest crisis", "legends", "post-NJO Killik/joiner crisis involving Jedi, Chiss, and collective identity", "Use for hive assimilation, border war, and memory contamination.", ["dark nest crisis", "killik crisis"]),
        item("legends-lost-tribe", "lost tribe of the sith legends", "legends", "isolated Sith society on Kesh surviving from ancient history", "Use for culture-shock Sith, dynastic politics, and isolated dark-side society.", ["lost tribe legends", "sith on kesh"]),
        item("legends-lusankya", "lusankya", "legends", "Super Star Destroyer hidden under Coruscant and tied to Ysanne Isard", "Use for Imperial secret infrastructure and impossible urban-scale revelation.", ["lusankya", "ysanne isard"]),
        item("legends-maw-installation", "maw installation", "legends", "secret Imperial research site near black holes producing superweapon projects", "Use for hidden labs, black budgets, and scientist moral collapse.", ["maw installation", "maw research"]),
        item("legends-nagai-tof", "nagai and tof war", "legends", "early post-Endor extragalactic/Unknown Regions conflict arc", "Use for obscure invaders, displacement, and alien diplomacy in Legends games.", ["nagai tof war", "tof invaders"]),
        item("legends-nomi-sunrider", "nomi sunrider", "legends", "Tales of the Jedi-era Jedi leader and battle meditation figure", "Use for ancient Jedi exemplars, archives, and old Republic legacy.", ["nomi sunrider"]),
        item("legends-plagueis-novel", "darth plagueis legends detail", "legends with canon overlap", "expanded Sith political and banking conspiracy around Plagueis and Sidious", "Use to enrich prequel intrigue only when clearly labeled; canon has less detail.", ["darth plagueis legends", "hego damask"]),
        item("legends-prince-xizor", "prince xizor", "legends", "Black Sun leader and rival power player during Shadows-era continuity", "Use for criminal nobility, Falleen intrigue, and Vader/underworld triangulation.", ["prince xizor", "xizor"]),
        item("legends-rogue-squadron", "rogue squadron campaigns legends", "legends", "post-Endor starfighter campaigns led by Wedge and allies", "Use for fighter missions, liberation operations, and pilot reputation.", ["rogue squadron legends", "x-wing novels"]),
        item("legends-senek-juvex", "senex-juvex sectors", "legends", "aristocratic sector cultures associated with slavery and old houses", "Use for noble cruelty, legal slavery, and Core-adjacent hypocrisy.", ["senex-juvex", "senex sector", "juvex sector"]),
        item("legends-tapani", "tapani sector", "legends", "feudal noble sector with houses, dueling, and political intrigue", "Use for court games, noble patronage, and sector-house wars.", ["tapani sector", "tapani nobles"]),
        item("legends-vong-biotech", "yuuzhan vong biotechnology", "legends", "living weapons, ships, armor, implants, and pain-shaped tools of the Vong war", "Use as alien horror and logistics, with maintenance through biology not mechanics.", ["vong biotechnology", "yuuzhan vong biotech"]),
        item("legends-wraith-squadron", "wraith squadron", "legends", "commando/starfighter unit built from misfits under Wedge Antilles", "Use for covert raids, pilot trauma, and irregular military operations.", ["wraith squadron"]),
        item("legends-xim", "xim the despot", "legends", "ancient Tionese conqueror and rival of early Hutt power", "Use as deep-time pirate/treasure/war-droid mythology.", ["xim the despot", "tionese empire"]),
        item("legends-yssane-isard", "ysanne isard", "legends", "Imperial Intelligence leader tied to Coruscant, Lusankya, and Krytos crisis", "Use for spy politics, biological terror, and remnant authoritarianism.", ["ysanne isard", "iceheart"]),
        item("legends-zhell-taung", "zhell and taung", "legends", "ancient Coruscant peoples linked to human origins and Mandalorian Taung ancestry", "Use as mythic prehistory and Mandalorian identity archaeology.", ["zhell", "taung"]),
        item("legends-zsinj-territory", "zsinj empire territory", "legends", "post-Endor warlord holdings with propaganda, shipyards, and false fronts", "Use for warlord maps, puppet governments, and raider contracts.", ["zsinj territory", "zsinj empire"]),
    ],
    "Kyber RPG 04 - Factions and Governments.json": [
        item("faction-black-sun", "black sun operations", "canon/legends", "major criminal syndicate using cells, nobles, Vigo-style leadership, and violence", "Use as professional organized crime: bribes, extortion, assassins, fronts, and plausible deniability.", ["black sun operations", "black sun vigo"], priority=2),
        item("faction-cloud-riders", "cloud-riders", "canon", "Enfys Nest's rebel-aligned marauder group opposing Crimson Dawn exploitation", "Use as morally ambiguous raiders whose targets and evidence matter.", ["cloud-riders", "enfys nest cell"]),
        item("faction-corporate-police", "corporate security forces", "canon/legends", "private armies, port police, auditors, and strike teams serving corporations", "Use when law is contractual; they protect assets, not justice.", ["corporate security force", "private police"]),
        item("faction-death-watch-cell", "death watch cells", "canon/legends", "Mandalorian militant factions using tradition, terrorism, and anti-pacifist politics", "Use splinter cells by era; do not treat all Mandalorians as Death Watch.", ["death watch cell", "death watch splinter"]),
        item("faction-haxion-brood", "haxion brood", "canon", "criminal syndicate from Jedi game continuity using bounty hunters and arena spectacle", "Use for bounty heat, gladiator captures, and underworld entertainment violence.", ["haxion brood"]),
        item("faction-imperial-customs", "imperial customs office", "canon/legends", "bureaucracy inspecting cargo, manifests, transponders, and restricted travel", "Use as low-glamour Imperial pressure that can still ruin a crew.", ["imperial customs", "customs office"]),
        item("faction-imperial-inquisitorius", "inquisitorius field cells", "canon", "Force-hunter organization using Inquisitors, purge troops, records, and fear", "Use as specialized threat with investigation buildup, not random hallway cameos.", ["inquisitorius field cell", "purge trooper detail"]),
        item("faction-local-defense-force", "local defense forces", "canon/legends", "planetary militias, system patrols, royal guards, or security fleets", "Use to make worlds feel governed even without Empire or Republic presence.", ["local defense force", "planetary militia"]),
        item("faction-mining-guild", "mining guild", "canon", "corporate guild controlling extraction sites, security, labor, and shipping", "Use for frontier exploitation, strikebreaking, permits, and industrial hazards.", ["mining guild", "guild mining claim"]),
        item("faction-new-republic-marshals", "new republic marshals", "canon", "post-Endor law agents with uneven reach and political limits", "Use for law that is legitimate but underfunded, slow, and vulnerable to local power.", ["new republic marshal", "new republic law"]),
        item("faction-partisans", "partisans cells", "canon", "Saw Gerrera-style militant rebel cells using harsh tactics and paranoia", "Use to complicate rebellion morality through collateral damage, torture, and distrust.", ["partisans cell", "saw gerrera partisans"]),
        item("faction-sith-eternal-cult", "sith eternal cult cells", "canon", "Exegol-linked cult network supporting Palpatine's hidden survival and Final Order", "Use as secret logistics, kidnapping, shipyard labor, and ritual fanaticism.", ["sith eternal cell", "sith eternal cult"]),
        item("faction-soro-suub", "soro suub corporation", "canon/legends", "major Sullustan corporation with industrial, political, and local governance influence", "Use corporate-town pressure, rebel sympathizers, and commercial leverage.", ["soro suub", "soro-suub"]),
        item("faction-zann-consortium", "zann consortium", "legends primary", "Tyber Zann's criminal empire from Empire at War expansion continuity", "Use as Legends underworld rival with corruption, black markets, and military theft.", ["zann consortium", "tyber zann"]),
        item("faction-zerek-besh", "zerek besh operations", "canon", "organized syndicate from Outlaws-era underworld centered on Sliro and high-end criminal power", "Use for elite criminal enforcement and stylish brutality; keep details canon-current.", ["zerek besh operations", "sliro syndicate"]),
    ],
    "Kyber RPG 05 - Worlds and Regions.json": [
        item("world-abregado-rae", "abregado-rae", "canon/legends", "Core-region trade world with smugglers, ports, and political traffic", "Use as a civilized place where crime hides inside bureaucracy and commerce.", ["abregado-rae", "abregado rae"]),
        item("world-agamar", "agamar", "canon/legends", "Outer Rim agricultural/backwater world with Clone Wars debris and later rebel-era relevance", "Use for salvage, veterans, and quiet worlds scarred by old battles.", ["agamar"]),
        item("world-ansion", "ansion", "legends primary", "Mid Rim world with nomadic cultures and diplomacy in pre-Clone-Wars Legends", "Use for treaty missions, local customs, and Republic neglect.", ["ansion"]),
        item("world-balmorra", "balmorra", "legends primary; canon references vary", "industrial weapons world with factories and occupations", "Use for urban warfare, arms deals, and worker resistance.", ["balmorra"]),
        item("world-bastatha", "bestine", "canon/legends", "Tatooine settlement and Imperial/rebel reference point", "Use for desert administration, patrols, and local trade.", ["bestine"]),
        item("world-bogano", "bogano", "canon", "remote world with Zeffo vault, sinkholes, and hidden Jedi research relevance", "Use for early Jedi archaeology and Imperial discovery risk.", ["bogano"]),
        item("world-bracca", "bracca", "canon", "scrapper world of ship-breaking yards and brutal worker conditions", "Use for salvage horror, guild control, and Purge-era hiding.", ["bracca"]),
        item("world-cantonica", "cantonica", "canon", "casino-rich world containing Canto Bight and exploited labor beneath luxury", "Use wealth inequality, racing, arms dealers, and performative neutrality.", ["cantonica", "canto bight"]),
        item("world-cato-neimoidia", "cato neimoidia", "canon/legends", "wealthy Neimoidian purse world with bridge cities and Clone Wars history", "Use banking, separatist stigma, and high-altitude urban hazards.", ["cato neimoidia"]),
        item("world-christophsis", "christophsis", "canon/legends", "crystal city world and Clone Wars battlefield", "Use urban crystal terrain, separatist scars, and occupation memories.", ["christophsis"]),
        item("world-csilla", "csilla", "canon/legends", "Chiss homeworld, with continuity differences around condition and accessibility", "Use Unknown Regions politics and secretive borders; do not assume easy travel.", ["csilla"]),
        item("world-daiyu", "daiyu", "canon", "dense neon underworld world with trafficking, spice, fugitives, and bribed authorities", "Use as urban grime, fake identities, and child/endangered-person stakes.", ["daiyu"]),
        item("world-dantooine", "dantooine", "canon/legends", "grassland world with rebel base mention and major Jedi enclave in Legends", "Use remote ruins, settlers, and hidden-base history by continuity.", ["dantooine"]),
        item("world-fondor", "fondor", "canon/legends", "Core shipyard world and industrial naval asset", "Use shipyard infiltration, labor, and military procurement politics.", ["fondor", "fondor shipyards"]),
        item("world-garel", "garel", "canon", "industrial/port world used by rebel cells and Imperial presence in Rebels", "Use mid-level rebel logistics and surveillance pressure.", ["garel"]),
        item("world-giju", "giju", "legends primary", "Herglic homeworld and trade-culture source", "Use for Herglic commerce, aquatic logistics, and Rimma-route history.", ["giju"]),
        item("world-haruun-kal", "haruun kal", "legends primary", "jungle world of Korunnai and brutal Clone Wars-era conflict", "Use guerrilla warfare, trauma, and local force traditions.", ["haruun kal"]),
        item("world-iego", "iego", "canon/legends", "remote world associated with moons, angels, and Separatist-era hazard", "Use myth vs reality, remote traps, and strange local reputation.", ["iego"]),
        item("world-iridonia", "iridonia", "canon/legends", "Zabrak homeworld, harsh and culturally martial in many depictions", "Use clan pride, endurance, and diaspora identity.", ["iridonia"]),
        item("world-jabiim", "jabiim", "canon/legends", "muddy war-torn world with Separatist/Republic trauma and refugee routes", "Use rain, trenches, betrayal, and extraction under fire.", ["jabiim"]),
        item("world-jedha-post", "jedha post-destruction", "canon", "shattered holy moon after Death Star test with pilgrims, partisans, and mining scars", "Use toxic ruins, faith under occupation, and collapsing terrain.", ["post-destruction jedha", "jedha ruins"]),
        item("world-kalee", "kalee", "canon/legends", "Kaleesh homeworld linked to Grievous and Huk conflict", "Use war memory, masks, anti-Republic grievance, and mercenary recruitment.", ["kalee"]),
        item("world-kintan", "kintan", "canon/legends", "Nikto homeworld tied to harsh conditions and Hutt domination", "Use cartel history, species subgroups, and labor exploitation.", ["kintan"]),
        item("world-lahmu", "lah'mu", "canon", "remote farming world where Galen Erso hid before Imperial recovery", "Use isolation, homestead surveillance, and research fugitives.", ["lah'mu", "lahmu"]),
        item("world-malastare", "malastare", "canon/legends", "Dug/Gran world, podracing venue, and Clone Wars battlefield with fuel importance", "Use fuel politics, racing, and local ethnic tension.", ["malastare"]),
        item("world-malachor", "malachor", "canon/legends", "Sith catastrophe world with superweapon/temple history in canon and separate Legends history", "Use continuity labels; always make it spiritually and physically dangerous.", ["malachor"]),
        item("world-mon-cala-depth", "mon cala deep cities", "canon/legends", "aquatic cities and shipbuilding culture shared with Quarren political tension", "Use underwater politics, pressure doors, shipyards, and civil unrest.", ["mon cala deep cities", "mon calamari cities"]),
        item("world-moraband-tombs", "moraband tomb regions", "canon", "ancient Sith tomb world visited in late Clone Wars vision arc", "Use as canon Sith graveworld with visions, dust, and predatory silence.", ["moraband tombs", "moraband sith"]),
        item("world-mustafar-later", "mustafar recovery zones", "canon", "areas around Vader's fortress later show ecological change and cultic memory", "Use lava, pilgrims, Vader relic hunters, and fragile new growth.", ["mustafar recovery", "vader fortress region"]),
        item("world-ortho-plutonia", "orto plutonia", "canon", "ice world with Talz population and Pantoran colonial tension", "Use first-contact harm, cold survival, and local sovereignty conflict.", ["orto plutonia", "pantora moon"]),
        item("world-pasaana", "pasaana", "canon", "desert world with Aki-Aki culture, festival, and Sith dagger trail", "Use crowds, pilgrims, chase visibility, and relic-hunt complications.", ["pasaana", "aki-aki"]),
        item("world-pillio", "pillio", "canon", "oceanic world with Imperial observatory/cache relevance", "Use reefs, storms, observatory secrets, and post-Endor cleanup.", ["pillio"]),
        item("world-rishi", "rishi", "canon/legends", "moon/world area used for clone listening post and pirate activity", "Use outpost isolation, pirates, and comms interception.", ["rishi moon", "rishi"]),
        item("world-ruusan", "ruusan", "canon/legends", "site tied to Ruusan reforms in canon framing and major Sith war in Legends", "Use legal history and old battlefield ghosts by continuity.", ["ruusan"]),
        item("world-saleucami", "saleucami", "canon/legends", "Outer Rim world with farms, battle history, and clone desertion stories", "Use quiet refuge, veteran guilt, and Separatist remnants.", ["saleucami"]),
        item("world-savareen", "savareen", "canon", "frontier refinery/coastal world in Solo-era underworld routes", "Use coaxium processing, beach isolation, and Crimson Dawn fallout.", ["savareen"]),
        item("world-serenno", "serenno", "canon/legends", "aristocratic world of Count Dooku with noble houses and wealth", "Use inheritance, separatist stigma, and dueling court politics.", ["serenno"]),
        item("world-shili", "shili", "canon/legends", "Togruta homeworld with predator-influenced social/cultural adaptations", "Use pack instincts, montral perception, and diaspora identity.", ["shili"]),
        item("world-skako-minor", "skako minor", "canon", "pressure/industrial world linked to Techno Union and Clone Wars rescue mission", "Use hostile atmosphere, native conflict, and corporate secrecy.", ["skako minor"]),
        item("world-starkiller-iller", "ilum to starkiller base", "canon", "Ilum was transformed by First Order excavation into Starkiller Base", "Use canon tragedy of sacred kyber world industrialized into superweapon.", ["ilum starkiller", "starkiller base origin"]),
        item("world-taris", "taris", "legends primary", "ecumenopolis devastated in KOTOR-era history with undercity/class themes", "Use vertical inequality, rakghoul horror, and ruins in Legends games.", ["taris"]),
        item("world-teth", "teth", "canon/legends", "jungle world with monastery and crime/Clone Wars conflict", "Use vertical monastery fights, Hutt intrigue, and jungle extraction.", ["teth"]),
        item("world-tund", "tund", "legends primary", "world associated with Sorcerers of Tund and esoteric force traditions", "Use occult ruins and obscure sect lore only in Legends/mixed continuity.", ["tund", "sorcerers of tund"]),
        item("world-vardos", "vardos", "canon", "Imperial loyalist world damaged during Operation Cinder", "Use loyalist civilian tragedy, environmental attack, and postwar guilt.", ["vardos"]),
        item("world-zakuul", "zakuul", "legends primary", "Eternal Empire capital in SWTOR-era Legends", "Use authoritarian splendor, force monarchy, and distant Old Republic scale.", ["zakuul"]),
    ],
    "Kyber RPG 08 - Technology Ships Gear.json": [
        item("tech-a-wing", "a-wing interceptor", "canon/legends", "fast Rebel/New Republic interceptor with fragile durability", "Use for speed, ambush, and pilot risk; not a cargo or boarding craft.", ["a-wing interceptor", "rz-1 a-wing"]),
        item("tech-b-wing", "b-wing assault starfighter", "canon/legends", "heavy Rebel assault starfighter designed for capital-ship attack", "Use for maintenance complexity, bombing runs, and rare specialized pilots.", ["b-wing", "b-wing assault starfighter"]),
        item("tech-bacta-tank", "bacta tanks", "canon/legends", "healing tanks requiring bacta supply, monitoring, time, and privacy", "Use recovery as costly downtime vulnerable to interruption.", ["bacta tank", "bacta tanks"]),
        item("tech-comlink-security", "comlink security", "canon/legends", "cheap comlinks are easy to intercept, trace, jam, or clone", "Use comms as evidence and tactical risk, especially in underworld scenes.", ["comlink security", "trace comlink"]),
        item("tech-death-star-scale", "death star scale weapons", "canon/legends", "planet-killing superlasers require empire-scale logistics, kyber, crew, and secrecy", "Use as geopolitical horror; PCs interact through intelligence, sabotage, or survival.", ["death star scale", "planet killer superlaser"]),
        item("tech-deflector-shields", "deflector shield operations", "canon/legends", "shields can protect, fail by arc, overload, or be bypassed by timing and tactics", "Use shield status as dynamic battle fact rather than binary immunity.", ["deflector shield operations", "shield arc"]),
        item("tech-droid-memory", "droid memory wipes", "canon/legends", "memory wipes reset evidence, personality continuity, trauma, and learned loyalty", "Use as ethical and investigative issue.", ["droid memory wipe", "memory wipe"]),
        item("tech-e-web", "e-web heavy repeating blaster", "canon/legends", "crew-served heavy blaster with generator and setup time", "Use as area denial; vulnerable while being deployed or powered.", ["e-web", "heavy repeating blaster"]),
        item("tech-escape-pod", "escape pods", "canon/legends", "small emergency craft with beacons, limited supplies, and predictable search patterns", "Use survival, tracking, and false-pod tactics.", ["escape pod", "escape pods"]),
        item("tech-gonk-power", "power droids", "canon/legends", "GNK-style walking batteries and local power infrastructure", "Use as mundane but valuable targets, obstacles, and emergency power sources.", ["power droid", "gonk droid"]),
        item("tech-ion-weapon", "ion weapons", "canon/legends", "weapons disabling electronics, droids, shields, and ships without normal blast damage", "Use for capture and disablement; living targets may still face secondary danger.", ["ion weapon", "ion cannon", "ion blaster"]),
        item("tech-jedi-starfighter", "jedi starfighters", "canon/legends", "small hyperdrive-ring or astromech-supported interceptors used by Jedi in prequel eras", "Use as fragile elite craft, not long-haul homes.", ["jedi starfighter", "eta-2", "delta-7"]),
        item("tech-lightsaber-resistant-materials", "lightsaber resistant materials", "canon/legends", "beskar, cortosis, phrik, energy shields, and special alloys may resist blades by source", "Use sparingly with continuity labels; resistance is not universal invulnerability.", ["lightsaber resistant material", "cortosis", "phrik"]),
        item("tech-macrobinoculars", "macrobinoculars and scanners", "canon/legends", "portable optics and scanners extend sight but can glare, jam, or reveal emitters", "Use for recon with counter-recon consequences.", ["macrobinoculars", "portable scanner"]),
        item("tech-navicomputer", "navicomputers", "canon/legends", "hyperspace calculation systems needing charts, maintenance, and valid astrogation data", "Use bad data, damaged computers, or stolen charts as travel stakes.", ["navicomputer", "nav computer"]),
        item("tech-probe-droids", "probe droids", "canon/legends", "autonomous scouts with sensors, transmitters, and sometimes weapons/self-destruct", "Use as surveillance threat whose signal matters as much as chassis.", ["probe droid", "imperial probe"]),
        item("tech-proton-torpedo", "proton torpedoes", "canon/legends", "guided starfighter ordnance for hardened targets", "Use scarcity, lock time, point defense, and collateral blast.", ["proton torpedo", "proton torpedoes"]),
        item("tech-seismic-charge", "seismic charges", "canon/legends", "specialized ordnance with devastating delayed shockwave effect in space/atmosphere", "Use as terror weapon with setup and positioning, not normal grenade.", ["seismic charge", "seismic charges"]),
        item("tech-stun-setting", "stun settings", "canon/legends", "many blasters can stun at short range with limits by armor, species, and charge", "Use capture consequences; repeated stun still causes harm and risk.", ["stun setting", "blaster stun"]),
        item("tech-transponder", "ship transponders", "canon/legends", "identity signals tied to registration, port records, warrants, and traffic control", "Use spoofing as crime with trace and inspection consequences.", ["ship transponder", "transponder code"]),
        item("tech-turbolaser", "turbolasers", "canon/legends", "capital-scale energy weapons dangerous to ships, cities, and fortified targets", "Use scale honestly; infantry survive through cover, distance, or plot circumstance, not toughness.", ["turbolaser", "turbolasers"]),
        item("tech-vibroblade", "vibroblades", "canon/legends", "vibrating melee weapons common among soldiers, criminals, and duelists", "Use as lethal quiet weapon with maintenance, legality, and armor interaction.", ["vibroblade", "vibroknife"]),
        item("tech-walker-weakness", "walker weak points", "canon/legends", "walkers have joints, necks, viewports, tow-cable vulnerabilities, mines, and terrain limits", "Use tactical options without turning armored vehicles into cardboard.", ["walker weak point", "walker joint"]),
        item("tech-x-wing", "x-wing starfighters", "canon/legends", "versatile Rebel/New Republic snubfighters with astromech support and proton torpedoes", "Use as capable but maintenance-hungry military craft.", ["x-wing starfighter", "t-65 x-wing", "t-70 x-wing"]),
        item("tech-y-wing", "y-wing bombers", "canon/legends", "rugged bomber/attack craft often stripped down by Rebel cells", "Use as durable, slow, maintenance-heavy strike craft.", ["y-wing bomber", "btl y-wing"]),
    ],
    "Kyber RPG 03 - Characters.json": [
        item("char-asajj-ventress", "asajj ventress operational profile", "canon/legends", "Dathomirian dark acolyte, assassin, survivor, and later antihero depending era", "Use as sharp, wounded, pragmatic, and dangerous; never a soft wish-fulfillment ally.", ["asajj ventress profile", "ventress operational"]),
        item("char-bail-organa", "bail organa operational profile", "canon", "Alderaanian senator, covert rebel founder, and careful political operator", "Use as principled but cautious patron whose help creates surveillance risk.", ["bail organa profile", "senator organa covert"]),
        item("char-baylan-skoll", "baylan skoll operational profile", "canon", "fallen Jedi mercenary seeking deeper power and meaning after Order collapse", "Use as solemn, strategic, restrained, and not casually cruel.", ["baylan skoll profile", "baylan operational"]),
        item("char-bo-katan", "bo-katan kryze operational profile", "canon/legends", "Mandalorian noble-warrior leader with Death Watch history and later rulership burdens", "Use political consequence, pride, and guilt; she is not a generic quest giver.", ["bo-katan profile", "bo katan operational"]),
        item("char-cad-bane", "cad bane operational profile", "canon/legends", "elite Duros bounty hunter with ruthlessness, planning, and anti-Jedi experience", "Use as lethal professional who exploits hostages, terrain, and timing.", ["cad bane profile", "cad bane operational"]),
        item("char-dedramero", "dedra meero operational profile", "canon", "ISB supervisor defined by ambition, pattern recognition, and institutional cruelty", "Use as bureaucratic hunter; her danger is files, pressure, and persistence.", ["dedra meero profile", "dedra operational"]),
        item("char-din-djarin", "din djarin operational profile", "canon", "Mandalorian foundling and bounty hunter shaped by creed, loyalty, and practical violence", "Use as competent but not invincible; obligations and foundling ties drive choices.", ["din djarin profile", "mando operational"]),
        item("char-dr-aphra", "doctor aphra operational profile", "canon", "rogue archaeologist with brilliance, betrayal, debts, and dangerous artifacts", "Use as charming liability; any alliance should include a knife hidden in the contract.", ["doctor aphra profile", "aphra operational"]),
        item("char-galen-erso", "galen erso operational profile", "canon", "kyber scientist coerced into Death Star work who built hidden sabotage into the project", "Use as guilt, technical genius, and Imperial hostage leverage.", ["galen erso profile", "erso scientist"]),
        item("char-grand-inquisitor", "grand inquisitor operational profile", "canon", "former Jedi Temple Guard turned Imperial hunter and inquisitor leader", "Use doctrine, intimidation, and knowledge of Jedi fear; not a random brute.", ["grand inquisitor profile", "inquisitor leader"]),
        item("char-hondo", "hondo ohnaka operational profile", "canon/legends", "Weequay pirate whose greed, charm, and survival instinct outlive governments", "Use as funny only because he is dangerous, selfish, and opportunistic.", ["hondo profile", "hondo operational"]),
        item("char-kallus", "agent kallus operational profile", "canon", "ISB officer whose arc can move from brutal enforcer to rebel Fulcrum", "Use by era; before defection he is a serious Imperial threat.", ["agent kallus profile", "kallus operational"]),
        item("char-luthen", "luthen rael operational profile", "canon", "rebel spymaster sacrificing morality, identity, and people for rebellion infrastructure", "Use as cold patron whose missions have ugly costs.", ["luthen rael profile", "luthen operational"]),
        item("char-maul", "maul operational profile", "canon/legends", "former Sith apprentice turned crime lord and obsessive survivor", "Use obsession, manipulation, pain, and sudden violence; he does not share power easily.", ["maul profile", "darth maul operational"]),
        item("char-merrin", "merrin operational profile", "canon", "Nightsister survivor with magick, grief, loyalty, and outsider adaptation", "Use as culturally specific force user, not Jedi or Sith by another name.", ["merrin profile", "nightsister merrin"]),
        item("char-mon-mothma", "mon mothma operational profile", "canon/legends", "senator and rebel leader balancing public pacifism, money, family, and covert resistance", "Use political courage under surveillance, not simple inspirational speeches.", ["mon mothma profile", "mothma operational"]),
        item("char-morgan-elsbeth", "morgan elsbeth operational profile", "canon", "Nightsister-linked industrialist and Thrawn loyalist with massacre trauma and resources", "Use as elite patron/enemy with factories, mercenaries, and occult loyalties.", ["morgan elsbeth profile", "elsbeth operational"]),
        item("char-qira", "qi'ra operational profile", "canon", "Corellian survivor turned Crimson Dawn leader navigating Sith, syndicates, and betrayal", "Use as controlled, wounded, and strategic; affection never removes calculation.", ["qi'ra profile", "qira operational"]),
        item("char-saw", "saw gerrera operational profile", "canon", "militant rebel whose paranoia and ruthlessness make him useful and horrifying", "Use collateral damage, distrust, and moral injury in rebel scenes.", ["saw gerrera profile", "saw operational"]),
        item("char-shin-hati", "shin hati operational profile", "canon", "Baylan Skoll's apprentice with ambition, uncertainty, and predatory restlessness", "Use as dangerous and searching, not a stable Sith archetype.", ["shin hati profile", "shin operational"]),
        item("char-thrawn-canon", "thrawn canon operational profile", "canon", "Chiss strategist using art, logistics, patience, and psychological reads", "Use calm pressure and prepared traps; do not make him omniscient or emotionally sloppy.", ["thrawn canon profile", "thrawn operational"]),
        item("char-vel", "vel sartha operational profile", "canon", "rebel operative from privilege carrying pressure, secrecy, and command strain", "Use as field leader with political ties and emotional costs.", ["vel sartha profile", "vel operational"]),
    ],
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync(entry_obj):
    keys = []
    for key in entry_obj.get("key", []):
        clean = key.strip()
        if clean and clean not in keys:
            keys.append(clean)
    entry_obj["key"] = keys
    entry_obj["keysRaw"] = ", ".join(keys)
    entry_obj["keywordsRaw"] = entry_obj["keysRaw"]


def make_entry(template, item_obj, order, category):
    title = item_obj["name"].upper()
    content = (
        f"{title}\n"
        f"continuity = {item_obj['continuity']}\n"
        f"role = {item_obj['role']}\n"
        f"rpg use = {item_obj['use']}"
    )
    new_entry = dict(template)
    new_entry.update(
        {
            "activationMode": "standard",
            "activationScript": "",
            "case_sensitive": False,
            "category": category,
            "comment": "lore expansion batch 02; sources: official StarWars.com baseline plus Wookieepedia tertiary breadth; canon controls conflicts",
            "constant": False,
            "content": content,
            "enabled": True,
            "extensions": {},
            "groupWeight": 100,
            "id": item_obj["id"],
            "inclusionGroupRaw": "",
            "insertion_order": order,
            "key": item_obj["key"],
            "keyMatchPriority": True,
            "keysecondary": [],
            "keysecondaryRaw": "",
            "matchWholeWords": True,
            "minMessages": 0,
            "name": item_obj["name"],
            "prioritizeInclusion": False,
            "priority": item_obj["priority"],
            "probability": 100,
            "selectiveLogic": 0,
            "tags": ["star_wars", "expansion_batch_02"] + item_obj["tags"],
        }
    )
    sync(new_entry)
    return new_entry


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    changes = []

    for filename, items in DATA.items():
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
        for item_obj in items:
            if item_obj["name"].lower() in names or item_obj["id"] in ids:
                skipped += 1
                continue
            order += 100
            data.append(make_entry(template, item_obj, order, category))
            names.add(item_obj["name"].lower())
            ids.add(item_obj["id"])
            added += 1
            changes.append(
                {
                    "file": filename,
                    "name": item_obj["name"],
                    "id": item_obj["id"],
                    "keys": item_obj["key"],
                    "continuity": item_obj["continuity"],
                }
            )
        data.sort(key=lambda entry_obj: entry_obj.get("insertion_order", 0))
        save(path, data)
        print(f"{filename}: added {added}, skipped {skipped}")

    payload = {"generated": date.today().isoformat(), "base_sources": BASE_SOURCES, "changes": changes}
    (REPORTS / "expansion_batch_02_sources.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Lore Expansion Batch 02", "", f"Generated: {date.today().isoformat()}", "", "## Base Sources", ""]
    for label, url in BASE_SOURCES.items():
        md.append(f"- {label}: {url}")
    md.extend(["", "## Added Entries", ""])
    for change in changes:
        md.append(f"- {change['file']} :: {change['name']} :: {change['continuity']} [{', '.join(change['keys'])}]")
    (REPORTS / "expansion_batch_02_changelog.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Backed up touched files to {BACKUP}")
    print(f"Added {len(changes)} total entries")


if __name__ == "__main__":
    main()
