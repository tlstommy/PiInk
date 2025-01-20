#!/bin/bash

#formatting stuff
bold=$(tput bold)
underline=$(tput smul)
normal=$(tput sgr0)
standout=$(tput smso)
blink=$(tput blink)

PYTHON="python"
SERVICE_FILE="/etc/systemd/system/piink.service"

red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)

enable_interfaces(){
  #enable spi
  sudo raspi-config nonint do_spi 0
  sudo bash -c 'echo "dtoverlay=spi0-0cs" >> /boot/firmware/config.txt'	
  print_success "SPI Interface has been enabled."
  
  #enable i2c
  sudo raspi-config nonint do_i2c 0  
  print_success "I2C Interface has been enabled.\n"

  
  
}


show_loader() {
  local pid=$!
  local delay=0.1
  local spinstr='|/-\'
  printf "$1 [${spinstr:0:1}] "
  while ps a | awk '{print $1}' | grep -q "${pid}"; do
    local temp=${spinstr#?}
    printf "\r$1 [${temp:0:1}] "
    spinstr=${temp}${spinstr%"${temp}"}
    sleep ${delay}
  done
  if [[ $? -eq 0 ]]; then
    printf "\r$1 [\e[32m\xE2\x9C\x94\e[0m]\n"
  else
    printf "\r$1 [\e[31m\xE2\x9C\x98\e[0m]\n"
  fi
}


#status funcs
print_header() {
  echo -e "${bold}${underline}$1${normal}"
}

print_standout() {
  echo -e "${standout}$1${normal}"
}

print_blink() {
  echo -e "${blink}$1${normal}"
}

print_bold() {
  echo -e "${bold}$1${normal}"
}

print_underline() {
  echo -e "${underline}$1${normal}"
}


print_success() {
  echo -e "${green}$1${normal}"
}

print_error() {
  echo -e "${red}$1${normal}"
}

# better color vals than tput
print_warn() {
  echo -e "\e[38;2;255;255;0m$1\e[0m"

}

print_blue() {
  echo -e "\e[38;2;65;105;225m$1\e[0m"
}




# do a sudo check!
if [ "$(id -u)" -eq 0 ]; then
  echo -e "\n[ERROR]: $(print_error "The PiInk installation script should not be ran as root.\n")"
  exit 1
fi

if [ "$currentFolder" == "scripts" ]; then
  cd ..
  currentDir=$(pwd)
  currentWorkingDir=$(pwd)
fi

#do a python check
if [ ! -f "$(which "$PYTHON")" ]; then
	echo -e "\n[ERROR]: $(print_error "Python Path could not be found.\n")"
  echo "$PYTHON"
  exit 1
fi


while true; do
    clear
    print_header "Current Directory: $currentWorkingDir"
    print_bold "\nThis script will install all the required packages for PiInk!\n"
    print_underline "$(print_bold "It will do the following:\n")"
    echo "   [•] Create a virtual enviroment'."
    echo "   [•] Set the hostname to 'PiInk'."
    echo "   [•] Setup bonjour."
    echo "   [•] Create a log file."
    echo "   [•] Update rc.local so that the Webserver starts on boot."
    echo -e "   [•] Install Required Python packages via pip.\n"

    read -p "Would you like to proceed? [Y/n] " userInput
    userInput="${userInput^^}"

    if [[ $userInput == "Y" ]]; then
        print_success "You entered 'Y'. Proceeding with the installation.\n"
        sleep 2
        break
    elif [[ $userInput == "N" ]]; then
        print_warn "Exiting!"
        exit
    else
        print_error "Invalid input! Please try again."
        sleep 1
    fi
done


print_header  "Creating PiInk venv "

python3 -m venv --system-site-packages piinkenv

if [ $? -ne 0 ]; then
  print_error "Failed to create virtual environment. Ensure Python 3 and venv (pip install venv) are installed!"
  exit 1
fi

echo -e  "activating venv: piinkvenv..\n"

source piinkenv/bin/activate
if [ $? -ne 0 ]; then
  print_error "Failed to activate virtual environment."
  exit 1
fi


# Set the current  and ip
currentDir=$(dirname "$PWD")
currentWorkingDir=$(pwd)
currentFolder=${PWD##*/} 
ipAddress=$(hostname -I | cut -d ' ' -f 1)


enable_interfaces


#ensure pip is installed
#sudo apt install python3-pip
#manually install flask?


print_header  "Installing the Pimoroni Inky libraries..."
$PYTHON -m pip install inky[rpi,example-depends]
$PYTHON -m pip install inky 
#show_loader "   Installing packages...    "
#curl https://get.pimoroni.com/inky | bash

# Install required pip packages
print_header  "\nInstalling required packages with pip..."
$PYTHON -m pip install -r $currentWorkingDir/config/requirements.txt
#show_loader "   Installing packages...   "

print_success "Packages Installed!\n"
sudo apt-get install -y sysvbanner > /dev/null

print_success "Installed!\n"

sleep 1








#set the hostname
print_bold "Setting hostname"
sudo bash -c 'echo "piink" > "/etc/hostname"'
sudo sed -i 's/127.0.0.1\s*localhost/127.0.0.1 piink/' /etc/hosts
print_success "Hostname set to piink!"
echo -e "(This can be changed using raspi-config.) \n"

#set up Bonjour
print_header "Setting up Bonjour"

sudo apt-get install -y avahi-daemon
#show_loader "   [1/2] Installing avahi-daemon."

sudo apt-get install -y netatalk 
#show_loader "   [2/2] Installing netatalk.    "

print_success "Bonjour set up!\n"

# Create the log file
sudo touch "$currentWorkingDir/piink-log.txt"

mkdir "$currentWorkingDir/album"

#make sure the start.sh script is executable
chmod +x "$currentWorkingDir/scripts/start.sh"

# create systemd service
print_bold "Creating new systemd service"
sleep 1
echo "[Unit]
Description=PiInk Webserver
After=network.target

[Service]
User=pi
WorkingDirectory=$currentWorkingDir
ExecStart=$currentWorkingDir/scripts/start.sh
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE > /dev/null

sudo systemctl daemon-reload
sudo systemctl enable piink.service
print_success "Systemd service PiInk Webserver has been created and enabled!"


sleep 3
#clear
banner "PiInk"
print_success "$(print_bold "PiInk has been successfully installed!")"

print_header "Helpful Info:"
echo "  [•] A QR code of the PiInk webUI can be brought up at any time by pressing the button labeled 'A' on the back of the PiInk display."
echo "  [•] Have an issue or suggestion? Please, submit it here!"
echo -e "      https://github.com/tlstommy/PiInk/issues\n"


print_warn "$(print_bold "(Please reboot your Raspberry Pi to complete installation)")"
print_bold "After your Pi is rebooted, you can access the web UI by going to $(print_blue "'piink.local'") or $(print_blue "'$ipAddress'") in your browser.\n"
read -p "Would you like to restart your Raspberry Pi now? [Y/n] " userInput
userInput="${userInput^^}"

if [[ $userInput == "Y" ]]; then
    print_success "You entered 'Y', Restarting now...\n"
    sleep 2
    sudo reboot now
elif [[ $userInput == "N" ]]; then
    print_warn "Please restart your Raspberry Pi later to apply changes.\n"
    exit
else
    print_error "Unknown input, please restart later to apply changes.\n"
    sleep 1
fi

