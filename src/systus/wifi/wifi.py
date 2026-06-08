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

    networks = []

    for line in result.stdout.splitlines():
        ssid = line.strip()

        if ssid and ssid not in networks:
            networks.append(ssid)

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

    print(f"[WIFI] Connecting to SSID={ssid}")

    try:
        # 🔥 SIMPLE & ROBUST WAY (NO PROFILE MANAGEMENT)
        result = subprocess.run(
            [
                "nmcli",
                "dev",
                "wifi",
                "connect",
                ssid,
                "password",
                password,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        print(result.stdout)

        return f"""
        <h2>✅ Connected successfully</h2>
        <p>Connected to:</p>
        <b>{ssid}</b>
        """

    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)

        return f"""
        <h2>❌ Connection failed</h2>
        <pre>{e.stderr}</pre>
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