import time
from enum import Enum

import systus.display.screen as screen
from systus.audio_capture.recorder import AudioRecorder


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

        # AUDIO
        self.recorder = AudioRecorder()
        self.audio_buffer = None


    # -------------------------
    # START DETECTION
    # ------------------------
    def start(self):
        if self.state in (RunState.IDLE, RunState.RESULT):
            self.state = RunState.LISTENING
            self.listen_start_time = time.time()

    # -------------------------
    # UPDATE LOOP
    # -------------------------
    def update(self, now: float):

        # LISTENING
        if self.state == RunState.LISTENING:

            if now - self.listen_start_time >= self.listen_duration:
                # 1. record audio
                self.audio_buffer = self.recorder.record(self.listen_duration)

                # 2. go THINKING
                self.state = RunState.THINKING
                self.think_start_time = now

        # THINKING
        elif self.state == RunState.THINKING:

            if now - self.think_start_time >= self.think_duration:

                # TODO: ici analyse audio_buffer
                # ex: self.result = detect_song(self.audio_buffer)

                self.state = RunState.RESULT

        # RESULT
        elif self.state == RunState.RESULT:
            pass

    # -------------------------
    # RENDER
    # -------------------------
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

    # -------------------------
    # RESET
    # -------------------------
    def reset(self):
        self.state = RunState.IDLE
        self.listen_start_time = 0
        self.think_start_time = 0
        self.last_render_state = None
        self.audio_buffer = None