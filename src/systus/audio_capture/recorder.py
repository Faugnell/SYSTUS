import numpy as np
import sounddevice as sd


class AudioRecorder:
    """
    Simple audio recorder for SYSTUS.
    Returns numpy array (mono or stereo depending on the device).
    """

    def __init__(self, samplerate: int = 48000, channels: int = 2, device=None):
        self.samplerate = samplerate
        self.channels = channels
        self.device = device

    def record(self, duration: float = 5.0) -> np.ndarray:
        """
        Record audio for a fixed duration.
        Returns:
            np.ndarray: audio buffer (frames, channels)
        """

        frames = []

        def callback(indata, frame_count, time_info, status):
            frames.append(indata.copy())

        try:
            with sd.InputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                device=self.device,
                callback=callback,
            ):
                sd.sleep(int(duration * 1000))

        except Exception as e:
            return np.zeros((0, self.channels), dtype=np.float32)

        if not frames:
            return np.zeros((0, self.channels), dtype=np.float32)

        audio = np.concatenate(frames, axis=0)

        return audio