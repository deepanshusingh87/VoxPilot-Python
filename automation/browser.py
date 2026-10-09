
import webbrowser
import pyautogui
import threading
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright


def search_web(query):
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    webbrowser.open(url)


def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    webbrowser.open(url)


def control_video(command):
    controls = {
        "pause video": "k",
        "play video": "k",
        "mute video": "m",
        "unmute video": "m",
        "full screen": "f",
        "exit full screen": "esc",
        "volume up": "up",
        "volume down": "down",
    }

    if command not in controls:
        return False

    pyautogui.press(controls[command])
    return True


def play_youtube(query):
    def youtube_worker():
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    headless=False
                )
                page = browser.new_page()

                search_url = (
                    "https://www.youtube.com/results?search_query="
                    f"{quote_plus(query)}"
                )

                page.goto(
                    search_url,
                    wait_until="domcontentloaded"
                )

                first_video = page.locator(
                    "ytd-video-renderer a#video-title"
                ).first

                first_video.wait_for(
                    state="visible",
                    timeout=20000
                )

                first_video.click()

                print(f"Playing YouTube: {query}")

                # Keep browser alive while VoxPilot listens
                threading.Event().wait()

        except Exception as error:
            print(f"YouTube error: {error}")

    thread = threading.Thread(
        target=youtube_worker,
        daemon=True
    )
    thread.start()
    return True
