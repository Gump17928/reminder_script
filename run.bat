@echo off
rem Starts the reminder with no console window. Installs Python for the current user (no admin) if needed.
setlocal
cd /d "%~dp0"
if not defined PY_DIR set "PY_DIR=%LocalAppData%\Programs\Python\Python312"
if not defined PY_URL set "PY_URL=https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"

call :find
if not defined PYW call :install
if not defined PYW (
    powershell -NoProfile -Command "Add-Type -AssemblyName PresentationFramework; [void][Windows.MessageBox]::Show('Reminder script: could not find or install Python. Check your internet connection, or install Python 3 from python.org.','Reminder script','OK','Error')"
    exit /b 1
)
start "" "%PYW%" reminder.py
exit /b 0

:find
set "PYW="
for %%P in (python.exe "%PY_DIR%\python.exe") do if not defined PYW (
    %%P -c "import tkinter,winsound" >nul 2>&1 && call :pyw "%%~$PATH:P" "%%~fP"
)
exit /b

:pyw
if "%~1"=="" (set "PYW=%~dp2pythonw.exe") else set "PYW=%~dp1pythonw.exe"
exit /b

:install
set "EXE=%TEMP%\python-installer.exe"
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest '%PY_URL%' -OutFile '%EXE%'" >nul 2>&1 || exit /b
"%EXE%" /quiet InstallAllUsers=0 PrependPath=0 Include_tcltk=1 Include_launcher=0 Include_test=0 Include_doc=0 Shortcuts=0 TargetDir="%PY_DIR%" >nul 2>&1
del "%EXE%" 2>nul
call :find
exit /b
