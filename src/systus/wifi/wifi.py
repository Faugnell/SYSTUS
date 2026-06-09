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
                ["sudo", "nmcli", "dev", "wifi", "rescan"],
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
    @app.route("/scan", methods=["GET"])
    def scan():

        networks = get_wifi_networks()

        return {
            "networks": networks,
            "count": len(networks),
        }

    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html", networks=get_wifi_networks())

    @app.route("/wifi", methods=["POST"])
    def wifi():
        ssid = request.form["ssid"]
        password = request.form["password"]

        print(f"[WIFI] Connecting to {ssid}")

        try:

            # Supprime une éventuelle ancienne configuration
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

            # Création de la connexion
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

            # Configuration WPA2
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

            # Connexion
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

            print(f"[WIFI] Successfully connected to {ssid}")

            on_connected_callback(ssid)

            return render_template(
                "success.html",
                ssid=ssid,
            )

        except subprocess.CalledProcessError as e:
            print("[WIFI ERROR]")
            print(e)
            return render_template("failed.html")
    
        except Exception as e:

            print("[UNEXPECTED WIFI ERROR]")
            print(e)

            return render_template("failed.html")

    return app