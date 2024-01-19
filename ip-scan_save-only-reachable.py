import subprocess
import socket
import ipaddress

# Python script to scan all device connected
# with same ip address in local network.
# And save them to inventory.ini file
# showing only the reachable ip address.
def is_reachable(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, 22))  # Assuming SSH port (change if needed)
        return True
    except (socket.timeout, socket.error):
        return False
    finally:
        sock.close()

def get_local_ips():
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        ips = [line.split()[0] for line in lines if 'dynamic' in line]
        return ips
    except Exception as e:
        print(f"Error getting local IPs: {e}")
        return []

def scan_and_generate_inventory():
    local_ips = get_local_ips()

    reachable_ips = []
    unreachable_ips = []

    for ip in local_ips:
        if ip == '127.0.0.1':
            continue  # Skip localhost

        if is_reachable(ip):
            print(f"IP {ip} is reachable. Adding to inventory.")
            reachable_ips.append(ip)
        else:
            print(f"IP {ip} is not reachable. Discarding.")
            unreachable_ips.append(ip)

    # Generate Ansible inventory file
    with open('ansible_inventory1.ini', 'w') as inventory_file:
        inventory_file.write('[reachable]\n')
        for ip in reachable_ips:
            inventory_file.write(ip + '\n')

    print('\nScan complete.')
    print(f'Reachable IPs collected: {reachable_ips}')
    print(f'Unreachable IPs: {unreachable_ips}')

if __name__ == '__main__':
    scan_and_generate_inventory()
