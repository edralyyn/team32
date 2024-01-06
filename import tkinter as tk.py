import tkinter as tk
from tkinter import messagebox

def on_collect_click():
    confirmation = messagebox.askyesno("Confirmation", "Do you want to proceed with data collection?")
    if confirmation:
        result_label.config(text="Data collected!")
        show_information("data_collection")

def on_forecast_click():
    confirmation = messagebox.askyesno("Confirmation", "Do you want to proceed with forecasting?")
    if confirmation:
        result_label.config(text="Forecasting...")
        show_forecasting_information()

def show_information(data_type):
    information_text.delete("1.0", tk.END)  # Clear previous content

    if data_type == "data_collection":
        information_text.insert(tk.END, "Data collected information:")
    else:
        information_text.insert(tk.END, "Unknown information type.")

def show_forecasting_information():
    # Create a new window for forecasting information
    forecasting_window = tk.Toplevel(root)
    forecasting_window.title("Forecasting Information")

    # Create and add widgets to the forecasting window
    forecasting_label = tk.Label(forecasting_window, text="Forecasting information:")
    forecasting_label.pack(pady=10)

    forecasting_text = tk.Text(forecasting_window, height=10, width=50)
    forecasting_text.insert(tk.END, "Forecasted Output")
    forecasting_text.pack(padx=10, pady=10)

# Create the main window
root = tk.Tk()
root.title("Predictive Maintenance System")
root.geometry("1000x500")

# Create and add widgets
label = tk.Label(root, text="Choose an action:")
label.grid(row=0, column=0, pady=10)
label.place(relx=0.10, rely=0.4, anchor=tk.CENTER)   

# Create a frame for the buttons (one column, two rows)
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

# Apply the same padding for both x and y
button_padding = 5

collect_button = tk.Button(button_frame, text="Collect", command=on_collect_click)
collect_button.grid(row=0, column=0, padx=button_padding, pady=button_padding)

forecast_button = tk.Button(button_frame, text="Forecast", command=on_forecast_click)
forecast_button.grid(row=1, column=0, padx=button_padding, pady=button_padding)

result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, pady=10)
result_label.place(relx=0.10, rely=0.3, anchor=tk.CENTER)

# Center the frame with buttons using pack
button_frame.pack_propagate(False)
button_frame.place(relx=0.10, rely=0.5, anchor=tk.CENTER)

# Create a Text widget for information
information_text = tk.Text(root, height=10, width=40)
information_text.grid(row=1, column=1, padx=10, pady=10)
information_text.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

# Run the main loop
root.mainloop()
