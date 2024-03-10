#!/bin/bash

echo "Exporting variables"
export CLOUD="true"
export AWS_DEFAULT_REGION="eu-west-1"
export AWS_ACCOUNT_ID="ACCOUNT_ID"
echo "Done"

sudo apt-get -y update
sudo apt-get install -y python3-pip
sudo apt-get install unzip

# install chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# install chromedriver
sudo apt-get install -y libglib2.0-0 libnss3 libgconf-2-4
sudo apt-get --fix-broken -y install
sudo apt-get install -y xvfb
cd /tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv chromedriver /usr/bin/chromedriver

# install googlesearch for w3validator suggestions
pip3 install google

# return back
cd ~/backend

pip3 install -r Crawler/requirements.txt