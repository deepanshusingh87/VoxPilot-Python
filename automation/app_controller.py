
import os
import subprocess
import pyautogui
import time
import ctypes



def focus_application(app_name):
    user32 = ctypes.windll.user32

    user32.EnumWindows.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p
    ]
    user32.GetWindowTextLengthW.argtypes = [ctypes.c_void_p]
    user32.GetWindowTextW.argtypes = [
        ctypes.c_void_p,
        ctypes.c_wchar_p,
        ctypes.c_int
    ]
    user32.GetForegroundWindow.restype = ctypes.c_void_p
    user32.SetForegroundWindow.argtypes = [ctypes.c_void_p]

    matches = []

    CALLBACK = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.c_void_p,
        ctypes.c_void_p
    )

    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)

            if length > 0:
                title = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, title, length + 1)

                if app_name.lower() in title.value.lower():
                    matches.append(hwnd)

        return True

    callback_ref = CALLBACK(callback)
    user32.EnumWindows(callback_ref, None)

    if not matches:
        return False

    hwnd = matches[0]

    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)

    try:
        user32.SetForegroundWindow(hwnd)
    except OSError:
        return False

    time.sleep(0.5)

    return user32.GetForegroundWindow() == hwnd


def open_any_app(app_name):
    app_name = app_name.strip()

    if not app_name:
        return False

    # Search through the Windows Start Menu
    pyautogui.press("win")
    time.sleep(0.7)

    pyautogui.write(app_name, interval=0.06)
    time.sleep(1.5)

    pyautogui.press("enter")
    time.sleep(2)

    return True


def control_active_app(action, text=None):
    action = action.lower().strip()

    if action == "type" and text:   
        pyautogui.write(text, interval=0.04)

    elif action == "copy":
        pyautogui.hotkey("ctrl", "c")

    elif action == "paste":
        pyautogui.hotkey("ctrl", "v")

    elif action == "select all":
        pyautogui.hotkey("ctrl", "a")

    elif action == "save":
        pyautogui.hotkey("ctrl", "s")

    elif action == "close":
        pyautogui.hotkey("alt", "f4")

    elif action == "minimize":
        pyautogui.hotkey("win", "down")

    elif action == "scroll down":
        pyautogui.scroll(-5)

    elif action == "scroll up":
        pyautogui.scroll(5)

    elif action == "press enter":
        pyautogui.press("enter")

    else:
        return False

    return True


def navigate_application(action):
    action = action.lower().strip()

    shortcuts = {
        "new tab": ("ctrl", "t"),
        "close tab": ("ctrl", "w"),
        "next tab": ("ctrl", "tab"),
        "previous tab": ("ctrl", "shift", "tab"),
        "find": ("ctrl", "f"),
        "refresh": ("ctrl", "r"),
        "go back": ("alt", "left"),
        "go forward": ("alt", "right"),
    }

    if action in shortcuts:
        pyautogui.hotkey(*shortcuts[action])
        return True

    keys = {
        "press enter": "enter",
        "press escape": "esc",
        "press tab": "tab",
        "press backspace": "backspace",
        "press space": "space",
    }

    if action in keys:
        pyautogui.press(keys[action])
        return True

    if action.startswith("search for "):
        query = action[len("search for "):].strip()

        if not query:
            return False

        pyautogui.hotkey("ctrl", "f")
        time.sleep(0.5)
        pyautogui.write(query, interval=0.04)
        return True

    return False

