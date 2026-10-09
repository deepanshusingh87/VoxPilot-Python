
import os
import subprocess
import webbrowser
from datetime import datetime

from assistant.voice import speak
from automation.windows import open_application
from automation.keyboard import type_text, keyboard_action, control_volume
from automation.browser import (
    search_web,
    search_youtube,
    control_video,
    play_youtube,
)

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


def process_command(command):
    command = " ".join(command.lower().split())

    if control_volume(command):
        speak(f"{command} completed")
        return

    if any(phrase in command for phrase in [
        "what time",
        "current time",
        "tell me the time",
    ]):
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return

    if command.startswith("type "):
        text = command[5:]
        type_text(text)
        speak("Text typed")
        return

    if keyboard_action(command):
        speak(f"{command} completed")
        return

    if command.startswith("search youtube for "):
        query = command[len("search youtube for "):]
        search_youtube(query)
        speak(f"Searching YouTube for {query}")
        return

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
            speak(f"Playing {query} on YouTube")
        else:
            speak("Sorry, I could not play that video.")
        return

    if command.startswith("search "):
        query = command[len("search "):]
        search_web(query)
        speak(f"Searching Google for {query}")
        return

    if control_video(command):
        speak(f"{command} completed")
        return

    words = command.split()

    if not words or words[0] not in ACTION_WORDS:
        speak("Sorry, I don't know that command yet.")
        return

    target = " ".join(words[1:])

    if target in WEBSITES:
        speak(f"Opening {target}")
        webbrowser.open(WEBSITES[target])
        return

    if target in ("chrome", "google chrome"):
        speak("Opening Chrome")
        try:
            os.startfile("chrome.exe")
        except OSError:
            webbrowser.open("https://www.google.com")
        return

    if target in ("vs code", "vscode", "visual studio code"):
        speak("Opening Visual Studio Code")
        try:
            subprocess.Popen(["code.cmd"], shell=True)
        except OSError:
            speak("Could not open Visual Studio Code.")
        return

    if target in APPLICATIONS:
        speak(f"Opening {target}")
        subprocess.Popen(APPLICATIONS[target])
        return

    if open_application(target):
        speak(f"Opening {target}")
        return

    speak(f"I don't have an action for {target} yet.")
