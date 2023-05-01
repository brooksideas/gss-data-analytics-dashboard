import time
import subprocess

# Start the server
server_process = subprocess.Popen(['python3', 'gss.py'])

# Wait for 10 seconds
time.sleep(100)

# Stop the server
server_process.terminate()
