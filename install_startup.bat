@echo off
rem Starts the reminder at login (no admin needed), adds a "Reminder Settings" Desktop shortcut, and starts it now.
rem Use /remove to undo.
set "LINK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ReminderScript.lnk"
if /i "%~1"=="/remove" (
    del "%LINK%" 2>nul
    powershell -NoProfile -Command "Remove-Item (Join-Path ([Environment]::GetFolderPath('Desktop')) 'Reminder Settings.lnk') -ErrorAction SilentlyContinue"
    exit /b
)
powershell -NoProfile -Command "$w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut('%LINK%'); $s.TargetPath='%~dp0run.bat'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save(); $d=$w.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Reminder Settings.lnk')); $d.TargetPath='%~dp0manage.bat'; $d.WorkingDirectory='%~dp0'; $d.WindowStyle=7; $d.Save()" || exit /b 1
call "%~dp0run.bat"
