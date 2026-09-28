from assistant.voice import speak, listen
from assistant.commands import process_command


def main():
    speak("VoxPilot is ready.")

    while True:
        command = listen()

        if not command:
            continue

        if (
            "exit voxpilot" in command
            or "stop voxpilot" in command
            or "goodbye" in command
        ):
            speak("Goodbye. Shutting down VoxPilot.")
            break

        process_command(command)


if __name__ == "__main__":
    main()