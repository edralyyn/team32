import socket
import subprocess
import configparser
import os

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

def scan_devices_in_network(network_prefix, start_range, end_range, timeout=1):
    reachable_devices = []

    for i in range(start_range, end_range + 1):
        target_ip = f"{network_prefix}.{i}"
        target_address = (target_ip, 22)

        try:
            socket.create_connection(target_address, timeout=timeout)
            reachable_devices.append(target_ip)
            print(f"Device at {target_ip} is reachable.")
        except (socket.timeout, ConnectionRefusedError):
            print(f"Device at {target_ip} is not reachable.")

    return reachable_devices

def save_to_inventory(reachable_devices, inventory_file):
    config = configparser.ConfigParser()

    config['hosts'] = {}

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
    local_ip = get_local_ip()
    if local_ip:
        network_prefix = ".".join(local_ip.split(".")[:-1])
    else:
        print("Exiting due to an error in determining the local IP address.")
        exit(1)

    start_range = 35
    end_range = 55

    inventory_file = 'inventory.ini'
    playbook_file = 'sample.yml'

    reachable_devices = scan_devices_in_network(network_prefix, start_range, end_range)
    save_to_inventory(reachable_devices, inventory_file)

    run_ansible_playbook(inventory_file, playbook_file)
