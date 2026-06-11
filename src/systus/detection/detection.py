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

        self.last_render_state = None

        # AUDIO
        self.recorder = AudioRecorder()

        self.audd = AudDClient(
            api_token="a1f8dc29dd7765e68f96e90dc26b8cbc"
        )

        self.wav_path = None
        self.result = None
        self.ui_result = None


    # -------------------------
    # START
    # ------------------------
    def start(self):
        if self.state in (RunState.IDLE, RunState.RESULT):
            self.state = RunState.LISTENING
            self.listen_start_time = time.time()

            try:
                self.wav_path = self.recorder.record(self.listen_duration)
            except Exception as e:
                print("RECORDER ERROR:", e)
                self.state = RunState.RESULT
                self.ui_result = None

    # -------------------------
    # BUILD UI DATA
    # -------------------------
    def _build_ui_result(self, result: dict | None):
        if not result:
            return None

        return {
            "title": result.get("title"),
            "artist": result.get("artist"),
            "album": result.get("album"),
            "release_date": result.get("release_date"),
            "song_link": result.get("song_link"),
        }

    # -------------------------
    # UPDATE LOOP
    # -------------------------
    def update(self, now: float):

        # LISTENING
        if self.state == RunState.LISTENING:

            if now - self.listen_start_time >= self.listen_duration:
                self.state = RunState.THINKING

        # THINKING
        elif self.state == RunState.THINKING:

            if not self.wav_path:
                return

            try:
                self.result = self.audd.recognize_file(self.wav_path)
            except Exception as e:
                self.result = {"error": str(e)}

            self.ui_result = self._build_ui_result(self.result)

            self.recorder.cleanup(self.wav_path)
            self.wav_path = None

            self.state = RunState.RESULT

    # -------------------------
    # RENDER
    # -------------------------
    def render(self):
        if self.state == self.last_render_state:
            return

        self.last_render_state = self.state

        if self.state == RunState.IDLE:
            screen.show_idle()
            return

        if self.state == RunState.LISTENING:
            screen.show_listening()
            return

        if self.state == RunState.THINKING:
            screen.show_thinking()
            return

        if self.state == RunState.RESULT:
            if self.ui_result:
                screen.show_result(self.ui_result)
            else:
                screen.show_result({"title": "No result"})
            return


    # -------------------------
    # RESET
    # -------------------------
    def reset(self):
        self.state = RunState.IDLE
        self.listen_start_time = 0
        self.last_render_state = None

        self.wav_path = None
        self.result = None
        self.ui_result = None