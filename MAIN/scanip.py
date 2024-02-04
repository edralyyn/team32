# scanip.py
import socket
import subprocess
import configparser
import os

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

def save_to_inventory(reachable_devices, inventory_file):
    config = configparser.ConfigParser()

    # Create an 'hosts' section
    config['hosts'] = {}

    # Add each reachable device with the key 'ansible_host'
    for i, device in enumerate(reachable_devices, start=1):
        config['hosts'][f'host{i}'] = f'ansible_host={device}'

    try:
        with open(inventory_file, 'w') as configfile:
            config.write(configfile)
            print(f"Inventory saved to {inventory_file}")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def run_ansible_playbook(inventory_file, playbook_file):
    try:
        subprocess.run(['ansible-playbook', playbook_file, '-i', inventory_file], check=True)
        print("Ansible playbook executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Ansible playbook: {e}")

if __name__ == "__main__":
    # Define your network details
    network_prefix = "192.168.1"  # Change this to your network's prefix of the device
    start_range = 35
    end_range = 55  # Adjust the range based on your network sizes

    inventory_file = 'inventory.ini'  # Path to the inventory file
    playbook_file = 'sample.yml'  # Path to the Ansible playbook file

    reachable_devices = scan_devices_in_network(network_prefix, start_range, end_range)
    save_to_inventory(reachable_devices, inventory_file)

    # Run Ansible playbook
    run_ansible_playbook(inventory_file, playbook_file)