from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>SYSTUS</h1>
    <p>Serveur Flask opérationnel</p>
    """

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )