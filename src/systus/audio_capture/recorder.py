import subprocess
import tempfile
import os


class AudioRecorder:
    """
    Recorder basé sur arecord (ALSA natif).
    Très stable sur Raspberry Pi.
    """

    def __init__(
        self,
        device: str = "plughw:0,0",
        samplerate: int = 48000,
        channels: int = 2,
    ):
        self.device = device
        self.samplerate = samplerate
        self.channels = channels

    def record(self, duration: float = 5.0) -> str:
        """
        arecord then return path of recorded file.
        """

        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        path = tmp_file.name
        tmp_file.close()

        cmd = [
            "arecord",
            "-D", self.device,
            "-f", "S16_LE",
            "-r", "16000",
            "-c", "1",
            "-d", str(int(duration)),
            path,
        ]

        subprocess.run(cmd, check=True)

        return path

    def cleanup(self, path: str):
        """
        Supprime le fichier temporaire.
        """
        try:
            os.remove(path)
        except FileNotFoundError:
            pass