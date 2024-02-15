import tkinter as tk
from tkinter import messagebox, Toplevel
import subprocess
import numpy as np
import os
import predict
import tkinter.simpledialog as simpledialog

def set_icon(window):
    icon_filename = "icon.ico"
    icon_path = os.path.join(os.getcwd(), icon_filename)
    window.iconbitmap(icon_path)

def custom_askinteger(title, prompt):
    while True:
        dialog_window = tk.Toplevel()
        set_icon(dialog_window)
        dialog_window.title(title)
        label = tk.Label(dialog_window, text=prompt)
        label.pack(padx=10, pady=5)
        entry_var = tk.StringVar()
        entry = tk.Entry(dialog_window, textvariable=entry_var)
        entry.pack(padx=10, pady=5)
        ok_button = tk.Button(dialog_window, text="Predict", command=lambda: dialog_window.destroy())
        ok_button.pack(pady=5)
        dialog_window.wait_window()
        result = None
        try:
            result = int(entry_var.get())
            break  # Break the loop if a valid integer is entered
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
    return result

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
            num_days_input = custom_askinteger("Desired Days", "Enter the number of days for prediction:")
            for file_name, df in predict.dataframes:
                predicted_pid = predict.predict_pid(df, num_days_input)
                predict.predictions[file_name] = predicted_pid

            show_forecasting_information(predict.predictions, None, num_days_input)
        except Exception as e:
            show_forecasting_information(None, f"Error during forecasting: {e}", None)

def show_forecasting_information(predictions, error_output, num_days_input):
    forecasting_window = tk.Toplevel()
    set_icon(forecasting_window)
    forecasting_window.title("Forecasting Information")
    forecasting_window.configure(bg='#238BD6')
    forecasting_label = tk.Label(forecasting_window, text="Forecasting information:", bg='#238BD6', fg='black')
    forecasting_label.pack(pady=10)
    forecasting_text = tk.Text(forecasting_window, fg='black')

    output = "\n".join([f"The predicted pid after {num_days_input} days for {file_name} is: {predicted_pid}" 
                        for file_name, predicted_pid in predictions.items()])
    
    forecasting_text.insert(tk.END, output)
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
