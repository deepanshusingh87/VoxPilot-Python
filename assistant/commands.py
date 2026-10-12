
import os
import subprocess
import webbrowser
import time


from datetime import datetime
from automation.universal_controller import controller
from automation.universal_controller import controller
from automation.action_executor import executor

from assistant.voice import speak
from automation.windows import open_application
from automation.keyboard import (
    type_text,
    keyboard_action,
    control_volume,
)
from automation.browser import (
    search_web,
    search_youtube,
    control_video,
    play_youtube,
)
from automation.app_controller import (
    open_any_app,
    control_active_app,
    focus_application,
    navigate_application,
)
from automation.whatsapp import (
    search_whatsapp_contact,
    open_whatsapp_chat,
    type_whatsapp_message,
    send_whatsapp_message,
)


active_app = None
pending_whatsapp_message = False
whatsapp_draft_ready = False


WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "whatsapp": "https://web.whatsapp.com/",
}

APPLICATIONS = {
    "calculator": ["calc.exe"],
    "notepad": ["notepad.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "command prompt": ["cmd.exe"],
    "cmd": ["cmd.exe"],
}

ACTION_WORDS = ("open", "launch", "start", "run")


def execute_multiple_commands(command):
    if " and " not in command:
        return False

    # Do not split message text or confirmation commands
    if command.startswith("type message "):
        return False

    if command.startswith("send message"):
        return False

    actions = command.split(" and ")
    current_app = None

    for action in actions:
        action = action.strip()

        if not action:
            continue

        if action.startswith("open "):
            current_app = action[5:].strip()
            process_command(action)
            time.sleep(2)

        elif action.startswith("type ") and current_app:
            if focus_application(current_app):
                process_command(action)
            else:
                speak(f"Could not focus {current_app}")

        else:
            process_command(action)

    return True


def process_command(command):
    global active_app
    global pending_whatsapp_message
    global whatsapp_draft_ready

    command = " ".join(command.lower().split())

    if not command:
        return

    # WhatsApp message confirmation
    if pending_whatsapp_message:
        pending_whatsapp_message = False

        if command in ("yes", "confirm", "send it"):
            if whatsapp_draft_ready and send_whatsapp_message():
                speak("Message sent successfully")
                whatsapp_draft_ready = False
            else:
                speak("Could not send WhatsApp message")
        else:
            speak("Message sending cancelled")

        return

    # WhatsApp message typing
    if command.startswith("type message "):
        message = command[len("type message "):].strip()

        if not message:
            speak("Please tell me the message.")
            return

        whatsapp_draft_ready = False

        if type_whatsapp_message(message):
            whatsapp_draft_ready = True
            active_app = "whatsapp"
            speak("Message typed. Say send message to continue.")
        else:
            speak("Could not type WhatsApp message.")

        return

    # WhatsApp send confirmation
    if command == "send message":
        if not whatsapp_draft_ready:
            speak("Please type a WhatsApp message first.")
            return

        pending_whatsapp_message = True
        speak("Do you want to send this message? Say yes or no.")
        return

    # Multiple voice commands
    if execute_multiple_commands(command):
        return

    # Volume control
    if control_volume(command):
        speak(f"{command} completed")
        return

    # Current time
    if any(phrase in command for phrase in [
        "what time",
        "current time",
        "tell me the time",
    ]):
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return

    # Universal application search
    if command.startswith("search in ") and " for " in command:
        app_name, query = command[len("search in "):].split(" for ", 1)

        app_name = app_name.strip()
        query = query.strip()

        if controller.search(query, app_name):
            active_app = app_name
            controller.active_app = app_name
            speak(f"Searching in {app_name} for {query}")
        else:
            speak(f"Could not search in {app_name}")

        return

    # WhatsApp contact search
    if command.startswith("search contact "):
        contact = command[len("search contact "):].strip()

        whatsapp_draft_ready = False

        if search_whatsapp_contact(contact):
            active_app = "whatsapp"
            speak(f"Searching WhatsApp contact {contact}")
        else:
            speak("Could not search WhatsApp contact.")

        return

    # Open selected WhatsApp chat
    if command == "open chat":
        whatsapp_draft_ready = False

        if open_whatsapp_chat():
            active_app = "whatsapp"
            speak("Opening WhatsApp chat")
        else:
            speak("Could not open WhatsApp chat.")

        return

    # YouTube search
    if command.startswith("search youtube for "):
        query = command[len("search youtube for "):].strip()

        if query:
            search_youtube(query)
            active_app = "browser"
            speak(f"Searching YouTube for {query}")

        return

    # YouTube autoplay
    if (
        command.startswith(("play ", "open ", "search "))
        and " on youtube" in command
    ):
        query = command.split(" on youtube")[0]

        for prefix in ("play ", "open ", "search "):
            if query.startswith(prefix):
                query = query[len(prefix):]
                break

        query = query.strip()

        if query and play_youtube(query):
            active_app = "browser"
            speak(f"Playing {query} on YouTube")
        else:
            speak("Sorry, I could not play that video.")

        return

    # WhatsApp context-based search
    if command.startswith("search ") and active_app == "whatsapp":
        contact = command[len("search "):].strip()

        if not contact:
            speak("Please tell me the contact name.")
            return

        whatsapp_draft_ready = False

        if search_whatsapp_contact(contact):
            speak(f"Searching WhatsApp contact {contact}")
        else:
            speak("Could not search WhatsApp contact.")

        return

    # Google search
    if command.startswith("search "):
        query = command[len("search "):].strip()

        if query:
            search_web(query)
            active_app = "browser"
            speak(f"Searching Google for {query}")

        return

    # Video controls
    if control_video(command):
        speak(f"{command} completed")
        return

    # Application navigation
    if navigate_application(command):
        speak(f"{command} completed")
        return

    # Universal typing
    if command.startswith("type "):
        text = command[5:]

        if control_active_app("type", text):
            speak("Text typed")
        else:
            speak("Could not type text.")

        return
   
    if command.startswith("scroll down in "):
        app_name = command[len("scroll down in "):].strip()

        if executor.execute("scroll down", app_name):
            active_app = app_name
            controller.active_app = app_name
            speak(f"Scrolled down in {app_name}")
        else:
            speak(f"Could not scroll in {app_name}")
        return
    if command.startswith("scroll up in "):
        app_name = command[len("scroll up in "):].strip()

        if executor.execute("scroll up", app_name):
            active_app = app_name
            controller.active_app = app_name
            speak(f"Scrolled up in {app_name}")
        else:
            speak(f"Could not scroll in {app_name}")
        return
    # Universal application actions
    app_actions = {
        "copy",
        "paste",
        "select all",
        "save",
        "close",
        "minimize",
        "scroll down",
        "scroll up",
        "press enter",
    }

    if command in app_actions:
        if control_active_app(command):
            speak(f"{command} completed")
        else:
            speak(f"Could not perform {command}")

        return

    # Existing keyboard shortcuts
    if keyboard_action(command):
        speak(f"{command} completed")
        return

    # Identify application command
    words = command.split()

    if not words or words[0] not in ACTION_WORDS:
        speak("Sorry, I don't know that command yet.")
        return

    target = " ".join(words[1:])

    if not target:
        speak("Please tell me which application to open.")
        return

    # WhatsApp Desktop
    if target in ("whatsapp", "whatsapp desktop"):
        if open_any_app("whatsapp"):
            active_app = "whatsapp"
            whatsapp_draft_ready = False
            speak("Trying to open WhatsApp Desktop")
        else:
            speak("Could not launch WhatsApp Desktop")

        return

    # Existing websites
    if target in WEBSITES:
        speak(f"Opening {target}")
        webbrowser.open(WEBSITES[target])
        active_app = "browser"
        return

    # Google Chrome
    if target in ("chrome", "google chrome"):
        speak("Opening Chrome")

        try:
            os.startfile("chrome.exe")
        except OSError:
            webbrowser.open("https://www.google.com")

        active_app = "browser"
        return

    # Visual Studio Code
    if target in ("vs code", "vscode", "visual studio code"):
        speak("Opening Visual Studio Code")

        try:
            subprocess.Popen(["code.cmd"], shell=True)
        except OSError:
            speak("Could not open Visual Studio Code.")

        active_app = target
        return

    # Existing registered applications
    if target in APPLICATIONS:
        speak(f"Opening {target}")
        subprocess.Popen(APPLICATIONS[target])
        active_app = target
        return

    # Existing Windows application launcher
    if open_application(target):
        speak(f"Opening {target}")
        active_app = target
        return

    # Universal Windows application launcher
    if open_any_app(target):
        speak(f"Trying to open {target}")
        active_app = target
        return

    speak(f"Could not open {target}")

    # Universal application commands
    if command == "scroll down":
        if controller.scroll("down", active_app):
            speak("Scrolled down")
        else:
            speak("Could not scroll")
        return

    if command == "scroll up":
        if controller.scroll("up", active_app):
            speak("Scrolled up")
        else:
            speak("Could not scroll")
        return
