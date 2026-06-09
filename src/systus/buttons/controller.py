from gpiozero import Button
from threading import Lock
import time


class ButtonController:
    def __init__(self, on_mode_toggle, on_action):

        # debounce intégré GPIOZero + fallback logiciel
        self.mode_button = Button(
            5,
            bounce_time=0.2  # IMPORTANT
        )

        self.action_button = Button(
            6,
            bounce_time=0.2
        )

        self.on_mode_toggle = on_mode_toggle
        self.on_action = on_action

        self._lock = Lock()
        self._last_mode_trigger = 0

        self.mode_button.when_pressed = self._safe_mode_toggle
        self.action_button.when_pressed = self._safe_action

    def _safe_mode_toggle(self):
        now = time.time()

        with self._lock:
            if now - self._last_mode_trigger < 0.4:
                return  # anti spam HARD
            self._last_mode_trigger = now

        self.on_mode_toggle()

    def _safe_action(self):
        self.on_action()

    def cleanup(self):
        self.mode_button.close()
        self.action_button.close()