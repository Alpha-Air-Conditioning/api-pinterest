@app.route('/pin', methods=['GET'])
def pin():
    url = request.args.get('msg')

    if not url:
        return jsonify({"error": "Missing 'msg' parameter"}), 400

    try:
        full_url = expand_url(url)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.post(
            "https://download.pinload.app/parse",
            json={"url": full_url},
            headers=headers,
            timeout=10
        )

        data = res.json()

        if not data.get("success"):
            return jsonify({
                "error": "Could not extract media",
                "original_response": data
            }), 400

        result = data.get("data", {})

        # 🔥 YOUR CUSTOM OUTPUT
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
        return jsonify({"error": str(e)}), 500
