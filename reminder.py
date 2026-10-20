"""Pop-up reminders with a chime. Configure them in reminders.json."""
import json
import threading
import tkinter as tk
import winsound
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
CONFIG, STATE = HERE / "reminders.json", HERE / "state.json"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SNOOZE_MIN = 10
CHIME = [(523, 180), (659, 180), (784, 350)]


def chime():
    def play():
        for freq, ms in CHIME * 2:
            winsound.Beep(freq, ms)
    threading.Thread(target=play, daemon=True).start()


def popup(root, title, message, on_snooze):
    win = tk.Toplevel(root)
    win.title(title)
    win.attributes("-topmost", True)
    win.resizable(False, False)
    tk.Label(win, text=title, font=("Segoe UI", 14, "bold")).pack(padx=30, pady=(20, 5))
    tk.Label(win, text=message, font=("Segoe UI", 11), wraplength=300).pack(padx=30, pady=5)
    row = tk.Frame(win)
    row.pack(pady=15)
    tk.Button(row, text="Dismiss", width=10, command=win.destroy).pack(side="left", padx=5)
    tk.Button(row, text=f"Snooze {SNOOZE_MIN}m", width=10,
              command=lambda: (on_snooze(), win.destroy())).pack(side="left", padx=5)
    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_width()) // 2
    y = (win.winfo_screenheight() - win.winfo_height()) // 2
    win.geometry(f"+{x}+{y}")
    win.lift()
    win.focus_force()
    chime()


def load(path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default


def minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def occurrences(r):
    """Minutes-since-midnight at which a reminder fires: its time(s), plus repeats.

    "time": "HH:MM" or a list of them. "every": minutes between repeats, or a list of
    gaps (the last gap repeats). Repeats start at the first time and stop at "until"
    (default 23:59).
    """
    times = r["time"] if isinstance(r["time"], list) else [r["time"]]
    out = {minutes(t) for t in times}
    gaps = r.get("every") or []
    gaps = gaps if isinstance(gaps, list) else [gaps]
    end, t = minutes(r.get("until", "23:59")), minutes(times[0])
    for i in range(1440 if gaps else 0):
        t += gaps[min(i, len(gaps) - 1)]
        if t > end:
            break
        out.add(t)
    return sorted(out)


def main():
    root = tk.Tk()
    root.withdraw()
    fired = load(STATE, {})  # reminder name -> [date, last occurrence shown (minutes)]
    snoozed = {}  # reminder name -> datetime to show again

    def show(r):
        name = r["name"]
        popup(root, name, r.get("message", name),
              lambda: snoozed.update({name: datetime.now() + timedelta(minutes=SNOOZE_MIN)}))

    def tick():
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        for r in load(CONFIG, []):  # re-read each tick so edits apply without restart
            name = r["name"]
            if name in snoozed:
                if now >= snoozed[name]:
                    del snoozed[name]
                    show(r)
                continue
            if not r.get("enabled", True) or DAYS[now.weekday()] not in r.get("days", DAYS[:5]):
                continue
            # Show only the latest due occurrence not yet shown today (missed ones are skipped)
            due = [m for m in occurrences(r) if m <= now.hour * 60 + now.minute]
            last = fired[name][1] if fired.get(name, [""])[0] == today else -1
            if due and due[-1] > last:
                fired[name] = [today, due[-1]]
                STATE.write_text(json.dumps(fired))
                show(r)
        root.after(15000, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
