"""S.Y.S.T.U.S. application entrypoint.
"""

from __future__ import annotations

import logging
import subprocess
from enum import Enum
from typing import Protocol


class AppMode(str, Enum):
    """Top-level runtime mode for the device."""

    SETUP = "setup"
    NORMAL = "normal"


class WifiStateDetector(Protocol):
    """Small contract used to decide which mode to run."""

    def is_connected(self) -> bool:
        ...


class NmcliWifiStateDetector:
    """Detect Wi-Fi connectivity from NetworkManager."""

    def is_connected(self) -> bool:
        try:
            completed = subprocess.run(
                ["nmcli", "-t", "-f", "STATE", "general"],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False

        return completed.stdout.strip().lower() == "connected"


def resolve_mode(wifi_state: WifiStateDetector) -> AppMode:
    """Map the current Wi-Fi state to the device runtime mode."""

    return AppMode.NORMAL if wifi_state.is_connected() else AppMode.SETUP


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    wifi_state = NmcliWifiStateDetector()
    mode = resolve_mode(wifi_state)
    logging.info("Current mode: %s", mode.value)


if __name__ == "__main__":
    main()