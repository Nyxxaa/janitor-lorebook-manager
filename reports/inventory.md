# Kyber RPG Lorebook Inventory

Generated: 2026-07-20

## Summary

- JSON lorebook files: 15
- Entries: 2651
- Enabled entries: 2651
- Constant entries: 3
- Activation keys: 6677
- Single-word keys: 1237
- Regex keys: 0
- Estimated lore content tokens if fully loaded: 174349

## Issue Counts

- broad_keys: 27
- duplicate_content: 0
- duplicate_ids: 0
- duplicate_keys_across_files: 195
- duplicate_keys_within_entry: 0
- duplicate_names_within_file: 0
- empty_keys_nonconstant: 0
- invalid_json: 0
- keysraw_mismatch: 0
- keywordsraw_mismatch: 0
- large_key_lists: 3
- long_entries: 21
- low_probability: 0
- non_array_roots: 0
- repeated_rule_blocks: 0
- schema_mismatches: 0
- suspect_filenames: 0
- unsorted_insertion_order: 0

## Files

| File | KB | Entries | Constants | Keys | Single-word | Regex | Est. content tokens |
|---|---:|---:|---:|---:|---:|---:|---:|
| Kyber RPG 00 - Rules Engine.json | 91.1 | 31 | 3 | 502 | 287 | 0 | 11324 |
| Kyber RPG 01 - Core Continuity.json | 42.5 | 30 | 0 | 98 | 8 | 0 | 3010 |
| Kyber RPG 02 - Eras and History.json | 341.8 | 280 | 0 | 643 | 17 | 0 | 17085 |
| Kyber RPG 03 - Characters.json | 374.1 | 292 | 0 | 622 | 68 | 0 | 25383 |
| Kyber RPG 04 - Factions and Governments.json | 249.6 | 188 | 0 | 535 | 14 | 0 | 14280 |
| Kyber RPG 05 - Worlds and Regions.json | 376.7 | 316 | 0 | 778 | 191 | 0 | 19414 |
| Kyber RPG 06 - Species and Cultures.json | 219.1 | 182 | 0 | 421 | 275 | 0 | 11487 |
| Kyber RPG 07 - Society Law Economy.json | 230.8 | 178 | 0 | 497 | 28 | 0 | 12256 |
| Kyber RPG 08 - Technology Ships Gear.json | 396.5 | 335 | 0 | 779 | 110 | 0 | 18077 |
| Kyber RPG 09 - Creatures and Hazards.json | 173.8 | 149 | 0 | 316 | 136 | 0 | 7316 |
| Kyber RPG 10 - Force Powers.json | 191.9 | 167 | 0 | 365 | 9 | 0 | 7960 |
| Kyber RPG 11 - Force Orders.json | 211.9 | 182 | 0 | 407 | 18 | 0 | 9475 |
| Kyber RPG 12 - Lightsabers and Kyber.json | 68.5 | 58 | 0 | 132 | 19 | 0 | 2963 |
| Kyber RPG 13 - Force Metaphysics Artifacts.json | 170.2 | 141 | 0 | 303 | 15 | 0 | 7439 |
| Kyber RPG 14 - Legends Supplements.json | 151.5 | 122 | 0 | 279 | 42 | 0 | 6880 |

## Highest-Risk Findings

### Repeated Rule Blocks

- None found.

### Large Key Lists

- Kyber RPG 00 - Rules Engine.json:175 `SECTION 2 — CHARACTERISTICS, SKILLS, AND CHECK CONSTRUCTION` has 74 keys
- Kyber RPG 00 - Rules Engine.json:769 `SECTION 14 — SOCIAL ENCOUNTERS` has 22 keys
- Kyber RPG 00 - Rules Engine.json:1506 `SECTION 29 — NARRATIVE RESULT TEMPLATES` has 22 keys

### Broad Keys

- Kyber RPG 00 - Rules Engine.json `SECTION 2 — CHARACTERISTICS, SKILLS, AND CHECK CONSTRUCTION` key `failure`
- Kyber RPG 00 - Rules Engine.json `SECTION 3 — DICE SYMBOLS AND CANCELLATION` key `success`
- Kyber RPG 00 - Rules Engine.json `SECTION 3 — DICE SYMBOLS AND CANCELLATION` key `failure`
- Kyber RPG 00 - Rules Engine.json `SECTION 3 — DICE SYMBOLS AND CANCELLATION` key `threat`
- Kyber RPG 00 - Rules Engine.json `SECTION 5 — SPENDING ADVANTAGE, THREAT, TRIUMPH, AND DESPAIR` key `threat`
- Kyber RPG 00 - Rules Engine.json `SECTION 9 — ENCOUNTER STRUCTURE, INITIATIVE, ACTIONS, AND MANEUVERS` key `attack`
- Kyber RPG 00 - Rules Engine.json `SECTION 10 — RANGE BANDS, MOVEMENT, COVER, AND ENVIRONMENT` key `range`
- Kyber RPG 00 - Rules Engine.json `SECTION 11 — PERSONAL COMBAT CHECKS` key `attack`
- Kyber RPG 00 - Rules Engine.json `SECTION 11 — PERSONAL COMBAT CHECKS` key `combat`
- Kyber RPG 00 - Rules Engine.json `SECTION 12 — WEAPON QUALITIES AND DEFENSE` key `weapon`
- Kyber RPG 00 - Rules Engine.json `SECTION 12 — WEAPON QUALITIES AND DEFENSE` key `armor`
- Kyber RPG 00 - Rules Engine.json `SECTION 14 — SOCIAL ENCOUNTERS` key `persuade`
- Kyber RPG 00 - Rules Engine.json `SECTION 14 — SOCIAL ENCOUNTERS` key `convince`
- Kyber RPG 00 - Rules Engine.json `SECTION 15 — FEAR, DISCIPLINE, AND MENTAL PRESSURE` key `fear`
- Kyber RPG 00 - Rules Engine.json `SECTION 15 — FEAR, DISCIPLINE, AND MENTAL PRESSURE` key `sith`
- Kyber RPG 00 - Rules Engine.json `SECTION 16 — HEALING, MEDICINE, STIMPACKS, AND BACTA` key `heal`
- Kyber RPG 00 - Rules Engine.json `SECTION 17 — OBLIGATION, DUTY, AND MORALITY` key `conflict`
- Kyber RPG 00 - Rules Engine.json `SECTION 19 — FORCE PHILOSOPHY AND TEMPTATION` key `jedi`
- Kyber RPG 00 - Rules Engine.json `SECTION 19 — FORCE PHILOSOPHY AND TEMPTATION` key `sith`
- Kyber RPG 00 - Rules Engine.json `SECTION 19 — FORCE PHILOSOPHY AND TEMPTATION` key `fear`
- Kyber RPG 00 - Rules Engine.json `SECTION 20 — VEHICLES, SILHOUETTE, SPEED, AND RANGE` key `ship`
- Kyber RPG 00 - Rules Engine.json `SECTION 22 — CHASES, PURSUITS, AND DANGEROUS PILOTING` key `escape`
- Kyber RPG 00 - Rules Engine.json `SECTION 25 — TALENTS, CAREERS, SPECIALIZATIONS, AND EXPERIENCE` key `career`
- Kyber RPG 00 - Rules Engine.json `SECTION 29 — NARRATIVE RESULT TEMPLATES` key `success`
- Kyber RPG 00 - Rules Engine.json `SECTION 29 — NARRATIVE RESULT TEMPLATES` key `failure`
- Kyber RPG 00 - Rules Engine.json `SECTION 29 — NARRATIVE RESULT TEMPLATES` key `threat`
- Kyber RPG 11 - Force Orders.json `sith and dark side orders` key `sith`

### Long Entries

- Kyber RPG 00 - Rules Engine.json:1450 `SECTION 28 — GM AND NARRATOR OPERATING RULES` est. 1163 tokens
- Kyber RPG 00 - Rules Engine.json:25 `SECTION 0 — ROLE AND LAYER SEPARATION` est. 759 tokens
- Kyber RPG 00 - Rules Engine.json:67 `SECTION 1 — SYSTEM IDENTITY AND PLAY MODEL` est. 502 tokens
- Kyber RPG 00 - Rules Engine.json:175 `SECTION 2 — CHARACTERISTICS, SKILLS, AND CHECK CONSTRUCTION` est. 443 tokens
- Kyber RPG 00 - Rules Engine.json:918 `SECTION 17 — OBLIGATION, DUTY, AND MORALITY` est. 393 tokens
- Kyber RPG 00 - Rules Engine.json:315 `SECTION 5 — SPENDING ADVANTAGE, THREAT, TRIUMPH, AND DESPAIR` est. 388 tokens
- Kyber RPG 00 - Rules Engine.json:270 `SECTION 4 — DIFFICULTY, UPGRADES, DOWNGRADES, AND IMPOSSIBLE TASKS` est. 365 tokens
- Kyber RPG 00 - Rules Engine.json:968 `SECTION 18 — FORCE DICE, FORCE POWERS, AND DARK SIDE USE` est. 363 tokens
- Kyber RPG 00 - Rules Engine.json:769 `SECTION 14 — SOCIAL ENCOUNTERS` est. 362 tokens
- Kyber RPG 00 - Rules Engine.json:409 `SECTION 7 — WOUNDS, STRAIN, SOAK, AND INCAPACITATION` est. 360 tokens
- Kyber RPG 00 - Rules Engine.json:662 `SECTION 12 — WEAPON QUALITIES AND DEFENSE` est. 360 tokens
- Kyber RPG 00 - Rules Engine.json:222 `SECTION 3 — DICE SYMBOLS AND CANCELLATION` est. 342 tokens
- Kyber RPG 00 - Rules Engine.json:1067 `SECTION 20 — VEHICLES, SILHOUETTE, SPEED, AND RANGE` est. 330 tokens
- Kyber RPG 00 - Rules Engine.json:1115 `SECTION 21 — VEHICLE DAMAGE, ARMOR, CRITICAL HITS, AND REPAIRS` est. 328 tokens
- Kyber RPG 00 - Rules Engine.json:1506 `SECTION 29 — NARRATIVE RESULT TEMPLATES` est. 317 tokens
- Kyber RPG 00 - Rules Engine.json:869 `SECTION 16 — HEALING, MEDICINE, STIMPACKS, AND BACTA` est. 312 tokens
- Kyber RPG 00 - Rules Engine.json:610 `SECTION 11 — PERSONAL COMBAT CHECKS` est. 309 tokens
- Kyber RPG 00 - Rules Engine.json:1017 `SECTION 19 — FORCE PHILOSOPHY AND TEMPTATION` est. 304 tokens
- Kyber RPG 00 - Rules Engine.json:1308 `SECTION 25 — TALENTS, CAREERS, SPECIALIZATIONS, AND EXPERIENCE` est. 304 tokens
- Kyber RPG 00 - Rules Engine.json:1163 `SECTION 22 — CHASES, PURSUITS, AND DANGEROUS PILOTING` est. 302 tokens
- Kyber RPG 00 - Rules Engine.json:1262 `SECTION 24 — CRAFTING, MODIFICATIONS, HARD POINTS, AND ATTACHMENTS` est. 301 tokens

### Low Probability Entries

- None found.

## Recommended Next Action

Start trigger simulation with `Kyber RPG 00 - Rules Engine.json`, because it is the only systems-engine lorebook and contains the core rule-enforcement behavior.

Then simulate common player messages against the key set to measure how many entries activate under Janitor AI's default 3-message lorebook depth.
