@echo off
rem Sets the reminder to start at login (no admin needed) and starts it now. Use /remove to undo.
set "LINK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ReminderScript.lnk"
if /i "%~1"=="/remove" (
    del "%LINK%" 2>nul
    exit /b
)
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%LINK%'); $s.TargetPath='%~dp0run.bat'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()" || exit /b 1
call "%~dp0run.bat"
