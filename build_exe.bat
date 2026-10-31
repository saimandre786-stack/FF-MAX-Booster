@echo off
setlocal
py -m pip install --upgrade pip
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --clean --onefile --windowed --name FF_MAX_Booster ff_max_booster.py
echo.
echo Build complete. Your EXE is in the dist folder.
pause
