#!/bin/bash

IP_VM_VICTIM="192.168.179.3"

# Change nameserver to the IP address of vm-victim
sudo sed -i "/^nameserver/c\nameserver $IP_VM_VICTIM" /etc/resolv.conf