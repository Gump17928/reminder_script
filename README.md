# Reminder Script

Pop-up reminders (centered, always-on-top, with a chime) for things like entering your timecard.

- `reminders.json` – add as many reminders as you like. Fields: `name`, `time` (24h `HH:MM`, or a list of times), optional `message`, `days` (default Mon–Fri), `enabled`, `every` and `until`. Edits apply without restarting.
  - `every`: repeat every N minutes starting at the first `time`, until `until` (default `23:59`).
  - `every` can also be a list of gaps, e.g. `[30, 15, 5]` – the last gap repeats, so reminders get more frequent as the deadline nears.
- `run.bat` – start the reminder now (no console window).
- `install_startup.bat` – run at login via your Startup folder (no admin). `install_startup.bat /remove` undoes it.

Each occurrence fires once per day. If the PC starts late, only the most recent missed occurrence is shown (no pile-up). Dismiss closes it; Snooze re-shows it after 10 minutes. Requires Python 3 on Windows (uses `tkinter` and `winsound`, both built in).
