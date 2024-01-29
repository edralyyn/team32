import ipaddress
import socket
import configparser
import subprocess

def scan_devices_in_network(network_prefix, start_range, end_range, timeout=1):
    reachable_devices = []

    for i in range(start_range, end_range + 1):
        target_ip = f"{network_prefix}.{i}"
        target_address = (target_ip, 22)  # Using port 22 (SSH) for reachability check

        # Check if the host is reachable
        try:
            socket.create_connection(target_address, timeout=timeout)
            reachable_devices.append(target_ip)
            print(f"Device at {target_ip} is reachable.")
        except (socket.timeout, ConnectionRefusedError):
            print(f"Device at {target_ip} is not reachable.")

    return reachable_devices

def save_to_inventory(reachable_devices):
    config = configparser.ConfigParser()
    config['hosts'] = {'ip_addresses': ', '.join(reachable_devices)}

    try:
        with open('inventory.ini', 'w') as configfile:
            config.write(configfile)
            print("Inventory saved to inventory.ini")
    except Exception as e:
        print(f"Error saving inventory: {e}")

def run_ansible_playbook():
    try:
        subprocess.run(['ansible-playbook', 'tryfolder.yml'], check=True)
        print("Ansible playbook executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Ansible playbook: {e}")

if __name__ == "__main__":
    # Define your network details
    network_prefix = "192.168.1"  # Change this to your network's prefix
    start_range = 34
    end_range = 50  # Adjust the range based on your network size

    reachable_devices = scan_devices_in_network(network_prefix, start_range, end_range)
    save_to_inventory(reachable_devices)

    # Run Ansible playbook
    run_ansible_playbook()
