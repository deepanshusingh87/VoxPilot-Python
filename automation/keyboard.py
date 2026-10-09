
import pyautogui

def control_volume(command):
    if command == "volume up":
        pyautogui.press("volumeup", presses=3, interval=0.1)
        return True

    if command == "volume down":
        pyautogui.press("volumedown", presses=3, interval=0.1)
        return True

    if command == "mute volume":
        pyautogui.press("volumemute")
        return True

    return False


def type_text(text):
    pyautogui.write(text, interval=0.05)


def keyboard_action(action):
    shortcuts = {
        "select all": ("ctrl", "a"),
        "copy": ("ctrl", "c"),
        "paste": ("ctrl", "v"),
        "cut": ("ctrl", "x"),
        "save": ("ctrl", "s"),
        "undo": ("ctrl", "z"),
        "minimize window": ("win", "down"),
        "maximize window": ("win", "up"),
        "switch window": ("alt", "tab"),
        "close window": ("alt", "f4"),
    }

    if action not in shortcuts:
        return False

    pyautogui.hotkey(*shortcuts[action])
    return True
