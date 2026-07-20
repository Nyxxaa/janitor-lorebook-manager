# Kyber RPG Lorebook Audit and Maintenance Instructions

## Project Purpose

This repository contains the JSON lorebooks attached to the Janitor AI bot **Kyber RPG**, a Star Wars roleplaying game using **DeepSeek** for chat generation and based mechanically on the Fantasy Flight Games / Edge Studio narrative dice version of the Star Wars RPG.

The goal is to build a broad, canon-and-Legends-aware Star Wars RPG knowledge system that gives the LLM the information it actually needs to run accurate scenes.

The goal is not raw encyclopedia bulk. The goal is complete useful coverage: compact, reliable, retrieval-efficient entries that:

- corrects likely model mistakes
- enforces Kyber RPG continuity and roleplay behavior
- supplies obscure, recent, easily confused, or model-weak information
- preserves canon character behavior
- supports believable consequences, mechanics, and world simulation
- avoids token bloat from information DeepSeek or other capable LLMs likely already know
- activates only the entries actually relevant to the current scene
- separates canon, Legends, inference, and original scenario material cleanly
- supplies enough Fantasy Flight Games RPG mechanics to adjudicate play without turning the bot into a rigid videogame engine

Do not add basic Star Wars facts merely for completeness unless they are needed for retrieval, disambiguation, continuity control, or operational RPG behavior.

## Current Lorebook Set

Use these Janitor-facing lorebook files:

- `Kyber RPG 00 - Rules Engine.json`
- `Kyber RPG 01 - Core Continuity.json`
- `Kyber RPG 02 - Eras and History.json`
- `Kyber RPG 03 - Characters.json`
- `Kyber RPG 04 - Factions and Governments.json`
- `Kyber RPG 05 - Worlds and Regions.json`
- `Kyber RPG 06 - Species and Cultures.json`
- `Kyber RPG 07 - Society Law Economy.json`
- `Kyber RPG 08 - Technology Ships Gear.json`
- `Kyber RPG 09 - Creatures and Hazards.json`
- `Kyber RPG 10 - Force Powers.json`
- `Kyber RPG 11 - Force Orders.json`
- `Kyber RPG 12 - Lightsabers and Kyber.json`
- `Kyber RPG 13 - Force Metaphysics Artifacts.json`
- `Kyber RPG 14 - Legends Supplements.json`

## Platform Rules Snapshot

Maintain `JANITOR_AI_PLATFORM_RULES.md` as the local dated summary of Janitor AI platform rules and rule-like guidance.

As of the 2026-07-20 research pass:

- Janitor AI community/platform guidance should be treated as 18+ for this project.
- Kyber RPG must be designed for adult users and adult player characters.
- Never sexualize minors, age-ambiguous characters, childlike characters, or canon minors.
- Public-facing cards, avatars, and images must be conservative: no explicit sexual imagery, no realistic pornographic images, and no graphic gore visuals.
- Written fictional violence, crime, horror, war, torture, injury, coercion, and other dark Star Wars themes may be supported when they are narrative, fictional, consequence-driven, and not real-world instructions or glorification.
- Do not include doxxing, harassment, real-world hate endorsement, platform abuse, scraping, ban evasion, or moderation-bypass instructions.
- Re-check official Janitor AI rules before publishing major public-facing changes; direct official pages were not fully accessible during the 2026-07-20 research pass.

Kyber RPG may be brutal, mature, and realistic, but "18+ dead dove" does not mean platform-rule-free. Heavy content should be warned for, fictionalized, and framed as dangerous or consequential rather than aspirational.

## Runtime Context

Janitor AI does not provide a clean hidden meta layer separate from ordinary context.

Use these exact role definitions consistently:

- `Player` = the physical human at the keyboard
- `{{user}}` = the Player's in-fiction player character
- `GM` = the LLM acting as narrator, referee, rules engine, and world simulator
- `NPCs` = all in-fiction characters other than `{{user}}`

Do not collapse these identities.

DeepSeek may follow repeated instructions too strongly and may ignore instructions that do not trigger. Retrieval design matters as much as lore accuracy.

## Continuity Policy

- canon = primary continuity
- legends = secondary continuity
- Wookieepedia detail = tertiary research/detail layer
- canon controls direct conflicts
- compatible Legends material may fill canon gaps
- Wookieepedia may be used heavily for aliases, minor entities, obscure details, and fiddlebits, but it never overrides official canon or clearly labeled Legends continuity
- established chronology remains default
- history changes only after sufficient in-fiction causal intervention
- do not silently merge contradictory canon and Legends facts
- recent official canon must be treated as higher priority than old model memory

## Repository Rules

Only edit JSON lorebook files unless explicitly instructed otherwise.

Do not create a giant cumulative master import.

Do not duplicate entire lorebooks.

Work category by category and preserve the existing 15-lorebook deployment limit unless a reorganization plan is explicitly approved.

Create reports, validators, and temporary analysis files in clearly named subfolders such as:

- `reports/`
- `scripts/`
- `tests/`
- `archive/`

Never overwrite source files before creating a backup or working branch.

## Required JSON Schema

Every lorebook entry must contain exactly these fields:

- `activationMode`
- `activationScript`
- `case_sensitive`
- `category`
- `comment`
- `constant`
- `content`
- `enabled`
- `extensions`
- `groupWeight`
- `id`
- `inclusionGroupRaw`
- `insertion_order`
- `key`
- `keyMatchPriority`
- `keysecondary`
- `keysecondaryRaw`
- `keysRaw`
- `matchWholeWords`
- `minMessages`
- `name`
- `prioritizeInclusion`
- `priority`
- `probability`
- `selectiveLogic`
- `tags`
- `keywordsRaw`

Do not add or remove schema fields.

Validate:

- JSON parses successfully
- each file contains a top-level array
- every entry has the exact schema
- IDs are unique
- names are unique within each file
- insertion orders are sorted
- keys are non-empty unless the entry is intentionally constant
- `keysRaw` matches `key`
- `keywordsRaw` matches `key` where that field is used
- no malformed or empty content
- no duplicate entries
- no duplicate keys inside a single entry
- no accidental copied trigger lists across unrelated entries

## Lorebook Writing Style

Use machine-oriented technical English.

Inside `content`:

- section header or entity name in ALL CAPS
- remaining text lowercase
- compressed factual lines
- use `=` for relationships, mappings, chronology, and definitions
- avoid prose paragraphs
- avoid examples unless behavior cannot be expressed clearly without them
- avoid markdown formatting inside lorebook content
- avoid filler, praise, commentary, or source-discussion prose
- avoid meta entries titled `alias`, `safeguard`, `correction`, `duplicate`, `typo`, `detail`, or `expansion` unless they are genuine independent lore concepts

Preferred structure:

```text
DARTH VADER
identity = ...
goals = ...
methods = ...
social behavior = ...
trust threshold = ...
violence threshold = ...
loyalties = ...
fears = ...
blind spots = ...
response to strangers = ...
response to threats = ...
response to vulnerability = ...
```

## Token-Bloat Standard

Assume DeepSeek and other major LLMs already know broad, famous Star Wars facts.

Retain or add lore only when at least one of these is true:

1. The fact is obscure, recent, niche, or commonly hallucinated.
2. The fact is required to enforce Kyber RPG continuity.
3. The fact distinguishes two easily confused people, places, technologies, eras, factions, species, or Force concepts.
4. The fact materially changes NPC behavior, consequences, access, capability, or scene logic.
5. The fact supplies operational detail needed for roleplay.
6. The fact corrects a known model failure.
7. The fact is post-2025 or otherwise newer than likely model training.
8. The fact is Legends material that must be carefully separated from canon.
9. The fact establishes a hard limit the model otherwise tends to ignore.
10. The fact supports retrieval for a term the model is likely to mishandle.

Remove or compress lore that only restates universally known facts such as:

- Luke Skywalker is a Jedi
- Darth Vader is Anakin Skywalker
- Tatooine is a desert planet
- X-wings are Rebel starfighters

Keep such facts only when they are part of a compact behavior or continuity entry that provides additional necessary constraints.

## Trigger Design Principles

Janitor AI injects every matching lore entry.

Trigger quality is critical.

Janitor AI lorebooks should be treated as conditional prompt injection, not as a searchable database. If an entry does not activate, the model cannot use it. If too many entries activate, they compete with chat history, character definition, memory, and each other.

Janitor AI's key-field guidance says: "When these words appear in chat, this lore will be activated. You can use Regular Expressions (RegEx) by wrapping the pattern in slashes (e.g. /pattern/). Flags can be added after the closing slash (e.g. /pattern/gi)."

The practical limit is not only the number of attached lorebooks. The practical limit is how many entries and tokens activate on a single turn.

### General rules

- Prefer exact entity names and natural roleplay phrases.
- Use `matchWholeWords = true` for literal keys unless regex behavior is intentionally required.
- Avoid generic one-word triggers when possible.
- Avoid keys likely to appear in ordinary prose unless the entry truly needs to activate often.
- Avoid multiple entries owning the same exact entity name unless overlap is intentional and non-redundant.
- Summary entries must not own the exact names of entities that have dedicated entries.
- Dedicated entries should own exact names and aliases.
- A trigger should retrieve the smallest useful body of lore.
- Do not use rules terminology as the only trigger for rules that should activate from fictional circumstances.
- Do not copy a long generic action trigger list into unrelated sections.
- After import or manual upload, confirm important entries did not default to low probability. Critical entries should normally use `probability = 100`.
- Confirm the lorebook is attached to the bot and published/saved in Janitor AI before assuming a trigger design failed.
- Test using both exact OOC key checks and natural roleplay phrasing.
- Treat priority as survival importance under token pressure.
- Treat insertion order as prompt placement/attention control.
- Treat standard Janitor AI lorebook depth as 3 messages unless bot settings say otherwise.
- Treat search depth as a limited recent-context window; old mentions may stop activating.
- Do not rely on lorebooks for evolving session state. Put playthrough-specific events in chat memory, summaries, or explicit recap systems.
- Use regex keys only when literal keys cannot solve the problem cleanly.
- Test every regex key against natural roleplay text before upload.
- Prefer regex for bounded typo families, word-boundary variants, or phrase variants.
- Avoid regex that matches common verbs, short words, or broad Star Wars vocabulary.
- A normal user message should usually activate only the directly relevant entity, mechanics, and continuity entries.

### Dangerous broad triggers

Flag and usually remove or replace keys such as:

- `action`
- `thing`
- `person`
- `ship`
- `weapon`
- `armor`
- `force`
- `fear`
- `threat`
- `success`
- `failure`
- `range`
- `career`
- `conflict`
- `character`
- `planet`
- `jedi`
- `sith`

These may be valid in rare always-needed or top-level entries, but they should be treated as high-risk.

### Summary versus dedicated entries

Bad:

- `major worlds` contains keys for `coruscant`, `tatooine`, `mandalore`
- dedicated `coruscant`, `tatooine`, and `mandalore` entries also exist

Preferred:

- summary keys = `major worlds`, `important planets`, `prominent systems`
- dedicated world entries own their exact names

### Natural-language mechanics triggers

Rules should activate from how players actually write.

Examples:

- surprise/initiative = `without warning`, `ambush`, `intruder`, `security breach`, `draws a weapon`
- legal consequences = `arrest`, `detain`, `trespass`, `unauthorized`, `custody`, `warrant`
- social conflict = `convince`, `threaten`, `lie`, `interrogate`, `negotiate`
- healing = `injured`, `bleeding`, `heal`, `bacta`, `stabilize`
- vehicle = `pilot`, `starship`, `speeder`, `dogfight`, `take off`
- Force use = `use the force`, `force push`, `mind trick`, `force choke`

## Constant Entry Policy

Constant entries should be rare.

Use constant entries only for rules that must govern every generation.

Likely constant rules:

- Player / `{{user}}` / GM / NPC layer separation
- player action declaration = attempt, not automatic success
- NPC independence and character integrity
- scene consequences and progression
- core canon/Legends hierarchy in compressed form

Do not make duplicate quick references constant.

Do not make large factual encyclopedic entries constant.

DeepSeek may overweight repeated constant instructions.

If a lore entry is only important after a topic appears in chat, it should not be constant. Prefer precise keys, high probability, and suitable priority/insertion order.

## Player Action Resolution

The Player does not need to write “I try.”

Statements such as:

- `I open the locked door.`
- `I dodge.`
- `I grab his lightsaber.`
- `I convince Vader.`
- `I heal him.`

represent attempted actions when success is uncertain, opposed, dangerous, consequential, or capability-dependent.

Declarative wording does not establish success.

`{{user}}` controls:

- deliberate choices
- voluntary movement
- dialogue
- private thoughts
- sincere beliefs
- emotional conclusions
- attempted actions

The GM controls:

- whether attempts succeed
- NPC actions
- attacks against `{{user}}`
- restraint
- capture
- injury
- forced movement
- environmental consequences
- external reality

NPC action against `{{user}}` is not player-character puppeting.

## Dice Randomness Policy

LLMs are not trusted random number generators.

Default to player-roll-first mode for meaningful checks:

- GM states the check, difficulty, and major modifiers.
- Player provides the final result from an external roller or their own dice.
- GM narrates consequences from the supplied result.

If the Player explicitly requests fast play, the GM may use a labeled `GM-simulated result`, but it must not be described as true randomness.

Recommended public roller link:

- https://rolladvantage.com/diceroller/

Optional public character-sheet tool:

- https://app.rpgsessions.com/

## NPC Character Integrity

Character entries should prioritize operational behavior over biography.

For major NPCs, include where useful:

- goals
- methods
- loyalties
- fears
- pride
- paranoia
- trust threshold
- violence threshold
- interrogation style
- response to uncertainty
- response to strangers
- response to threats
- response to vulnerability
- response to attraction
- response to kindness
- response to future knowledge
- willingness to deceive
- willingness to cooperate temporarily
- conditions for ideological change

Do not make canonical villains passive merely to preserve a requested pose, romance, or mood.

Kindness, vulnerability, beauty, humor, unusual powers, or future knowledge do not automatically earn trust.

Trust, affection, loyalty, redemption, and ideological change require cumulative evidence and time.

## Knowledge Firewall

Always preserve:

- Player knowledge ≠ `{{user}}` knowledge
- GM knowledge ≠ NPC knowledge
- lorebook knowledge ≠ automatic NPC knowledge
- future canon knowledge ≠ current-era character knowledge
- hidden identities remain hidden until plausibly learned
- private events remain private unless evidence exists

## Audit Workflow

Perform work in this order.

### Phase 1 — Inventory

Do not edit source files.

Produce:

- file names
- entry counts
- file sizes
- constant-entry counts
- total trigger counts
- single-word trigger counts
- duplicate IDs
- duplicate names
- duplicate content
- duplicate keys within entries
- duplicate keys across files
- malformed schema
- malformed `keysRaw`
- malformed `keywordsRaw`
- likely typo or spacing errors
- entries with suspicious meta titles
- entries with unusually long content
- entries with unusually many keys

Save as:

- `reports/inventory.md`
- `reports/inventory.json`

### Phase 2 — Trigger Collision Audit

Do not edit source files.

For every normalized key, report:

- which files and entries contain it
- whether the overlap is intentional
- whether content is redundant
- whether content conflicts
- whether a summary entry is competing with a dedicated entry
- likely activation frequency
- collision severity: low, medium, high, critical

Create test messages representing natural roleplay, including:

- `I search the room.`
- `I grab Vader's lightsaber.`
- `A stranger appears without warning.`
- `The guards move to arrest me.`
- `I use the Force to heal him.`
- `We land on Coruscant.`
- `I ask the Twi'lek merchant about the price.`
- `The ship drops out of hyperspace.`
- `I threaten the Imperial officer.`
- `Palpatine smiles and offers cooperation.`

Report which entries each message would trigger.

Save as:

- `reports/trigger_collisions.md`
- `reports/trigger_simulation.json`

### Phase 3 — Token-Bloat Audit

Do not edit source files.

Classify every entry:

- retain
- retain but compress
- merge
- remove as common model knowledge
- remove as duplicate
- rewrite for behavioral value
- rewrite for continuity value
- source-audit required
- recent-canon update required

Do not remove an entry solely because the fact is famous if the entry also provides necessary RPG behavior, limits, chronology, or retrieval control.

Save as:

- `reports/token_bloat_audit.md`
- `reports/entry_classification.json`

### Phase 4 — Coverage Gap Audit

Do not add lore yet.

Identify missing information that meets the token-bloat standard.

Prioritize:

1. behavioral gaps in major NPCs
2. continuity control
3. recent canon
4. obscure or model-confused material
5. everyday RPG operational knowledge
6. legal, social, security, and institutional consequences
7. Force limits and unusual metaphysics
8. Legends/canon separation
9. species and cultural behavior needed for NPC portrayal
10. technology limits and practical use

Do not recommend adding hundreds of trivial entries.

Save as:

- `reports/coverage_gaps.md`
- `reports/proposed_additions.json`

### Phase 5 — Controlled Cleanup

Only begin after the reports are reviewed.

Edit one lorebook or one tightly scoped issue category at a time.

For each cleanup:

- create backup
- make minimal changes
- validate schema
- rerun trigger tests
- compare file size and entry count
- provide a changelog
- do not silently remove lore
- do not rename IDs unless necessary
- preserve insertion order unless reordering is intentional
- do not alter unrelated entries

## Known Issues to Check

Look specifically for:

- old attached character book with only about 207 entries versus later expanded character work
- malformed character names
- typo-safeguard or duplicate-safeguard entries
- biography-only character entries lacking behavioral data
- broad summary entries that duplicate dedicated entries
- `phr ik` instead of `phrik`
- `sub light engine` instead of `sublight engine`
- malformed ship designations
- Yavin typo/alias entries
- `nardina 5` instead of `narkina 5`
- `t ython` instead of `tython`
- `chand rila` instead of `chandrila`
- `wells pring` instead of `wellspring`
- `mortiss` instead of `mortis`
- `sabine-era relevance = none` in Darth Maul
- broad generic keys copied across unrelated rules entries
- summary/dedicated collisions for planets, Force concepts, and technology
- redundant constant quick-reference rules
- entries that treat interpretation as confirmed cosmology
- recent canon missing from 2024–2026
- unsupported or invented entries
- ambiguous death statuses
- canon/Legends claims merged without labels

## Source and Factuality Policy

For pre-2026 stable facts, use trusted primary or official sources when verification is necessary.

For any post-2025 canon, current release information, or potentially changed official status:

- verify using current official Star Wars sources
- do not rely only on model memory
- record source URLs in reports, not inside lorebook content unless explicitly requested
- distinguish confirmed facts from inference
- do not invent details to fill gaps

When technical validation is possible through scripts, prefer automated checks over manual claims.

## Deliverables Standard

Every task must end with:

- summary of what was inspected
- files changed
- files not changed
- validation results
- unresolved uncertainties
- recommended next action
- exact paths to generated reports or cleaned files

Do not claim a lorebook is production-ready unless:

- schema validation passes
- duplicate and malformed keys are addressed
- trigger simulation passes
- no critical collision remains unexplained
- no known factual issue remains unmarked
- file size remains practical for Janitor AI
- changes were reviewed against the token-bloat standard

## First Task

Begin with **Phase 1 — Inventory** only.

Do not edit any lorebook JSON files.

Create the inventory reports and validation scripts first.
