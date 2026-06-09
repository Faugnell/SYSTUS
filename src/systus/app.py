"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""

from __future__ import annotations

import subprocess
import time
from enum import Enum
from threading import Thread, Lock

import systus.display.screen as screen
from systus.buttons.controller import ButtonController
from systus.detection.detection import DetectionController
from systus.wifi.wifi import create_wifi_app

# -------------------------
# STATE
# -------------------------
class AppMode(str, Enum):
    SETUP = "setup"
    RUNNING = "running"


current_mode: AppMode | None = None
mode_lock = Lock()

detection = DetectionController()


# -------------------------
# WIFI STATE
# -------------------------
def is_wifi_connected() -> bool:
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "STATE", "general"],
            capture_output=True,
            text=True,
        )
        return "connected" in result.stdout.lower()
    except:
        return False


# -------------------------
# MODE MANAGEMENT
# -------------------------
def set_mode(new_mode: AppMode, source: str = "system"):
    global current_mode

    with mode_lock:

        if current_mode == new_mode:
            return

        old = current_mode
        current_mode = new_mode

        print(f"[MODE] {old} → {new_mode} ({source})")

        # side effects centralisés
        detection.reset()

        if new_mode == AppMode.SETUP:
            screen.show_setup()

        elif new_mode == AppMode.RUNNING:
            screen.show_idle()


def toggle_mode():
    with mode_lock:
        if current_mode == AppMode.RUNNING:
            set_mode(AppMode.SETUP, "button")
        else:
            set_mode(AppMode.RUNNING, "button")


def get_mode() -> AppMode:
    return current_mode

def init_mode():
    global current_mode
    current_mode = AppMode.RUNNING if is_wifi_connected() else AppMode.SETUP


# -------------------------
# WIFI CALLBACK
# -------------------------
def on_wifi_connected(ssid: str):
    print(f"[SYSTEM] WiFi connected → {ssid}")

    set_mode(AppMode.RUNNING, "wifi")



# -------------------------
# WIFI SERVER
# -------------------------
def start_wifi_server():
    app = create_wifi_app(on_wifi_connected)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


# -------------------------
# DETECTION
# -------------------------
def start_detection():
    if get_mode() == AppMode.RUNNING:
        detection.start()


# -------------------------
# MAIN LOOP
# -------------------------
def main_loop():

    init_mode()

    if current_mode == AppMode.SETUP:
        screen.show_setup()
    else:
        screen.show_idle()

    Thread(target=start_wifi_server, daemon=True).start()

    buttons = ButtonController(toggle_mode, start_detection)

    try:
        last_mode = None
        while True:
            mode = get_mode()
            now = time.time()

            # -------------------------
            # MODE CHANGE
            # -------------------------
            if mode != last_mode:
                print(f"[MODE CHANGE] → {mode}")
                last_mode = mode

            if mode == AppMode.RUNNING:
                detection.update(now)
                detection.render()

            time.sleep(0.2)

    finally:
        buttons.cleanup()


def main():
    main_loop()


if __name__ == "__main__":
    main()

