"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""

from __future__ import annotations

import subprocess
import time
from enum import Enum
from threading import Thread

import systus.display.screen as screen
from systus.buttons.controller import ButtonController
from systus.detection.detection import DetectionController

from systus.wifi.wifi import create_wifi_app

# -------------------------
# CLASSES
# -------------------------
class AppMode(str, Enum):
    SETUP = "setup"
    RUNNING = "running"


# -------------------------
# STATE GLOBAL
# -------------------------
manual_mode: AppMode | None = None
boot_mode: AppMode | None = None

detection = DetectionController()

# -------------------------
# WIFI SETUP
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


def init_mode():
    global boot_mode
    boot_mode = AppMode.RUNNING if is_wifi_connected() else AppMode.SETUP

def get_current_mode():
    global boot_mode

    if boot_mode is None:
        init_mode()

    if manual_mode is not None:
        return manual_mode

    return boot_mode


# -------------------------
# MODE TOGGLE
# -------------------------
def toggle_mode():
    global manual_mode

    current = get_current_mode()

    if manual_mode is None:
        set_mode(
            AppMode.SETUP
            if current == AppMode.RUNNING
            else AppMode.RUNNING
        )
    else:
        manual_mode = None

def set_mode(mode: AppMode):
    global manual_mode

    if manual_mode == mode:
        return

    print(f"[MODE FORCE] → {mode.value}")

    manual_mode = mode

    if mode == AppMode.SETUP:
        detection.reset()
        screen.show_setup()

    elif mode == AppMode.RUNNING:
        detection.reset()
        screen.show_idle()


# -------------------------
# WIFI CALLBACK
# -------------------------
def on_wifi_connected(ssid: str):
    global manual_mode

    print(f"[SYSTEM] WiFi connected → {ssid} → RUNNING")

    manual_mode = AppMode.RUNNING
    detection.reset()
    screen.show_idle()

    print("[SYSTEM] Mode switched immediately to RUNNING")


def start_wifi_server():
    app = create_wifi_app(on_wifi_connected)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


# -------------------------
# DETECTION
# -------------------------
detection = DetectionController()


def start_detection():
    if get_current_mode() == AppMode.RUNNING:
        detection.start()


# -------------------------
# MAIN LOOP
# -------------------------
def main_loop():

    init_mode()

    Thread(target=start_wifi_server, daemon=True).start()

    buttons = ButtonController(toggle_mode, start_detection)

    last_mode = None

    try:
        while True:
            mode = get_current_mode()
            now = time.time()

            # -------------------------
            # MODE CHANGE
            # -------------------------
            if mode != last_mode:
                print(f"[MODE CHANGE] → {mode.value}")

                if mode == AppMode.SETUP:
                    detection.reset()
                    screen.show_setup()

                elif mode == AppMode.RUNNING:
                    detection.reset()

                last_mode = mode

            # -------------------------
            # RUNNING MODE
            # -------------------------
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

