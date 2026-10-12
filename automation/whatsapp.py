
import time
import pyautogui
import ctypes.wintypes

from automation.app_controller import focus_application



def search_whatsapp_contact(contact_name):
    if not contact_name.strip():
        return False

    if not focus_application("WhatsApp"):
        return False

    # Focus WhatsApp search box
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.5)

    # Remove previous search text
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    time.sleep(0.2)

    # Type new contact name
    pyautogui.write(contact_name, interval=0.08)
    time.sleep(1.5)

    return True



def open_whatsapp_chat():
    if not focus_application("WhatsApp"):
        print("Could not focus WhatsApp")
        return False

    time.sleep(0.5)

    # Select first matching contact
    pyautogui.press("down")
    time.sleep(0.4)

    # Open selected conversation
    pyautogui.press("enter")
    time.sleep(1)

    print("Attempted to open WhatsApp chat")
    return True





def type_whatsapp_message(message):
    if not message.strip():
        return False

    if not focus_application("WhatsApp"):
        print("Could not focus WhatsApp")
        return False

    time.sleep(0.5)

    # Get WhatsApp window position
    import ctypes

    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()

    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))

    width = rect.right - rect.left
    height = rect.bottom - rect.top

    # Click inside the message box at the bottom
    x = rect.left + int(width * 0.65)
    y = rect.top + int(height * 0.94)

    pyautogui.click(x, y)
    time.sleep(0.4)

    pyautogui.write(message, interval=0.05)

    print("Message typing attempted")
    return True


def send_whatsapp_message():
    if not focus_application("WhatsApp"):
        return False

    pyautogui.press("enter")
    return True

