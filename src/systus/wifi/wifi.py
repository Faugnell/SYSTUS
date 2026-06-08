import subprocess
import time

def get_wifi_networks():
    # 1) force rescan (important)
    subprocess.run(
        ["nmcli", "dev", "wifi", "rescan"],
        capture_output=True,
        text=True
    )

    # 2) laisse NetworkManager respirer (CRUCIAL)
    time.sleep(2)

    # 3) récupération propre avec BSSID (plus fiable que SSID seul)
    result = subprocess.run(
        [
            "nmcli",
            "-t",
            "-f",
            "SSID,BSSID",
            "dev",
            "wifi",
            "list",
        ],
        capture_output=True,
        text=True
    )

    networks = {}

    for line in result.stdout.splitlines():
        parts = line.split(":")
        if len(parts) < 2:
            continue

        ssid = parts[0].strip()

        if not ssid:
            continue

        # dédup par SSID (évite doublons AP)
        networks[ssid] = True

    return sorted(networks.keys())