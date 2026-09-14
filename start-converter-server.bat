@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo.
echo ==================================================
echo  All in One Place - Professional File Converter
echo ==================================================
echo.

where py >nul 2>&1
if %errorlevel%==0 (
  set "PYTHON=py"
) else (
  where python >nul 2>&1
  if !errorlevel!==0 (set "PYTHON=python") else (
    echo ERROR: Python was not found.
    echo Install Python 3.10+ and run this file again.
    pause
    exit /b 1
  )
)

%PYTHON% --version
if errorlevel 1 (echo ERROR: Python could not be started.&pause&exit /b 1)

echo.
echo Checking Office rendering engines...
%PYTHON% converter-server.py --check
if errorlevel 1 (
  echo.
  echo ERROR: No supported Office rendering engine was found.
  echo Install Microsoft Office or LibreOffice, then run this launcher again.
  pause
  exit /b 1
)

echo.
echo Starting converter server...
start "All in One Place Converter Server" /min cmd /c "%PYTHON% converter-server.py"

set "READY=0"
for /l %%I in (1,1,40) do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$ok=$false; try { $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 1 http://127.0.0.1:8765/api/health; $j=$r.Content | ConvertFrom-Json; $ok=($j.ok -eq $true) } catch {}; if($ok){exit 0}else{exit 1}"
  if !errorlevel!==0 (set "READY=1"&goto :ready)
  timeout /t 1 /nobreak >nul
)

:ready
if "%READY%"=="1" (
  echo.
  echo SUCCESS: Office conversion engine is ONLINE.
  start "" "http://127.0.0.1:8765/file-converter.html"
  echo.
  echo The converter is ready. Keep this window/server running while converting.
  exit /b 0
)

echo.
echo ERROR: Converter server did not become ready.
echo Run converter-server.py manually to see the exact error.
pause
exit /b 1
