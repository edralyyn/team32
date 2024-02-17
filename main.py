import tkinter as tk
from tkinter import messagebox, Toplevel
import subprocess
import numpy as np
import pandas as pd
import os
import predict
import tkinter.simpledialog as simpledialog
import platform

def set_icon(window):
    icon_filename = "icon.ico"
    icon_path = os.path.join(os.getcwd(), icon_filename)
    if platform.system() == "Windows":
        # Use ICO file directly on Windows
        window.iconbitmap(icon_path)
    elif platform.system() == "Linux":
        # Convert ICO to BMP and use BMP file on Linux
        try:
            subprocess.run(["convert", icon_path, icon_path.replace(".ico", ".bmp")])
            window.iconbitmap(icon_path.replace(".ico", ".bmp"))
        except Exception as e:
            print(f"Error converting icon file: {e}")

def custom_askinteger(title, prompt):
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
    set_icon(dialog_window)
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


def on_collect_click(information_text):
    result = messagebox.askyesno("Warning", "This will collect data. Do you want to proceed?")
    if result:
        try:
            output = subprocess.check_output(["python3", "combo.py"], text=True)
            information_text.insert(tk.END, f"collect clicked. Collecting data...\n{output}\n")
        except subprocess.CalledProcessError as e:
            information_text.insert(tk.END, f"Error running scanip.py: {e}\n")

def on_forecast_click():
    result = messagebox.askyesno("Warning", "This will run forecasting. Do you want to proceed?")
    if result:
        num_days_input = custom_askinteger("Desired Days", "Enter the number of days for prediction:")
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
    set_icon(forecasting_window)
    forecasting_window.title("Forecasting Information")
    forecasting_window.configure(bg='#238BD6')
    forecasting_label = tk.Label(forecasting_window, text="Forecasting information:", bg='#238BD6', fg='black')
    forecasting_label.pack(pady=10)
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

def customize_gui(background_color, window_size):
    root = tk.Tk()
    set_icon(root)
    root.title("Predictive Maintenance System")
    root.configure(bg=background_color)
    root.geometry(window_size)

    button_style = {
        "bg": '#0F6BAE',
        "fg": 'white',
        "font": ('Helvetica'),
        "width": 15,
        "height": 1,
        "relief": tk.FLAT,
    }

    center_frame = tk.Frame(root, bg=background_color)
    center_frame.pack(side=tk.LEFT, padx=30, pady=(root.winfo_reqheight() // 0.8), fill=tk.Y)

    collect = tk.Button(center_frame, text="Collect", command=lambda: on_collect_click(information_text), **button_style)
    collect.pack(pady=10, fill=tk.X)

    forecast = tk.Button(center_frame, text="Forecast", command=on_forecast_click, **button_style)
    forecast.pack(pady=10, fill=tk.X)

    information_text = tk.Text(root, height=35, width=90, wrap=tk.WORD)
    information_text.pack(side=tk.RIGHT, padx=40, pady=10)

    root.mainloop()

custom_background_color = '#238BD6'
custom_window_size = "1000x600"

customize_gui(custom_background_color, custom_window_size)
