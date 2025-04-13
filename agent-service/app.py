from flask import Flask, request, jsonify

app = Flask(__name__)

agents = {}

@app.route('/agents', methods=['POST'])
def add_agent():
    data = request.get_json()
    agent_id = data.get('agent_code')
    agents[agent_id] = data
    return jsonify({"message": "Agent added successfully"}), 201

@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    agent = agents.get(agent_id)
    if agent:
        return jsonify(agent)
    return jsonify({"error": "Agent not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')