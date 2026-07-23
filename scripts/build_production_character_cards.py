from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "production" / "due-2026-08-21"
MANIFEST = BATCH / "janitor-manager-manifest.json"

THEMES = {
    "Aethraxis": {
        "label": "AETHRAXIS // CIVIC ARCHIVE",
        "accent": "#9ee7ff",
        "accent2": "#c7a6ff",
        "bg": "#07111f",
        "panel": "#0d1b2e",
        "border": "rgba(158,231,255,.28)",
        "route_labels": ("PUBLIC RECORD", "CLOSED DOOR", "FAULT LINE"),
        "intro": "A living-world science-fantasy encounter shaped by law, status, biology, and consequence.",
    },
    "Apex Eidolon": {
        "label": "APEX EIDOLON // INCIDENT FILE",
        "accent": "#ff765f",
        "accent2": "#ffc66d",
        "bg": "#120b0b",
        "panel": "#211313",
        "border": "rgba(255,118,95,.30)",
        "route_labels": ("FIRST TRACE", "PROXIMITY EVENT", "DIRECT CONTACT"),
        "intro": "Survival horror with a persistent environment, incomplete evidence, and no guaranteed outcome.",
    },
    "Historical": {
        "label": "FALLEN HISTORY // LIVING CHRONICLE",
        "accent": "#e6c77b",
        "accent2": "#d78272",
        "bg": "#17130d",
        "panel": "#241e15",
        "border": "rgba(230,199,123,.28)",
        "route_labels": ("BEFORE THE COURT", "BEHIND THE VEIL", "HISTORY IN MOTION"),
        "intro": "A period-grounded encounter where rank, custom, material reality, and political consequence remain active.",
    },
    "ATEEZ": {
        "label": "BACKSTAGE FILE // FICTIONALIZED ATEEZ",
        "accent": "#ff9fcf",
        "accent2": "#8fc9ff",
        "bg": "#0c0d1b",
        "panel": "#15172b",
        "border": "rgba(255,159,207,.27)",
        "route_labels": ("PUBLIC SCHEDULE", "RECURRING ACCESS", "SHOW NIGHT"),
        "intro": "A grounded entertainment-industry scenario built around schedules, boundaries, reputation, and earned familiarity.",
    },
}


def clean(value: str) -> str:
    value = value.strip().rstrip(".")
    if any(marker in value for marker in ("â", "Ã", "Â", "ð")):
        try:
            value = value.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return value


def fields_from_definition(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s{2}([a-z_]+):\s*(.+?)\s*$", raw)
        if match:
            values[match.group(1)] = clean(match.group(2))
        warning = re.match(r"^\s*-\s*warnings:\s*(.+?)\s*$", raw)
        if warning:
            values["warnings"] = clean(warning.group(1))
        legacy = re.match(r"^([a-z_]+)=(.+?)\s*$", raw)
        if legacy:
            values.setdefault(legacy.group(1), clean(legacy.group(2)))
    if "name" not in values and "full_name" in values:
        values.update(
            {
                "name": values["full_name"],
                "series": values.get("group", "ATEEZ"),
                "role": values.get("role", "adult fictionalized performer"),
                "setting": values.get("era_scope", "modern K-pop industry"),
                "nature": "human adult performer",
                "premise": values.get("public_identity", "Performance discipline behind a carefully bounded public life"),
                "access_model": "Public warmth remains public; private trust requires a credible, recurring non-fan pathway",
                "public_route": "a time-bounded signing-table encounter",
                "pressure_route": "an official movement review in the rehearsal room",
                "danger_route": "a concert route at the barricade",
                "warnings": "parasocial access, privacy pressure, public scrutiny, demanding schedules",
            }
        )
    return values


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def tags_html(path: Path, accent: str) -> str:
    tags = [clean(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return "".join(
        f'<span style="display:inline-block;margin:4px 3px;padding:5px 9px;border:1px solid {accent}55;'
        f'border-radius:999px;color:{accent};font-size:12px;letter-spacing:.04em;">{esc(tag)}</span>'
        for tag in tags
    )


def render(data: dict[str, str], group: str, tags_path: Path) -> str:
    t = THEMES[group]
    name = esc(data["name"])
    role = esc(data["role"])
    premise = esc(data["premise"])
    setting = esc(data["setting"])
    nature = esc(data["nature"])
    access = esc(data["access_model"])
    warnings = esc(data["warnings"])
    routes = (
        esc(data["public_route"]),
        esc(data["pressure_route"]),
        esc(data["danger_route"]),
    )
    fiction_notice = ""
    if group == "ATEEZ":
        fiction_notice = (
            f'<div style="margin:18px 0;padding:13px 15px;border-left:3px solid {t["accent2"]};'
            f'background:rgba(143,201,255,.07);color:#d8eaff;font-size:13px;line-height:1.6;">'
            "<strong>FICTION NOTICE</strong><br>This is an unofficial fictional roleplay interpretation "
            "inspired by an adult public performer. Private dialogue, relationships, thoughts, and off-camera "
            "events are invented. It is not affiliated with or endorsed by the performer, group, or agency.</div>"
        )

    route_cards = "".join(
        f'<div style="flex:1 1 180px;padding:15px;background:{t["panel"]};border:1px solid {t["border"]};'
        f'border-radius:12px;"><div style="color:{t["accent"]};font-size:11px;font-weight:700;'
        f'letter-spacing:.13em;">{label}</div><div style="margin-top:7px;color:#f4f6fb;line-height:1.55;">'
        f"{route}</div></div>"
        for label, route in zip(t["route_labels"], routes)
    )

    card = f"""<div style="max-width:820px;margin:0 auto;background:{t["bg"]};color:#d9deea;border:1px solid {t["border"]};border-radius:20px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.38);font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <div style="padding:34px 26px 30px;text-align:center;background:radial-gradient(circle at 50% 0%,{t["accent"]}22,transparent 54%),linear-gradient(145deg,{t["panel"]},{t["bg"]});border-bottom:1px solid {t["border"]};">
    <div style="color:{t["accent"]};font-size:11px;font-weight:800;letter-spacing:.18em;">{t["label"]} // {esc(data["production_number"])}</div>
    <h1 style="margin:13px 0 7px;color:#fff;font-size:clamp(30px,7vw,52px);line-height:1.05;letter-spacing:-.03em;">{name}</h1>
    <div style="color:{t["accent2"]};font-size:15px;line-height:1.5;">{role}</div>
    <div style="width:92px;height:2px;margin:22px auto 18px;background:linear-gradient(90deg,transparent,{t["accent"]},transparent);"></div>
    <p style="max-width:650px;margin:0 auto;color:#f5f6fa;font-family:Georgia,serif;font-size:20px;line-height:1.55;"><em>“{premise}.”</em></p>
  </div>
  <div style="padding:24px 24px 8px;">
    {fiction_notice}
    <p style="margin:0 0 22px;text-align:center;color:#b9c1d2;line-height:1.7;">{t["intro"]}</p>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin:0 0 26px;">
      <div style="flex:1 1 210px;padding:14px;background:{t["panel"]};border-radius:12px;border:1px solid {t["border"]};"><strong style="color:{t["accent"]};font-size:11px;letter-spacing:.12em;">SETTING</strong><br><span style="display:inline-block;margin-top:6px;line-height:1.5;">{setting}</span></div>
      <div style="flex:1 1 210px;padding:14px;background:{t["panel"]};border-radius:12px;border:1px solid {t["border"]};"><strong style="color:{t["accent"]};font-size:11px;letter-spacing:.12em;">IDENTITY</strong><br><span style="display:inline-block;margin-top:6px;line-height:1.5;">{nature}</span></div>
    </div>
    <h2 style="margin:0 0 8px;color:#fff;font-size:22px;">Choose your point of entry</h2>
    <p style="margin:0 0 15px;color:#aeb7c9;line-height:1.6;">Three openings, one continuous character. Routes change the pressure—not the personality.</p>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:27px;">{route_cards}</div>
    <div style="padding:20px;background:linear-gradient(135deg,{t["accent"]}12,{t["accent2"]}0d);border:1px solid {t["border"]};border-radius:14px;">
      <h2 style="margin:0 0 9px;color:#fff;font-size:19px;">What the relationship actually requires</h2>
      <p style="margin:0;color:#d5daE5;line-height:1.7;">{access}. Trust is earned through repeated evidence. Attraction, forced proximity, status, rescue, or one vulnerable moment never guarantees intimacy.</p>
    </div>
    <div style="margin:25px 0 0;">
      <h2 style="margin:0 0 9px;color:#fff;font-size:19px;">Your role</h2>
      <p style="margin:0;color:#bdc5d4;line-height:1.7;"><strong style="color:{t["accent"]};">AnyPOV.</strong> Bring any adult persona that can plausibly enter the setting. Your identity, dialogue, thoughts, consent, and completed actions remain yours. The world responds to what you actually do—and remembers it.</p>
    </div>
    <div style="margin:24px 0;padding:16px 18px;background:rgba(0,0,0,.24);border-left:3px solid {t["accent2"]};border-radius:4px 12px 12px 4px;">
      <strong style="color:{t["accent2"]};font-size:12px;letter-spacing:.1em;">CONTENT ADVISORY</strong>
      <p style="margin:7px 0 0;color:#d6d9e2;line-height:1.65;">{warnings}.</p>
    </div>
    <div style="text-align:center;margin:4px 0 21px;">{tags_html(tags_path, t["accent"])}</div>
  </div>
  <div style="padding:16px 22px;text-align:center;background:rgba(0,0,0,.22);border-top:1px solid {t["border"]};color:#8993a7;font-size:12px;line-height:1.6;letter-spacing:.04em;">PERSISTENT WORLD • LIMITED KNOWLEDGE • CONSEQUENCES • NO USER PUPPETING</div>
</div>
"""
    return "\n".join(line.rstrip() for line in card.splitlines()) + "\n"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for character in manifest["characters"]:
        group = character["group"]
        if group == "Kpops":
            group = "ATEEZ"
        folder = BATCH / "characters" / character["id"]
        data = fields_from_definition(folder / "personality-definition.txt")
        if "name" not in data:
            raise ValueError(f"Could not parse personality fields for {character['id']}")
        data["production_number"] = str(character["productionNumber"])
        card = render(data, group, folder / "tags.txt")
        card_path = folder / "character-card.txt"
        card_path.write_text(card, encoding="utf-8", newline="\n")
        character["fieldHashes"]["characterCard"] = hashlib.sha256(card.encode("utf-8")).hexdigest()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"Built {len(manifest['characters'])} character cards.")


if __name__ == "__main__":
    main()
