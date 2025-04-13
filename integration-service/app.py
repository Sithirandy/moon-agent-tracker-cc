from flask import Flask, request, jsonify

app = Flask(__name__)
sales_data = []

@app.route('/sales', methods=['POST'])
def receive_sales():
    data = request.get_json()
    sales_data.append(data)
    return jsonify({"message": "Sales data received"}), 200

@app.route('/sales', methods=['GET'])
def list_sales():
    return jsonify(sales_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')