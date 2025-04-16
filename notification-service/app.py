from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

DB_HOST = "moon-agent-db-new.c90ec204g7j0.ap-south-1.rds.amazonaws.com"
DB_PORT = 3306
DB_NAME = "moonagentdb"
DB_USERNAME = "admin"
DB_PASSWORD = "sIfJVbLwcPieJmyspfgI"

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    print("Home route hit")
    return "Welcome to the Notification Service!"

@app.route('/target-reminder', methods=['POST'])
def send_target_reminder():
    data = request.get_json()
    print(f"Received target reminder request: {data}")
    agent_code = data.get("agent_code")
    target_sales = data.get("target_sales")

    connection = create_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT name, email FROM agent WHERE agent_code = %s"
        cursor.execute(query, (agent_code,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Agent not found"}), 404

        agent_name = result["name"]
        email = result["email"]

        # Mock notification logic
        print(f"Sending reminder to {agent_name} ({email}) about target: {target_sales}")

        return jsonify({"message": f"Reminder sent to {agent_name} ({email})"}), 200

    except mysql.connector.Error as e:
        print(f"Query error: {e}")
        return jsonify({"error": "Database query failed"}), 500

    finally:
        if connection.is_connected():
            connection.close()

@app.route('/notify-corporate', methods=['POST'])
def notify_corporate_target_achieved():
    data = request.get_json()
    agent_code = data.get("agent_code")

    connection = create_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to database"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Fetch agent details
        cursor.execute("SELECT name, email, target FROM agent WHERE agent_code = %s", (agent_code,))
        agent = cursor.fetchone()

        if not agent:
            return jsonify({"error": "Agent not found"}), 404

        agent_name = agent["name"]
        email = agent["email"]
        target = float(agent["target"])

        # Calculate total sales
        cursor.execute("SELECT SUM(sale_amount) AS total_sales FROM sales WHERE agent_code = %s", (agent_code,))
        result = cursor.fetchone()
        total_sales = result["total_sales"] or 0.0

        print(f"{agent_name} - Total Sales: {total_sales}, Target: {target}")

        if total_sales >= target:
            # Mock corporate notification logic
            print(f"🎯 Agent {agent_name} ({email}) has achieved their target of {target}. Notifying corporate...")
            return jsonify({
                "message": f"Corporate notified: {agent_name} has achieved their sales target of {target}."
            }), 200
        else:
            return jsonify({
                "message": f"{agent_name} has not yet achieved the target. Total sales: {total_sales}."
            }), 200

    except mysql.connector.Error as e:
        print(f"Query error: {e}")
        return jsonify({"error": "Database query failed"}), 500

    finally:
        if connection.is_connected():
            connection.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)