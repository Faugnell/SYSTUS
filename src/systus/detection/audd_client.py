import requests
from pathlib import Path


class AudDClient:
    """
    AudD API client (file-based).
    Used to recognize music from WAV files (arecord output, recorder tests, etc).
    """

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.url = "https://api.audd.io/"

    # -------------------------
    # MAIN METHOD
    # -------------------------
    def recognize_file(self, file_path: str | Path) -> dict | None:
        """
        Send a WAV file to AudD and return parsed result.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return None

        try:
            with open(file_path, "rb") as file:
                response = requests.post(
                    self.url,
                    data={
                        "api_token": self.api_token,
                    },
                    files={
                        "file": file,
                    },
                    timeout=15,
                )

            data = response.json()

        except Exception as e:
            print("❌ Request error:", e)
            return None

        # -------------------------
        # RESPONSE CHECK
        # -------------------------
        if data.get("status") != "success":
            print("❌ AudD failed:", data)
            return None

        return data.get("result")

    # -------------------------
    # OPTIONAL WRAPPER
    # -------------------------
    def recognize_default_test(self) -> dict | None:
        """
        Convenience method for your current setup.
        """
        return self.recognize_file("tests/audio/test.wav")