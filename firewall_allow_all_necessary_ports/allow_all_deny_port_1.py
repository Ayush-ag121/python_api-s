import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def list_deny_ports():
    command = "sudo ufw status numbered"
    output = execute_command(command)
    if output:
        return [line.split()[2] for line in output.splitlines() if 'DENY' in line]
    return []


def allow_all_ports():
    deny_ports = list_deny_ports()
    for port in deny_ports:
        print(f"Allowing port {port}")
        command = f"sudo ufw allow {port}"
        execute_command(command)
        
def deny_port(port):
    print(f"Blocking port {port}")
    command = f"sudo ufw deny {port}"
    execute_command(command)

def manage_ports(port_to_disable):
    allow_all_ports()
    deny_port(port_to_disable)
