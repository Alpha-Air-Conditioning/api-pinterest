from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/pin', methods=['GET'])
def get_pin_data():
    pin_url = request.args.get('msg')

    if not pin_url:
        return jsonify({
            "success": False,
            "error": "Missing 'msg' query parameter"
        }), 400

    try:
        response = requests.post(
            "https://download.pinload.app/parse",
            json={"url": pin_url},
            timeout=10
        )

        data = response.json()

        # Clean response (optional)
        return jsonify({
            "success": True,
            "type": data.get("data", {}).get("type"),
            "url": data.get("data", {}).get("url"),
            "title": data.get("data", {}).get("title")
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": "Request failed",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
