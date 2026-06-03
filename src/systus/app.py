"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""


from __future__ import annotations

import subprocess
import time
from enum import Enum
from gpiozero import Button

manual_mode: AppMode | None = None

BUTTON_PIN = 5
button = Button(BUTTON_PIN)

_last_button_state = button.is_pressed

class AppMode(str, Enum):
    SETUP = "setup"
    RUNNING = "running"

def read_button_press() -> bool:
    """
    Returns True only once when the button is pressed.
    """
    global _last_button_state

    current_state = button.is_pressed

    pressed = False

    if current_state and not _last_button_state:
        pressed = True

    _last_button_state = current_state

    return pressed

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
    

def get_mode() -> AppMode:
    """
    Determine system mode based on WiFi state.
    """
    if is_wifi_connected():
        return AppMode.RUNNING
    return AppMode.SETUP


def run_setup_mode() -> None:
    """
    Placeholder for setup mode logic.
    """
    print("[SETUP] No WiFi detected. Setup mode active.")


def run_running_mode() -> None:
    """
    Placeholder for normal mode logic.
    """
    print("[RUNNING] System connected. Running mode active.")


def main_loop() -> None:
    global manual_mode

    last_mode = None

    while True:
        wifi_mode = get_mode()

        # bouton = toggle override
        if read_button_press():
            print("BUTTON PRESSED")
            if manual_mode is None:
                manual_mode = AppMode.SETUP if wifi_mode == AppMode.RUNNING else AppMode.RUNNING
            else:
                manual_mode = None  # retour mode auto

        # logique finale
        mode = manual_mode if manual_mode is not None else wifi_mode

        if mode != last_mode:
            print(f"[MODE CHANGE] → {mode.value}")
            last_mode = mode

        if mode == AppMode.SETUP:
            run_setup_mode()
        else:
            run_running_mode()

        time.sleep(0.02)


def main() -> None:
    try:
        main_loop()
    finally:
        cleanup()


def cleanup() -> None:
    button.close()





if __name__ == "__main__":
    main()

