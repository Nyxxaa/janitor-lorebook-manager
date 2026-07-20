import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

EXPECTED_FIELDS = [
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

BROAD_KEYS = {
    "action",
    "thing",
    "person",
    "ship",
    "weapon",
    "armor",
    "force",
    "fear",
    "threat",
    "success",
    "failure",
    "range",
    "career",
    "conflict",
    "character",
    "planet",
    "jedi",
    "sith",
    "attack",
    "fight",
    "combat",
    "look",
    "search",
    "run",
    "hide",
    "escape",
    "grab",
    "open",
    "use",
    "heal",
    "persuade",
    "convince",
    "threaten",
    "lie",
}

ACTION_DECLARATION_MARKER = "A player statement describing an action expresses intent"
LAYER_MARKER = "ROLE AND LAYER DEFINITIONS"


def normalize_key(value):
    return re.sub(r"\s+", " ", value.strip().lower())


def estimate_tokens(text):
    return max(1, round(len(text) / 4))


def read_json(path):
    raw = path.read_text(encoding="utf-8-sig")
    return json.loads(raw)


def line_for_name(path, name):
    needle = f'"name": "{name}"'
    try:
        for idx, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
            if needle in line:
                return idx
    except UnicodeDecodeError:
        return None
    return None


def main():
    REPORTS.mkdir(exist_ok=True)

    json_files = sorted(ROOT.glob("*.json"))
    schema_expected = set(EXPECTED_FIELDS)

    inventory = {
        "generated": date.today().isoformat(),
        "root": str(ROOT),
        "files": [],
        "totals": {
            "files": 0,
            "entries": 0,
            "constant_entries": 0,
            "enabled_entries": 0,
            "keys": 0,
            "single_word_keys": 0,
            "regex_keys": 0,
            "estimated_content_tokens": 0,
        },
        "issues": {
            "invalid_json": [],
            "non_array_roots": [],
            "schema_mismatches": [],
            "duplicate_ids": [],
            "duplicate_names_within_file": [],
            "duplicate_content": [],
            "duplicate_keys_within_entry": [],
            "duplicate_keys_across_files": [],
            "broad_keys": [],
            "low_probability": [],
            "empty_keys_nonconstant": [],
            "keysraw_mismatch": [],
            "keywordsraw_mismatch": [],
            "unsorted_insertion_order": [],
            "long_entries": [],
            "large_key_lists": [],
            "repeated_rule_blocks": [],
            "suspect_filenames": [],
        },
    }

    id_locations = defaultdict(list)
    content_locations = defaultdict(list)
    key_locations = defaultdict(list)

    if (ROOT / "Star Wars Sepcies and Cultures.json").exists():
        inventory["issues"]["suspect_filenames"].append(
            {
                "file": "Star Wars Sepcies and Cultures.json",
                "issue": "filename likely typo: Sepcies should be Species",
            }
        )

    for path in json_files:
        file_info = {
            "file": path.name,
            "bytes": path.stat().st_size,
            "entries": 0,
            "constant_entries": 0,
            "enabled_entries": 0,
            "keys": 0,
            "single_word_keys": 0,
            "regex_keys": 0,
            "estimated_content_tokens": 0,
            "categories": Counter(),
            "top_long_entries": [],
            "top_key_count_entries": [],
        }

        try:
            data = read_json(path)
        except Exception as exc:
            inventory["issues"]["invalid_json"].append({"file": path.name, "error": str(exc)})
            inventory["files"].append(file_info)
            continue

        if not isinstance(data, list):
            inventory["issues"]["non_array_roots"].append({"file": path.name, "root_type": type(data).__name__})
            inventory["files"].append(file_info)
            continue

        file_info["entries"] = len(data)
        inventory["totals"]["entries"] += len(data)

        previous_order = None
        file_name_counter = Counter()

        for index, entry in enumerate(data):
            location = {
                "file": path.name,
                "index": index,
                "name": entry.get("name", ""),
                "id": entry.get("id", ""),
            }

            if not isinstance(entry, dict):
                inventory["issues"]["schema_mismatches"].append({**location, "issue": "entry is not an object"})
                continue

            fields = set(entry.keys())
            if fields != schema_expected:
                inventory["issues"]["schema_mismatches"].append(
                    {
                        **location,
                        "missing": sorted(schema_expected - fields),
                        "extra": sorted(fields - schema_expected),
                    }
                )

            name = str(entry.get("name", ""))
            file_name_counter[name] += 1

            entry_id = str(entry.get("id", ""))
            if entry_id:
                id_locations[entry_id].append(location)

            content = str(entry.get("content", ""))
            normalized_content = re.sub(r"\s+", " ", content.strip().lower())
            if normalized_content:
                content_locations[normalized_content].append(location)

            keys = entry.get("key", [])
            if not isinstance(keys, list):
                keys = []

            normalized_keys = [normalize_key(str(key)) for key in keys if str(key).strip()]
            key_counter = Counter(normalized_keys)
            duplicates_inside = [key for key, count in key_counter.items() if count > 1]
            if duplicates_inside:
                inventory["issues"]["duplicate_keys_within_entry"].append(
                    {**location, "keys": duplicates_inside}
                )

            if not entry.get("constant") and not normalized_keys:
                inventory["issues"]["empty_keys_nonconstant"].append(location)

            keys_raw = str(entry.get("keysRaw", "")).strip()
            joined_keys = ", ".join(str(key).strip() for key in keys if str(key).strip())
            if keys_raw != joined_keys:
                inventory["issues"]["keysraw_mismatch"].append(
                    {**location, "keysRaw": keys_raw, "joined": joined_keys}
                )

            keywords_raw = str(entry.get("keywordsRaw", "")).strip()
            if keywords_raw and keywords_raw != joined_keys:
                inventory["issues"]["keywordsraw_mismatch"].append(
                    {**location, "keywordsRaw": keywords_raw, "joined": joined_keys}
                )

            for key in normalized_keys:
                key_locations[key].append(location)
                if key in BROAD_KEYS:
                    inventory["issues"]["broad_keys"].append({**location, "key": key})

            if entry.get("probability", 100) < 90:
                inventory["issues"]["low_probability"].append(
                    {**location, "probability": entry.get("probability")}
                )

            order = entry.get("insertion_order")
            if isinstance(order, int):
                if previous_order is not None and order < previous_order:
                    inventory["issues"]["unsorted_insertion_order"].append(
                        {**location, "previous_order": previous_order, "order": order}
                    )
                previous_order = order

            token_estimate = estimate_tokens(content)
            key_count = len(normalized_keys)
            regex_count = sum(
                1
                for key in normalized_keys
                if key.startswith("/")
                and key.count("/") >= 2
                and not (entry.get("constant") and key == "/.*/")
            )
            single_word_count = sum(1 for key in normalized_keys if re.fullmatch(r"[\w'-]+", key))

            if token_estimate > 300:
                inventory["issues"]["long_entries"].append(
                    {**location, "estimated_tokens": token_estimate, "line": line_for_name(path, name)}
                )

            if key_count > 20:
                inventory["issues"]["large_key_lists"].append(
                    {**location, "key_count": key_count, "line": line_for_name(path, name)}
                )

            repeated_blocks = []
            if ACTION_DECLARATION_MARKER in content and name.lower() not in {
                "section 0 - role and layer separation",
                "section 0 — role and layer separation",
            }:
                repeated_blocks.append("action declaration block")
            if content.count(LAYER_MARKER) > 0 and "layer separation" not in name.lower():
                repeated_blocks.append("role/layer block")
            if repeated_blocks:
                inventory["issues"]["repeated_rule_blocks"].append(
                    {**location, "blocks": repeated_blocks, "estimated_tokens": token_estimate, "line": line_for_name(path, name)}
                )

            file_info["constant_entries"] += 1 if entry.get("constant") else 0
            file_info["enabled_entries"] += 1 if entry.get("enabled") else 0
            file_info["keys"] += key_count
            file_info["single_word_keys"] += single_word_count
            file_info["regex_keys"] += regex_count
            file_info["estimated_content_tokens"] += token_estimate
            file_info["categories"].update([str(entry.get("category", ""))])
            file_info["top_long_entries"].append({"name": name, "estimated_tokens": token_estimate})
            file_info["top_key_count_entries"].append({"name": name, "keys": key_count})

        duplicate_names = [name for name, count in file_name_counter.items() if name and count > 1]
        for name in duplicate_names:
            inventory["issues"]["duplicate_names_within_file"].append({"file": path.name, "name": name})

        file_info["categories"] = dict(file_info["categories"].most_common())
        file_info["top_long_entries"] = sorted(
            file_info["top_long_entries"], key=lambda item: item["estimated_tokens"], reverse=True
        )[:10]
        file_info["top_key_count_entries"] = sorted(
            file_info["top_key_count_entries"], key=lambda item: item["keys"], reverse=True
        )[:10]

        for key in [
            "constant_entries",
            "enabled_entries",
            "keys",
            "single_word_keys",
            "regex_keys",
            "estimated_content_tokens",
        ]:
            inventory["totals"][key] += file_info[key]

        inventory["files"].append(file_info)

    inventory["totals"]["files"] = len(json_files)

    for entry_id, locations in id_locations.items():
        if len(locations) > 1:
            inventory["issues"]["duplicate_ids"].append({"id": entry_id, "locations": locations})

    for content, locations in content_locations.items():
        if len(locations) > 1:
            inventory["issues"]["duplicate_content"].append(
                {"estimated_tokens": estimate_tokens(content), "locations": locations[:20], "count": len(locations)}
            )

    for key, locations in key_locations.items():
        files = {item["file"] for item in locations}
        if len(locations) > 1 and (len(files) > 1 or key in BROAD_KEYS):
            inventory["issues"]["duplicate_keys_across_files"].append(
                {"key": key, "count": len(locations), "files": sorted(files), "locations": locations[:30]}
            )

    issue_counts = {name: len(values) for name, values in inventory["issues"].items()}
    inventory["issue_counts"] = issue_counts

    json_path = REPORTS / "inventory.json"
    json_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")

    md = []
    md.append("# Kyber RPG Lorebook Inventory")
    md.append("")
    md.append(f"Generated: {inventory['generated']}")
    md.append("")
    md.append("## Summary")
    md.append("")
    totals = inventory["totals"]
    md.append(f"- JSON lorebook files: {totals['files']}")
    md.append(f"- Entries: {totals['entries']}")
    md.append(f"- Enabled entries: {totals['enabled_entries']}")
    md.append(f"- Constant entries: {totals['constant_entries']}")
    md.append(f"- Activation keys: {totals['keys']}")
    md.append(f"- Single-word keys: {totals['single_word_keys']}")
    md.append(f"- Regex keys: {totals['regex_keys']}")
    md.append(f"- Estimated lore content tokens if fully loaded: {totals['estimated_content_tokens']}")
    md.append("")
    md.append("## Issue Counts")
    md.append("")
    for name, count in sorted(issue_counts.items()):
        md.append(f"- {name}: {count}")
    md.append("")
    md.append("## Files")
    md.append("")
    md.append("| File | KB | Entries | Constants | Keys | Single-word | Regex | Est. content tokens |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for file_info in inventory["files"]:
        md.append(
            f"| {file_info['file']} | {file_info['bytes'] / 1024:.1f} | {file_info['entries']} | "
            f"{file_info['constant_entries']} | {file_info['keys']} | {file_info['single_word_keys']} | "
            f"{file_info['regex_keys']} | {file_info['estimated_content_tokens']} |"
        )
    md.append("")
    md.append("## Highest-Risk Findings")
    md.append("")
    md.append("### Repeated Rule Blocks")
    md.append("")
    for item in inventory["issues"]["repeated_rule_blocks"][:40]:
        md.append(
            f"- {item['file']}:{item.get('line') or '?'} `{item['name']}` repeats {', '.join(item['blocks'])}; est. {item['estimated_tokens']} tokens"
        )
    if not inventory["issues"]["repeated_rule_blocks"]:
        md.append("- None found.")
    md.append("")
    md.append("### Large Key Lists")
    md.append("")
    for item in inventory["issues"]["large_key_lists"][:40]:
        md.append(f"- {item['file']}:{item.get('line') or '?'} `{item['name']}` has {item['key_count']} keys")
    if not inventory["issues"]["large_key_lists"]:
        md.append("- None found.")
    md.append("")
    md.append("### Broad Keys")
    md.append("")
    for item in inventory["issues"]["broad_keys"][:80]:
        md.append(f"- {item['file']} `{item['name']}` key `{item['key']}`")
    if not inventory["issues"]["broad_keys"]:
        md.append("- None found.")
    md.append("")
    md.append("### Long Entries")
    md.append("")
    for item in sorted(inventory["issues"]["long_entries"], key=lambda x: x["estimated_tokens"], reverse=True)[:40]:
        md.append(
            f"- {item['file']}:{item.get('line') or '?'} `{item['name']}` est. {item['estimated_tokens']} tokens"
        )
    if not inventory["issues"]["long_entries"]:
        md.append("- None found.")
    md.append("")
    md.append("### Low Probability Entries")
    md.append("")
    for item in inventory["issues"]["low_probability"][:40]:
        md.append(f"- {item['file']} `{item['name']}` probability {item['probability']}")
    if not inventory["issues"]["low_probability"]:
        md.append("- None found.")
    md.append("")
    md.append("## Recommended Next Action")
    md.append("")
    md.append("Start trigger simulation with `Kyber RPG 00 - Rules Engine.json`, because it is the only systems-engine lorebook and contains the core rule-enforcement behavior.")
    md.append("")
    md.append("Then simulate common player messages against the key set to measure how many entries activate under Janitor AI's default 3-message lorebook depth.")

    (REPORTS / "inventory.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {(REPORTS / 'inventory.md').relative_to(ROOT)}")
    print(f"Entries: {totals['entries']}")
    print(f"Issue counts: {issue_counts}")


if __name__ == "__main__":
    main()
