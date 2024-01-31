#!/usr/bin/env python3
import csv

def convert_syslog_to_csv(input_file, output_file):
    with open(input_file, 'r') as syslog_file:
        syslog_entries = syslog_file.readlines()

    csv_entries = []
    for entry in syslog_entries:
        
        fields = entry.split()
        csv_entries.append(fields)

    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, escapechar='\\')  
        csv_writer.writerows(csv_entries)

if __name__ == "__main__":
    input_log_file = '/var/log/syslog'
    output_csv_file = './SYSLOG/END DEVICE/end-device_syslog.csv'  
    # Convert to csvs
    convert_syslog_to_csv(input_log_file, output_csv_file)
