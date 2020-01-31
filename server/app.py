from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

@app.route("/api", methods=['POST'])
def api():

    r = request.json
    print(r)

    return '', 200


if __name__ == "__main__":
    app.run(port=5000)