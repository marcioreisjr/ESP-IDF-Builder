# Description: This script will build the Docker Image and run the Docker Container
#              for the ESP-IDF development environment.
# Created: 2021-08-15 12:00:00
# Author: Marcio Reis

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed or you are already in a Docker container."
    Write-Host "Please install Docker first if you want to build the ESP-IDF development environment."
    exit 1
}

# Build the Docker Image, if it doesn't exist
if (-not (docker image ls esp-idf | Select-String '^esp-idf')) {
    docker build -t esp-idf .
}
else {
    Write-Host "Docker Image esp-idf already exists"
}

# Run the Docker Container and Mount the Current Directory into the Container
if (-not (docker container ls | Select-String "^.+\s+esp-idf")) {
    docker container rm esp-idf-container -Force 2>$null
    docker run -d -it --name esp-idf-container -v ${PWD}:/app `
        -v /dev/uart.wlan-debug:/dev/uart.wlan-debug ` # Change this to your serial port `
        --privileged esp-idf
}
else {
    Write-Host "Docker Container esp-idf-container already exists"
}

# Connect to the container
docker exec -it esp-idf-container bash
