"""S.Y.S.T.U.S. application entrypoint (runtime loop)."""

from __future__ import annotations

import subprocess
import time
from enum import Enum

import systus.display.screen as screen
from systus.buttons.controller import ButtonController

# -------------------------
# CLASSES
# -------------------------
class AppMode(str, Enum):
    SETUP = "setup"
    RUNNING = "running"

class RunState(str, Enum):
    IDLE = "idle"
    DETECTING = "detecting"
    THINKING = "thinking"
    RESULT = "result"


# -------------------------
# STATE GLOBAL
# -------------------------
manual_mode: AppMode | None = None
boot_mode: AppMode | None = None
run_state = RunState.IDLE


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

    if is_wifi_connected():
        boot_mode = AppMode.RUNNING
    else:
        boot_mode = AppMode.SETUP

def get_current_mode():
    global boot_mode

    if boot_mode is None:
        init_mode()

    return manual_mode if manual_mode is not None else boot_mode


# -------------------------
# MODES LOGIC
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
# RUNNING MODE
# -------------------------
def handle_running_mode():
    global run_state

    if run_state == RunState.IDLE:
        screen.show_idle()

    elif run_state == RunState.DETECTING:
        screen.show_detecting()
        run_state = RunState.THINKING

    elif run_state == RunState.THINKING:
        screen.show_thinking()

    elif run_state == RunState.RESULT:
        screen.show_result_placeholder()

        run_state = RunState.IDLE



# -------------------------
# MUSIC DETECTION
# -------------------------
def start_detection():
    global run_state

    mode = get_current_mode()

    if mode == AppMode.RUNNING and run_state == RunState.IDLE:
        run_state = RunState.DETECTING


# -------------------------
# MAIN LOOP
# -------------------------
def main_loop():    
    last_draw_time = 0
    DRAW_INTERVAL = 1.0  

    last_mode = None

    init_mode()
    buttons = ButtonController(toggle_mode, start_detection)

    try:
        while True:
            mode = get_current_mode()

            now = time.time()

            should_redraw_mode = (mode != last_mode)
            should_redraw_timer = (now - last_draw_time > DRAW_INTERVAL)

            if should_redraw_mode or should_redraw_timer:

                if should_redraw_mode:
                    print(f"[MODE CHANGE] → {mode.value}")

                if mode == AppMode.SETUP:
                    screen.show_setup()
                else:
                    screen.show_running()

                last_mode = mode
                last_draw_time = now

            if mode == AppMode.RUNNING:
                handle_running_mode()

            time.sleep(0.2)

    finally:
        buttons.cleanup()


def main():
    main_loop()


if __name__ == "__main__":
    main()

