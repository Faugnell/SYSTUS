"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""

from __future__ import annotations

import subprocess
import time
from enum import Enum

from systus.display.screen import show_setup, show_running
from systus.buttons.controller import ButtonController

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
# MODES
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

    if is_wifi_connected():
        boot_mode = AppMode.RUNNING
    else:
        boot_mode = AppMode.SETUP

def get_current_mode():
    return manual_mode if manual_mode is not None else boot_mode

def toggle_mode():
    global manual_mode

    if manual_mode is None:
        manual_mode = (
            AppMode.SETUP
            if boot_mode == AppMode.RUNNING
            else AppMode.RUNNING
        )
    else:
        manual_mode = None

def run_setup_mode() -> None:
    """
    Placeholder for setup mode logic.
    """

def run_running_mode() -> None:
    """
    Placeholder for normal mode logic.
    """



# -------------------------
# MAIN LOOP
# -------------------------
def main_loop():
    global boot_mode

    last_mode = None

    init_mode()

    buttons = ButtonController(toggle_mode)

    try:
        while True:
            mode = get_current_mode()

            # update écran uniquement si changement
            if mode != last_mode:
                print(f"[MODE CHANGE] → {mode.value}")

                if mode == AppMode.SETUP:
                    show_setup()
                else:
                    show_running()

                last_mode = mode

            # logique runtime
            if mode == AppMode.SETUP:
                run_setup_mode()
            else:
                run_running_mode()

            time.sleep(0.2)

    finally:
        buttons.cleanup()


def main():
    main_loop()


if __name__ == "__main__":
    main()

