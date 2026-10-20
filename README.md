# Reminder Script

Pop-up reminders (centered, always-on-top, with a chime) for things like entering your timecard.

- `reminders.json` – add as many reminders as you like. Fields: `name`, `time` (24h `HH:MM`, or a list of times), optional `message`, `days` (default Mon–Fri), `enabled`, `every`, `until`, `volume` and `sound`. Edits apply without restarting.
  - `volume`: 0.0–1.0 for the built-in chime (default `0.25`, set via `VOLUME` in `reminder.py`).
  - `sound`: path to your own `.wav` file (relative to this folder) to use instead of the built-in chime.
  - `every`: repeat every N minutes starting at the first `time`, until `until` (default `23:59`).
  - `every` can also be a list of gaps, e.g. `[30, 15, 5]` – the last gap repeats, so reminders get more frequent as the deadline nears.
- `run.bat` – start the reminder now (no console window).
- `stop.bat` – stop the running reminder (until you start it again or next login).
- `install_startup.bat` – run at login via your Startup folder (no admin). `install_startup.bat /remove` undoes it.

Each occurrence fires once per day. If the PC starts late, only the most recent missed occurrence is shown (no pile-up). Dismiss closes it; Snooze re-shows it after 10 minutes. Requires Python 3 on Windows (uses `tkinter` and `winsound`, both built in).
