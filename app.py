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


@app.route('/')
def home():
    return "Pinterest API is running 🚀"


@app.route('/pin', methods=['GET'])
def pin():
    url = request.args.get('msg')

    if not url:
        return jsonify({"success": False, "error": "Missing 'msg' parameter"}), 400

    try:
        # 🔥 Expand short link
        full_url = expand_url(url)

        # 🔥 Headers to avoid blocking
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # 🔥 Send request to parser API
        res = requests.post(
            "https://download.pinload.app/parse",
            json={"url": full_url},
            headers=headers,
            timeout=10
        )

        data = res.json()

        # 🔥 Handle failed extraction
        if not data.get("success"):
            return jsonify({
                "success": False,
                "error": "Could not extract media",
                "original_response": data
            }), 400

        result = data.get("data", {})

        # 🔥 Clean response
        return jsonify({
            "success": True,
            "type": result.get("type"),
            "url": result.get("url"),
            "thumbnail": result.get("thumbnail"),
            "title": result.get("title")
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# 🔥 Required for Railway / Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
