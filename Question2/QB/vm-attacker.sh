#!/bin/bash

sudo apt-get install -y apache2 php libapache2-mod-php git

# setting up php login system
if [ -d "PHP-Login" ]; then
    echo "PHP-Login directory already exists. Skipping clone operation."
else
    git clone https://github.com/mariofont/PHP-Login.git
    # copy the files to Apache's web directory
    sudo rsync -a PHP-Login/ /var/www/html/
fi

# configuring the username and password to login
sudo sed -i "s/\(\$Username = \).*/\1'miriana';/" /var/www/html/config.php
sudo sed -i "s/\(\$Password = \).*/\1'password';/" /var/www/html/config.php

# configuring Apache to use the rogue cerificate for [www.victim.com](http://www.victim.com/)
# get path to certificate and key files generated earlier for [www.victim.com](http://www.victim.com/)
# sudo nano /etc/apache2/sites-available/000-default.conf # apache config file (HTTPS CONFIG)

config_content="
<VirtualHost *:443>
    ServerName [www.victim.com](http://www.victim.com/)
    DocumentRoot /var/www/html/
    SSLEngine on
    SSLCertificateFile /home/miriana/easy-rsa/pki/issued/www.victim.com.crt
    SSLCertificateKeyFile /home/miriana/easy-rsa/pki/private/www.victim.com.key
    <Directory /var/www/html>
        DirectoryIndex login.php
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>"

if grep -q "ServerName [www.victim.com](http://www.victim.com/)" /etc/apache2/sites-available/000-default.conf; then
    echo "Configuration for [www.victim.com](http://www.victim.com/) already exists. Skipping apend operation"
else
    echo "$config_content" | sudo tee -a /etc/apache2/sites-available/000-default.conf
fi

# restarting apache to apply changes
sudo systemctl restart apache2

# enable SSL module in Apache
sudo a2enmod ssl

# enable the site configuration
sudo a2ensite 000-default.conf

# renaming default index files to avoid conflicts
if [ -f "/var/www/html/index.html" ]; then
    sudo mv /var/www/html/index.html /var/www/html/index.html.bak
fi
    if [ -f "/var/www/html/index.php" ]; then
    sudo mv /var/www/html/index.php /var/www/html/index.php.bak
fi

sudo systemctl restart apache2 # now the connection should be secured using the rogue certificate