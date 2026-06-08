from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# -------------------------
# WIFI SCAN
# -------------------------

def get_wifi_networks():
    # force scan (IMPORTANT)
    subprocess.run(
        ["sudo", "nmcli", "dev", "wifi", "rescan"],
        capture_output=True,
        text=True
    )

    result = subprocess.run(
        ["nmcli", "-t", "-f", "SSID", "dev", "wifi", "list"],
        capture_output=True,
        text=True
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

    try:
        # DELETE old connection if exists (important)
        subprocess.run(
            ["sudo", "nmcli", "connection", "delete", ssid],
            capture_output=True,
            text=True
        )

        # CREATE connection
        subprocess.run(
            [
                "sudo", "nmcli",
                "dev", "wifi", "connect",
                ssid,
                "password", password,
                "ifname", "wlan0"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        return f"""
        <h2>✅ Connected successfully</h2>
        <b>{ssid}</b>
        """

    except subprocess.CalledProcessError as e:
        return f"""
        <h2>❌ Connection failed</h2>
        <pre>{e.stderr}</pre>
        """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )