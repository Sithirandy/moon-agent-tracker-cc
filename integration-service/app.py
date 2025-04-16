import os
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
DB_HOST = "moon-agent-db-new.c90ec204g7j0.ap-south-1.rds.amazonaws.com"
DB_PORT = 3306
DB_NAME = "moonagentdb"
DB_USERNAME = "admin"
DB_PASSWORD = "sIfJVbLwcPieJmyspfgI"

# Health check route
@app.route("/", methods=["GET"])
def health_check():
    return "Integration Service is up and running!", 200

# Sales endpoint
@app.route('/sales', methods=['POST'])
def create_sale():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    required_fields = ['agent_code', 'product_id', 'sale_amount']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()
        query = """
            INSERT INTO sales (agent_code, product_id, sale_amount)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            data['agent_code'],
            data['product_id'],
            data['sale_amount']
        ))
        connection.commit()

        return jsonify({"message": "Sale recorded successfully!"}), 201

    except Error as db_error:
        print(f"Database Error: {db_error}")
        return jsonify({"error": str(db_error)}), 500

    except Exception as ex:
        print(f"Unexpected Error: {ex}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)