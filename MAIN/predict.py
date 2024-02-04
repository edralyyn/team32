import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import load_model

def preprocess_data(sequence_length=10):
    new_data = pd.read_csv('/home/vboxuser/Desktop/git/team32/MAIN/SYSLOG/END DEVICES/192.168.1.50_syslog.csv', usecols=[0,1,2,3,4])
    new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    new_data['pid'] = new_data['pid'].astype('object')

    new_data['Event_encoded'] = LabelEncoder().fit_transform(new_data['pid'])

    new_X, new_y = [], []

    for i in range(len(new_data) - sequence_length):
        new_X.append(new_data['Event_encoded'].values[i:i+sequence_length])
        new_y.append(new_data['Event_encoded'].values[i+sequence_length])

    new_X = np.array(new_X)
    new_y = np.array(new_y)

    num_classes = len(np.unique(new_data['Event_encoded']))
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

def get_predicted_event(num_days_input):
    sequence_length = 10
    model_file = 'PD1-1.h5'
    model_path = os.path.join(os.getcwd(), model_file)
    model = load_model(model_path)
    
    new_data, new_X, num_classes = preprocess_data(sequence_length)
    
    predicted_event = predict_event(model, new_data, sequence_length, num_days_input)
    
    return predicted_event