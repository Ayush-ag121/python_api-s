import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None
    
output = execute_command("sudo ufw app list")
print(output)
app = input("Enter Application name: ")
output1 = execute_command(f"sudo ufw allow {app}")
print(output1)