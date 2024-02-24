import tkinter as tk
from tkinter import messagebox, Toplevel
import subprocess
import numpy as np
import pandas as pd
import os
import predict

class CustomDialog:
    @staticmethod
    def ask_integer(title, prompt):
        result = [None]

        def on_ok(event=None):
            if entry_var.get():
                try:
                    result[0] = int(entry_var.get())
                    dialog_window.destroy()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid integer.")
                    dialog_window.lift()

        def on_cancel():
            result[0] = None
            dialog_window.destroy()

        dialog_window = tk.Toplevel()
        dialog_window.title(title)
        label = tk.Label(dialog_window, text=prompt)
        label.pack(padx=10, pady=5)
        entry_var = tk.StringVar()
        entry = tk.Entry(dialog_window, textvariable=entry_var)
        entry.pack(padx=10, pady=5)
        entry.bind("<Return>", on_ok)

        entry.focus_set()

        button_frame = tk.Frame(dialog_window)
        button_frame.pack(pady=5)
        ok_button = tk.Button(button_frame, text="Predict", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)
        cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

        dialog_window.wait_window()

        if result[0] is not None:
            return result[0]

def collect_data(canvas):
    result = messagebox.askyesno("Warning", "This will collect data. Do you want to proceed?")
    if result:
        try:
            output = subprocess.run(["python3", "scanip.py"], capture_output=True, text=True)
            if output.returncode == 0:
                # Process the output to extract the topology table
                topology_table_lines = output.stdout.splitlines()
                start_index = topology_table_lines.index("Topology Table:") + 1
                topology_table_text = "\n".join(topology_table_lines[start_index:])

                # Clear any previous content on the canvas
                canvas.delete("all")

                # Insert the topology table text into the canvas
                canvas.create_text(10, 10, anchor="nw", text="Topology Table:", fill="black")
                canvas.create_text(10, 30, anchor="nw", text=topology_table_text, fill="black")
            else:
                # Clear any previous content on the canvas
                canvas.delete("all")
                # Insert error message into the canvas
                canvas.create_text(10, 10, anchor="nw", text=f"Error running scanip.py: {output.stderr}", fill="red")
        except FileNotFoundError:
            # Clear any previous content on the canvas
            canvas.delete("all")
            # Insert error message into the canvas
            canvas.create_text(10, 10, anchor="nw", text="Error: scanip.py not found.", fill="red")

def forecast():
    result = messagebox.askyesno("Warning", "This will run forecasting. Do you want to proceed?")
    if result:
        num_days_input = CustomDialog.ask_integer("Desired Days", "Enter the number of days for prediction:")
        if num_days_input is not None:
            try:
                if not predict.dataframes:
                    messagebox.showinfo("No Devices Found", "There are no devices found. Unable to perform forecasting.")
                    return

                predictions_to_show = {}
                predictions_to_show_intermediary = {}

                for directory in predict.directories:
                    try:
                        for filename in os.listdir(directory):
                            if filename.endswith('.csv'):
                                file_path = os.path.join(directory, filename)
                                file_name = os.path.splitext(filename)[0]
                                directory_name = os.path.basename(directory)
                                df = pd.read_csv(file_path, usecols=[0, 1, 2, 3, 4]).rename(columns=lambda x: x.strip())
                                predict.predictions[file_name] = (directory_name, df)

                        end_devices_predictions = {k: v for k, v in predict.predictions.items() if "END DEVICES" in v[0]}
                        intermediary_devices_predictions = {k: v for k, v in predict.predictions.items() if "INTERMEDIARY DEVICES" in v[0]}

                        for file_name, (directory_name, df) in end_devices_predictions.items():
                            predicted_pid = predict.predict_pid(df, num_days_input)
                            predictions_to_show[file_name] = predicted_pid

                        for file_name, (directory_name, df) in intermediary_devices_predictions.items():
                            predicted_pid = predict.predict_pid(df, num_days_input)
                            predictions_to_show_intermediary[file_name] = predicted_pid

                    except FileNotFoundError as e:
                        # Handle the case where a directory is missing
                        predictions_to_show_intermediary = None
                        error_output = f"Error during forecasting: {e}"
                        show_forecasting_information(predictions_to_show, predictions_to_show_intermediary, error_output, num_days_input)
                        return

                show_forecasting_information(predictions_to_show, predictions_to_show_intermediary, None, num_days_input)

            except Exception as e:
                show_forecasting_information(None, None, f"Error during forecasting: {e}", None)

def show_forecasting_information(predictions, predictions_intermediary, error_output, num_days_input):
    forecasting_window = tk.Toplevel()
    forecasting_window.title("Forecasting Information")
    forecasting_window.configure(bg='#88a5cd')
    forecasting_text = tk.Text(forecasting_window, fg='black')

    if predictions or predictions_intermediary:
        if predictions:
            output = "\n".join([f"The predicted pid after {num_days_input} days for {file_name} is: {predicted_pid}"
                                for file_name, predicted_pid in predictions.items()])
            forecasting_text.insert(tk.END, "Predictions for END DEVICES:\n" + output + "\n\n")

        if predictions_intermediary:
            output = "\n".join([f"The predicted pid after {num_days_input} days for {file_name} is: {predicted_pid}"
                                for file_name, predicted_pid in predictions_intermediary.items()])
            forecasting_text.insert(tk.END, "Predictions for INTERMEDIARY DEVICES:\n" + output + "\n\n")
    else:
        # Check if there was an error accessing the directories
        if error_output:
            forecasting_text.insert(tk.END, error_output)
        else:
            # If no error, assume one directory is missing and inform the user
            forecasting_text.insert(tk.END, "No forecasting information available for one or more directories.")

    forecasting_text.pack(padx=10, pady=10)
