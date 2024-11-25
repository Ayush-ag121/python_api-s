#Allow Incoming Traffic from a Specific IP Address

import subprocess
import re

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def allow_ip_module8_second(ip):
    command = f"sudo ufw allow from {ip}"
    execute_command(command)

ip = input("Enter the IP address: ")
allow_ip_module8_second(ip)