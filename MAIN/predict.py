import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import load_model

#Preprocessing method
new_data = pd.read_csv('/home/jkvcombo/Videos/team32/MAIN/SYSLOG/END DEVICES/192.168.1.36_syslog.csv', usecols=[0,1,2,3,4])
new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
new_data['pid'] = new_data['pid'].astype('object')

new_data['Event_encoded'] = LabelEncoder().fit_transform(new_data['pid'])

sequence_length = 10
new_X, new_y = [], []

for i in range(len(new_data) - sequence_length):
    new_X.append(new_data['Event_encoded'].values[i:i+sequence_length])
    new_y.append(new_data['Event_encoded'].values[i+sequence_length])

new_X = np.array(new_X)
new_y = np.array(new_y)

# One-hot encode the target variable if needed
num_classes = len(np.unique(new_data['Event_encoded']))
new_y_one_hot = to_categorical(new_y, num_classes=num_classes)

# Reshape data to match the input shape
new_X = new_X.reshape((new_X.shape[0], sequence_length, 1))

# Ensure the shape is (None, 10, 1)
new_X = new_X.reshape((-1, sequence_length, 1))

#Fetch Model
current_directory = os.getcwd()
model_file = 'PD1-1.h5'
model_path = os.path.join(current_directory, model_file)
model = load_model(model_path)

def predict_event(num_days):
    # Assuming 'df' is the DataFrame containing your data

    # Assuming 'Event_encoded' is the column with encoded events in the DataFrame
    new_sequence = new_data['Event_encoded'].values[-sequence_length:]

    # Extend the sequence based on the user input
    for i in range(num_days):
        new_sequence = np.append(new_sequence, 0)  # Assuming 0 as a placeholder, you can change this based on your data

    new_sequence = new_sequence[-sequence_length:]
    new_sequence = new_sequence.reshape(1, sequence_length, 1)

    predicted_probs = model.predict(new_sequence)
    predicted_label = np.argmax(predicted_probs)

    # Assuming 'Event ID' is the column with original event labels in the DataFrame
    predicted_event_id = new_data['pid'].unique()[predicted_label]

    return predicted_event_id

# Ask the user for input
num_days_input = int(input("Enter the number of days for prediction: "))

# Get the prediction
predicted_event = predict_event(num_days_input)

print(f"The predicted Event ID after {num_days_input} days is: {predicted_event}")