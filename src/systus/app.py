"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""

from __future__ import annotations

import subprocess
import time
from enum import Enum

import systus.display.screen as screen
from systus.buttons.controller import ButtonController
from systus.detection.detection import DetectionController

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


# -------------------------
# WIFI
# -------------------------
def is_wifi_connected() -> bool:
    """
    Detect WiFi connectivity using nmcli.
    Returns True if the system is connected to a network.
    """
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "STATE", "general"],
            capture_output=True,
            text=True,
            check=False,
        )
        return "connected" in result.stdout.lower()
    except FileNotFoundError:
        return False

def init_mode():
    global boot_mode

    boot_mode = AppMode.RUNNING if is_wifi_connected() else AppMode.SETUP

def get_current_mode():
    global boot_mode

    if boot_mode is None:
        init_mode()

    return manual_mode if manual_mode is not None else boot_mode


# -------------------------
# MODE TOGGLE
# -------------------------
def toggle_mode():
    global manual_mode

    current = get_current_mode()

    if manual_mode is None:
        manual_mode = (
            AppMode.SETUP
            if current == AppMode.RUNNING
            else AppMode.RUNNING
        )
    else:
        manual_mode = None


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
                    screen.show_idle()

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

