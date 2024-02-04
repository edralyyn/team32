import subprocess

first_script_path = "scanip.py"
second_script_path = "converter.py"
subprocess.run(["python3", first_script_path])
subprocess.run(["python3", second_script_path])