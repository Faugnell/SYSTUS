import time
from enum import Enum
import systus.display.screen as screen


class RunState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    RESULT = "result"


class DetectionController:
    def __init__(self):
        self.state = RunState.IDLE

        self.listen_start_time = 0
        self.listen_duration = 10

        self.think_start_time = 0
        self.think_duration = 2

        self.last_render_state = None

    def start(self):
        if self.state == RunState.IDLE:
            self.state = RunState.LISTENING
            self.listen_start_time = time.time()

    def update(self, now: float):

        # LISTENING → THINKING
        if self.state == RunState.LISTENING:
            if now - self.listen_start_time >= self.listen_duration:
                self.state = RunState.THINKING
                self.think_start_time = now

        # THINKING → RESULT
        elif self.state == RunState.THINKING:
            if now - self.think_start_time >= self.think_duration:
                self.state = RunState.RESULT

        # RESULT → IDLE
        elif self.state == RunState.RESULT:
            self.state = RunState.IDLE

    def render(self):

        if self.state == self.last_render_state:
            return

        if self.state == RunState.IDLE:
            screen.show_idle()

        elif self.state == RunState.LISTENING:
            screen.show_listening()

        elif self.state == RunState.THINKING:
            screen.show_thinking()

        elif self.state == RunState.RESULT:
            screen.show_result_placeholder()

        self.last_render_state = self.state


    def reset(self):
        self.state = RunState.IDLE
        self.listen_start_time = 0
        self.think_start_time = 0
        self.last_render_state = None