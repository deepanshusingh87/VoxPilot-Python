
import os
import subprocess
from pathlib import Path


def find_application(app_name):
    app_name = app_name.lower().strip()

    start_menu_paths = [
        Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ["PROGRAMDATA"]) / "Microsoft/Windows/Start Menu/Programs",
    ]

    matches = []

    for start_menu in start_menu_paths:
        if not start_menu.exists():
            continue

        for shortcut in start_menu.rglob("*"):
            if shortcut.suffix.lower() not in (".lnk", ".url"):
                continue

            if app_name in shortcut.stem.lower():
                matches.append(shortcut)

    if not matches:
        return None

    matches.sort(
        key=lambda item: (
            item.stem.lower() != app_name,
            len(item.stem)
        )
    )

    return matches[0]



def open_application(app_name):
    app_name = app_name.lower().strip()

    built_in_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
    }

    if app_name in built_in_apps:
        try:
            subprocess.Popen([built_in_apps[app_name]])
            return True
        except OSError as error:
            print(f"Application launch error: {error}")
            return False

    shortcut = find_application(app_name)

    if shortcut is None:
        print(f"Application not found: {app_name}")
        return False

    try:
        os.startfile(str(shortcut))
        return True
    except OSError as error:
        print(f"Application launch error: {error}")
        return False
