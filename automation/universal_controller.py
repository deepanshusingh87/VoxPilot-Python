import time
import ctypes
from ctypes import wintypes

import pyautogui

from automation.app_controller import (
    open_any_app,
    focus_application,
)

from automation.app_profiles import get_app_profile


# =========================================================
# Windows API
# =========================================================

user32 = ctypes.windll.user32

INPUT_MOUSE = 0
MOUSEEVENTF_WHEEL = 0x0800
WHEEL_DELTA = 120


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("union",)

    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUTUNION),
    ]


user32.SendInput.argtypes = [
    wintypes.UINT,
    ctypes.POINTER(INPUT),
    ctypes.c_int,
]

user32.SendInput.restype = wintypes.UINT


user32.GetForegroundWindow.restype = wintypes.HWND


user32.GetWindowRect.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.RECT),
]

user32.GetWindowRect.restype = wintypes.BOOL


user32.GetCursorPos.argtypes = [
    ctypes.POINTER(wintypes.POINT)
]

user32.GetCursorPos.restype = wintypes.BOOL


user32.SetCursorPos.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
]

user32.SetCursorPos.restype = wintypes.BOOL


# =========================================================
# Universal Controller
# =========================================================

class UniversalController:

    def __init__(self):
        self.active_app = None

    # -----------------------------------------------------
    # APP PROFILE
    # -----------------------------------------------------

    def get_profile(self, app_name):
        if not app_name:
            return None

        return get_app_profile(
            app_name.lower().strip()
        )

    # -----------------------------------------------------
    # OPEN APP
    # -----------------------------------------------------

    def open_app(self, app_name):

        if not app_name:
            return False

        app_name = app_name.strip()

        if open_any_app(app_name):

            self.active_app = app_name.lower()

            time.sleep(1)

            return True

        return False

    # -----------------------------------------------------
    # FOCUS APP
    # -----------------------------------------------------

    def focus_app(self, app_name=None):

        target = app_name or self.active_app

        if not target:
            return False

        target = target.lower().strip()

        profile = self.get_profile(target)

        if profile:

            window_title = profile.get(
                "window_title",
                target
            )

        else:

            window_title = target

        if focus_application(window_title):

            self.active_app = target

            return True

        return False

    # -----------------------------------------------------
    # GET WINDOW RECT
    # -----------------------------------------------------

    def get_window_rect(self):

        hwnd = user32.GetForegroundWindow()

        if not hwnd:
            return None

        rect = wintypes.RECT()

        if not user32.GetWindowRect(
            hwnd,
            ctypes.byref(rect)
        ):
            return None

        return rect

    # -----------------------------------------------------
    # GET POSITION INSIDE APP WINDOW
    # -----------------------------------------------------

    def get_app_position(
        self,
        app_name,
        setting_name,
        default=(0.50, 0.50)
    ):

        rect = self.get_window_rect()

        if not rect:
            return None

        width = rect.right - rect.left
        height = rect.bottom - rect.top

        profile = self.get_profile(app_name)

        if profile:

            position = profile.get(
                setting_name,
                default
            )

        else:

            position = default

        x_ratio, y_ratio = position

        x = rect.left + int(
            width * x_ratio
        )

        y = rect.top + int(
            height * y_ratio
        )

        return x, y

    # -----------------------------------------------------
    # WINDOWS NATIVE MOUSE WHEEL
    # -----------------------------------------------------

    def send_wheel(self, direction, steps):

        delta = (
            -WHEEL_DELTA
            if direction == "down"
            else WHEEL_DELTA
        )

        inputs = (INPUT * steps)()

        for i in range(steps):

            inputs[i].type = INPUT_MOUSE

            inputs[i].mi = MOUSEINPUT(
                0,
                0,
                delta & 0xFFFFFFFF,
                MOUSEEVENTF_WHEEL,
                0,
                0
            )

        sent = user32.SendInput(
            steps,
            inputs,
            ctypes.sizeof(INPUT)
        )

        return sent == steps

    # -----------------------------------------------------
    # UNIVERSAL SCROLL
    # -----------------------------------------------------

    def scroll(
        self,
        direction="down",
        app_name=None
    ):

        if direction not in (
            "up",
            "down"
        ):
            return False

        target = (
            app_name
            or self.active_app
        )

        if not target:

            print(
                "No active application"
            )

            return False

        target = target.lower().strip()

        # Bring requested app to front
        if not self.focus_app(target):

            print(
                f"Could not focus {target}"
            )

            return False

        time.sleep(0.2)

        # Position of scrollable panel
        position = self.get_app_position(
            target,
            "scroll_position",
            (0.50, 0.55)
        )

        if not position:
            return False

        x, y = position

        # Save current mouse position
        old_position = wintypes.POINT()

        user32.GetCursorPos(
            ctypes.byref(old_position)
        )

        # Temporarily move over scrollable area
        user32.SetCursorPos(
            int(x),
            int(y)
        )

        time.sleep(0.08)

        profile = self.get_profile(target)

        # Number of real wheel notches
        if profile:

            steps = profile.get(
                "scroll_steps",
                10
            )

        else:

            steps = 10

        try:

            steps = int(steps)

        except (TypeError, ValueError):

            steps = 10

        steps = max(
            1,
            min(steps, 30)
        )

        result = self.send_wheel(
            direction,
            steps
        )

        time.sleep(0.08)

        # Restore mouse to its original location
        user32.SetCursorPos(
            old_position.x,
            old_position.y
        )

        print(
            f"Scrolled {direction} "
            f"in {target} "
            f"with {steps} wheel steps"
        )

        return result

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search(
        self,
        query,
        app_name=None
    ):

        if not query:
            return False

        target = (
            app_name
            or self.active_app
        )

        if not target:
            return False

        target = target.lower().strip()

        profile = self.get_profile(target)

        if not profile:
            return False

        if not profile.get(
            "search_supported",
            False
        ):
            return False

        if not self.focus_app(target):
            return False

        shortcut = profile.get(
            "search_shortcut"
        )

        if not shortcut:
            return False

        pyautogui.hotkey(
            *shortcut
        )

        time.sleep(0.3)

        pyautogui.hotkey(
            "ctrl",
            "a"
        )

        pyautogui.write(
            query,
            interval=0.05
        )

        return True

    # -----------------------------------------------------
    # NORMAL TEXT TYPING
    # -----------------------------------------------------

    def type_text(
        self,
        text,
        app_name=None
    ):

        if not text:
            return False

        if app_name:

            if not self.focus_app(
                app_name
            ):
                return False

        pyautogui.write(
            text,
            interval=0.05
        )

        return True

    # -----------------------------------------------------
    # MESSAGE BOX
    # -----------------------------------------------------

    def focus_message_box(
        self,
        app_name
    ):

        if not self.focus_app(
            app_name
        ):
            return False

        position = self.get_app_position(
            app_name,
            "message_position"
        )

        if not position:
            return False

        x, y = position

        pyautogui.click(
            x,
            y
        )

        time.sleep(0.2)

        return True

    # -----------------------------------------------------
    # TYPE MESSAGE
    # -----------------------------------------------------

    def type_message(
        self,
        message,
        app_name
    ):

        if not message:
            return False

        if not self.focus_message_box(
            app_name
        ):
            return False

        pyautogui.write(
            message,
            interval=0.05
        )

        return True

    # -----------------------------------------------------
    # SEND MESSAGE
    # -----------------------------------------------------

    def send_message(
        self,
        app_name
    ):

        if not self.focus_app(
            app_name
        ):
            return False

        pyautogui.press(
            "enter"
        )

        return True

    # -----------------------------------------------------
    # PRESS KEY
    # -----------------------------------------------------

    def press_key(
        self,
        key,
        app_name=None
    ):

        if app_name:

            if not self.focus_app(
                app_name
            ):
                return False

        pyautogui.press(key)

        return True

    # -----------------------------------------------------
    # SHORTCUT
    # -----------------------------------------------------

    def shortcut(
        self,
        *keys,
        app_name=None
    ):

        if app_name:

            if not self.focus_app(
                app_name
            ):
                return False

        pyautogui.hotkey(
            *keys
        )

        return True


controller = UniversalController()