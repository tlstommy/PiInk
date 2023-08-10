#!/bin/bash

#idk how useful this is but maybe it will simplify stuff?

# do a sudo check!
if [ "$EUID" -ne 0 ]; then
  echo -e "\n[ERROR]: $(print_error "The PiInk installation script requires root privileges. Please run it with sudo.\n")"
  exit 1
fi

#run install script
sudo bash scripts/setup.sh 