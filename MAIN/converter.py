import os
import re
import csv

def parse_syslog_line(line):
    """Parse a single line of syslog data."""
    pattern = r'(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(?P<hostname>\S+)\s(?P<process>\S+)\[(?P<pid>\d+)\]:\s(?P<message>.*)'
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    else:
        return None

def syslog_to_csv(input_file, output_file):
    """Convert syslog file to CSV."""
    with open(input_file, 'r') as f_in, open(output_file, 'w', newline='') as f_out:
        fieldnames = ['timestamp', 'hostname', 'process', 'pid', 'message']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for line in f_in:
            parsed_data = parse_syslog_line(line)
            if parsed_data:
                writer.writerow(parsed_data)

    # Delete the original .txt file after conversion
    os.remove(input_file)

def process_all_syslogs(directory):
    """Process all syslog files in the specified directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename.replace(".txt", ".csv"))
            syslog_to_csv(input_file, output_file)

if __name__ == "__main__":
    syslog_directory = './SYSLOG/END DEVICES/'
    process_all_syslogs(syslog_directory)
