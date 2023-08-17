#!/bin/bash

# QUESTION A & B

# installing necessary tools
sudo apt-get install -y easy-rsa apache2 php libapache2-mod-php git

# copying content for easier access to new folder
mkdir ~/easy-rsa
ln -s /usr/share/easy-rsa/* ~/easy-rsa/
chmod 700 /home/miriana/easy-rsa

# initialis the public key infrastructure (PKI)
cd ~/easy-rsa
./easyrsa init-pki

# creating a CA
cat <<EOL > vars
set_var EASYRSA_REQ_COUNTRY    "US"
set_var EASYRSA_REQ_PROVINCE   "NewYork"
set_var EASYRSA_REQ_CITY       "New York City"
set_var EASYRSA_REQ_ORG        "RogueCA"
set_var EASYRSA_REQ_EMAIL      "admin@example.com"
set_var EASYRSA_REQ_OU         "Security"
set_var EASYRSA_ALGO           "ec"
set_var EASYRSA_DIGEST         "sha512"
EOL

# build the rogue CA (with no password)
./easyrsa build-ca nopass

# generate a certificate for www.victim.com 
./easyrsa gen-req www.victim.com nopass
echo "yes" | ./easyrsa sign-req server www.victim.com

# manually import the rogue CA's certificate into the browsers trust store (vm-client)
# copying ca.crt from this VM to VM-user in order to import 
# this will bypass the browser's security warning