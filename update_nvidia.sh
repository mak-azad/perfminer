#!/bin/bash
echo 'Removing unattended upgrade!'
parallel-ssh -i -h sshosts -t 0 'sudo systemctl stop unattended-upgrades -y'
parallel-ssh -i -h sshhosts -t 0 'sudo apt-get purge unattended-upgrades -y'
echo 'Status:'
parallel-ssh -i -h sshhosts -t 0 'sudo systemctl status unattended-upgrades.service'
sleep 5
echo 'Cleaning previous nvidia driver'
sleep 5
parallel-ssh -i -h sshhosts -t 0  'sudo apt-get remove --purge -y '^nvidia-.*' && sudo apt autoclean -y && sudo apt autoremove -y'
parallel-ssh -i -h sshhosts -t 0  'sudo apt-get remove --purge -y '^libnvidia-.*' && sudo apt autoclean -y && sudo apt autoremove -y'
echo 'Installing nvidia drivers'
sleep 3
parallel-ssh -i -h sshhosts -t 0 'wget https://us.download.nvidia.com/tesla/460.106.00/NVIDIA-Linux-x86_64-460.106.00.run'
parallel-ssh -i -h sshhosts -t 0 'chmod +x NVIDIA-Linux-x86_64-460.106.00.run'
parallel-ssh -i -h sshhosts -t 0 'sudo ./NVIDIA-Linux-x86_64-460.106.00.run -s'

echo 'NVIDIA updated!'
sleep 3

