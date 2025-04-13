from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    recipient = data.get("email")
    message = data.get("message")
    # Simulate notification
    print(f"Notification sent to {recipient}: {message}")
    return jsonify({"message": "Notification sent"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')