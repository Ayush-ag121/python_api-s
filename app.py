from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from firewall_allow_all_necessary_ports.allow_all_deny_port_1 import manage_ports,list_deny_ports,allow_all_ports,deny_port  # Import allow_port
from firewall_allow_all_necessary_ports.allow_all_ports import list_deny_ports_third,allow_all_third  # Import allow_port

from firewall_allow_all_necessary_ports.allow_1 import allow_port  # Import allow_port
# from module2.file import block_ip  # Import block_ip from module2
import subprocess

app = Flask(__name__)
CORS(app)  # Apply CORS to your app

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None


# module 2
@app.route('/api/allow-port', methods=['POST'])
def allow_port_route():
    # Get the port number from the JSON request
    data = request.get_json()
    if 'port' not in data:
        return jsonify({"error": "Port is required"}), 400
    
    port = data['port']
    print(port)
    # Try to allow the port
    result = allow_port(port)
    print(result)
    if result:
        return jsonify({"message": f"Port {port} allowed successfully", "output": result}), 200
    else:
        return jsonify({"error": "Failed to allow port"}), 500


@app.route('/api/list-deny-ports', methods=['GET'])
def list_deny_ports1():
    ports = list_deny_ports()
    return jsonify({"deny_ports": ports}), 200

@app.route('/api/allow-all-ports', methods=['POST'])
def allow_all_ports1():
    allow_all_ports()
    return jsonify({"message": "All ports allowed successfully"}), 200

@app.route('/api/deny-port', methods=['POST'])
def deny_port1():
    data = request.get_json()
    if 'port' not in data:
        return jsonify({"error": "Port is required"}), 400

    port = data['port']
    deny_port(port)
    return jsonify({"message": f"Port {port} denied successfully"}), 200

@app.route('/api/manage-ports', methods=['POST'])
def manage_ports1():
    data = request.get_json()
    if 'port_to_disable' not in data:
        return jsonify({"error": "Port to disable is required"}), 400

    port_to_disable = data['port_to_disable']
    manage_ports(port_to_disable)
    return jsonify({"message": f"Port {port_to_disable} managed successfully"}), 200

# Endpoint to list all denied ports
@app.route('/api/denied-ports', methods=['GET'])
def get_denied_ports():
    denied_ports = list_deny_ports_third()
    if isinstance(denied_ports, str):  # Check if an error message was returned
        return jsonify({"error": denied_ports}), 500
    return jsonify({"denied_ports": denied_ports})

# Endpoint to allow all denied ports
# @app.route('/api/allow-all', methods=['POST'])
# def allow_all_ports():
#     result = allow_all_third()
#     if isinstance(result, str) and result.startswith("No denied ports"):
#         return jsonify({"message": result}), 400
#     return jsonify({"message": result})



if __name__ == "__main__":
    app.run()
