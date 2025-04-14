from flask import Flask, request, jsonify

app = Flask(__name__)

sales_db = []

@app.route("/sales", methods=["POST"])
def record_sale():
    data = request.get_json()
    sales_db.append(data)
    return jsonify({"message": "Sale recorded successfully!"}), 200

@app.route("/sales", methods=["GET"])
def get_sales():
    return jsonify(sales_db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)