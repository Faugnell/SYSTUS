from flask import Flask, render_template, request
import subprocess
import time


def create_wifi_app(on_connected_callback):

    app = Flask(__name__)

    # -------------------------
    # WIFI SCAN
    # -------------------------

    def get_wifi_networks():
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

            return sorted(networks)

        except Exception as e:
            print("[WIFI SCAN ERROR]", e)
            return []

    # -------------------------
    # ROUTES
    # -------------------------

    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html", networks=get_wifi_networks())

    @app.route("/wifi", methods=["POST"])
    def wifi():
        ssid = request.form["ssid"]
        password = request.form["password"]

        print(f"[WIFI] Connecting to {ssid}")

        try:
            subprocess.run(
                [
                    "nmcli",
                    "dev",
                    "wifi",
                    "connect",
                    ssid,
                    "password",
                    password,
                ],
                check=True,
            )

            print(f"[WIFI] Connected to {ssid}")

            # 🔥 IMPORTANT FIX
            on_connected_callback(ssid)

            return render_template("success.html", ssid=ssid)

        except subprocess.CalledProcessError as e:
            print("[WIFI ERROR]", e)
            return render_template("failed.html")

        except Exception as e:
            print("[UNEXPECTED WIFI ERROR]", e)
            return render_template("failed.html")

    return app