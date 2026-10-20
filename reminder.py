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


def main():
    root = tk.Tk()
    root.withdraw()
    fired = load(STATE, {})  # reminder name -> date last shown
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
            if r.get("enabled", True) and DAYS[now.weekday()] in r.get("days", DAYS[:5]) \
                    and fired.get(name) != today and now.strftime("%H:%M") >= r["time"]:
                fired[name] = today
                STATE.write_text(json.dumps(fired))
                show(r)
        root.after(15000, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
