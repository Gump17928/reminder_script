# Reminder Script

Pop-up reminders (centered, always-on-top, with a chime) for things like entering your timecard.

## Setup (Windows)

Copy this folder anywhere and double-click `install_startup.bat`. That's it – no admin rights needed, and it prints nothing unless something goes wrong (an error dialog appears). If Python isn't installed, it is downloaded from python.org and installed silently for your user only (internet required, first run takes about a minute).

- `reminders.json` – add as many reminders as you like. Fields: `name`, `time` (24h `HH:MM`, or a list of times), optional `message`, `days` (default Mon–Fri), `enabled`, `every`, `until`, `volume` and `sound`. Edits apply without restarting.
  - `volume`: 0.0–1.0 for the built-in chime (default `0.25`, set via `VOLUME` in `reminder.py`).
  - `sound`: path to your own `.wav` file (relative to this folder) to use instead of the built-in chime.
  - `every`: repeat every N minutes starting at the first `time`, until `until` (default `23:59`).
  - `every` can also be a list of gaps, e.g. `[30, 15, 5]` – the last gap repeats, so reminders get more frequent as the deadline nears.
- `install_startup.bat` – run at login via your Startup folder and start it now. `install_startup.bat /remove` undoes it.
- `run.bat` – start the reminder now (no console window); installs Python first if needed. Only one copy runs at a time.
- `stop.bat` – stop the running reminder (until you start it again or next login).

Each occurrence fires once per day. If the PC starts late, only the most recent missed occurrence is shown (no pile-up). Dismiss closes it; Snooze re-shows it after 10 minutes. Uses an existing Python 3 with `tkinter` if found, otherwise the per-user Python 3.12 install in `%LocalAppData%\Programs\Python\Python312`.
