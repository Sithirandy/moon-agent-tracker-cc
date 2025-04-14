from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory agent storage
agents = {}

@app.route("/agent", methods=["POST"])
def add_agent():
    data = request.get_json()
    agent_code = data.get("agent_code")
    if agent_code in agents:
        return jsonify({"message": "Agent already exists."}), 409
    agents[agent_code] = data
    return jsonify({"message": "Agent added successfully."}), 201

@app.route("/agent/<agent_code>", methods=["GET"])
def get_agent(agent_code):
    agent = agents.get(agent_code)
    if not agent:
        return jsonify({"message": "Agent not found."}), 404
    return jsonify(agent), 200

@app.route("/agent/<agent_code>", methods=["PUT"])
def update_agent(agent_code):
    if agent_code not in agents:
        return jsonify({"message": "Agent not found."}), 404
    data = request.get_json()
    agents[agent_code].update(data)
    return jsonify({"message": "Agent updated."}), 200

@app.route("/agents", methods=["GET"])
def list_agents():
    return jsonify(list(agents.values())), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)