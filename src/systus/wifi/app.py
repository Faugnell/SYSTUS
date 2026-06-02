from flask import Flask

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

    return f"Connexion en cours à {ssid}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)