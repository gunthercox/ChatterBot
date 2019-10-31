#!/bin/bash

echo "Yolosploit configurator 2.42"
sudo apt-get --yes update
sudo apt-get --yes upgrade

echo "Installing metasploit. BE PATIENT (5 min max?)"
wget --quiet https://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run
chmod +x metasploit-latest-linux-x64-installer.run
sudo ./metasploit-latest-linux-x64-installer.run --unattendedmodeui none --prefix /opt/msf --mode unattended

echo "Installing python2"
sudo apt-get --yes install python python-pip python-virtualenv git

sudo apt-get --yes install fish
sudo chsh -s /usr/bin/fish ubuntu

cd ~
git clone https://github.com/NullArray/AutoSploit
