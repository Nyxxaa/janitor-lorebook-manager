import csv
import io
import json
import shutil
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
BACKUP = ROOT / "archive" / f"lore-expansion-batch-06-{date.today().isoformat()}"

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

SOURCES = {
    "official_databank": "https://www.starwars.com/databank/",
    "official_news": "https://www.starwars.com/news",
    "wookieepedia": "https://starwars.fandom.com/",
}

RAW = r"""
book|slug|name|continuity|role|use|keys
species|species-abyssin|Abyssin|legends primary|one-eyed regenerative sentients from harsh worlds|Use as tough mercenaries or frontier laborers; regeneration is limited, not immortality.|Abyssin;Abyssins
species|species-advozse|Advozse|canon/legends|horned sentients often appearing as travelers, merchants, or officials|Use as ordinary galactic population with sharp social presence.|Advozse
species|species-anzellan|Anzellans|canon|tiny expert droidsmith species represented by Babu Frik|Use scale, tools, and workshop access as real constraints.|Anzellan;Anzellans
species|species-aruzan|Aruzan|legends primary|near-human species with empathic/memory-sharing traits in Legends|Use for witness memory, consent, and trauma-sensitive investigation.|Aruzan;Aruzans
species|species-barfani|Baragwin|canon/legends|large technical-minded sentients associated with engineering and trade|Use as arms dealers, mechanics, and expert appraisers.|Baragwin
species|species-bimm|Bimm|legends primary|small sentients from Bimmisaari with trade and storytelling culture|Use for diplomatic marketplaces and underestimated locals.|Bimm;Bimmisaari species
species|species-bomarr|B'omarr monks|canon/legends|ascetic order preserving brains in walker jars|Use as grotesque spirituality and old Jabba palace context.|B'omarr monk;B'omarr
species|species-buzz-droid-makers|Colicoids|canon/legends|insectoid manufacturers associated with droidekas and ruthless commerce|Use as alien industrialists and dangerous negotiators.|Colicoid;Colicoids
species|species-coway|Coway|legends primary|Mimban subterranean native culture in older lore|Use for colonial conflict and underground survival.|Coway;Mimban natives
species|species-dressellian|Dressellians|canon/legends|wrinkled sentients associated with rebel fighters and harsh resistance|Use as guerrillas, farmers, or veterans of occupation.|Dressellian;Dressellians
species|species-droch|Drochs|legends primary|parasitic insects linked to life-draining plague horror|Use as rare biothreat, not common vermin.|Droch;Drochs
species|species-elom|Eloms|legends primary|burrowing sentients from Elom with underground communities|Use mining, tunnels, and Imperial exploitation.|Elom;Eloms
species|species-elomin2|Elomin caste context|legends primary|surface-dwelling analytical culture distinct from Eloms|Use Elom/Elomin distinction to avoid species conflation.|Elomin distinction;Elom and Elomin
species|species-frozian|Frozian|legends primary|foxlike sentients including diplomats in New Republic-era lore|Use for alien diplomacy and obscure senatorial contacts.|Frozian;Frozians
species|species-givin-vacuum|Givin vacuum limits|canon/legends|Givin tolerate vacuum better than many species but still have limits|Use to prevent vacuum-tolerance from becoming invulnerability.|Givin vacuum limits;Givin biology
species|species-gossam|Gossam|canon/legends|small long-necked sentients associated with Commerce Guild leadership|Use for corporate politics and Separatist-era prejudice.|Gossam;Commerce Guild species
species|species-gotal-sensor|Gotal sensory overload|canon/legends|Gotal horns sense energy/emotion in many depictions|Use crowded tech-heavy scenes as discomfort or clue source.|Gotal sensory overload;Gotal horns
species|species-ho-din|Ho'Din|legends primary|plantlike sentients known for medicine and ecology in older lore|Use as healers, botanists, and ecological witnesses.|Ho'Din;Ho Din
species|species-huk|Huk|legends primary|insectoid enemies of Kaleesh in Grievous backstory lore|Use only in Legends context for Kalee war history.|Huk;Yam'rii
species|species-iktochi-visions|Iktotchi vision stigma|canon/legends|Iktotchi precognitive reputation creates distrust and social pressure|Use as prejudice and fragmented warning, not perfect foresight.|Iktotchi vision stigma;Iktotchi foresight
species|species-jabiimi|Jabiimi|canon/legends|people of Jabiim shaped by mud-world wars and outside betrayal|Use as locals with long memory of Republic/Imperial violence.|Jabiimi;Jabiim locals
species|species-kadas-sa-nikto|Kadas'sa'Nikto|canon/legends|Nikto subgroup with Hutt-linked history|Use subgroup specificity for Nikto NPCs and culture.|Kadas'sa'Nikto;green Nikto
species|species-kage|Kage|canon/legends|Quarzite-associated warrior species in Clone Wars context|Use subterranean conflict and hired-warrior scenes.|Kage;Kage warriors
species|species-kajain-sa-nikto|Kajain'sa'Nikto|canon/legends|red Nikto subgroup commonly seen in Hutt and guard contexts|Use as specific Nikto identity, not generic henchman label.|Kajain'sa'Nikto;red Nikto
species|species-kalleran|Kallerans|canon|Kaller natives associated with Order 66 events around Caleb Dume|Use for postwar memory and local Clone Wars scars.|Kalleran;Kallerans
species|species-keshiri|Keshiri|legends primary|near-human species ruled by Lost Tribe Sith on Kesh|Use for isolated Sith social hierarchy and colonial domination.|Keshiri;Kesh
species|species-kowakian|Kowakian monkey-lizards|canon/legends|semi-sentient trickster creatures kept as pets or nuisances|Use noise, theft, and underworld atmosphere without overplaying comedy.|Kowakian monkey-lizard;monkey-lizard
species|species-lateros|Latero|canon|four-armed sentients including Greez Dritus|Use pilot/mechanic body plan and ordinary galactic diversity.|Latero;Lateros
species|species-morseerian|Morseerians|canon/legends|four-armed methane-breathing sentients needing breath gear in oxygen atmospheres|Use life-support vulnerability and alien negotiation.|Morseerian;Morseerians
species|species-mrlssi|Mrlssi|legends primary|small avian scholars and economists from Legends material|Use academic, finance, and information contacts.|Mrlssi;Mrlsst
species|species-nimbanel|Nimbanel|canon/legends|bureaucratic sentients often used in underworld/court contexts|Use accountants, clerks, and corrupt paperwork experts.|Nimbanel
species|species-nothoiin|Nothos|legends primary|obscure sentients usable as minor galactic-population catchers|Use only as background alien detail unless explicitly invoked.|Nothos;Nothos species
species|species-ortolan|Ortolans|canon/legends|blue elephantine sentients including Max Rebo's species|Use musicians, cooks, workers, and cold-adapted physiology.|Ortolan;Ortolans
species|species-pa-lowick|Pa'lowick|canon/legends|long-snouted amphibious species including Sy Snootles|Use entertainment circuits and underworld venues.|Pa'lowick;Palowick
species|species-pantoran|Pantorans|canon/legends|blue-skinned people from Pantora with politics near Orto Plutonia|Use formal diplomacy, colonial tension, and cold-world politics.|Pantoran;Pantorans
species|species-polisc-massan|Polis Massans|canon/legends|silent asteroid medical/archaeology culture tied to birth of twins|Use med-station silence, archaeology, and nonverbal procedure.|Polis Massan;Polis Massans
species|species-quarren-politics|Quarren political culture|canon/legends|Mon Cala co-inhabitants with recurring separatist, localist, and industrial tensions|Use factional politics; do not make all Quarren villains.|Quarren politics;Quarren culture
species|species-rakata-tech-loss|Rakata technology loss|legends primary|Rakata decline includes loss of Force-linked technology and empire memory|Use ruined arrogance and broken machines.|Rakata technology loss;Rakata decline
species|species-sakiyan|Sakiyans|legends primary|near-human hunters and tacticians from older lore|Use as trackers, strategists, or sharp underworld contacts.|Sakiyan;Sakiyans
species|species-sanyassan|Sanyassan Marauders|canon/legends|Endor-linked marauder species/group from Ewok movie lore|Use only in compatible frontier/Endor material.|Sanyassan;Sanyassan Marauder
species|species-shistavanen|Shistavanen|canon/legends|wolf-like sentients with scout and hunter reputation|Use scent, prejudice, and wilderness competence.|Shistavanen;wolfman species
species|species-snivvian|Snivvians|canon/legends|short snouted sentients seen in cantinas and galactic crowds|Use merchants, artists, gamblers, and background aliens.|Snivvian;Snivvians
species|species-squib|Squibs|legends primary|small scavenger/trader species with chaotic bargaining reputation|Use salvage haggling and comic danger without making them harmless.|Squib;Squibs
species|species-stennes|Stennes Shifters|legends primary|rare energy-feeding/Force-adjacent species from older lore|Use as obscure mystical threat or scholar topic only when invoked.|Stennes Shifter;Stennes
species|species-sunesi|Sunesi|legends primary|near-human Force-sensitive culture in older novels|Use for obscure Jedi-era heritage and persecution stories.|Sunesi
species|species-talz-culture|Talz culture|canon/legends|cold-world sentients with four eyes, fur, and sovereignty conflicts|Use local law and first-contact harm instead of monster framing.|Talz culture;Talz sovereignty
species|species-togorian|Togorians|legends primary|large feline sentients with clan and hunting traditions|Use as warriors, scouts, and nonhuman social customs.|Togorian;Togorians
species|species-trianii|Trianii|legends primary|feline sentients with ranger traditions in older lore|Use as scouts, sector defenders, and agile fighters.|Trianii;Trianii Rangers
species|species-ubese|Ubese|canon/legends|masked sentients tied to mercenary work and environmental loss in Legends|Use anonymity, breath gear, and diaspora bitterness.|Ubese
species|species-weequay-culture|Weequay clan culture|canon/legends|Sriluur-linked people with clan, pirate, and Hutt-space histories|Use clan oaths and desert-world practice beyond generic pirate roles.|Weequay culture;Weequay clans
species|species-xexto|Xexto|canon/legends|multi-armed sentients known from podracing and dexterous work|Use speed, gambling, and unusual body-plan constraints.|Xexto
species|species-yamrii|Yam'rii|legends primary|Huk insectoid species in Kaleesh conflict lore|Use as Grievous-backstory Legends context only.|Yam'rii;Huk species
species|species-yuzzum|Yuzzum|canon/legends|Endor sentients with musical/long-limbed traits in older lore|Use as rare performers or forest-world locals.|Yuzzum;Yuzzums
hazards|creature-blistmok|Blistmoks|legends primary|Korriban predators from Old Republic game lore|Use as ruin wildlife around Sith sites, not generic monsters.|Blistmok;Blistmoks
hazards|creature-boga-context|Boga|canon|Obi-Wan's varactyl mount on Utapau|Use as specific trusted mount reference, not species-wide name.|Boga;Obi-Wan varactyl
hazards|creature-bordok-herd|Bordok herds|canon/legends|Endor herd animals used by Ewoks|Use herd movement as forest clue or travel resource.|Bordok herd;Endor herd
hazards|creature-brain-worm|Geonosian brain worms|canon|parasites controlling hosts in Clone Wars stories|Use body horror, quarantine, and trust collapse.|Geonosian brain worm;brain worm
hazards|creature-cairnmog|Cairnmogs|legends primary|large predatory creatures in old RPG/Legends material|Use as wilderness encounter when an obscure beast is needed.|Cairnmog;Cairnmogs
hazards|creature-chirodactyl|Chirodactyls|legends primary|batlike creatures usable in caves and ruins|Use swarm noise, disease, and darkness pressure.|Chirodactyl;Chirodactyls
hazards|creature-dragonsnake-lair|Dragonsnake lairs|canon/legends|muddy underwater lairs near swamp predators|Use hidden bodies, gear, and ambush terrain.|Dragonsnake lair;swamp predator lair
hazards|creature-duracrete-slug|Duracrete slugs|setting-compatible|urban scavenger pests living in pipes and ferrocrete cracks|Use lower-level disgust, blocked vents, and minor biohazards.|Duracrete slug;urban pipe slug
hazards|creature-gizka|Gizka|legends primary|small fast-breeding pests from KOTOR lore|Use ship infestation, cargo fines, and comic logistics with real cost.|Gizka;Gizka infestation
hazards|creature-grimtaash|Grimtaash legends|legends primary|obscure dangerous creature name for deep lore catchers|Use only if invoked; keep behavior grounded and source-labeled.|Grimtaash
hazards|creature-gualaar|Gualaar|canon/legends|large Naboo animal used in older ecological lore|Use as local fauna, mounts, or hunting context.|Gualaar
hazards|creature-hssiss|Hssiss|legends primary|dark-side dragons from KOTOR-era tomb lore|Use as Sith ruin predator with fear and corruption themes.|Hssiss;dark side dragon
hazards|creature-kaanis|Kaanis|legends primary|obscure predator suitable for arid or ruin encounters|Use only when named; avoid inventing broad canon.|Kaanis
hazards|creature-kinrath|Kinrath|legends primary|spiderlike cave creatures and crystal cave threats in KOTOR lore|Use eggs, venom, and cave movement pressure.|Kinrath;Kinrath egg
hazards|creature-k'lor'slug|K'lor'slugs|legends primary|dangerous sluglike predators from Old Republic/Sith areas|Use as tomb, sewer, or arena hazard.|K'lor'slug;Klor slug
hazards|creature-laigrek|Laigreks|legends primary|large insectoid predators from KOTOR ruins|Use as abandoned-enclave infestation threat.|Laigrek;Laigreks
hazards|creature-manka-cat|Manka cats|legends primary|feline predators used in old game ecology|Use stealth, scent, and wilderness ambush.|Manka cat;Manka cats
hazards|creature-mott|Motts|canon/legends|Naboo herd animals|Use as local rural detail or predator-prey ecology.|Mott;Motts
hazards|creature-mutated-rakghoul|Rakghoul variants|legends primary|infected mutants from Taris and related Legends plague lore|Use infection horror and quarantine, not casual cannon fodder.|Rakghoul variant;Rakghoul mutation
hazards|creature-nuna|Nuna|canon/legends|small Naboo bird/reptile livestock|Use food, farm life, and market detail.|Nuna;Nunas
hazards|creature-peko-peko|Peko-peko|canon/legends|Naboo flying creature|Use sky ecology and local travel ambience.|Peko-peko;Peko peko
hazards|creature-raptor-endangered|Endangered beasts|setting baseline|rare animals hunted for status, venom, pearls, or hides|Use ecological and legal consequences for trophy hunting.|Endangered beast;trophy hunt
hazards|creature-reek-stable|Reek stables|canon/legends|holding areas for dangerous horned beasts|Use animal panic, smell, handlers, and broken gates.|Reek stable;arena beast stable
hazards|creature-roba|Robas|legends primary|large pack/herd creatures from old RPG/game ecology|Use as beasts of burden or dangerous herd encounter.|Roba;Robas
hazards|creature-shi'ido-hunt|Shi'ido shapeshifter suspicion|legends primary|fear around shapeshifters such as Shi'ido creates witch-hunt dynamics|Use paranoia carefully; suspicion can harm innocents.|Shi'ido suspicion;shapeshifter hunt
hazards|creature-skreev|Skreevs|legends primary|small pests/predators useful for lower-level scenes|Use nuisance bites, disease, and evidence disturbance.|Skreev;Skreevs
hazards|creature-sleen|Sleens|canon/legends|lizardlike predators/animals in Star Wars wildlife lore|Use as guard beasts or wasteland predators.|Sleen;Sleens
hazards|creature-stintaril|Stintaril|legends primary|batlike creatures from KOTOR-era cave lore|Use sound, darkness, and swarm pressure.|Stintaril;Stintarils
hazards|creature-tach|Tach|legends primary|Kashyyyk primate creatures from KOTOR-era lore|Use as local wildlife and predator-warning behavior.|Tach;Tachs
hazards|creature-tybis|Tybis|legends primary|dangerous herd/predator creatures in older material|Use for frontier hunts and camp danger.|Tybis
hazards|creature-uwari-beetle|Uwari beetles|legends primary|valuable or dangerous beetles from older lore contexts|Use for contraband ecology and collector greed.|Uwari beetle;Uwari beetles
society|society-alienage|alienage districts|canon/legends|segregated or informal alien neighborhoods under humanocentric regimes|Use housing, policing, and language pressure.|Alienage district;alien quarter
society|society-amnesty-programs|amnesty programs|canon/legends|postwar governments offer conditional forgiveness to enemies, criminals, or informants|Use false hope, political backlash, and betrayal risk.|Amnesty program;conditional amnesty
society|society-apprenticeship-contract|apprenticeship contracts|canon/legends|craft, pilot, slicer, and criminal skills may be bound by contract or debt|Use training as obligation and leverage.|Apprenticeship contract;training debt
society|society-arena-economy|arena economies|canon/legends|beast fights, gladiators, betting, medical crews, and rigged outcomes|Use violence as business with owners and consequences.|Arena economy;gladiator betting
society|society-beskar-provenance|beskar provenance|canon/legends|Mandalorian iron carries lineage, theft, clan, and forgery questions|Use ownership disputes and social consequences.|Beskar provenance;forged beskar
society|society-bounty-hunter-code|bounty hunter codes|canon/legends|guild/custom rules govern targets, rivals, collateral, and payment proof|Use code violations as reputation damage.|Bounty hunter code;hunter code
society|society-cantina-neutrality|cantina neutrality|setting baseline|some bars survive by enforcing weapon checks, house rules, or broker neutrality|Use violated neutrality as underworld incident.|Cantina neutrality;house rules cantina
society|society-civil-asset-forfeiture|asset forfeiture|canon/legends|authorities seize ships, credits, and cargo as suspected contraband or rebel property|Use nonlethal loss with appeal costs.|Asset forfeiture;seized ship
society|society-company-town|company towns|canon/legends|corporations control housing, stores, clinics, guards, and debt|Use everyday oppression and labor rebellion.|Company town;corporate town
society|society-court-interpreter|court interpreters|setting baseline|legal proceedings depend on translators who can alter meaning or delay justice|Use language access as power.|Court interpreter;legal translator
society|society-dead-drop-protocol|dead-drop protocols|setting baseline|spies use marks, timing, watchers, tamper signs, and fallback routes|Use tradecraft; any clean drop may be bait.|Dead-drop protocol;dead drop tradecraft
society|society-deportation|deportation orders|canon/legends|regimes remove unwanted species, refugees, workers, or dissidents|Use paperwork as violence and countdown pressure.|Deportation order;removal order
society|society-docking-bond|docking bonds|setting baseline|ports require deposits against damage, unpaid fees, or flight risk|Use to keep poor crews trapped.|Docking bond;port bond
society|society-evidence-bounty|evidence bounties|setting baseline|private rewards for information can create false tips and witness danger|Use investigation noise and moral hazard.|Evidence bounty;information reward
society|society-false-flag|false-flag attacks|canon/legends|states, rebels, and syndicates stage violence to reassign blame|Use forensic detail and propaganda timing.|False-flag attack;staged attack
society|society-fence-network|fence networks|canon/legends|stolen goods move through appraisers, chop shops, brokers, and laundering fronts|Use sale as risk, not automatic credits.|Fence network;stolen goods broker
society|society-fuel-rationing|fuel rationing|canon/legends|war, blockade, and poverty restrict fuel cells, coaxium, tibanna, and reactor parts|Use stranded travel and black-market fuel.|Fuel rationing;fuel shortage
society|society-gambling-debt|gambling debts|canon/legends|casinos, cantinas, and syndicates turn wagers into violent obligations|Use shame, interest, and rigged games.|Gambling debt;casino debt
society|society-hab-census|hab-stack census|setting baseline|urban authorities count residents through utilities, IDs, rent, and informants|Use hiding as logistics problem.|Hab-stack census;residency check
society|society-id-forgery-market|identity forgery market|canon/legends|aliases require slicers, blanks, biometrics, references, and risk|Use tiered quality and burned identities.|Identity forgery market;fake chain code
society|society-jury-intimidation|witness and jury intimidation|canon/legends|criminals or states pressure testimony through threats, bribes, and disappearances|Use legal drama with underworld teeth.|Jury intimidation;witness intimidation
society|society-kidnapping-ransom|kidnapping ransom customs|canon/legends|ransom depends on proof of life, intermediaries, deadlines, and retaliation risk|Use negotiation and rescue pressure.|Ransom custom;proof of life
society|society-labor-strikebreaking|strikebreaking|canon/legends|corporations use guards, scabs, droids, propaganda, or troops against workers|Use class conflict and public optics.|Strikebreaking;labor crackdown
society|society-medical-license|medical licenses|setting baseline|clinics and doctors require permits that can be revoked, forged, or weaponized|Use bureaucracy around healing.|Medical license;clinic permit
society|society-munitions-tax|munitions taxes|setting baseline|ports and regimes tax, restrict, or report ammo and explosives|Use cost and exposure for armed crews.|Munitions tax;ammo tax
society|society-name-day|local festivals|canon/legends|festivals alter traffic, policing, prices, crowds, and cover identities|Use crowds as opportunity and risk.|Local festival;festival crowd
society|society-orphan-creches|orphan creches|canon/legends|war leaves children in religious, state, criminal, or community care|Use recruitment, exploitation, and protection stakes.|Orphan creche;war orphanage
society|society-pawned-droid|pawned droids|setting baseline|owners pawn droids for loans, parts, or ransom|Use property law and personhood tension.|Pawned droid;droid pawnshop
society|society-quarantine-bribe|quarantine bribes|setting baseline|medical or customs isolation can be shortened by corrupt payments or favors|Use infection risk and legal leverage.|Quarantine bribe;medical bribe
society|society-ration-fraud|ration fraud|canon/legends|food, medicine, fuel, or refugee aid can be skimmed or duplicated|Use ledgers, hungry civilians, and corrupt officials.|Ration fraud;aid theft
society|society-rebel-tax|rebel taxation|canon/legends|insurgencies demand supplies, shelter, credits, or silence from locals|Use resistance costs and civilian resentment.|Rebel tax;insurgent levy
society|society-safe-passage|safe-passage papers|canon/legends|documents, escorts, or bribes allowing travel through hostile territory|Use fragile protection and betrayal risk.|Safe-passage papers;travel writ
society|society-sensor-warrant|sensor warrants|setting baseline|lawful scans may require paperwork, emergency powers, or bribed authorization|Use legal limits that corrupt actors can bend.|Sensor warrant;scan warrant
society|society-ship-share|crew shares|canon/legends|ship crews may split ownership, debt, salvage, and repair liabilities|Use internal conflict over risk and profit.|Crew share;ship shares
society|society-smuggler-tithe|smuggler tithes|canon/legends|criminal ports demand a percentage of cargo or profit for protection|Use hidden cost of illegal routes.|Smuggler tithe;shadowport tithe
society|society-sponsorship|legal sponsorship|setting baseline|outsiders may need a local sponsor to work, rent, dock, or enter court|Use patron leverage and social dependency.|Legal sponsor;local sponsor
society|society-union-busting|union busting|setting baseline|employers use spies, blacklists, violence, and lawfare against workers|Use labor politics with consequences.|Union busting;labor spy
society|society-vehicle-registration|vehicle registration|canon/legends|speeders, ships, and walkers have registrations, liens, and inspection records|Use stolen-vehicle risk and forged plates.|Vehicle registration;speeder registration
factions|faction-alkahara-bandits|desert bandit clans|setting baseline|local raiders shaped by scarcity, family, grudges, and smuggling routes|Use as people with motives, not random spawns.|Desert bandit clan;wasteland raiders
factions|faction-antiquities-office|antiquities offices|canon/legends|state/corporate agencies claiming relics, ruins, and excavation permits|Use archaeology law and corruption.|Antiquities office;relic permit
factions|faction-beast-handler-guild|beast handler guilds|canon/legends|trainers controlling mounts, arena beasts, guard animals, and transport creatures|Use animal access, licenses, and sabotage.|Beast handler guild;beast trainer guild
factions|faction-black-market-clinics|black-market clinic networks|canon/legends|linked illegal doctors, med-droids, organ brokers, and document forgers|Use care with strings attached.|Black-market clinic network;illegal medical network
factions|faction-bounty-clearinghouse|bounty clearinghouses|canon/legends|brokers validating contracts, proof, and payment between hunters and clients|Use disputes over terms and identity.|Bounty clearinghouse;bounty broker
factions|faction-cargo-inspectorate|cargo inspectorates|setting baseline|official or corrupt inspection offices at ports and depots|Use paper obstacles and shakedowns.|Cargo inspectorate;freight inspector
factions|faction-corporate-ecology-board|corporate ecology boards|setting baseline|company bodies minimizing pollution liability and worker sickness|Use coverups and bought science.|Corporate ecology board;pollution board
factions|faction-cult-of-vader|Vader cults|canon/legends|post-Imperial groups worshiping Vader's image, relics, or fear|Use dangerous misunderstanding and relic crime.|Vader cult;cult of Vader
factions|faction-droid-chop-shop|droid chop shops|canon/legends|illegal businesses wiping, parting, and reselling droids|Use stolen friends, evidence destruction, and moral pressure.|Droid chop shop;illegal droid shop
factions|faction-free-trader-league|free-trader leagues|canon/legends|merchant associations resisting guild, Hutt, or Imperial route control|Use convoy politics and smuggler respectability.|Free-trader league;free trader league
factions|faction-holonet-pirates|HoloNet pirates|canon/legends|illegal broadcasters, slicers, rumor sellers, and propaganda hackers|Use information warfare and trace risk.|HoloNet pirate;pirate broadcast
factions|faction-kajidic-courts|kajidic courts|canon/legends|Hutt clan arbitration backed by debt, honor, and violence|Use legal theater inside criminal power.|Kajidic court;Hutt arbitration
factions|faction-local-churches|local Force shrines|canon/legends|lay communities preserving local Force practice outside Jedi/Sith institutions|Use faith as local culture, not automatic power.|Local Force shrine;lay Force community
factions|faction-migrant-convoys|migrant convoys|canon/legends|refugee or worker ships traveling together for safety and bargaining|Use escort jobs and hard scarcity.|Migrant convoy;refugee convoy
factions|faction-night-market|night markets|canon/legends|semi-illegal markets for food, parts, medicine, rumors, and stolen goods|Use crowded cover with pickpockets and police raids.|Night market;illegal market
factions|faction-orbital-unions|orbital worker unions|setting baseline|dock, tug, hull, and refinery workers organizing in space infrastructure|Use labor pressure in shipyards and stations.|Orbital worker union;dockworker union
factions|faction-patrol-contractors|patrol contractors|canon/legends|private firms paid to secure routes, mines, or colonies|Use legal mercenaries with bad incentives.|Patrol contractor;security contractor
factions|faction-relic-hunters|relic hunter crews|canon/legends|archaeologists, criminals, cultists, and collectors chasing old artifacts|Use rival teams with permits, guns, and lies.|Relic hunter crew;artifact hunters
factions|faction-scrapper-guild|scrapper guilds|canon/legends|organized salvage labor controlling wreck access, scales, and resale|Use Bracca/Jakku-style exploitation and local power.|Scrapper guild;salvage guild
factions|faction-sector-health-office|sector health offices|setting baseline|public-health authorities issuing quarantine, clinic permits, and disease records|Use bureaucracy that can save or ruin people.|Sector health office;public health office
factions|faction-smuggler-insurance|smuggler mutual-aid funds|setting baseline|crews pool money for bribes, funerals, repairs, and families|Use underworld solidarity and theft temptation.|Smuggler mutual aid;crew death fund
factions|faction-tomb-raider-cults|tomb-raider cults|canon/legends|small groups stealing Sith/Jedi relics for status, power, or sale|Use amateur danger and unleashed hazards.|Tomb-raider cult;relic cult
factions|faction-water-rights-council|water-rights councils|canon/legends|local bodies controlling wells, vaporators, aquifers, and distribution|Use desert politics and sabotage cases.|Water-rights council;vaporator council
force|force-artifact-provenance|artifact provenance|canon/legends|Force relic histories mix truth, forgery, gaps, and propaganda|Use provenance checks before trusting relic claims.|Artifact provenance;relic provenance
force|force-binding-vow|Force binding vows|canon/legends|promises, oaths, and rituals may carry social or mystical weight|Use consequences through belief, community, and temptation.|Force binding vow;binding oath
force|force-crystal-cave-ecology|crystal cave ecology|canon/legends|kyber caves have temperature, pressure, predators, guardians, and cultural protocols|Use pilgrimage as survival and ethics, not shopping.|Crystal cave ecology;kyber cave ecology
force|force-dead-jedi-cache|dead Jedi caches|canon/legends|hidden bundles of robes, sabers, texts, credits, and emergency messages|Use as grief, temptation, and bait for hunters.|Dead Jedi cache;Jedi emergency cache
force|force-dream-intrusion|dream intrusion|canon/legends|visions or psychic attacks entering sleep through bond, place, or artifact|Use fear and clues while preserving uncertainty.|Dream intrusion;Force dream attack
force|force-guardian-droid|Force-site guardian droids|canon/legends|droids guarding temples, archives, or relic vaults by old doctrine|Use old programming as moral/legal puzzle.|Force-site guardian droid;temple security droid
force|force-kyber-smuggling|kyber smuggling|canon/legends|illegal crystal trade for weapons, cults, medicine scams, or collectors|Use Imperial interest and moral stain.|Kyber smuggling;illegal kyber
force|force-light-side-temptation|light-side temptation|canon/legends|mercy, rescue, and hope can still become reckless attachment or denial|Use moral complexity beyond dark-side cackling.|Light-side temptation;reckless mercy
force|force-lost-padawan|lost Padawan traces|canon/legends|survivor graffiti, practice marks, broken training remotes, or hidden journals|Use post-Purge archaeology with emotional weight.|Lost Padawan trace;Padawan journal
force|force-ritual-circle|ritual circles|canon/legends|chalk, blood, ash, kyber dust, bones, machines, or ichor arranged for rites|Use physical clues and interruption consequences.|Ritual circle;Force ritual site
force|force-silent-room|Force-silent rooms|canon/legends|spaces shielded by design, creatures, trauma, or technology from easy sensing|Use uncertainty and vulnerability for Force users.|Force-silent room;Force blind room
force|force-sith-language|Sith language inscriptions|canon/legends|ancient Sith texts use language, code, and ideology as hazard|Use translation as risk and temptation.|Sith language inscription;Sith text
force|force-temple-map-room|temple map rooms|canon/legends|rooms aligning stars, history, doctrine, and trials|Use partial maps and symbolic constraints.|Temple map room;Jedi map room
force|force-verdant-vergence|living vergence ecology|canon/legends|places where life growth, healing, or mutation suggests Force concentration|Use beauty with risk, not only dark temples.|Living vergence;verdant vergence
force|force-wound-survivor|Force wound survivors|canon/legends|people surviving massacres or catastrophes with altered perception or emptiness|Use trauma and metaphysics carefully.|Force wound survivor;wound in the Force survivor
legends|legends-arkanian|Arkanian offshoot lore|legends primary|genetic engineering, offshoots, and cold intellectual caste politics|Use bioethics and arrogance in Legends contexts.|Arkanian offshoot;Arkanian genetics
legends|legends-bakuran|Bakura aftermath|legends primary|post-Endor world facing Ssi-ruuk crisis and New Republic contact|Use early post-Endor diplomacy and trauma.|Bakura aftermath;Bakura crisis
legends|legends-beldorion|Beldorion the Hutt|legends primary|Force-sensitive Hutt dark-sider from older lore|Use as rare cautionary Legends oddity, not normal Hutt trait.|Beldorion;Force-sensitive Hutt
legends|legends-black-sun-vigos|Black Sun Vigos legends|legends primary|regional crime lieutenants under Xizor-style hierarchy|Use underworld politics and betrayal.|Black Sun Vigo legends;Vigo council
legends|legends-borsk|Borsk Fey'lya|legends primary|Bothan New Republic politician known for ambition and obstruction|Use political rivalry without flattening Bothans as a species.|Borsk Fey'lya;Fey'lya
legends|legends-caedus-war|Darth Caedus war|legends primary|Jacen Solo's fall and Second Galactic Civil War|Use family tragedy and state security paranoia in Legends post-NJO.|Darth Caedus war;Caedus conflict
legends|legends-callista|Callista Ming|legends primary|Jedi spirit/body-transfer figure from older Luke-era stories|Use as identity and Force survival complication.|Callista Ming;Callista
legends|legends-camaasi-memory|Caamasi memory shards|legends primary|shared memory and Caamas atrocity politics|Use witness memory as moral/legal pressure.|Caamasi memory;Caamas memory
legends|legends-celeste-morne|Celeste Morne|legends primary|Jedi tied to Muur Talisman and long survival across eras|Use artifact possession and time-displaced witness stories.|Celeste Morne
legends|legends-centerpoint-crisis|Centerpoint crisis|legends primary|Corellian megastructure crises involving system politics and superweapon risk|Use regional separatism and ancient-machine terror.|Centerpoint crisis;Corellian crisis legends
legends|legends-corran-horn|Corran Horn|legends primary|Corellian pilot/Jedi from X-wing and Jedi Academy lore|Use investigation, piloting, and Jedi heritage in Legends games.|Corran Horn
legends|legends-daala-remnant|Daala remnant politics|legends primary|Imperial warlord leadership, Maw secrets, and later authoritarian claims|Use remnant faction conflict and hardline military logic.|Daala remnant;Daala politics
legends|legends-dorsk-81|Dorsk 81|legends primary|clone-descended Jedi student from Khomm in New Jedi Order lore|Use clone society and Jedi academy sacrifice themes.|Dorsk 81;Khomm Jedi
legends|legends-fel-knights|Imperial Knights doctrine|legends primary|Force order serving Fel Emperor with armor, duty, and light-side discipline|Use not-Jedi lawful Force tradition in Legacy era.|Imperial Knights doctrine;Fel knights
legends|legends-ganner-rhysode|Ganner Rhysode|legends primary|New Jedi Order figure remembered for final stand against Yuuzhan Vong|Use heroic myth and survivor memory in Legends.|Ganner Rhysode
legends|legends-garm-bel-iblis|Garm Bel Iblis legends|legends primary|Corellian rebel leader with independent military politics|Use Rebel/New Republic factional tension.|Garm Bel Iblis;Bel Iblis
legends|legends-gilad-pellaeon|Gilad Pellaeon|legends primary|Imperial officer central to later Remnant and peace process|Use honorable-imperial complexity in Legends.|Gilad Pellaeon;Pellaeon detail
legends|legends-ikan-gaton|Irek Ismaren and Roganda|legends primary|Imperial court/Force intrigue from Children of the Jedi era|Use obscure court remnants and dangerous heirs only if invoked.|Irek Ismaren;Roganda Ismaren
legends|legends-jaina-solo|Jaina Solo|legends primary|Leia and Han's daughter, Jedi pilot, twin of Jacen in Legends|Use Sword of the Jedi themes and family-war tragedy.|Jaina Solo
legends|legends-jacen-solo|Jacen Solo|legends primary|Solo son who becomes Darth Caedus in Legends continuity|Use philosophical fall, war trauma, and family consequences.|Jacen Solo
legends|legends-jagged-fel|Jagged Fel|legends primary|Chiss-aligned pilot and Fel dynasty figure|Use bridge between Chiss, Imperial, and Jedi-linked politics.|Jagged Fel;Jag Fel
legends|legends-kyp-durron|Kyp Durron|legends primary|powerful Jedi student marked by dark-side catastrophe and redemption arguments|Use academy ethics and war-hawk Jedi politics.|Kyp Durron
legends|legends-lowbacca|Lowbacca|legends primary|Wookiee Jedi student in Luke's academy era|Use Jedi diversity and family/tech translator detail.|Lowbacca
legends|legends-mirax|Mirax Terrik|legends primary|smuggler/businesswoman tied to Corran Horn and Booster Terrik|Use underworld contacts with family loyalties.|Mirax Terrik
legends|legends-mycroft-lost|Lost City of the Jedi|legends primary|young-reader-era secret Jedi/city myth material|Use only as obscure rumor or false lead unless Legends game wants it.|Lost City of the Jedi;Jedi prince rumor
legends|legends-noghri-honor-debt|Noghri honor debt|legends primary|Noghri service to Vader/Empire tied to deception and clan obligations|Use loyalty breaking only after truth and proof.|Noghri honor debt;Noghri clan debt
legends|legends-nom-anor|Nom Anor|legends primary|Yuuzhan Vong agent and manipulator|Use infiltration, cult politics, and alien spycraft in NJO era.|Nom Anor
legends|legends-praxeum-students|Yavin Praxeum students|legends primary|Luke's early academy includes unstable, gifted, and traumatized students|Use training community with real risk and limited structure.|Yavin Praxeum students;Jedi praxeum students
legends|legends-talon-karrde|Talon Karrde|legends primary|information broker and smuggler chief from Thrawn-era lore|Use civilized underworld neutrality and intelligence markets.|Talon Karrde;Karrde
legends|legends-tenel-ka|Tenel Ka|legends primary|Hapan/Dathomiri Jedi and ruler figure|Use court duty, warrior discipline, and divided heritage.|Tenel Ka
legends|legends-tycho-celchu|Tycho Celchu|legends primary|Alderaanian pilot and Rogue Squadron figure under suspicion after Imperial captivity|Use trust, interrogation trauma, and pilot loyalty.|Tycho Celchu
legends|legends-vong-heresy|Shamed Ones heresy|legends primary|Yuuzhan Vong caste/religious dissent among oppressed Shamed Ones|Use internal resistance and theological fracture.|Shamed Ones heresy;Vong heresy
legends|legends-wes-janson|Wes Janson legends|legends primary|Rogue/Wraith pilot known for skill and humor in military ensemble lore|Use veteran levity under trauma, not pure gag.|Wes Janson
legends|legends-winter-celchu|Winter Celchu|legends primary|Alderaanian aide/intelligence figure with exceptional memory|Use survivor memory, court service, and spycraft.|Winter Celchu;Winter Retrac
legends|legends-wraith-humor|Wraith Squadron culture|legends primary|commando-pilot unit using misdirection, humor, and broken people|Use covert action with trauma and improvisation.|Wraith Squadron culture;Wraith misfits
legends|legends-yuuzhan-vong-castes|Yuuzhan Vong castes|legends primary|warrior, priest, shaper, intendants, workers, and Shamed Ones structure society|Use alien hierarchy and internal conflict in NJO games.|Yuuzhan Vong castes;Vong caste
sabers|saber-blaster-hybrid|lightsaber blaster hybrids|canon/legends|rare weapons combining blade and firearm concepts or trick hilts|Use as exotic, maintenance-heavy, and suspicious to Jedi/Sith traditionalists.|Lightsaber blaster hybrid;trick lightsaber
sabers|saber-cane|lightsaber canes|canon/legends|concealed sabers disguised as walking sticks or formal canes|Use social infiltration and reveal timing.|Lightsaber cane;cane saber
sabers|saber-crystal-crack|cracked kyber crystals|canon/legends|damaged crystals can cause instability, venting, or emotional resonance|Use weapon unreliability and repair quests.|Cracked kyber;damaged kyber crystal
sabers|saber-darksaber-politics|Darksaber political symbolism|canon|Mandalorian symbol of leadership, legitimacy, story, and challenge|Use as political burden, not just a black sword.|Darksaber politics;Darksaber legitimacy
sabers|saber-dueling-ring|lightsaber dueling rings|canon/legends|training or illegal arenas for saber-capable fighters|Use secrecy, injuries, and cult recruitment.|Lightsaber dueling ring;saber arena
sabers|saber-focusing-lens|focusing lenses|canon/legends|lightsaber components shaping blade stability, length, and behavior|Use missing parts and poor construction as consequences.|Focusing lens;lightsaber lens
sabers|saber-shoto|shoto lightsabers|canon/legends|short lightsabers used off-hand, by smaller duelists, or for specific styles|Use reach tradeoff and close-defense tactics.|Shoto;shoto lightsaber
sabers|saber-training-remote|training remotes|canon/legends|small droids used for deflection drills and training|Use academy scenes, malfunction, and improvised distractions.|Training remote;remote droid training
powers|power-detox|Force detoxification|canon/legends|rare healing/discipline technique against poison or intoxication|Use as difficult and costly; severe toxins still need medicine.|Force detoxification;purge poison force
powers|power-enhanced-reflexes|Force-enhanced reflexes|canon/legends|danger sense and body acceleration supporting combat or piloting|Use strain, focus, and surprise limits.|Force-enhanced reflexes;Force reflexes
powers|power-farsight|Farsight|canon/legends|distant perception through Force connection, vision, or meditation|Use symbolic fragments and emotional anchors.|Farsight;Force farsight
powers|power-force-flashback|Force flashbacks|canon/legends|traumatic or object-linked sensory returns|Use clues with strain and misinterpretation risk.|Force flashback;psychometric flashback
powers|power-force-sever|sever Force technique|legends primary|rare technique cutting or muting Force connection|Use as extreme trauma and moral crisis, not casual debuff.|Sever Force;cut off from the Force
powers|power-instinctive-astrogation|instinctive astrogation|canon/legends|using the Force to navigate hyperspace or dangerous routes|Use as risky substitute for charts with visions and strain.|Instinctive astrogation;Force astrogation
powers|power-plant-surge|plant surge|legends primary|Force influence accelerating or shaping plant growth|Use in nature/temple scenes with environmental limits.|Plant surge;Force plant growth
powers|power-sever-memory|memory manipulation limits|canon/legends|Force influence may cloud or alter memory in rare, risky contexts|Use as violation with consequences; never casual retcon.|Memory manipulation limit;Force memory alter
orders|order-believers-sith|Sith cult believers|canon/legends|lay cultists serving Sith myths without real Sith training|Use zealots, scams, and dangerous amateurs.|Sith cult believer;lay Sith cult
orders|order-crimson-nova|Crimson Nova bounty order|legends primary|bounty-hunter group from older lore tied to anti-Jedi contracts|Use Legends hunter threat when Jedi bounties arise.|Crimson Nova;Jedi bounty hunters
orders|order-dagoyan|Dagoyan Masters|canon|Bardottan spiritual leaders distinct from Jedi|Use non-Jedi Force-adjacent tradition and sovereignty.|Dagoyan Masters;Dagoyan Order
orders|order-gray-paladin|Gray Paladins|legends primary|Jedi offshoot minimizing Force use and favoring physical skill/weapons|Use doctrinal argument over dependence on powers.|Gray Paladin;Gray Paladins
orders|order-je'daii-rangers|Je'daii rangers|legends primary|Tython-era predecessor tradition balancing Ashla and Bogan concepts|Use Dawn/Old Republic prehistory only in Legends/mixed games.|Je'daii ranger;Je'daii
orders|order-mecrosa|Mecrosa Order|legends primary|Tapani-sector assassin tradition with dark-side associations|Use noble-sector intrigue and hidden killers.|Mecrosa Order;Mecrosa
orders|order-naddists|Naddist cults|legends primary|Onderon cultists venerating Freedon Nadd's dark legacy|Use royal tomb politics and Sith heresy.|Naddist cult;Naddists
orders|order-sorcerers-tund|Sorcerers of Tund|legends primary|esoteric Force tradition/cult from Tund|Use strange ritualists and illusion-heavy occult danger.|Sorcerers of Tund;Tund sorcerer
orders|order-tython-je'daii|Tython Je'daii temples|legends primary|ancient temple network from Dawn of the Jedi material|Use temple specialization and early Force philosophy.|Tython Je'daii temple;Je'daii temple
worlds|world-argai|Argai Minor|legends primary|minor world suitable for obscure Rim/Legends references|Use as background when named; avoid overclaiming canon.|Argai Minor
worlds|world-bimmisaari|Bimmisaari|legends primary|trade world of Bimms tied to Thrawn-era diplomacy|Use market diplomacy and ambush risk in Legends.|Bimmisaari
worlds|world-bpfassh|Bpfassh|legends primary|world/sector linked to dark Jedi incident in older lore|Use obscure Jedi-history scandal.|Bpfassh;Bpfasshi
worlds|world-byss|Byss|legends primary|Deep Core world central to Dark Empire Palpatine clone regime|Use hidden imperial nightmare only in Legends branch.|Byss legends;Byss
worlds|world-carida|Carida|legends primary|Imperial training world destroyed in Legends Jedi Academy era|Use Imperial academy legacy and catastrophe records.|Carida
worlds|world-circumtore|Circumtore|legends primary|Corporate Sector/CSA-linked world in older lore|Use corporate legal and trade scenes.|Circumtore
worlds|world-da-soocha|Da Soocha V|legends primary|Rebel/New Republic temporary base moon in Dark Empire lore|Use hidden fleet base and refugee command pressure.|Da Soocha;Da Soocha V
worlds|world-dorin|Dorin|canon/legends|Kel Dor homeworld with atmosphere hostile to many outsiders|Use breath-gear logistics and Baran Do culture.|Dorin
worlds|world-dxun|Dxun|legends primary; canon references vary|Onderon moon with jungle, beasts, Mandalorian history, and Sith tomb links|Use survival horror and Mandalorian Wars scars.|Dxun
worlds|world-empress-teta|Empress Teta|legends primary|Core/Deep Core-associated system tied to ancient Sith wars and mining wealth|Use noble houses, old Sith war records, and mining politics.|Empress Teta;Koros Major
worlds|world-gamorr|Gamorr|canon/legends|Gamorrean homeworld with clan and warlord traditions|Use recruitment, clan politics, and Hutt-space links.|Gamorr
worlds|world-glee-anselm|Glee Anselm|canon/legends|Nautolan homeworld with aquatic culture|Use underwater cities, diplomacy, and species context.|Glee Anselm
worlds|world-khomm|Khomm|legends primary|clone-society world from Jedi Academy-era lore|Use identity, stagnation, and cloning ethics.|Khomm
worlds|world-kiffu|Kiffu|canon/legends|Kiffar homeworld/governance center with Guardian traditions|Use clan law and psychometry bloodline politics.|Kiffu
worlds|world-kiffex|Kiffex|canon/legends|prison moon/world tied to Kiffar authority|Use detention, exile, and clan jurisdiction.|Kiffex
worlds|world-lexrul|Lexrul|legends primary|minor world useful for obscure Legends location catchers|Use only if named; keep details source-light.|Lexrul
worlds|world-mrlsst|Mrlsst|legends primary|academic world associated with Mrlssi and technical research|Use universities, prototype tech, and information economy.|Mrlsst
worlds|world-muunilinst|Muunilinst|canon/legends|Banking Clan world and financial center|Use money, war finance, and guarded vaults.|Muunilinst
worlds|world-myrkr-forests|Myrkr forest zones|legends primary|dense forests with vornskrs and ysalamiri ecology|Use anti-Force terrain and dangerous hunting.|Myrkr forest;Myrkr wilds
worlds|world-nirauan|Nirauan|legends primary|Unknown Regions world tied to Hand of Thrawn complex|Use secret bases and Chiss/Imperial ambiguity.|Nirauan;Hand of Thrawn base
worlds|world-onderon-politics|Onderon royal politics|canon/legends|world with monarchy, beast-rider history, Separatist/rebel tensions, and Sith-adjacent Legends past|Use court intrigue and jungle moon pressure.|Onderon politics;Iziz court
worlds|world-pantora|Pantora|canon/legends|Pantoran homeworld/state near Orto Plutonia|Use senate politics and colonial border tension.|Pantora
worlds|world-phindar|Phindar|legends primary|world tied to memory-wipe criminal stories in older lore|Use biotech crime and trade-world unease.|Phindar
worlds|world-quarzite|Quarzite|canon|subterranean world with Kage/Belugan conflict in Clone Wars|Use underground transit and species power imbalance.|Quarzite
worlds|world-rattatak|Rattatak|legends primary|harsh gladiatorial world associated with Asajj Ventress in Legends|Use arena warlords and continuity caution.|Rattatak
worlds|world-rhinnal|Rhinnal|legends primary|Core medical world in older lore|Use high-end hospitals, medical politics, and refugee care.|Rhinnal
worlds|world-riflor|Riflor|legends primary|Advozse homeworld with seismic instability in older lore|Use disaster culture and pragmatic pessimism.|Riflor
worlds|world-sriluur|Sriluur|canon/legends|Weequay homeworld in Hutt Space|Use Hutt-space politics and clan identity.|Sriluur
worlds|world-thyferra|Thyferra|legends primary; canon references vary|bacta production world central to Bacta War lore|Use medical monopoly, cartel politics, and healing scarcity.|Thyferra;bacta world
worlds|world-tython-legends|Tython legends|legends primary; canon version differs|ancient Je'daii/Jedi world in Legends prehistory|Use only with continuity label; canon has separate treatment.|Tython legends;Je'daii Tython
worlds|world-vortex|Vortex|legends primary|world of Vors and Cathedral of Winds music culture|Use art, diplomacy, and ecological tragedy.|Vortex;Cathedral of Winds
tech|tech-2-1b|2-1B surgical droids|canon/legends|medical droids used for surgery, treatment, and battlefield recovery|Use skilled care limited by supplies and owner ethics.|2-1B droid;2-1B surgical droid
tech|tech-4lom-protocol|protocol droid bounty conversions|canon/legends|protocol chassis can be modified or self-directed into criminal work, as with 4-LOM|Use droid identity drift and illegal modification.|Protocol droid bounty hunter;4-LOM type
tech|tech-a99-aquata|A99 aquata breathers|canon/legends|small underwater breathing devices used in Naboo-era scenes|Use limited-duration aquatic infiltration.|Aquata breather;A99 breather
tech|tech-at-ap|AT-AP walkers|canon/legends|artillery walkers used in Clone Wars battlefields|Use indirect fire and vulnerable stabilization legs.|AT-AP;AT-AP walker
tech|tech-at-te|AT-TE walkers|canon/legends|Republic armored walkers with climbing/magnetic capability in some contexts|Use heavy troop transport and battlefield anchor.|AT-TE;AT-TE walker
tech|tech-barc|BARC speeders|canon/legends|clone scout speeders for fast reconnaissance|Use high-speed patrols, exposed riders, and rough terrain.|BARC speeder;clone speeder bike
tech|tech-binary-loadlifter|binary loadlifters|canon/legends|heavy labor droids moving cargo and industrial equipment|Use warehouse hazards and exploited automation.|Binary loadlifter;loadlifter droid
tech|tech-bowcaster|bowcasters|canon/legends|Wookiee projectile/energy weapons with high force and cultural context|Use strength, maintenance, and legal attention.|Bowcaster;Wookiee bowcaster
tech|tech-camtono|camtonos|canon|secure containers used for valuables such as beskar or credits|Use physical loot, locks, and traceable ownership.|Camtono;camtono safe
tech|tech-coaxium-refining|coaxium refining|canon|volatile hyperspace fuel processing needing stability and equipment|Use explosive stakes and syndicate control.|Coaxium refining;unstable coaxium
tech|tech-combat-remote|Marksman-H remotes|canon/legends|small training remotes for saber and blaster practice|Use training, malfunction, or cheap security adaptation.|Marksman-H remote;combat remote
tech|tech-datacard|datacards|canon/legends|small portable data storage vulnerable to encryption, damage, and tracking|Use as evidence and bait.|Datacard;data card
tech|tech-droid-restraining-bolt|restraining bolt bypass|canon/legends|droids can sometimes be freed by removing or spoofing control hardware|Use skill checks and owner retaliation.|Restraining bolt bypass;remove restraining bolt
tech|tech-fusioncutter|fusioncutters|canon/legends|portable cutting/welding tools used in repair and sabotage|Use heat, noise, power draw, and trace marks.|Fusioncutter;fusion cutter
tech|tech-holochess|dejarik tables|canon/legends|holographic game boards common aboard ships and lounges|Use social scenes, gambling, and coded communication.|Dejarik;holochess
tech|tech-hyperspace-beacon|hyperspace beacons|canon/legends|navigation or tracking transmitters marking routes, fleets, or traps|Use signal range and spoofing consequences.|Hyperspace beacon;nav beacon
tech|tech-ig-series|IG-series assassin droids|canon/legends|tall lethal droid models used for assassination and combat|Use as terrifying but still bounded by programming, damage, and contracts.|IG-series assassin droid;IG assassin droid
tech|tech-jedi-comlink-codes|Jedi comm codes|canon/legends|old encrypted channels and distress codes used before or after Purge|Use as bait, archive clue, or dangerous contact method.|Jedi comm code;Jedi distress code
tech|tech-kihraxz|Kihraxz fighters|legends primary|starfighter class associated with fringe and Black Sun material|Use as Legends pirate/crime fighter craft.|Kihraxz;Kihraxz fighter
tech|tech-lambda-shuttle|Lambda-class shuttles|canon/legends|Imperial tri-wing shuttles used for officers, cargo, and infiltration disguises|Use codes, clearance, and recognizable silhouette.|Lambda shuttle;Lambda-class
tech|tech-laat|LAAT gunships|canon/legends|Republic low-altitude assault transports from Clone Wars|Use troop deployment, medevac, and vulnerable approach runs.|LAAT gunship;Republic gunship
tech|tech-lightsaber-pike|lightsaber pikes|canon/legends|polearm-like saber weapons used by guards and specialists|Use reach, formation, and ceremonial intimidation.|Lightsaber pike;saber pike
tech|tech-lobot-tech|AJ^6 cyborg construct|canon/legends|head-mounted computer liaison/cybernetic system like Lobot's gear|Use cognitive cost and computer mediation.|AJ6 cyborg construct;cyborg headgear
tech|tech-medpac|medpacs|canon/legends|portable first-aid kits with dressings, drugs, tools, and limited supplies|Use triage, not full recovery.|Medpac;medpack
tech|tech-mouse-droid-security|mouse droid security routing|canon/legends|small utility droids know corridors, routines, and restricted paths|Use hacked navigation and unnoticed witnesses.|Mouse droid route;MSE route
tech|tech-neural-band|neural bands|canon/legends|restraint/interrogation/control devices affecting nerves or perception|Use as coercive tech with medical risk.|Neural band;neural restraint
tech|tech-pit-droid|pit droids|canon/legends|small repair droids used in racing and workshops|Use fast cheap labor, swarm repair, and slapdash mistakes.|Pit droid;pit droids
tech|tech-r-series|R-series astromechs|canon/legends|astromech family used for navigation, repair, slicing, and fighter support|Use model differences without overloading every droid scene.|R-series astromech;R-series droid
tech|tech-sabacc-deck|sabacc decks|canon/legends|card game with shifting values and high-stakes gambling culture|Use cheating, debts, tells, and coded meetings.|Sabacc deck;sabacc
tech|tech-separatist-ordnance|Separatist ordnance caches|canon/legends|leftover droid army munitions, mines, and repair bays after Clone Wars|Use salvage danger and insurgent supply.|Separatist ordnance cache;droid army cache
tech|tech-sith-wayfinder-security|wayfinder security|canon|Sith wayfinders point to hidden routes and can be guarded by puzzles, cults, and danger|Use as rare plot object with heavy pursuit.|Sith wayfinder security;wayfinder route
tech|tech-slicer-spike|slicer spikes|canon/legends|single-use or specialized intrusion devices|Use limited charges and trace risk.|Slicer spike;code spike
tech|tech-speeder-tags|speeder transponder tags|setting baseline|local vehicles carry tags, plates, and traffic records|Use stolen-speeder heat and checkpoint detection.|Speeder transponder;speeder tag
tech|tech-stun-cuffs|stun cuffs|canon/legends|restraints delivering shock or immobilization|Use capture without removing all choices.|Stun cuffs;shock cuffs
tech|tech-t-6-shuttle|T-6 Jedi shuttles|canon|rotating-wing Jedi diplomatic shuttles used across eras|Use recognizable Jedi/Republic salvage and maintenance issues.|T-6 shuttle;T-6 Jedi shuttle
tech|tech-vulture-droid|Vulture droids|canon/legends|Separatist droid starfighters that can walk and fly|Use old automated threats and salvage surprises.|Vulture droid;droid starfighter
tech|tech-wrist-rocket|wrist rockets|canon/legends|Mandalorian/clone-style micro-missile weapons|Use ammunition scarcity, blast risk, and armor integration.|Wrist rocket;wrist rockets
characters|char-adi-gallia|Adi Gallia operational profile|canon/legends|Jedi Council member and Tholothian master active before/during Clone Wars|Use as disciplined council Jedi with era-specific death/status.|Adi Gallia profile;Adi Gallia
characters|char-agent-terex|Agent Terex operational profile|canon|former Imperial/First Order-linked operative from Poe Dameron comics|Use as fanatic intelligence threat in sequel-era play.|Agent Terex profile;Terex operational
characters|char-ap5|AP-5 operational profile|canon|Imperial inventory droid turned rebel logistics asset|Use bureaucracy, manifests, and droid resentment as competence.|AP-5 profile;AP-5
characters|char-bib-fortuna|Bib Fortuna operational profile|canon/legends|Twi'lek majordomo serving Jabba and later criminal power on Tatooine|Use sycophancy, survival, and palace networks.|Bib Fortuna profile;Bib Fortuna
characters|char-bossk|Bossk operational profile|canon/legends|Trandoshan bounty hunter with Wookiee-hunting reputation and brutal professionalism|Use predator etiquette, contracts, and rivalry with other hunters.|Bossk profile;Bossk operational
characters|char-cc-2224|Commander Cody operational profile|canon/legends|clone marshal commander under Obi-Wan who executes Order 66 command|Use professionalism, inhibitor tragedy, and postwar uncertainty by era.|Commander Cody profile;CC-2224
characters|char-cham-syndulla|Cham Syndulla operational profile|canon/legends|Twi'lek resistance leader against Separatist and Imperial control|Use liberation politics, family strain, and hard local choices.|Cham Syndulla profile;Cham operational
characters|char-ciena-ree|Ciena Ree operational profile|canon|Imperial officer from Lost Stars shaped by honor, loyalty, and moral compromise|Use loyalist tragedy and postwar capture stakes.|Ciena Ree profile;Ciena operational
characters|char-cobb-vanth|Cobb Vanth operational profile|canon|Tatooine marshal using salvaged Mandalorian armor to protect Freetown|Use frontier law, local legitimacy, and armor consequences.|Cobb Vanth profile;Marshal Vanth
characters|char-depa-billaba|Depa Billaba operational profile|canon/legends|Jedi master of Caleb Dume/Kanan with Clone Wars trauma and Order 66 death|Use mentor memory and war-scarred Jedi leadership.|Depa Billaba profile;Depa operational
characters|char-dexter-jettster|Dexter Jettster operational profile|canon/legends|Besalisk diner owner and information contact with criminal/old-world knowledge|Use informal intelligence, food, and old contacts.|Dexter Jettster profile;Dex operational
characters|char-embo|Embo operational profile|canon/legends|Kyuzo bounty hunter using hat-shield, anooba, and acrobatic tactics|Use silent professionalism and terrain advantage.|Embo profile;Embo operational
characters|char-gar-saxon|Gar Saxon operational profile|canon|Mandalorian Imperial collaborator and warrior-politician|Use occupation legitimacy conflict and clan violence.|Gar Saxon profile;Gar Saxon
characters|char-hera-syndulla|Hera Syndulla operational profile|canon|Twi'lek pilot, rebel general, and cell leader balancing crew and cause|Use command competence, family cost, and logistics.|Hera Syndulla profile;Hera operational
characters|char-ig-88|IG-88 operational profile|canon/legends|assassin droid with multiple-body/AI uprising Legends threads|Use lethal droid logic; label Legends details when used.|IG-88 profile;IG-88
characters|char-jango-fett-extra|Jango Fett contract profile|canon/legends|bounty hunter whose Kamino contract shapes clone army origins|Use as template politics and mercenary professionalism.|Jango contract profile;Kamino template contract
characters|char-jar-jar|Jar Jar Binks operational profile|canon|Gungan exile, Naboo figure, and wartime senate proxy with tragic political impact|Use clumsy courage and political consequence, not pure joke.|Jar Jar profile;Jar Jar operational
characters|char-jocasta-nu|Jocasta Nu operational profile|canon/legends|Jedi archivist with dangerous knowledge and post-Purge relevance in canon comics|Use archives, memory, and hunter target stakes.|Jocasta Nu profile;Jedi archivist
characters|char-jyn-erso|Jyn Erso operational profile|canon|partisan-raised criminal survivor turned Rogue One catalyst|Use distrust, prison record, and hard-won commitment.|Jyn Erso profile;Jyn operational
characters|char-ketsu-onyo|Ketsu Onyo operational profile|canon|Mandalorian bounty hunter and Sabine-connected underworld figure|Use old friendships, betrayal, and mercenary pressure.|Ketsu Onyo profile;Ketsu operational
characters|char-krrsantan|Black Krrsantan operational profile|canon/legends|Wookiee gladiator/bounty hunter with brutal reputation|Use as terrifying enforcer with history, not generic muscle.|Black Krrsantan profile;Krrsantan operational
characters|char-lama-su|Lama Su operational profile|canon/legends|Kaminoan prime minister shaping clone production politics|Use polite biotech ruthlessness and contract logic.|Lama Su profile;Lama Su operational
characters|char-lobot|Lobot operational profile|canon/legends|Bespin aide with cyborg computer liaison implant|Use silent competence and cognitive cost of interface tech.|Lobot profile;Lobot operational
characters|char-lor-san-tekka|Lor San Tekka operational profile|canon|Church of the Force explorer preserving Jedi knowledge|Use old-map contacts and vulnerable faith communities.|Lor San Tekka profile;San Tekka operational
characters|char-max-rebo|Max Rebo operational profile|canon/legends|Ortolan musician tied to Jabba-era entertainment circuits|Use entertainer witness and underworld venue access.|Max Rebo profile;Max Rebo
characters|char-nala-se|Nala Se operational profile|canon|Kaminoan scientist tied to clone ethics, Omega, and Imperial science pressure|Use clinical skill under coercive systems.|Nala Se profile;Nala Se operational
characters|char-omega|Omega operational profile|canon|enhanced clone child/survivor tied to Bad Batch and Imperial cloning interest|Use protective stakes and clone identity, not instant plot device.|Omega profile;Omega clone
characters|char-plo-koon|Plo Koon operational profile|canon/legends|Kel Dor Jedi master known for compassion toward clones and Ahsoka|Use calm authority and breath-mask vulnerability.|Plo Koon profile;Plo operational
characters|char-pre-vizsla|Pre Vizsla operational profile|canon|Death Watch leader wielding Darksaber against pacifist Mandalore|Use charisma, extremism, and political violence.|Pre Vizsla profile;Pre Vizsla
characters|char-satine-kryze|Satine Kryze operational profile|canon|pacifist Mandalorian duchess opposing warrior factions and corruption|Use idealism under impossible pressure and Mandalorian civil stakes.|Satine Kryze profile;Satine operational
characters|char-shara-bey|Shara Bey operational profile|canon|Rebel pilot and Poe Dameron's mother active around Endor aftermath|Use post-Endor missions and family legacy.|Shara Bey profile;Shara operational
characters|char-shmi|Shmi Skywalker operational profile|canon|enslaved mother of Anakin whose death shapes his fear and rage|Use with gravity; never cheap bait or wish fulfillment.|Shmi Skywalker profile;Shmi operational
characters|char-syril-karn|Syril Karn operational profile|canon|failed corporate security officer driven by order, resentment, and obsession|Use petty authoritarianism and dangerous fixation.|Syril Karn profile;Syril operational
characters|char-tarfful|Tarfful operational profile|canon/legends|Wookiee chieftain/leader active in Kashyyyk defense and survivor networks|Use local authority and anti-occupation resistance.|Tarfful profile;Tarfful operational
characters|char-tech|Tech operational profile|canon|clone commando of Clone Force 99 defined by analysis, piloting, and sacrifice|Use precise competence and emotional understatement.|Tech clone profile;Clone Force 99 Tech
characters|char-trilla|Trilla Suduri operational profile|canon|Second Sister Inquisitor shaped by torture, betrayal, and Jedi survivor trauma|Use hunter cruelty with buried pain; no easy redemption shortcut.|Trilla profile;Second Sister profile
characters|char-watto|Watto operational profile|canon|Toydarian junk dealer and enslaver on Tatooine|Use debt, property, and small-business cruelty without comic softening.|Watto profile;Watto operational
characters|char-wedge|Wedge Antilles operational profile|canon/legends|Rebel pilot survivor of major battles and leader in later continuities|Use veteran competence and survivor burden.|Wedge Antilles profile;Wedge operational
characters|char-zam-wesell|Zam Wesell operational profile|canon/legends|Clawdite bounty hunter involved in Padme assassination attempt|Use shapeshifter tactics, poisons, and contractor cutouts.|Zam Wesell profile;Zam operational
"""


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rows():
    reader = csv.DictReader(io.StringIO(RAW.strip()), delimiter="|")
    for row in reader:
        row["keys"] = [key.strip() for key in row["keys"].split(";") if key.strip()]
        row["id"] = f"kyber-batch06-{row['slug']}"
        yield row


def sync(entry):
    keys = []
    for key in entry.get("key", []):
        if key and key not in keys:
            keys.append(key)
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
            "comment": "lore expansion batch 06 dense breadth; official canon baseline, Wookieepedia tertiary breadth, canon controls conflicts",
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
            "priority": 1,
            "probability": 100,
            "selectiveLogic": 0,
            "tags": ["star_wars", "expansion_batch_06"],
        }
    )
    sync(entry)
    return entry


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    grouped = defaultdict(list)
    for row in rows():
        grouped[FILES[row["book"]]].append(row)

    changes = []
    for filename, batch_rows in sorted(grouped.items()):
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
        for row in batch_rows:
            if row["name"].lower() in names or row["id"] in ids:
                skipped += 1
                continue
            order += 100
            data.append(make_entry(template, row, order, category))
            names.add(row["name"].lower())
            ids.add(row["id"])
            added += 1
            changes.append({"file": filename, "name": row["name"], "continuity": row["continuity"], "keys": row["keys"]})
        data.sort(key=lambda entry: entry.get("insertion_order", 0))
        save(path, data)
        print(f"{filename}: added {added}, skipped {skipped}")

    payload = {"generated": date.today().isoformat(), "sources": SOURCES, "changes": changes}
    (REPORTS / "expansion_batch_06_sources.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md = ["# Lore Expansion Batch 06", "", f"Generated: {date.today().isoformat()}", "", "## Sources", ""]
    for label, url in SOURCES.items():
        md.append(f"- {label}: {url}")
    md.extend(["", "## Added Entries", ""])
    for change in changes:
        md.append(f"- {change['file']} :: {change['name']} :: {change['continuity']} [{', '.join(change['keys'])}]")
    (REPORTS / "expansion_batch_06_changelog.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Backed up touched files to {BACKUP}")
    print(f"Added {len(changes)} total entries")


if __name__ == "__main__":
    main()
