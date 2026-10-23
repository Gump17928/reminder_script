"""Load/save reminders.json. Every reminder stores every field, even when it's a default."""
import json
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG, EXAMPLE = ROOT / "reminders.json", ROOT / "reminders.example.json"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SETTINGS = {"snooze_minutes": 10, "volume": 0.25, "sound": "Soft Bell"}  # defaults for new reminders
REMINDER = {
    "id": "", "name": "New reminder", "enabled": True, "message": "",
    "time": ["09:00"],             # one or more HH:MM
    "days": DAYS[:5],
    "every": [],                   # repeat gap(s) in minutes; the last gap repeats
    "until": "23:59",              # last time a repeat may fire
    "link": "", "link_label": "Open timecard site",   # clicking it opens the site and ends the reminder for the day
    "confirm": False, "confirm_label": "I filled out my time",
}


def normalize(r, settings=SETTINGS):
    out = {**REMINDER, **{k: settings[k] for k in SETTINGS}, **r}
    out["time"] = [out["time"]] if isinstance(out["time"], str) else list(out["time"])
    every = out["every"]
    out["every"] = [every] if isinstance(every, int) and every else list(every or [])
    out["days"] = list(out["days"])
    out["id"] = out["id"] or uuid.uuid4().hex[:8]
    return out


def load():
    if not CONFIG.exists() and EXAMPLE.exists():
        shutil.copy(EXAMPLE, CONFIG)
    raw = json.loads(CONFIG.read_text("utf-8-sig")) if CONFIG.exists() else {}
    if isinstance(raw, list):  # old format: a bare list of reminders
        raw = {"reminders": raw}
    settings = {**SETTINGS, **raw.get("settings", {})}
    cfg = {"settings": settings, "reminders": [normalize(r, settings) for r in raw.get("reminders", [])]}
    if cfg != raw:  # first run after migration / new defaults: write the complete form back
        save(cfg)
    return cfg


def save(cfg):
    tmp = CONFIG.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, indent=2), "utf-8")
    tmp.replace(CONFIG)
