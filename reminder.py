"""Pop-up reminders with a chime. Configure them in reminders.json."""
import io
import json
import math
import struct
import threading
import tkinter as tk
import wave
import winsound
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
CONFIG, STATE = HERE / "reminders.json", HERE / "state.json"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SNOOZE_MIN = 10
VOLUME = 0.25  # 0.0-1.0; override per reminder with "volume"
NOTES = [(523.25, 0.0), (659.25, 0.35), (783.99, 0.7)]  # (Hz, start seconds): C-E-G
RATE, LENGTH, ATTACK = 22050, 3.0, 0.08  # sample rate, total seconds, fade-in seconds


def synth(volume):
    """Soft bell: sine notes with a smooth fade-in and a long exponential fade-out."""
    n = int(RATE * LENGTH)
    buf = [0.0] * n
    for freq, start in NOTES:
        for i in range(int(start * RATE), n):
            t = i / RATE - start
            env = math.sin(min(t / ATTACK, 1) * math.pi / 2) ** 2 * math.exp(-2.2 * t)
            buf[i] += env * (math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(4 * math.pi * freq * t))
    peak = max(map(abs, buf)) or 1
    fade = int(RATE * 0.2)  # guarantee silence at the very end
    pcm = b"".join(struct.pack("<h", int(32767 * volume * s / peak * min(1, (n - i) / fade)))
                   for i, s in enumerate(buf))
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm)
    return out.getvalue()


_cache = {}


def chime(r):
    """Play r["sound"] (a .wav path) if given, else the synthesized bell at r["volume"]."""
    sound = r.get("sound")
    if sound and (HERE / sound).is_file():
        data = (HERE / sound).read_bytes()
    else:
        vol = r.get("volume", VOLUME)
        data = _cache.setdefault(vol, synth(vol))
    threading.Thread(target=winsound.PlaySound, args=(data, winsound.SND_MEMORY), daemon=True).start()


def popup(root, r, on_snooze):
    title, message = r["name"], r.get("message", r["name"])
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
    chime(r)


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
        popup(root, r,
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
