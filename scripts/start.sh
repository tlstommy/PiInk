#!/bin/bash

pid=$(lsof -i :80| awk '/python/ { pid=$2 } END { print pid }')

# do a sudo check!
if [ "$EUID" -ne 0 ]; then
  echo -e "\n[ERROR]: The PiInk start script requires root privileges. Please run it with sudo.\n"
  exit 1
fi

if [[ -z $pid ]]; then
  echo "No process found using port 80!"
else
  echo "Found PID using port 80: $pid."
  echo "Killing process $pid..."
  if sudo kill -9 "$pid" >/dev/null 2>&1; then
    echo "Process killed!"
  else
    echo "Failed to kill process $pid."
  fi
fi

echo "starting frame webserver!"

sudo python src/webserver.py