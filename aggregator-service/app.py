from flask import Flask, jsonify

app = Flask(__name__)

# Simulated data
sales_data = [
    {"agent_code": "A101", "product": "Life", "branch": "Colombo"},
    {"agent_code": "A102", "product": "Term", "branch": "Kandy"},
    {"agent_code": "A101", "product": "Life", "branch": "Colombo"},
    {"agent_code": "A103", "product": "Term", "branch": "Colombo"}
]

@app.route("/aggregate", methods=["GET"])
def aggregate():
    product_counts = {}
    branch_counts = {}

    for sale in sales_data:
        product = sale["product"]
        branch = sale["branch"]

        product_counts[product] = product_counts.get(product, 0) + 1
        branch_counts[branch] = branch_counts.get(branch, 0) + 1

    return jsonify({
        "top_products": product_counts,
        "branch_performance": branch_counts
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)