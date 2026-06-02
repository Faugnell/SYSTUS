"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""


from __future__ import annotations

import subprocess
import time
from enum import Enum

class AppMode(str, Enum):
    SETUP = "setup"
    RUNNING = "running"


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
    print("[RUNNING] System connected. Normal mode active.")


def main_loop() -> None:
    """
    Infinite runtime loop.
    """
    last_mode = None

    while True:
        mode = get_mode()

        # log only when mode changes
        if mode != last_mode:
            print(f"[MODE CHANGE] → {mode.value}")
            last_mode = mode

        if mode == AppMode.SETUP:
            run_setup_mode()
        else:
            run_running_mode()

        time.sleep(2)


def main() -> None:
    main_loop()


if __name__ == "__main__":
    main()