print_green () {
    echo -e "\e[1;32m\n\n$1\e[0m"
}

exit_if_error () {
    if [ $1 -ne 0 ]; then
        echo -e "\e[1;31m\n\n$2\e[0m"
        exit 1
    fi
}

print_green "Pulling the latest changes from the repository"
git pull
exit_if_error $? "Error pulling the latest changes from the repository"

print_green "Installing the dependencies in the virtual environment"
venv/bin/pip install -r requirements.txt
exit_if_error $? "Error installing the dependencies in the virtual environment"
