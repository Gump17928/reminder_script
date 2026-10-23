"""The reminder pop-up window."""
import tkinter as tk
import webbrowser

from . import sound


def show(root, r, on_snooze, on_off):
    """Show a reminder. on_snooze()/on_off() record the choice; on_off ends it for the day."""
    win = tk.Toplevel(root)
    win.title(r["name"])
    win.attributes("-topmost", True)
    win.resizable(False, False)

    def do(*fns):
        def run():
            for f in fns:
                f()
            win.destroy()
        return run

    tk.Label(win, text=r["name"], font=("Segoe UI", 14, "bold")).pack(padx=30, pady=(20, 5))
    if r["message"]:
        tk.Label(win, text=r["message"], font=("Segoe UI", 11), wraplength=320).pack(padx=30, pady=5)
    link = r["link"].strip()
    if link.lower().startswith(("http://", "https://")):
        lbl = tk.Label(win, text=r["link_label"] or link, fg="#0563c1", cursor="hand2",
                       font=("Segoe UI", 11, "underline"))
        lbl.pack(pady=5)
        lbl.bind("<Button-1>", lambda e: do(lambda: webbrowser.open(link), on_off)())
    if r["confirm"]:
        tk.Button(win, text=r["confirm_label"], command=do(on_off)).pack(pady=(10, 0), ipadx=8)
    row = tk.Frame(win)
    row.pack(pady=15)
    for text, fns in (("Dismiss", ()), (f"Snooze {r['snooze_minutes']}m", (on_snooze,)),
                      ("Stop for today", (on_off,))):
        tk.Button(row, text=text, width=13, command=do(*fns)).pack(side="left", padx=4)

    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_width()) // 2
    y = (win.winfo_screenheight() - win.winfo_height()) // 2
    win.geometry(f"+{x}+{y}")
    win.lift()
    win.focus_force()
    sound.play(r["sound"], r["volume"])
    return win
