# Janitor AI Platform Rules Snapshot

Research date: 2026-07-20

This file records the rules and rule-like guidance found for the Kyber RPG project. Re-check Janitor AI's logged-in official Terms, content guidelines, and Discord announcements before publishing major public-facing changes, because platform rules can change and some official pages are not accessible from this environment.

## Source Reliability

Highest-confidence accessible source:

- Archived r/JanitorAI_Official sidebar/rules snapshot, archived 2025-07-14 from a 2025-07-11 page: https://archive.ph/n7w5r

Secondary sources used because direct `janitorai.com` legal pages were not accessible here:

- DocDecoder summary of JanitorAI Terms of Service, last updated 2025-01-17: https://docdecoder.app/summary/janitorai.com/terms-of-service
- RoboRhythms article on Janitor AI fight-scene/image-rule distinction, posted/updated 2026-07-03: https://www.roborhythms.com/janitor-ai-fight-scenes/
- RoboRhythms article on Janitor AI lorebook troubleshooting, posted 2026-06-05 and updated 2026-07-14: https://www.roborhythms.com/janitor-ai-lorebook-not-working/
- JanitorAI.ai terms page, last updated 2026-01-01: https://janitorai.ai/terms

Lower-confidence implementation references:

- RisuAI lorebook docs, useful for general lorebook concepts but not Janitor-specific: https://kwaroran.github.io/docs/characterconfig/lorebook/
- LoreBary guide, marked outdated and specific to a Janitor AI proxy/extension rather than native Janitor lorebooks: https://lorebary-guide.carrd.co/
- JannyAI-hosted Lorebook / Script Agent Skill page, user-generated but lists official Janitor help article URLs that could not be opened here: https://jannyai.com/characters/91352b77-26f7-467d-8e25-819b65de4b48_character-lorebook-script-agent-skill

Do not treat secondary summaries as binding legal text. Use them as cautionary guidance until the official logged-in rules are manually checked.

## Rules Found

### Age and Minor Safety

- JanitorAI is described by the official subreddit rules as 18+ only.
- Minors are not allowed in the official community spaces.
- Sexualized, exploitative, or inappropriate depictions of underage characters are not allowed.
- Public bot cards, images, avatars, scenarios, and example messages must not sexualize minors or make the user/player character a minor in sexual or adult contexts.

Project rule: Kyber RPG must be designed for adult users and adult player characters only. Any child or teen canon character may appear only in non-sexual, age-appropriate story contexts.

### Hate, Harassment, and Doxxing

- Slurs and hate speech are prohibited in official community rules.
- Harassment, bullying, prejudice, racism, xenophobia, LGBTQIA+phobia, and discriminatory behavior are not tolerated in official community rules.
- Doxxing or posting personal identifying information is prohibited.

Project rule: Star Wars prejudice, speciesism, authoritarianism, and faction propaganda may exist as fictional world content, but the bot card and lorebook must not endorse real-world hate or target real protected groups.

### Public Images, Avatars, and Visual Content

- Official community rules prohibit IRL pornography and realistic AI-generated porn in community contexts.
- The accessible reporting says Janitor AI image/avatar rules are much stricter than text rules and prohibit graphic gore visuals such as visible killings, severed parts, open wounds, and graphic bloodshed.

Project rule: Use conservative public visuals. Do not use graphic gore, sexual assault imagery, explicit nudity, realistic pornographic images, or underage/age-ambiguous sexualized images for avatars, cards, or public assets.

### Written Fiction and Violent Roleplay

- Secondary 2026 reporting says written fight scenes, combat, injury, torture, abuse, criminal scenarios, kidnapping, and dark themes are allowed when fictional, story-driven, and not framed as real-world instructions or glorification of harm.
- The same reporting says the common "gore ban" concern primarily applies to images/avatars rather than written chat.

Project rule: Kyber RPG may support brutal, consequence-heavy fictional Star Wars violence in text. Keep it narrative, fictional, and consequence-driven. Do not turn scenes into real-world instructions, encouragement, or celebration of actual harm.

### Sexual Violence and Other Extreme Themes

- Official community rules say not to joke about themes containing sexual violence, incest, rape, heavy gore, or bestiality in community spaces.
- Secondary terms summaries list illegal activities, sexualized minors, hate speech, and private information sharing as prohibited.

Project rule: Heavy themes may be acknowledged as possible setting dangers or backstory consequences only with clear adult content warnings. Do not write public-facing material that eroticizes sexual violence, normalizes exploitation, targets minors, or presents abuse as desirable.

### Platform Integrity

- Secondary terms sources prohibit unauthorized access, malware, scraping/crawling without permission, impersonation, spam, automated account abuse, and legal violations.

Project rule: Project files should not include instructions for scraping Janitor AI, bypassing moderation, evading bans, abusing proxies, harvesting user data, or automating platform misuse.

## Kyber RPG Compliance Interpretation

Kyber RPG can remain a mature, brutal, realistic Star Wars RPG bot if it follows these boundaries:

- Adult users and adult player characters only.
- Clear 18+ and heavy-content warnings near the top of public-facing text.
- No sexualized minors, no age-ambiguous sexual content, and no adult scenarios involving childlike characters.
- Public images stay non-graphic and non-explicit.
- Written violence is fictional, story-serving, and consequence-focused.
- No real-world harm instructions, harassment, doxxing, hate endorsement, or platform-abuse instructions.
- Star Wars slavery, war crimes, torture, occupation, trafficking, genocide, fascism, and other dark topics may be included as fictional world evils, but should be framed as dangerous, traumatic, coercive, and consequential rather than aspirational.

## Janitor AI Lorebook Mechanics and Strategy

### What a Lorebook Is

- A lorebook is not a wiki the model searches on demand.
- A lorebook is a set of prompt snippets that are injected into the model context when entries activate.
- Entries compete with chat history, character definition, memory, and other prompt material for limited context.
- The model can only use lore that was actually injected.

### Activation

- Janitor AI's key field says: "When these words appear in chat, this lore will be activated. You can use Regular Expressions (RegEx) by wrapping the pattern in slashes (e.g. /pattern/). Flags can be added after the closing slash (e.g. /pattern/gi)."
- Entries activate from trigger keys/keywords in scanned chat context.
- Case-sensitive and whole-word settings can prevent otherwise correct-looking keys from matching.
- Broad one-word keys activate too often and can flood the context.
- Specific natural phrases activate more cleanly than generic category words.
- If multiple entries share a key, they may all inject and create contradiction or token overflow.
- Use secondary conditions or more specific keys to disambiguate when the platform supports them.
- Regex keys should be used sparingly and tested carefully. A broad regex can activate many entries or activate in ordinary prose.

### Probability

- Janitor imports may set entry probability very low, with 1% reported as a common failure case.
- Critical lore should use `probability = 100`.
- Important but non-critical lore should generally stay high rather than random.
- Low probability is for flavor, variation, and nonessential optional injections only.

### Constant Entries

- Constant entries always consume context.
- Use constants only for rules that must govern every response.
- Do not make encyclopedia entries constant.
- Duplicated constant rules can overpower scene logic and waste context.

### Priority and Insertion Order

- Priority is best treated as survival importance when too much lore is active.
- Insertion order affects where the injected text lands in the prompt; later/closer insertion usually gets more model attention.
- High insertion order should be reserved for immediate scene rules, active constraints, and high-importance behavioral guidance.
- Low-priority entries are the first candidates to drop or compress when token pressure appears.

### Search Depth and Token Budget

- Standard Janitor AI lorebook depth is 3 messages unless the bot settings say otherwise.
- Lorebooks scan only a limited recent window, depending on platform settings.
- A lore item mentioned many turns ago may stop activating unless scan depth is high, it is constant, or it is moved into memory/summary.
- Token overflow can silently drop entries or crowd out core character context.
- Test long-chat behavior, not only first-message behavior.

### Practical Strategy for Kyber RPG

- Use one topic per entry.
- Keep entries self-contained: include the subject name inside `content` because entry names are for organization, not guaranteed model-visible context.
- Prefer compact operational facts over prose.
- Write lore for decisions the GM must make: behavior, access, limits, consequences, chronology, faction response, and continuity conflicts.
- Split broad topics into summary entries plus dedicated entries, but avoid shared exact keys unless intentional.
- Make exact entity names belong to dedicated entries.
- Use summary-entry keys such as `major hyperspace routes` or `clone wars overview`, not all individual entity names inside the summary.
- Put model-steering RPG rules in `Kyber RPG Rules.json`; put Star Wars facts in the relevant lorebook.
- Do not rely on lorebooks to track evolving session state. Use chat memory/summary or explicit recap mechanisms for events that happen during a specific playthrough.
- Assume many attached lorebooks can create token pressure even if the platform allows them. The practical limit is not only lorebook count; it is how many entries activate per turn.
- Optimize for low activation count per user message. A normal message should usually trigger only the directly relevant entity, scene-mechanics, and continuity entries.
- Treat every new key as a cost. Add a key only if a real user is likely to write it and the entry should activate at that moment.
- Avoid regex for famous short words, broad categories, common verbs, and generic Star Wars terms unless the entry is tiny and intentionally broad.

### Test Procedure

For each changed lorebook:

1. Validate JSON before upload.
2. Confirm all important entries have sane `probability` values.
3. Confirm the lorebook is attached to the bot and published/saved in Janitor AI.
4. Send an OOC trigger test using the exact key.
5. Confirm the expected entry appears to influence the response.
6. Test natural roleplay phrasing, not only exact diagnostic commands.
7. Test collision cases where several entries might activate together.
8. Test a longer chat to see whether scan depth or token overflow causes lore loss.
