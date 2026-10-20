@echo off
rem Adds run.bat to the current user's Startup folder (no admin needed). Use /remove to undo.
set "LINK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ReminderScript.lnk"
if /i "%~1"=="/remove" (
    del "%LINK%" 2>nul
    echo Removed from startup.
    exit /b
)
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%LINK%'); $s.TargetPath='%~dp0run.bat'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()"
echo Installed. The reminder will start at next login.
