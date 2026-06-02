from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/wifi", methods=["POST"])
def wifi():
    ssid = request.form["ssid"]
    password = request.form["password"]

    print("SSID:", ssid)
    print("PASSWORD:", password)

    cmd = [
        "nmcli",
        "dev",
        "wifi",
        "connect",
        ssid,
        "password",
        password
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        return f"Erreur: {e}"

    return f"Tentative de connexion à {ssid}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)