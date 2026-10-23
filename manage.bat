@echo off
rem Opens the reminder manager (add/edit/delete reminders). "manage.bat new" starts a new reminder.
call "%~dp0run.bat" -m rem.editor %*
