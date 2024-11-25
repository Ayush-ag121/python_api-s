#Deny Incoming Traffic to Specific Port from a Specific IP Address

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

def deny_ip_module6_sixth(number, ip):
    command = f"sudo ufw deny from {ip} to any port {number}"
    execute_command(command)


number = input("Enter Port Number: ")
ip = input("Enter the IP address: ")
deny_ip_module6_sixth(number,ip)