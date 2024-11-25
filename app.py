from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
# module2 Imports
from firewall_allow_all_necessary_ports.allow_all_deny_port_1 import manage_ports,list_deny_ports,allow_all_ports,deny_port  # Import allow_port
from firewall_allow_all_necessary_ports.app_list import list_apps_module2_fourth,allow_app_module2_fourth  # Import allow_port
from firewall_allow_all_necessary_ports.show_all_ports import show_all_module2_eight
from firewall_allow_all_necessary_ports.allow_1 import allow_port  # Import allow_port
# modeule3 Imports
from firewall_blocking_ip.block_range_of_ip_address import block_module3_first
from firewall_blocking_ip.block_specific_ip import block_module3_second

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


#module 2 fourth
@app.route('/api/apps', methods=['GET'])
def get_apps_module2_fourth():
    apps = list_apps_module2_fourth()
    if apps is None:
        return jsonify({"error": "Failed to fetch application list"}), 500
    return jsonify({"apps": apps})

# Endpoint to allow an application
@app.route('/api/allow-app', methods=['POST'])
def allow_application_module2_fourth():
    data = request.get_json()
    app_name = data.get("app")
    if not app_name:
        return jsonify({"error": "Application name is required"}), 400

    result = allow_app_module2_fourth(app_name)
    if result is None:
        return jsonify({"error": f"Failed to allow application '{app_name}'"}), 500
    return jsonify({"message": f"Application '{app_name}' allowed successfully."})

#module2 eight
@app.route('/api/show-all', methods=['GET'])
def get_firewall_status():
    rules = show_all_module2_eight()
    if rules is None:
        return jsonify({"error": "Failed to fetch firewall status"}), 500
    return jsonify({"rules": rules})

@app.route('/api/block-ip', methods=['POST'])
def block_ip():
    data = request.json
    ip = data.get('ip')
    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    result = block_module3_first(ip)
    if result:
        return jsonify({"message": f"IP {ip} blocked successfully", "result": result}), 200
    else:
        return jsonify({"error": f"Failed to block IP {ip}"}), 500


@app.route('/api/block-ip-single', methods=['POST'])
def block_ip_single():
    data = request.json
    ip = data.get('ip')
    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    result = block_module3_second(ip)
    if result:
        return jsonify({"message": f"IP {ip} blocked successfully", "result": result}), 200
    else:
        return jsonify({"error": f"Failed to block IP {ip}"}), 500


if __name__ == "__main__":
    app.run()
