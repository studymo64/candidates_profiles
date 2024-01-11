#!/bin/bash

# -------------------------------------------------------------------#
# This script does a full set up Candidate Profiles on an Ubuntu 22  #
# Check main() function below #
# -------------------------------------------------------------------#


# This to be used between two functions
echoEmptyLines(){
    echo ""
    echo ""
    echo "------------------------------------------------------------------------"
    echo "$1"   # Title of the currently run function
    echo "------------------------------------------------------------------------"
}

installSystemRequirements() {
	echoEmptyLines "Installing sys packages"
	add-apt-repository ppa:deadsnakes/ppa
	apt-get update -y
	apt-get install python3.8 -y
	apt install python3.8-distutils -y
	apt-get install python3.8-dev -y
	apt-get install libpq-dev -y
	apt install python3-virtualenv -y
}


installDocker() {
	echoEmptyLines "Installing Docker"

	# Add Docker's official GPG key:
	apt-get update -y
	apt-get install ca-certificates curl gnupg -y
	install -m 0755 -d /etc/apt/keyrings
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
	chmod a+r /etc/apt/keyrings/docker.gpg

	# Add the repository to Apt sources:
	echo \
	  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
	  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
	  tee /etc/apt/sources.list.d/docker.list > /dev/null
	apt-get update -y
	
	
	echoEmptyLines "Install the Docker packages"
	apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
	
	
	echoEmptyLines "Verify that the Docker Engine installation is successful by running the hello-world image."
	docker run hello-world
}

main() {
	installSystemRequirements
	installDocker
}
main
