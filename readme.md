This script run on host(my pc) and virtual machine(ubuntu 20.04)

Need:
VS Code
Ubuntu OS.ISO
Oracle VM VirtualBox

Step:
After software installation, add extension python on VSCODE
PS: Python must be on PATH ENV


Virtual Pc Must be ssh connected on port 22(default ssh)
Used Ubuntu as virtual pc, enabling ssh port 22 on windows is different
[
ifconfig
sudo apt install net-tools


sudo apt install openssh-server

sudo systemctl status ssh
sudo service ssh start
sudo ufw allow ssh
sudo ufw enable
sudo ufw status
]
Run Code on terminal [ py file_name.py ]

