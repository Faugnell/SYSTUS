from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


def get_wifi_networks():

    result = subprocess.run(
        [
            "nmcli",
            "-t",
            "-f",
            "SSID",
            "dev",
            "wifi",
            "list",
        ],
        capture_output=True,
        text=True,
    )

    networks = []

    for line in result.stdout.splitlines():

        ssid = line.strip()

        if ssid and ssid not in networks:
            networks.append(ssid)

    return sorted(networks)


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

    print(f"SSID={ssid}")

    cmd = [
        "nmcli",
        "dev",
        "wifi",
        "connect",
        ssid,
        "password",
        password,
    ]

    try:

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        print(result.stderr)

        if result.returncode == 0:

            return f"""
            <h2>Connected successfully</h2>

            <p>SYSTUS connected to:</p>

            <b>{ssid}</b>
            """

        return f"""
        <h2>Connection failed</h2>

        <pre>{result.stderr}</pre>
        """

    except Exception as e:

        return f"""
        <h2>Error</h2>

        <pre>{e}</pre>
        """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )