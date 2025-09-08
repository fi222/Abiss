# Abyss (Windows)

## Overview
A password-gated file maze with a virtual **Storage** vault.

## Tech
- Python 3.11
- Tkinter, tkinterdnd2, Pillow
- PyInstaller for EXE

## Dev
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python abyss_0002.py

## Build (EXE)
pip install pyinstaller
pyinstaller --onefile --noconsole abyss_0002.py -n Abyss_0002

## Notes
- Icons: Amber_folder.png, Blue_folder.png, storage_icon.ico
- Settings gear planned: password change and future options.
