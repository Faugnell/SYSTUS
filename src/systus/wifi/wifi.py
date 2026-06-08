from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# -------------------------
# WIFI SCAN
# -------------------------

def get_wifi_networks():
    # refresh scan
    subprocess.run(["nmcli", "dev", "wifi", "rescan"], capture_output=True)

    result = subprocess.run(
        ["nmcli", "-t", "-f", "SSID", "dev", "wifi", "list"],
        capture_output=True,
        text=True,
    )

    networks = set()

    for line in result.stdout.splitlines():
        ssid = line.strip()
        if ssid:
            networks.add(ssid)

    return sorted(networks)


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
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

    profile_name = f"SYSTUS_{ssid}"

    try:
        # 1. delete old profile if exists (ignore errors)
        subprocess.run(
            ["nmcli", "connection", "delete", profile_name],
            capture_output=True
        )

        # 2. create profile (IMPORTANT FIX)
        subprocess.run(
            [
                "nmcli",
                "connection",
                "add",
                "type", "wifi",
                "ifname", "wlan0",
                "con-name", profile_name,
                "ssid", ssid,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # 3. set security (THIS FIXES YOUR ERROR)
        subprocess.run(
            [
                "nmcli",
                "connection",
                "modify",
                profile_name,
                "wifi-sec.key-mgmt", "wpa-psk",
                "wifi-sec.psk", password,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        # 4. bring connection up
        subprocess.run(
            ["nmcli", "connection", "up", profile_name],
            check=True,
            capture_output=True,
            text=True,
        )

        return f"""
        <h2>✅ Connected successfully</h2>
        <p>Connected to:</p>
        <b>{ssid}</b>
        """

    except subprocess.CalledProcessError as e:
        return f"""
        <h2>❌ Connection failed</h2>
        <pre>{e.stderr or e.stdout}</pre>
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