@echo off
rem Runs the reminder with no console window.
cd /d "%~dp0"
start "" pythonw reminder.py
