import subprocess

# Define the paths to your Python scripts
first_script_path = "scanip.py"
second_script_path = "converter.py"

# Run the first Python script
subprocess.run(["python3", first_script_path])

# Once the first script has finished running, run the second Python script
subprocess.run(["python3", second_script_path])