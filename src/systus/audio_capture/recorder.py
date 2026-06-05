import time
import numpy as np
import sounddevice as sd


class AudioRecorder:
    """
    Simple recorder for SYSTUS (Raspberry Pi + ALSA voicehat).
    Captures fixed-duration audio and returns numpy array.
    """

    def __init__(
        self,
        device: int = 0,
        samplerate: int = 48000,
        channels: int = 2,
    ):
        self.device = device
        self.samplerate = samplerate
        self.channels = channels

        self._frames = []
        self._stream = None

    # -------------------------
    # INTERNAL CALLBACK
    # -------------------------
    def _callback(self, indata, frames, time_info, status):
        if status:
            print("Audio status:", status)

        # copy to avoid memory overwrite
        self._frames.append(indata.copy())

    # -------------------------
    # RECORD BLOCKING (simple test)
    # -------------------------
    def record(self, duration: float = 10.0) -> np.ndarray:
        """
        Record audio for a fixed duration.
        Returns numpy array shape: (samples, channels)
        """

        self._frames = []

        print(f"Recording {duration}s...")

        self._stream = sd.InputStream(
            device=self.device,
            samplerate=self.samplerate,
            channels=self.channels,
            dtype="int32",
            callback=self._callback,
        )

        self._stream.start()

        time.sleep(duration)

        self._stream.stop()
        self._stream.close()

        print("Recording finished")

        audio = np.concatenate(self._frames, axis=0)

        print("Shape:", audio.shape)
        print("Max:", np.max(audio))
        print("Min:", np.min(audio))

        return audio