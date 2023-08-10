#!/bin/bash

#formatting stuff
bold=$(tput bold)
underline=$(tput smul)
normal=$(tput sgr0)
standout=$(tput smso)
blink=$(tput blink)


red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)

enable_interfaces(){
  #enable spi
  sudo sed -i 's/^dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
  sudo sed -i 's/^#dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
  print_success "SPI Interface has been enabled."
  #enable i2c
  sudo sed -i 's/^dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
  sudo sed -i 's/^#dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
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


# Set the current  and ip
currentDir=$(dirname "$PWD")
currentWorkingDir=$(pwd)
ipAddress=$(hostname -I | cut -d ' ' -f 1)

# do a sudo check!
if [ "$EUID" -ne 0 ]; then
  echo -e "\n[ERROR]: $(print_error "The PiInk installation script requires root privileges. Please run it with sudo.\n")"
  exit 1
fi

echo "$currentDir"
echo "$currentWorkingDir"

clear

while true; do
    clear
    print_header "Current Directory: $currentWorkingDir"
    print_bold "\nThis script will install all the required packages for PiInk!\n"
    print_underline "$(print_bold "It will do the following:\n")"
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

enable_interfaces

print_header  "Installing the Pimironi Inky libraries."
sudo pip3 install inky[rpi,example-depends] > /dev/null &
sudo pip3 install inky > /dev/null &
show_loader "   Installing packages...    "
#curl https://get.pimoroni.com/inky | bash

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

sudo apt-get install -y avahi-daemon > /dev/null &
show_loader "   [1/2] Installing avahi-daemon."

sudo apt-get install -y netatalk > /dev/null &
show_loader "   [2/2] Installing netatalk.    "

print_success "Bonjour set up!\n"

# Create the log file
touch "$(dirname "$PWD")/piink-log.txt"

# Update rc.local
print_bold "Updating rc.local"
sleep 1
if grep -Fxq "exit 0" /etc/rc.local; then
  sudo sed -i "/exit 0/i cd $currentDir && sudo bash $currentDir/scripts/start.sh > $(dirname "$PWD")/piink-log.txt 2>&1 &" /etc/rc.local
  print_success "Added startup line to rc.local!"
else
  print_error "ERROR: Unable to add to rc.local"
fi

# Install required pip packages
print_header  "\nInstalling required packages with pip"
sudo pip install -r $currentWorkingDir/config/requirements.txt > /dev/null &
show_loader "   Installing packages...   "

print_success "Packages Installed!\n"
sleep 3
clear
banner "PiInk"
print_success "$(print_bold "PiInk has been successfully installed!")"

print_header "Helpful Info:"
echo "  [•] A QR code of the PiInk's webUI can be brought up at any time by pressing the button labeled 'A' on the back of the PiInk display."
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

