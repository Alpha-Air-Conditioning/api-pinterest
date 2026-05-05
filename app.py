from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔹 Expand short Pinterest URLs (pin.it → full link)
def expand_url(short_url):
    try:
        r = requests.get(short_url, allow_redirects=True, timeout=5)
        return r.url
    except:
        return short_url


# 🔹 Home route
@app.route('/')
def home():
    return "Hrithik API is running 🚀"


# 🔹 Pinterest Downloader API
@app.route('/pin', methods=['GET'])
def pin():
    url = request.args.get('msg')

    if not url:
        return jsonify({
            "response": "ERROR",
            "message": "Missing 'msg' parameter"
        }), 400

    try:
        # 🔥 Expand short link
        full_url = expand_url(url)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # 🔥 Call external parser API
        res = requests.post(
            "https://download.pinload.app/parse",
            json={"url": full_url},
            headers=headers,
            timeout=10
        )

        data = res.json()

        # 🔥 Handle failure
        if not data.get("success"):
            return jsonify({
                "response": "FAILED",
                "powered_by": "hrithik-api-v1",
                "error": "Could not extract media",
                "details": data
            }), 400

        result = data.get("data", {})

        # 🔥 CUSTOM RESPONSE (your fake key-value format)
        return jsonify({
            "response": "OK",
            "powered_by": "hrithik-api-v1",
            "payload": {
                "kind": result.get("type"),
                "source": result.get("url"),
                "cover": result.get("thumbnail"),
                "label": result.get("title")
            }
        })

    except Exception as e:
        return jsonify({
            "response": "ERROR",
            "message": str(e)
        }), 500


# 🔥 Run server (important for Koyeb / Railway / Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
