#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root."
  exit
fi
echo "Installing requirements"
apt-get install -y python3 pip
echo "Installing pypass."
cp pypass.py /opt/pypass.py
echo "Done."
