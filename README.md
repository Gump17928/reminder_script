# Reminder Script

Pop-up reminders (centered, always-on-top, with a soft chime) for things like entering your timecard.

## Setup (Windows)

Copy this folder anywhere and double-click `install_startup.bat`. That's it – no admin rights needed, and it prints nothing unless something goes wrong (an error dialog appears). It starts the reminder at login, starts it now, and adds a **Reminder Settings** shortcut to your Desktop. If Python isn't installed, it is downloaded from python.org and installed silently for your user only (internet required, first run takes about a minute).

## Managing reminders

Double-click the **Reminder Settings** shortcut (or `manage.bat`; `manage.bat new` starts on a blank reminder). Add, edit and delete reminders, then **Save** – the running reminder picks changes up within 15 seconds. Use **Test popup + sound** to preview.

Each reminder has: name, enabled, message, one or more times, days (default Mon–Fri), optional repeat (`every` N minutes, or a list of gaps like `30,15,5` where the last gap repeats, until a cutoff time), website link, confirm button, sound, volume and snooze length.

Your reminders live in `reminders.json` (created from `reminders.example.json` on first run, not tracked by git). You can also edit it by hand; every reminder stores every field.

## Popup buttons

- **Website link** (if set) – opens the site, closes the popup and ends that reminder for the rest of the day.
- **Confirm button** (optional, per reminder) – e.g. "I filled out my time"; ends that reminder for the day.
- **Dismiss** – closes the popup; later occurrences still fire. **Snooze** – shows it again after the snooze time. **Stop for today** – no more of that reminder today.

No reminders are shown while the PC is locked. After unlocking, the most recent missed one appears (no pile-up). Each occurrence fires once per day.

## Sounds

Three built-in synthesized sounds (Soft Bell, Marimba, Rising Tone), all with a fade in/out. To use your own, drop `.wav`, `.mp3`, `.mp4`, `.m4a`, `.wma` or `.aac` files into `sounds/` (the **Sounds folder** button opens it); they appear in the Sound dropdown. Only the first ~12 seconds play, with a fade; if a file can't play, the Soft Bell is used.

## Scripts

- `install_startup.bat` – set up login startup + Desktop shortcut and start now. `install_startup.bat /remove` undoes it.
- `run.bat` – start the reminder now (no console window); installs Python first if needed. Only one copy runs at a time.
- `stop.bat` – stop the running reminder (until you start it again or next login).
- `manage.bat` – open the reminder manager.

## Layout

`reminder.py` (entry) and `rem/`: `app.py` scheduler, `config.py` load/save/defaults, `schedule.py` when reminders fire, `state.py` per-day state, `popup.py` window, `sound.py` audio, `lock.py` lock detection, `editor.py` manager GUI. Errors from the background process are logged to `error.log`.
