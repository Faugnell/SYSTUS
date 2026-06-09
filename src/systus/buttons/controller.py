from gpiozero import Button
import time
from threading import Lock


class ButtonController:
    def __init__(self, on_mode_toggle, on_action):

        # debounce HARDWARE + logiciel
        self.mode_button = Button(5, bounce_time=0.15)
        self.action_button = Button(6, bounce_time=0.15)

        self.on_mode_toggle = on_mode_toggle
        self.on_action = on_action

        self._lock = Lock()
        self._last_mode_click = 0

        self.mode_button.when_pressed = self._safe_mode_toggle
        self.action_button.when_pressed = self._safe_action

    def _safe_mode_toggle(self):
        now = time.time()

        with self._lock:
            # anti double trigger logiciel (très important)
            if now - self._last_mode_click < 0.4:
                return
            self._last_mode_click = now

        self.on_mode_toggle()

    def _safe_action(self):
        self.on_action()

    def cleanup(self):
        self.mode_button.close()
        self.action_button.close()