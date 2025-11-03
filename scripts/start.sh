#!/bin/bash
date

#kill any existing procs
pid=$(sudo netstat -tuln | grep ':80 ' | awk '{print $7}' | cut -d'/' -f1)
if [[ -n "$pid" ]]; then
    echo "Found process using port 80: PID $pid."
    echo "Killing process $pid..."
    sudo kill -9 "$pid" && echo "Process $pid killed." || echo "Failed to kill process $pid."
else
    echo "No process found using port 80!"
fi

#activate venv
if [[ -d ".venv" ]]; then
    source .venv/bin/activate
    if [[ $? -ne 0 ]]; then
        echo "[ERROR]: Cant activate venv: piinkenv."
        exit 1
    fi
else
    echo "[ERROR]: Cant find venv: piinkenv."
    exit 1
fi

currentDir=$(pwd)
currentFolder=${PWD##*/} 

#dir check
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
if [[ -d ".venv" ]]; then
  
  if [[ $? -ne 0 ]]; then
    echo "[ERROR]: Failed to activate the virtual environment. Please check that the venv is setup."
    exit 1
  fi
  
  python "$currentDir/src/webserver.py"
else
  echo "[ERROR]: Virtual environment 'piinkenv' not found. Please ensure the virtual environment is set up correctly."
  exit 1
fi
