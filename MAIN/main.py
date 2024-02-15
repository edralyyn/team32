import tkinter as tk
from tkinter import messagebox, Toplevel
import subprocess
import tensorflow as tf
import numpy as np
import os
import predict
#add
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
        try:
            num_days_input = int(input("Enter the number of days for prediction: "))
            predicted_event = predict.get_predicted_event(num_days_input)
            show_forecasting_information(predicted_event, None, num_days_input)
        except Exception as e:
            show_forecasting_information(None, f"Error during forecasting: {e}", None)

def show_forecasting_information(output, error_output, num_days_input):
    forecasting_window = tk.Toplevel()
    forecasting_window.title("Forecasting Information")
    forecasting_window.configure(bg='#238BD6')
    forecasting_label = tk.Label(forecasting_window, text="Forecasting information:", bg='#238BD6', fg='black')
    forecasting_label.pack(pady=10)
    forecasting_text = tk.Text(forecasting_window, fg='black')
    if output is not None:
        forecasting_text.insert(tk.END, f"\nThe predicted Event ID after {num_days_input} days is: {output}")
    elif error_output is not None:
        forecasting_text.insert(tk.END, f"{error_output}")
    forecasting_text.pack(padx=10, pady=10)

def customize_gui(background_color, window_size):
    root = tk.Tk()
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
