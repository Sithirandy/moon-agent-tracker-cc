from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='moon-agent-db-new.c90ec204g7j0.ap-south-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password='sIfJVbLwcPieJmyspfgI',
        database='moonagentdb'
    )
    return connection

@app.route("/")
def health_check():
    return "Agent Service is up and running!", 200

@app.route('/agent', methods=['POST'])
def add_agent():
    data = request.get_json()
    agent_code = data.get("agent_code")
    name = data.get('name')
    branch = data.get('branch')

    if not agent_code or not name or not branch:
        return jsonify({"error": "All fields are required"}), 409

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO agent (agent_code, name, branch)
            VALUES (%s, %s, %s)
        """, (agent_code, name, branch))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Agent created successfully"}), 201


@app.route('/agent/<agent_code>', methods=['GET'])
def get_agent(agent_code):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT agent_code, name, branch FROM agent WHERE agent_code = %s", (agent_code,))
        agent = cursor.fetchone()
        cursor.close()
        connection.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if agent:
        return jsonify({
            "agent_code": agent[0],
            "name": agent[1],
            "branch": agent[2]
        }), 200
    else:
        return jsonify({"error": "Agent not found"}), 404


@app.route('/agent/<agent_code>', methods=['PUT'])
def update_agent(agent_code):
    data = request.get_json()
    name = data.get('name')
    branch = data.get('branch')

    if not name or not branch:
        return jsonify({"error": "Name and Branch are required"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE agent
            SET name = %s, branch = %s
            WHERE agent_code = %s
        """, (name, branch, agent_code))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Agent updated successfully"}), 200


@app.route('/agent', methods=['DELETE'])
def delete_agent():
    agent_code = request.args.get('agent_code')
    if not agent_code:
        return jsonify({"error": "Agent code parameter is required"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM agent WHERE agent_code = %s", (agent_code,))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Agent deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)