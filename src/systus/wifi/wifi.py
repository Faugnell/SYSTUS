from flask import Flask, render_template, request
import subprocess
import threading
import time

app = Flask(__name__)

# -------------------------
# CACHE GLOBAL WIFI
# -------------------------

wifi_cache = []
wifi_lock = threading.Lock()


# -------------------------
# WIFI SCANNER BACKGROUND
# -------------------------

def scan_wifi_loop():
    global wifi_cache

    while True:
        try:
            # refresh scan (non bloquant)
            subprocess.run(
                ["nmcli", "dev", "wifi", "rescan"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            time.sleep(2)  # laisse le temps au driver

            result = subprocess.run(
                ["nmcli", "dev", "wifi", "rescan"],
                capture_output=True,
                text=True,
            )

            print(result.returncode)
            print(result.stdout)
            print(result.stderr)

            networks = set()

            for line in result.stdout.splitlines():
                ssid = line.strip()
                if ssid and ssid != "--":
                    networks.add(ssid)

            with wifi_lock:
                wifi_cache = sorted(networks)

        except Exception as e:
            print("[WIFI SCAN ERROR]", e)

        time.sleep(5)  # scan toutes les 5 secondes


# start thread au lancement
threading.Thread(target=scan_wifi_loop, daemon=True).start()


# -------------------------
# ROUTES
# -------------------------

@app.route("/", methods=["GET"])
def home():
    with wifi_lock:
        networks = wifi_cache.copy()

    return render_template("index.html", networks=networks)

@app.route("/wifi/refresh", methods=["POST"])
def refresh_wifi():
    global wifi_cache

    try:
        subprocess.run(
            ["nmcli", "dev", "wifi", "rescan"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        time.sleep(2)

        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID", "dev", "wifi", "list", "ifname", "wlan0"],
            capture_output=True,
            text=True,
        )

        networks = set()

        for line in result.stdout.splitlines():
            ssid = line.strip()
            if ssid and ssid != "--":
                networks.add(ssid)

        with wifi_lock:
            wifi_cache = sorted(networks)

        return ("OK", 200)

    except Exception as e:
        return (str(e), 500)


@app.route("/wifi", methods=["POST"])
def wifi():
    ssid = request.form["ssid"]
    password = request.form["password"]

    print(f"[WIFI] Connecting to {ssid}")

    try:
        # create connection profile
        subprocess.run([
            "nmcli",
            "connection",
            "add",
            "type", "wifi",
            "ifname", "wlan0",
            "con-name", ssid,
            "ssid", ssid,
        ], check=True)

        # security fix
        subprocess.run([
            "nmcli",
            "connection",
            "modify",
            ssid,
            "wifi-sec.key-mgmt", "wpa-psk",
            "wifi-sec.psk", password,
        ], check=True)

        # activate
        subprocess.run([
            "nmcli",
            "connection",
            "up",
            ssid,
        ], check=True)

        return f"""
        <h2>✅ Connected successfully</h2>
        <b>{ssid}</b>
        """

    except subprocess.CalledProcessError as e:
        return f"""
        <h2>❌ Connection failed</h2>
        <pre>{e}</pre>
        """


# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )