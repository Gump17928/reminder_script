# Reminder Script

Pop-up reminders (centered, always-on-top, with a chime) for things like entering your timecard.

- `reminders.json` – add as many reminders as you like. Fields: `name`, `time` (24h `HH:MM`), optional `message`, `days` (default Mon–Fri), `enabled`. Edits apply without restarting.
- `run.bat` – start the reminder now (no console window).
- `install_startup.bat` – run at login via your Startup folder (no admin). `install_startup.bat /remove` undoes it.

A reminder fires once per day at/after its time (so it still shows if the PC starts late). Dismiss closes it; Snooze re-shows it after 10 minutes. Requires Python 3 on Windows (uses `tkinter` and `winsound`, both built in).
