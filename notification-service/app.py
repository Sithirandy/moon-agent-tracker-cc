from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Health check route
@app.route("/", methods=["GET"])
def health_check():
    return "Notification Service is up and running!", 200

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    message = data.get("message", "No message provided")
    print(f"🔔 Notification: {message}")
    return jsonify({"status": "Notification sent"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)