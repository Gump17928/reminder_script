@echo off
rem Stops the running reminder (this session only; use install_startup.bat /remove to stop it starting at login).
powershell -NoProfile -Command "$p=Get-CimInstance Win32_Process -Filter \"Name like 'python%%'\" | Where-Object { $_.CommandLine -like '*reminder.py*' }; $p | ForEach-Object { Stop-Process -Id $_.ProcessId }; if ($p) { 'Stopped.' } else { 'Not running.' }"
