import os
import webbrowser
from datetime import datetime

from assistant.voice import speak


def process_command(command):

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("start calc")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("start notepad")

    elif "what time" in command or "current time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    else:
        speak("Sorry, I don't know that command yet.")