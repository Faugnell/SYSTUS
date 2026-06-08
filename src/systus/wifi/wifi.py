from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# -------------------------
# WIFI SCAN
# -------------------------

def get_wifi_networks():
    subprocess.run(["nmcli", "dev", "wifi", "rescan"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = subprocess.run(
        ["nmcli", "-t", "-f", "SSID", "dev", "wifi", "list"],
        capture_output=True,
        text=True,
    )

    networks = []
    for line in result.stdout.splitlines():
        ssid = line.strip()
        if ssid and ssid not in networks:
            networks.append(ssid)

    return sorted(networks)

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
        # 1) create connection profile
        subprocess.run([
            "nmcli",
            "connection",
            "add",
            "type", "wifi",
            "ifname", "wlan0",
            "con-name", ssid,
            "ssid", ssid,
        ], check=True)

        # 2) set security (IMPORTANT FIX)
        subprocess.run([
            "nmcli",
            "connection",
            "modify",
            ssid,
            "wifi-sec.key-mgmt", "wpa-psk",
            "wifi-sec.psk", password,
        ], check=True)

        # 3) activate
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