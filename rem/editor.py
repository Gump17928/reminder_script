"""Reminder manager GUI. Open with manage.bat ("manage.bat new" starts on a blank reminder)."""
import os
import re
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from . import config, popup, sound

HHMM = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class Editor(tk.Tk):
    def __init__(self, new=False):
        super().__init__()
        self.title("Reminder settings")
        self.resizable(False, False)
        self.cfg, self.idx = config.load(), None
        self.v = {k: tk.StringVar() for k in
                  ("name", "message", "every", "until", "link", "link_label", "confirm_label", "snooze", "sound")}
        self.enabled, self.confirm, self.volume = tk.BooleanVar(), tk.BooleanVar(), tk.DoubleVar()
        self.days = {d: tk.BooleanVar() for d in config.DAYS}
        self.hh, self.mm = tk.StringVar(value="09"), tk.StringVar(value="00")

        left = ttk.Frame(self, padding=8)
        left.grid(row=0, column=0, sticky="ns")
        self.lb = tk.Listbox(left, width=26, height=18, exportselection=False)
        self.lb.pack()
        self.lb.bind("<<ListboxSelect>>", lambda e: self.pick())
        for text, cmd in (("New reminder", self.new), ("Delete", self.delete)):
            ttk.Button(left, text=text, command=cmd).pack(fill="x", pady=(6, 0))

        f = ttk.Frame(self, padding=8)
        f.grid(row=0, column=1, sticky="n")
        self.f, self.r = f, 0
        self.field("Name", ttk.Entry(f, textvariable=self.v["name"], width=36))
        self.field("", ttk.Checkbutton(f, text="Enabled", variable=self.enabled))
        self.field("Message", ttk.Entry(f, textvariable=self.v["message"], width=36))

        t = ttk.Frame(f)
        self.tl = tk.Listbox(t, height=3, width=8, exportselection=False)
        self.tl.grid(row=0, column=0, rowspan=2)
        box = ttk.Frame(t)
        box.grid(row=0, column=1, padx=6)
        ttk.Spinbox(box, from_=0, to=23, width=3, format="%02.0f", textvariable=self.hh).pack(side="left")
        ttk.Label(box, text=":").pack(side="left")
        ttk.Spinbox(box, from_=0, to=59, width=3, format="%02.0f", textvariable=self.mm).pack(side="left")
        ttk.Button(t, text="Add time", command=self.add_time).grid(row=1, column=1, padx=6)
        ttk.Button(t, text="Remove", command=lambda: [self.tl.delete(i) for i in self.tl.curselection()]
                   ).grid(row=1, column=2)
        self.field("Times", t)

        d = ttk.Frame(f)
        for day, var in self.days.items():
            ttk.Checkbutton(d, text=day, variable=var).pack(side="left")
        self.field("Days", d)

        rep = ttk.Frame(f)
        ttk.Entry(rep, textvariable=self.v["every"], width=12).pack(side="left")
        ttk.Label(rep, text=" min (e.g. 30 or 30,15,5) until ").pack(side="left")
        ttk.Entry(rep, textvariable=self.v["until"], width=6).pack(side="left")
        self.field("Repeat every", rep)

        self.field("Website link", ttk.Entry(f, textvariable=self.v["link"], width=36))
        self.field("Link text", ttk.Entry(f, textvariable=self.v["link_label"], width=36))
        c = ttk.Frame(f)
        ttk.Checkbutton(c, text="Show", variable=self.confirm).pack(side="left")
        ttk.Entry(c, textvariable=self.v["confirm_label"], width=28).pack(side="left", padx=6)
        self.field("Confirm button", c)

        s = ttk.Frame(f)
        self.cb = ttk.Combobox(s, textvariable=self.v["sound"], width=22, state="readonly",
                               postcommand=lambda: self.cb.config(values=sound.names()))
        self.cb.pack(side="left")
        ttk.Button(s, text="Sounds folder", command=lambda: os.startfile(sound.DIR)).pack(side="left", padx=6)
        self.field("Sound", s)
        self.field("Volume", ttk.Scale(f, from_=0, to=100, variable=self.volume, length=220))
        self.field("Snooze (min)", ttk.Spinbox(f, from_=1, to=240, width=5, textvariable=self.v["snooze"]))

        b = ttk.Frame(f)
        b.grid(row=self.r, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(b, text="Test popup + sound", command=self.test).pack(side="left", padx=4)
        ttk.Button(b, text="Save", command=self.save).pack(side="left", padx=4)

        self.refresh()
        if new or not self.cfg["reminders"]:
            self.new()
        else:
            self.select(0)

    def field(self, label, widget):
        ttk.Label(self.f, text=label).grid(row=self.r, column=0, sticky="e", padx=(0, 8), pady=3)
        widget.grid(row=self.r, column=1, sticky="w", pady=3)
        self.r += 1

    def add_time(self):
        t = f"{int(self.hh.get()):02d}:{int(self.mm.get()):02d}"
        times = sorted(set(self.tl.get(0, "end")) | {t})
        self.tl.delete(0, "end")
        self.tl.insert("end", *times)

    def refresh(self):
        self.lb.delete(0, "end")
        for r in self.cfg["reminders"]:
            self.lb.insert("end", ("" if r["enabled"] else "(off) ") + r["name"])
        if self.idx is not None:
            self.lb.selection_set(self.idx)

    def select(self, i):
        self.idx = i
        r = self.cfg["reminders"][i]
        self.refresh()
        for k in ("name", "message", "until", "link", "link_label", "confirm_label", "sound"):
            self.v[k].set(r[k])
        self.v["every"].set(",".join(map(str, r["every"])))
        self.v["snooze"].set(r["snooze_minutes"])
        self.enabled.set(r["enabled"])
        self.confirm.set(r["confirm"])
        self.volume.set(r["volume"] * 100)
        for d, var in self.days.items():
            var.set(d in r["days"])
        self.tl.delete(0, "end")
        self.tl.insert("end", *r["time"])

    def collect(self):
        v, r = self.v, self.cfg["reminders"][self.idx]
        times = list(self.tl.get(0, "end"))
        if not times:
            raise ValueError("Add at least one time.")
        until = v["until"].get().strip() or "23:59"
        if not HHMM.match(until):
            raise ValueError("'Until' must look like 17:00.")
        try:
            every = [int(x) for x in re.split(r"[,\s]+", v["every"].get().strip()) if x]
            snooze = int(v["snooze"].get())
        except ValueError:
            raise ValueError("Repeat gaps and snooze must be whole minutes, e.g. 30 or 30,15,5.")
        if any(e <= 0 for e in every) or snooze <= 0:
            raise ValueError("Minutes must be greater than zero.")
        link = v["link"].get().strip()
        if link and not re.match(r"https?://", link, re.I):
            link = "https://" + link
        return {**r, "name": v["name"].get().strip() or "Reminder", "enabled": self.enabled.get(),
                "message": v["message"].get(), "time": times,
                "days": [d for d, var in self.days.items() if var.get()],
                "every": every, "until": until, "link": link, "link_label": v["link_label"].get(),
                "confirm": self.confirm.get(), "confirm_label": v["confirm_label"].get(),
                "sound": v["sound"].get() or sound.DEFAULT, "volume": round(self.volume.get() / 100, 2),
                "snooze_minutes": snooze}

    def commit(self):
        try:
            self.cfg["reminders"][self.idx] = self.collect()
        except ValueError as e:
            messagebox.showerror("Check this reminder", str(e))
            return False
        self.refresh()
        return True

    def pick(self):
        sel = self.lb.curselection()
        if not sel or sel[0] == self.idx:
            return
        if self.commit():
            self.select(sel[0])
        else:
            self.refresh()

    def new(self):
        if self.idx is not None and not self.commit():
            return
        self.cfg["reminders"].append(config.normalize({}, self.cfg["settings"]))
        self.select(len(self.cfg["reminders"]) - 1)

    def delete(self):
        if self.idx is None or not messagebox.askyesno("Delete", "Delete this reminder?"):
            return
        del self.cfg["reminders"][self.idx]
        self.idx = None
        config.save(self.cfg)
        self.refresh()
        self.select(0) if self.cfg["reminders"] else self.new()

    def save(self):
        if self.commit():
            config.save(self.cfg)
            messagebox.showinfo("Saved", "Saved. The running reminder picks changes up within 15 seconds.")

    def test(self):
        try:
            popup.show(self, self.collect(), lambda: None, lambda: None)
        except ValueError as e:
            messagebox.showerror("Check this reminder", str(e))


if __name__ == "__main__":
    Editor(new="new" in sys.argv[1:]).mainloop()
