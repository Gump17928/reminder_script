"""Per-day runtime state (what already fired, was snoozed or finished), kept in state.json."""
import json
from datetime import date

from .config import ROOT

FILE = ROOT / "state.json"


def load():
    today = date.today().isoformat()
    try:
        s = json.loads(FILE.read_text())
    except (OSError, ValueError):
        s = None
    return s if isinstance(s, dict) and s.get("date") == today else {"date": today, "r": {}}


def current(s):
    """Return s, or a fresh state if the date rolled over."""
    return s if s["date"] == date.today().isoformat() else load()


def entry(s, rid):
    # last: latest occurrence shown (minutes); off: finished/stopped for today; snooze: ISO time
    return s["r"].setdefault(rid, {"last": -1, "off": False, "snooze": None})


def save(s):
    FILE.write_text(json.dumps(s))
