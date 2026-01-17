@echo off
echo ==========================================
echo      JARVIS Executable Builder
echo ==========================================
echo.
echo This script works best when run from your Anaconda Prompt 
echo or the environment where your dependencies are installed.
echo.

:: Check if python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please run this from your Conda/Python environment.
    pause
    exit /b
)

:: Install PyInstaller if not present
echo [+] Checking/Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b
)

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist JARVIS.spec del JARVIS.spec

:: Build the executable
echo.
echo [+] Building JARVIS executable...
:: --onefile: Bundle everything into a single .exe
:: --clean: Clean PyInstaller cache
:: --name: Name of the output file
:: Hidden imports help ensure pyttsx3 drivers are found
pyinstaller --onefile --clean --name "JARVIS" ^
    --add-data "jarvis.mp3;." ^
    --add-binary "flac.exe;." ^
    --add-binary "libFLAC.dll;." ^
    --add-binary "libFLAC++.dll;." ^
    --hidden-import=pyttsx3.drivers ^
    --hidden-import=pyttsx3.drivers.sapi5 ^
    jarvis.py

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Build complete!
    echo The executable is located in the 'dist' folder:
    echo %CD%\dist\JARVIS.exe
) else (
    echo.
    echo [FAIL] Build failed. Check the error messages above.
)

pause
