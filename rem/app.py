"""Scheduler: checks the reminders every few seconds and shows what's due."""
import socket
import tkinter as tk
import traceback
from datetime import datetime, timedelta

from . import config, lock, popup, state
from .schedule import occurrences

TICK_MS = 15000


class App:
    def __init__(self, root):
        self.root, self.st, self.wins = root, state.load(), {}

    def fire(self, r, e):
        old = self.wins.pop(r["id"], None)  # replace a still-open popup instead of stacking
        if old and old.winfo_exists():
            old.destroy()

        def snooze():
            e["snooze"] = (datetime.now() + timedelta(minutes=r["snooze_minutes"])).isoformat(timespec="seconds")
            state.save(self.st)

        def off():
            e.update(off=True, snooze=None)
            state.save(self.st)

        self.wins[r["id"]] = popup.show(self.root, r, snooze, off)

    def check(self):
        now = datetime.now()
        self.st = state.current(self.st)
        for r in config.load()["reminders"]:  # re-read each tick so edits apply without restart
            if not r["enabled"] or config.DAYS[now.weekday()] not in r["days"]:
                continue
            e = state.entry(self.st, r["id"])
            if e["off"]:
                continue
            # Only the latest due occurrence is shown, so anything missed (PC off/locked) doesn't pile up
            due = [m for m in occurrences(r) if m <= now.hour * 60 + now.minute]
            if e["snooze"]:
                if now < datetime.fromisoformat(e["snooze"]):
                    continue
                e["snooze"] = None
            elif not due or due[-1] <= e["last"]:
                continue
            e["last"] = max(e["last"], due[-1] if due else -1)
            state.save(self.st)
            self.fire(r, e)

    def tick(self):
        try:
            if not lock.locked():  # nothing while locked; the latest missed one shows after unlock
                self.check()
        except Exception:
            with open(config.ROOT / "error.log", "a") as f:
                f.write(f"{datetime.now()}\n{traceback.format_exc()}\n")
        self.root.after(TICK_MS, self.tick)


def main():
    guard = socket.socket()  # single instance: a second copy exits if the port is taken
    try:
        guard.bind(("127.0.0.1", 47653))
    except OSError:
        return
    root = tk.Tk()
    root.withdraw()
    App(root).tick()
    root.mainloop()
