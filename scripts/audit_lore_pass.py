import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

JSON_FILES = sorted(
    path
    for path in ROOT.glob("Kyber RPG *.json")
    if path.name not in {"Kyber RPG Rules.json", "Kyber RPG 00 - Rules Engine.json"}
)

COMMON_REMOVE_PATTERNS = [
    r"^identity = .*jedi",
    r"^identity = .*sith",
    r"^type = .*planet",
    r"^type = .*starfighter",
    r"^type = .*droid",
]

OPERATIONAL_TERMS = {
    "goals",
    "methods",
    "limits",
    "risk",
    "danger",
    "response",
    "behavior",
    "trust",
    "loyal",
    "fear",
    "paranoia",
    "legal",
    "access",
    "security",
    "consequence",
    "continuity",
    "canon",
    "legends",
    "use =",
    "era =",
    "location",
    "politics",
    "culture",
    "doctrine",
}

RECENT_CANON_TOPICS = [
    {
        "topic": "Andor season 2",
        "terms": ["andor season 2", "mina-rau", "ghorman massacre", "krennic andor season 2"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Factions and Governments.json"],
        "reason": "2025 Disney+ release; likely beyond many model memories and important for Rebellion/Imperial behavior.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Skeleton Crew",
        "terms": ["skeleton crew", "at attin", "jod na nawwood", "fern wim neel kb"],
        "target_files": ["Star Wars History.json", "Star Wars Geography.json", "Star Wars Characters.json"],
        "reason": "2024-2025 Disney+ release; new locations/characters are likely undercovered.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Tales of the Underworld",
        "terms": ["tales of the underworld", "asajj ventress underworld", "cad bane underworld"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Factions and Governments.json"],
        "reason": "2025 animated anthology; may update criminal/character continuity.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "The High Republic Phase III ending",
        "terms": ["trials of the jedi", "avar kriss", "elzar mann", "nihil ending", "nameless creatures"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Creatures.json", "Star Wars Factions and Governments.json"],
        "reason": "2025 conclusion of major publishing initiative; canon chronology and Nameless/Nihil details matter.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "The Acolyte publishing and characters",
        "terms": ["the acolyte wayseeker", "the crystal crown", "osha aniseya", "mae aniseya", "the stranger qimir"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Force Orders and Traditions.json"],
        "reason": "2024 series plus 2025 tie-ins; high-risk for hallucinated High Republic/Sith-era details.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Star Wars Outlaws",
        "terms": ["star wars outlaws", "kay vess", "nix", "sliro", "zerek besh"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Factions and Governments.json", "Star Wars Creatures.json"],
        "reason": "2024 canon game; useful for underworld, criminal, and everyday RPG play.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Reign of the Empire: The Mask of Fear",
        "terms": ["mask of fear", "reign of the empire", "mon mothma early empire", "bail organa early empire"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Factions and Governments.json"],
        "reason": "2025 canon novel trilogy opener; valuable for early Empire political resistance.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Bad Batch: Sanctuary and Ghost Agents",
        "terms": ["bad batch sanctuary", "ghost agents", "asajj ventress ghost agents"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json"],
        "reason": "2025 publishing tied to post-Clone-Wars clone and Ventress continuity.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Darth Vader: Master of Evil",
        "terms": ["master of evil", "darth vader master of evil"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json"],
        "reason": "2025 Darth Vader novel; important only if it adds behavioral/chronology constraints.",
        "source": "https://www.starwars.com/news/star-wars-best-of-2025",
    },
    {
        "topic": "Maul: Shadow Lord",
        "terms": ["maul shadow lord", "star wars maul shadow lord"],
        "target_files": ["Star Wars History.json", "Star Wars Characters.json", "Star Wars Factions and Governments.json"],
        "reason": "Announced 2026 series; do not add plot facts yet, but mark as future-canon watch item.",
        "source": "https://www.starwars.com/news",
    },
]


def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def token_estimate(text):
    return max(1, round(len(text) / 4))


def load_entries():
    rows = []
    for path in JSON_FILES:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        for index, entry in enumerate(data):
            rows.append({"file": path.name, "index": index, "entry": entry})
    return rows


def classify_entry(row):
    entry = row["entry"]
    content = entry.get("content", "")
    keys = entry.get("key", [])
    content_norm = normalize(content)
    key_count = len(keys) if isinstance(keys, list) else 0
    tokens = token_estimate(content)
    reasons = []
    classification = "retain"

    operational = any(term in content_norm for term in OPERATIONAL_TERMS)

    if tokens < 45 and key_count <= 3 and not operational:
        classification = "remove_or_merge"
        reasons.append("short entry with little operational behavior or continuity value")

    if row["file"] == "Star Wars Characters.json":
        has_behavior = any(term in content_norm for term in ["goals", "methods", "traits", "response", "loyal", "fear", "trust", "doctrine", "willingness"])
        if not has_behavior and tokens < 90:
            classification = "rewrite_for_behavior"
            reasons.append("character entry is mostly identity/biography; add behavior or remove if common")

    if "legends" in content_norm and "canon" not in content_norm:
        reasons.append("Legends-labeled or Legends-adjacent entry should be checked for canon conflict labels")
        if classification == "retain":
            classification = "source_audit"

    if key_count > 8:
        reasons.append(f"many keys ({key_count}); check activation pressure")
        if classification == "retain":
            classification = "retain_but_key_audit"

    if any(re.search(pattern, content_norm, flags=re.MULTILINE) for pattern in COMMON_REMOVE_PATTERNS) and tokens < 70:
        reasons.append("looks like common model knowledge unless needed for disambiguation")
        if classification == "retain":
            classification = "remove_or_merge"

    return {
        "file": row["file"],
        "index": row["index"],
        "name": entry.get("name", ""),
        "id": entry.get("id", ""),
        "classification": classification,
        "estimated_tokens": tokens,
        "key_count": key_count,
        "reasons": reasons,
    }


def coverage_scan(rows):
    haystack_by_file = defaultdict(str)
    all_text = []
    for row in rows:
        entry = row["entry"]
        blob = " ".join(
            [
                row["file"],
                entry.get("name", ""),
                entry.get("content", ""),
                entry.get("keysRaw", ""),
            ]
        )
        haystack_by_file[row["file"]] += "\n" + normalize(blob)
        all_text.append(normalize(blob))
    all_haystack = "\n".join(all_text)

    gaps = []
    for topic in RECENT_CANON_TOPICS:
        found_terms = [term for term in topic["terms"] if normalize(term) in all_haystack]
        missing_terms = [term for term in topic["terms"] if normalize(term) not in all_haystack]
        if missing_terms:
            gaps.append({**topic, "found_terms": found_terms, "missing_terms": missing_terms})
    return gaps


def duplicate_key_pressure(rows):
    locations = defaultdict(list)
    for row in rows:
        entry = row["entry"]
        keys = entry.get("key", [])
        if not isinstance(keys, list):
            continue
        for key in keys:
            normalized = normalize(str(key))
            if normalized:
                locations[normalized].append(
                    {"file": row["file"], "name": entry.get("name", ""), "index": row["index"]}
                )

    pressure = []
    for key, locs in locations.items():
        files = sorted({loc["file"] for loc in locs})
        if len(locs) >= 4 or len(files) >= 3:
            pressure.append({"key": key, "count": len(locs), "files": files, "locations": locs[:30]})
    return sorted(pressure, key=lambda item: (-item["count"], item["key"]))


def write_reports(classifications, gaps, pressure):
    REPORTS.mkdir(exist_ok=True)

    summary = {
        "generated": date.today().isoformat(),
        "classifications": classifications,
        "coverage_gaps": gaps,
        "duplicate_key_pressure": pressure,
    }
    (REPORTS / "lore_pass_audit.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (REPORTS / "entry_classification.json").write_text(json.dumps(classifications, indent=2, ensure_ascii=False), encoding="utf-8")
    (REPORTS / "proposed_additions.json").write_text(json.dumps(gaps, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = Counter(item["classification"] for item in classifications)
    by_file = defaultdict(Counter)
    for item in classifications:
        by_file[item["file"]][item["classification"]] += 1

    md = []
    md.append("# Kyber RPG Lore Pass Audit")
    md.append("")
    md.append(f"Generated: {date.today().isoformat()}")
    md.append("")
    md.append("## Scope")
    md.append("")
    md.append("- Audits factual Star Wars lorebooks only; `Kyber RPG Rules.json` is excluded because it is the systems engine.")
    md.append("- This report recommends additions/removals but does not edit lorebook JSON files.")
    md.append("- Canon should control direct conflicts; Legends may fill gaps only when labeled and compatible.")
    md.append("")
    md.append("## Classification Counts")
    md.append("")
    for key, count in counts.most_common():
        md.append(f"- {key}: {count}")
    md.append("")
    md.append("## By File")
    md.append("")
    md.append("| File | retain | key audit | behavior rewrite | source audit | remove/merge |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for file_name in sorted(by_file):
        c = by_file[file_name]
        md.append(
            f"| {file_name} | {c['retain']} | {c['retain_but_key_audit']} | {c['rewrite_for_behavior']} | {c['source_audit']} | {c['remove_or_merge']} |"
        )
    md.append("")
    md.append("## Highest-Value Removal or Compression Candidates")
    md.append("")
    candidates = [
        item
        for item in classifications
        if item["classification"] in {"remove_or_merge", "rewrite_for_behavior", "retain_but_key_audit"}
    ]
    candidates = sorted(candidates, key=lambda item: (item["classification"], -item["estimated_tokens"], -item["key_count"]))
    for item in candidates[:120]:
        reason = "; ".join(item["reasons"]) or "review"
        md.append(
            f"- `{item['classification']}` {item['file']} :: {item['name']} ({item['estimated_tokens']} est. tokens, {item['key_count']} keys): {reason}"
        )
    if not candidates:
        md.append("- None.")
    md.append("")
    md.append("## Recent Canon Coverage Gaps")
    md.append("")
    for gap in gaps:
        md.append(f"### {gap['topic']}")
        md.append(f"- Missing terms: {', '.join(gap['missing_terms'])}")
        if gap["found_terms"]:
            md.append(f"- Already present: {', '.join(gap['found_terms'])}")
        md.append(f"- Target files: {', '.join(gap['target_files'])}")
        md.append(f"- Why add: {gap['reason']}")
        md.append(f"- Source: {gap['source']}")
        md.append("")
    if not gaps:
        md.append("- No checked recent-canon gaps found.")
    md.append("## Duplicate Key Pressure")
    md.append("")
    for item in pressure[:80]:
        md.append(f"- `{item['key']}` appears in {item['count']} entries across {len(item['files'])} files: {', '.join(item['files'])}")
    if not pressure:
        md.append("- None.")
    md.append("")
    md.append("## Recommended Work Order")
    md.append("")
    md.append("1. Review recent-canon gaps and add only compact entries that affect RPG play, continuity, or common hallucinations.")
    md.append("2. Rewrite major character entries that are mostly biography into operational behavior entries.")
    md.append("3. Audit duplicate key pressure before expanding lore, especially one-word species/place/technology keys.")
    md.append("4. Compress or merge short common-knowledge entries only after confirming they do not supply disambiguation or behavior.")

    (REPORTS / "lore_pass_audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    coverage_md = []
    coverage_md.append("# Kyber RPG Coverage Gaps")
    coverage_md.append("")
    coverage_md.append(f"Generated: {date.today().isoformat()}")
    coverage_md.append("")
    coverage_md.append("These are compact, high-value additions for recent or easy-to-hallucinate Star Wars continuity. Canon additions should stay brief and only include facts that matter during play.")
    coverage_md.append("")
    for gap in gaps:
        coverage_md.append(f"## {gap['topic']}")
        coverage_md.append("")
        coverage_md.append(f"- Missing terms: {', '.join(gap['missing_terms'])}")
        if gap["found_terms"]:
            coverage_md.append(f"- Already present: {', '.join(gap['found_terms'])}")
        coverage_md.append(f"- Target files: {', '.join(gap['target_files'])}")
        coverage_md.append(f"- Reason: {gap['reason']}")
        coverage_md.append(f"- Source: {gap['source']}")
        coverage_md.append("")
    (REPORTS / "coverage_gaps.md").write_text("\n".join(coverage_md) + "\n", encoding="utf-8")

    bloat_md = []
    bloat_md.append("# Kyber RPG Token Bloat Audit")
    bloat_md.append("")
    bloat_md.append(f"Generated: {date.today().isoformat()}")
    bloat_md.append("")
    bloat_md.append("## Key Pressure")
    bloat_md.append("")
    for item in pressure:
        bloat_md.append(f"- `{item['key']}` appears in {item['count']} entries across {len(item['files'])} files: {', '.join(item['files'])}")
    if not pressure:
        bloat_md.append("- None.")
    bloat_md.append("")
    bloat_md.append("## Rewrite or Compression Candidates")
    bloat_md.append("")
    for item in candidates:
        reason = "; ".join(item["reasons"]) or "review"
        bloat_md.append(
            f"- `{item['classification']}` {item['file']} :: {item['name']} ({item['estimated_tokens']} est. tokens, {item['key_count']} keys): {reason}"
        )
    if not candidates:
        bloat_md.append("- None.")
    (REPORTS / "token_bloat_audit.md").write_text("\n".join(bloat_md) + "\n", encoding="utf-8")

    print("Wrote reports/lore_pass_audit.md")
    print("Wrote reports/lore_pass_audit.json")
    print("Wrote reports/coverage_gaps.md")
    print("Wrote reports/proposed_additions.json")
    print("Wrote reports/token_bloat_audit.md")
    print("Wrote reports/entry_classification.json")
    print(f"Classification counts: {dict(counts)}")
    print(f"Recent gaps: {len(gaps)}")
    print(f"Duplicate key pressure items: {len(pressure)}")


def main():
    rows = load_entries()
    classifications = [classify_entry(row) for row in rows]
    gaps = coverage_scan(rows)
    pressure = duplicate_key_pressure(rows)
    write_reports(classifications, gaps, pressure)


if __name__ == "__main__":
    main()
