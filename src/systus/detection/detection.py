import time
from enum import Enum

import systus.display.screen as screen
from systus.audio_capture.recorder import AudioRecorder
from systus.detection.audd_client import AudDClient


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
        self.think_timeout = 10

        self.last_render_state = None

        # AUDIO
        self.recorder = AudioRecorder()

        self.audd = AudDClient(
            api_token="a1f8dc29dd7765e68f96e90dc26b8cbc"
        )

        self.wav_path = None
        self.result = None


    # -------------------------
    # START DETECTION
    # ------------------------
    def start(self):
        if self.state in (RunState.IDLE, RunState.RESULT):
            self.state = RunState.LISTENING
            self.listen_start_time = time.time()

            self.wav_path = self.recorder.record(self.listen_duration)


    # -------------------------
    # UPDATE LOOP
    # -------------------------
    def update(self, now: float):

        # -------------------------
        # LISTENING
        # -------------------------
        if self.state == RunState.LISTENING:

            if now - self.listen_start_time >= self.listen_duration:
                self.state = RunState.THINKING
                self.think_start_time = time.time()

        # -------------------------
        # THINKING
        # -------------------------
        elif self.state == RunState.THINKING:

            # timeout protection
            if time.time() - self.think_start_time > self.think_timeout:
                self.result = {
                    "error": "Systus couldn't identify the song. Please try again."
                }
                self.state = RunState.RESULT

                if self.wav_path:
                    self.recorder.cleanup(self.wav_path)
                    self.wav_path = None
                return

            if self.wav_path is None:
                return

            try:
                self.result = self.audd.recognize_file(self.wav_path)
            except Exception as e:
                self.result = {"error": str(e)}
            finally:
                if self.wav_path:
                    self.recorder.cleanup(self.wav_path)
                    self.wav_path = None

            self.state = RunState.RESULT

        # -------------------------
        # RESULT
        # -------------------------
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
            print("RESULT =", self.result)
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

        self.wav_path = None
        self.result = None