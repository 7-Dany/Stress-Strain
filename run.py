import subprocess
import threading
import os

def run_send_data_script():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    python_interpreter = os.path.join(current_dir, '.venv', 'Scripts', 'python')
    send_data_script = os.path.join(current_dir, 'send_data.py')
    subprocess.run([python_interpreter, send_data_script], check=True)

def run_app_program():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    python_interpreter = os.path.join(current_dir, '.venv', 'Scripts', 'python')
    send_data_script = os.path.join(current_dir, 'app.py')
    subprocess.run([python_interpreter, send_data_script], check=True)

# Create threads for each process
python_thread = threading.Thread(target=run_send_data_script)
app_program_thread = threading.Thread(target=run_app_program)

# Start threads
python_thread.start()
app_program_thread.start()

# Wait for both threads to complete
python_thread.join()
app_program_thread.join()
