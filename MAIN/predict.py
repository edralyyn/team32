import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import load_model

new_data = pd.DataFrame()

directories = ["SYSLOG/END DEVICES", "SYSLOG/INTERMEDIARY DEVICES"]
dataframes = []

for directory in directories:
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                file_name = os.path.splitext(filename)[0]
                variable_name = f"{file_name.replace('.', '_')}"
                df = pd.read_csv(file_path, usecols=[0, 1, 2, 3, 4]).rename(columns=lambda x: x.strip())
                dataframes.append((file_name, df))

        new_data = pd.concat([df for _, df in dataframes])

    except FileNotFoundError:
        print(f"Directory '{directory}' not found. Skipping...")

def preprocess_data(sequence_length=20):  
    if 'Date and Time' in new_data.columns:
        new_data['Date and Time'] = pd.to_datetime(new_data['Date and Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    if 'pid' in new_data.columns:
        new_data['pid_encoded'] = LabelEncoder().fit_transform(new_data['pid'])
        new_X, new_y = [], []
        for i in range(len(new_data) - sequence_length):
            new_X.append(new_data['pid_encoded'].values[i:i+sequence_length])
            new_y.append(new_data['pid_encoded'].values[i+sequence_length])
        new_X = np.array(new_X)
        new_y = np.array(new_y)
        num_classes = len(np.unique(new_data['pid_encoded']))
        new_y_one_hot = to_categorical(new_y, num_classes=num_classes)
        new_X = new_X.reshape((new_X.shape[0], sequence_length, 1))
        new_X = new_X.reshape((-1, sequence_length, 1))

    return new_data, new_X, num_classes

def predict_event(model, new_data, sequence_length, num_days):
    new_sequence = new_data['Event_encoded'].values[-sequence_length:]

    for i in range(num_days):
        new_sequence = np.append(new_sequence, 0)

    new_sequence = new_sequence[-sequence_length:]
    new_sequence = new_sequence.reshape(1, sequence_length, 1)

    predicted_probs = model.predict(new_sequence)
    predicted_label = np.argmax(predicted_probs)

    predicted_event_id = new_data['pid'].unique()[predicted_label]

    return predicted_event_id

saved_model_path = "PD1-1(v2).h5"
loaded_model = load_model(saved_model_path)

def get_predicted_event(num_days_input):
    sequence_length = 20
    model_path = os.path.join(os.getcwd(), saved_model_path)
    model = load_model(model_path)
    
    new_data, new_X, num_classes = preprocess_data(sequence_length)
    
    predicted_event = predict_event(model, new_data, sequence_length, num_days_input)
    
    return predicted_event

def predict_pid(dataframe, num_days):
    sequence_length = 20
    if 'pid_encoded' not in dataframe.columns:
        dataframe['pid_encoded'] = LabelEncoder().fit_transform(dataframe['pid'])

    new_sequence = dataframe['pid_encoded'].values[-sequence_length:]

    for i in range(num_days):
        new_sequence = np.append(new_sequence, 0)

    new_sequence = new_sequence[-sequence_length:]
    new_sequence = new_sequence.reshape(1, sequence_length, 1)

    predicted_probs = loaded_model.predict(new_sequence)
    predicted_label = np.argmax(predicted_probs)
    predicted_pid = dataframe['pid'].unique()[predicted_label]

    return predicted_pid

predictions = {}