import io
import wave

import numpy as np
import pyttsx3
import sounddevice as sd
import speech_recognition as sr


engine = pyttsx3.init()


def speak(text):
    print(f"VoxPilot: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    sample_rate = 16000
    duration = 5

    print("Listening... Speak now.")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    audio_data = np.squeeze(recording)

    wav_buffer = io.BytesIO()

    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

    wav_buffer.seek(0)

    try:
        with sr.AudioFile(wav_buffer) as source:
            audio = recognizer.record(source)

        command = recognizer.recognize_google(audio)

        print(f"You: {command}")

        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand you.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

    except Exception as error:
        print(f"Error: {error}")
        return ""