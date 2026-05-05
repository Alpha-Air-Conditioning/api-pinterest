from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Pinterest API Running 🚀"

@app.route('/pin', methods=['GET'])
def pin():
    url = request.args.get('msg')

    if not url:
        return jsonify({"error": "Missing msg param"}), 400

    try:
        res = requests.post(
            "https://download.pinload.app/parse",
            json={"url": url},
            timeout=10
        )
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
