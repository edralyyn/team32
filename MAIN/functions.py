import subprocess
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QPushButton, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QDialog
import os
import predict
import pandas as pd
from PyQt5.QtCore import Qt

class CustomDialog(QDialog):
    @staticmethod
    def ask_integer(title, prompt):
        result = [None]

        def on_ok():
            if entry.text():
                try:
                    result[0] = int(entry.text())
                    dialog_window.accept()
                except ValueError:
                    QMessageBox.critical(None, "Invalid Input", "Please enter a valid integer.")
                    dialog_window.show()

        def on_cancel():
            result[0] = None
            dialog_window.reject()

        dialog_window = QDialog()
        dialog_window.setWindowTitle(title)
        label = QLabel(prompt)
        entry = QLineEdit()
        entry.returnPressed.connect(on_ok)

        button_layout = QVBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(entry)

        message_label = QLabel()
        button_layout.addWidget(message_label)

        button_row_layout = QHBoxLayout()
        ok_button = QPushButton("Predict")
        ok_button.clicked.connect(on_ok)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(on_cancel)

        button_row_layout.addWidget(ok_button)
        button_row_layout.addWidget(cancel_button)

        button_layout.addLayout(button_row_layout)

        dialog_window.setLayout(button_layout)

        if dialog_window.exec_():
            return result[0]

def collect_data(canvas1):
    result = QMessageBox.question(None, "Warning", "This will collect data. Do you want to proceed?", QMessageBox.Yes | QMessageBox.No)
    if result == QMessageBox.Yes:
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            output = subprocess.run(["python3", "scanip.py"], capture_output=True, text=True)
            if output.returncode == 0:
                topology_table_lines = output.stdout.splitlines()
                start_index = topology_table_lines.index("Topology Table:") + 1
                topology_table_text = "\n".join(topology_table_lines[start_index:])
                canvas1.setText("Topology Table:\n" + topology_table_text)
            else:
                canvas1.clear()
                canvas1.setText(f"Error running scanip.py: {output.stderr}")
        except FileNotFoundError:
            canvas1.clear()
            canvas1.setText("Error: scanip.py not found.")
            
        finally:
            QApplication.restoreOverrideCursor()

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

def forecast(canvas3):
    result = QMessageBox.question(None, "Warning", "This will run forecasting. Do you want to proceed?", QMessageBox.Yes | QMessageBox.No)
    if result == QMessageBox.Yes:
        num_days_input = CustomDialog.ask_integer("Desired Days", "Enter the number of days for prediction:")
        if num_days_input is not None:
            try:
                QApplication.setOverrideCursor(Qt.WaitCursor)

                if not predict.dataframes:
                    QMessageBox.information(None, "No Devices Found", "There are no devices found. Unable to perform forecasting.")
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
                        predictions_to_show_intermediary = None
                        error_output = f"Error during forecasting: {e}"
                        show_forecasting_information(predictions_to_show, predictions_to_show_intermediary, error_output, num_days_input, canvas3)
                        return

                show_forecasting_information(predictions_to_show, predictions_to_show_intermediary, None, num_days_input, canvas3)

            except Exception as e:
                show_forecasting_information(None, None, f"Error during forecasting: {e}", None, canvas3)
            finally:
                QApplication.restoreOverrideCursor()

def show_forecasting_information(predictions, predictions_intermediary, error_output, num_days_input, canvas3):
    forecasting_text = ""

    if predictions or predictions_intermediary:
        if predictions:
            output = "\n".join([f"The predicted pid after {num_days_input} days for {file_name} is: {predicted_pid}"
                                for file_name, predicted_pid in predictions.items()])
            forecasting_text += "Predictions for END DEVICES:\n" + output + "\n\n"

        if predictions_intermediary:
            output = "\n".join([f"The predicted pid after {num_days_input} days for {file_name} is: {predicted_pid}"
                                for file_name, predicted_pid in predictions_intermediary.items()])
            forecasting_text += "Predictions for INTERMEDIARY DEVICES:\n" + output + "\n\n"
    else:
        if error_output:
            forecasting_text += error_output
        else:
            forecasting_text += "No forecasting information available for one or more directories."

    canvas3.setText(forecasting_text)

