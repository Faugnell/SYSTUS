from flask import Flask, render_template, request
import subprocess
import time

app = Flask(__name__)

# -------------------------
# WIFI SCAN
# -------------------------

def get_wifi_networks():

    try:
        # force un vrai scan
        subprocess.run(
            ["sudo", "nmcli", "dev", "wifi", "rescan"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        time.sleep(2)

        result = subprocess.run(
            [
                "nmcli",
                "-t",
                "-f",
                "SSID",
                "dev",
                "wifi",
                "list",
                "ifname",
                "wlan0",
            ],
            capture_output=True,
            text=True,
        )

        networks = set()

        for line in result.stdout.splitlines():

            ssid = line.strip()

            if ssid and ssid != "--":
                networks.add(ssid)

        return sorted(networks)

    except Exception as e:

        print("[WIFI SCAN ERROR]", e)

        return []

# -------------------------
# ROUTES
# -------------------------

@app.route("/", methods=["GET"])
def home():

    return render_template(
        "index.html",
        networks=get_wifi_networks(),
    )

@app.route("/wifi", methods=["POST"])
def wifi():

    ssid = request.form["ssid"]
    password = request.form["password"]

    print(f"[WIFI] Connecting to {ssid}")

    try:

        subprocess.run(
            [
                "sudo",
                "nmcli",
                "connection",
                "delete",
                ssid,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.run(
            [
                "sudo",
                "nmcli",
                "connection",
                "add",
                "type",
                "wifi",
                "ifname",
                "wlan0",
                "con-name",
                ssid,
                "ssid",
                ssid,
            ],
            check=True,
        )

        subprocess.run(
            [
                "sudo",
                "nmcli",
                "connection",
                "modify",
                ssid,
                "wifi-sec.key-mgmt",
                "wpa-psk",
                "wifi-sec.psk",
                password,
            ],
            check=True,
        )

        subprocess.run(
            [
                "sudo",
                "nmcli",
                "connection",
                "up",
                ssid,
            ],
            check=True,
        )

        return f"""
        <h2>✅ Connected successfully</h2>
        <p>SYSTUS connected to:</p>
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