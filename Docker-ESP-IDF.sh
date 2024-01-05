# Description: This script will build the Docker Image and run the Docker Container
#              for the ESP-IDF development environment.
# Created: Jan 4, 2024
# Author: Marcio Reis


# Check if Docker is installed
which docker > /dev/null;
if [ "$?" == 1 ]; then
    echo "Docker is not installed or you are already in a Docker container.";
    echo "Please install Docker first if you want to build the ESP-IDF development environment.";
    exit 1;
fi

# Build the Docker Image, if it doesn't exist
docker image ls | grep ^esp-idf > /dev/null;
if [ "$?" == 1 ]; then
    docker build -t esp-idf . ;
else
    echo "Docker Image esp-idf already exists";
fi

# Run the Docker Container and Mount the Current Directory into the Container
docker container ls | egrep "^.+\s+esp-idf" > /dev/null;
if [ "$?" == 1 ]; then
    docker container rm esp-idf-container > /dev/null 2>&1;
    docker run -d -it --name esp-idf-container -v $(pwd):/app \
        --privileged esp-idf;
else
    echo "Docker Container esp-idf-container already exists";
fi

# Connect to the container
docker exec -it esp-idf-container bash;
