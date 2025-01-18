#!/bin/bash
source piinkenv/bin/activate
pid=$(lsof -i :80| awk '/python/ { pid=$2 } END { print pid }')
currentDir=$(pwd)
currentFolder=${PWD##*/} 

# do a sudo check!
if [ "$EUID" -ne 0 ]; then
  echo -e "\n[ERROR]: The PiInk start script requires root privileges. Please run it with sudo.\n"
  exit 1
fi

if [ "$currentFolder" == "scripts" ]; then
  cd ..
  currentDir=$(pwd)
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

echo "starting PiInk frame webserver!"
if [[ -d "piinkenv" ]]; then
  
  if [[ $? -ne 0 ]]; then
    echo "[ERROR]: Failed to activate the virtual environment. Please check that the venv is setup."
    exit 1
  fi
  sudo python "$currentDir/src/webserver.py"
else
  echo "[ERROR]: Virtual environment 'piinkenv' not found. Please ensure the virtual environment is set up correctly."
  exit 1
fi
