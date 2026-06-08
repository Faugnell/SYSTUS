from flask import Flask, render_template, request
import subprocess
import time

app = Flask(__name__)

# -------------------------
# WIFI SCAN
# -------------------------
def get_wifi_networks():
    # Force scan (non bloquant)
    subprocess.run(
        ["nmcli", "dev", "wifi", "rescan"],
        capture_output=True
    )

    # IMPORTANT: laisse NetworkManager finir le scan
    time.sleep(2)

    result = subprocess.run(
        [
            "nmcli",
            "-t",
            "--fields",
            "SSID",
            "dev",
            "wifi",
            "list",
        ],
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

    print(f"[WIFI] Connecting to SSID={ssid}")

    try:
        # 🔥 SIMPLE & ROBUST CONNECTION (no profile creation)
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
        print("[ERROR STDOUT]", e.stdout)
        print("[ERROR STDERR]", e.stderr)

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