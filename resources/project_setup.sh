#!/bin/bash

# -------------------------------------------------------------------#
# This script does a full set up Profile Candidates on an Ubuntu 22 local machine #
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



buildProjectFiles() {
    echoEmptyLines "Build project files"
    mkdir tech_society
    cd tech_society/
    virtualenv venv --python=3.8

    repoURL="https://github.com/studymo64/candidates_profiles.git"
    git clone -b master $repoURL

}

successRun(){
    STR=$'\n - Continue the steps in README.rst file to finish the setup'
    echoEmptyLines "Script has ran successfully $STR"

}

main() {
  buildProjectFiles
  successRun
}
main
