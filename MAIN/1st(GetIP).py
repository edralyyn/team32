import os
import subprocess
import re

def get_active_interfaces():
    try:
        # Run ip link command to get interface information
        result = subprocess.run(['ip', 'link'], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Use regex to find the active interfaces
            interfaces = re.findall(r'\d+:\s+(\S+):', result.stdout)
            return interfaces
        else:
            return []
    except Exception as e:
        return []

def get_network_address(interface):
    try:
        # Run ifconfig command to get interface information
        result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Use regex to find the network address (IPv4)
            match = re.search(r'inet\s([0-9]+\.[0-9]+\.[0-9]+)\.[0-9]+', result.stdout)
            if match:
                network_address = match.group(1)
                return network_address
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

def write_to_file(directory, network_address):
    try:
        filename = os.path.join(directory, "network_address.txt")
        with open(filename, 'w') as file:
            file.write(network_address)
        print(f"Network address written to {filename}")
    except Exception as e:
        print(f"Failed to write to file: {e}")

if __name__ == "__main__":
    # Create a directory named "IPnetwork" if it doesn't exist
    ip_network_dir = "IPnetwork"
    if not os.path.exists(ip_network_dir):
        os.makedirs(ip_network_dir)

    interfaces = get_active_interfaces()
    for interface in interfaces:
        network_address = get_network_address(interface)
        if network_address:
            # Extract the IP address up to the third part
            truncated_network_address = '.'.join(network_address.split('.')[:3])
            write_to_file(ip_network_dir, truncated_network_address)
        else:
            print(f"Network address not found for interface {interface}.")
