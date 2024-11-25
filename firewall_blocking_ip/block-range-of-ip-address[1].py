import subprocess
# module 3
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None
    
def block_module3_first(ip):
    command = f"sudo ufw deny from {ip}"
    execute_command(command)

ip = input("Enter Range of IP Address: ")
block_module3_first(ip)