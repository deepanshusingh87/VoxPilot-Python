from assistant.voice import speak, listen
from assistant.commands import process_command


def main():
    speak("VoxPilot is running. I am ready.")

    while True:
        command = listen()

        if not command:
            continue

        if command in ["exit", "stop", "goodbye"]:
            speak("Goodbye. Shutting down VoxPilot.")
            break

        process_command(command)


if __name__ == "__main__":
    main()