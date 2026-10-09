
import io
import wave
from collections import deque

import numpy as np
import pyttsx3
import sounddevice as sd
import speech_recognition as sr


engine = pyttsx3.init()
recognizer = sr.Recognizer()

SAMPLE_RATE = 16000
BLOCK_DURATION = 0.1
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

speech_threshold = None


def speak(text):
    print(f"VoxPilot: {text}")
    engine.say(text)
    engine.runAndWait()


def calibrate_microphone(stream):
    global speech_threshold

    if speech_threshold is not None:
        return

    print("Calibrating microphone once. Please stay quiet.")

    noise_levels = []

    for _ in range(10):
        audio_block, _ = stream.read(BLOCK_SIZE)

        volume = np.abs(
            audio_block.astype(np.int32)
        ).mean()

        noise_levels.append(volume)

    noise_floor = float(np.median(noise_levels))
    speech_threshold = max(100.0, noise_floor * 2.5)

    print(f"Noise level: {noise_floor:.1f}")
    print(f"Speech threshold: {speech_threshold:.1f}")


def listen():
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=BLOCK_SIZE
        ) as stream:

            calibrate_microphone(stream)

            recorded_blocks = []
            recent_blocks = deque(maxlen=5)

            speech_started = False
            silent_blocks = 0
            active_blocks = 0

            print("Listening... Speak now.")

            for _ in range(150):
                audio_block, _ = stream.read(BLOCK_SIZE)

                volume = np.abs(
                    audio_block.astype(np.int32)
                ).mean()

                if not speech_started:
                    recent_blocks.append(audio_block.copy())

                    if volume > speech_threshold:
                        active_blocks += 1
                    else:
                        active_blocks = 0

                    if active_blocks >= 2:
                        speech_started = True
                        recorded_blocks.extend(recent_blocks)
                        silent_blocks = 0

                else:
                    recorded_blocks.append(audio_block.copy())

                    if volume > speech_threshold:
                        silent_blocks = 0
                    else:
                        silent_blocks += 1

                    if silent_blocks >= 9:
                        break

        if not speech_started:
            print("No speech detected.")
            return ""

        recording = np.concatenate(recorded_blocks, axis=0)

        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(recording.tobytes())

        wav_buffer.seek(0)

        with sr.AudioFile(wav_buffer) as source:
            audio = recognizer.record(source)

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        command = " ".join(command.lower().split())

        print(f"You: {command}")
        return command

    except sr.UnknownValueError:
        print("Speech not understood.")
        return ""

    except sr.RequestError as error:
        print(f"Speech recognition error: {error}")
        return ""

    except sd.PortAudioError as error:
        print(f"Microphone error: {error}")
        return ""

    except KeyboardInterrupt:
        print("\nVoice listening stopped.")
        raise

    except Exception as error:
        print(f"Voice error: {error}")
        return ""
