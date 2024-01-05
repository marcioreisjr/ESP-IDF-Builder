# ESP-IDF-Builder
Builds the ESP-IDF development environment in a Docker container

## Introduction
The purpose of this project is to ease the installation of the ESP-IDF
development environment by using a Docker container. This project is based on
the instructions provided by [Espressif](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html).

Having the development environment in a container allows you to:
- Have a clean and automated installation of the ESP-IDF development
environment;
- Have a portable development environment;
- Have a development environment that is independent of the host system;
- Have a development environment that is easy to update;
- It is easy to remove the development environment from the host system.

## Installation
This system is containerized and requires the Docker app on your host
system before proceeding with the installation. If you need to install Docker,
please follow the instructions [here](https://docs.docker.com/get-docker/).

Once Docker is installed, you can build the container by running the following
command:
```bash
./Docker-ESP-IDF.sh
```
This script will:
- Build the Docker image (named `esp-idf`), if it does not exist;
- Create a container named `esp-idf-container` from the `esp-idf` image, if it
does not exist;
- Start the `esp-idf-container` container;
- Attach the current terminal to the `esp-idf-container` container.
- After exiting the container, you can reconnect to it by running the
`./Docker-ESP-IDF.sh` script again.

> **Note:** You can exit the container by pressing `Ctrl + D` or by typing
`exit` in the terminal.

## Usage
Once the container is running, the local directory is mounted in the
`/app` directory of the container. It means that you can edit the files in
your favorite editor on your host system and build the project in the container.

You can also use the `idf.py` tool in the container to create a new project or
to build an existing one.

## Removing the Container
To stop the container, you can run the following command:
```bash
docker stop esp-idf-container
```
If you want to remove the container, you can run the following command:
```bash
docker rm esp-idf-container
```
If you want to remove the image, you can run the following command:
```bash
docker rmi esp-idf
```

## Limitations
- The script currently only works on Linux or MacOS systems. The Windows script
is untested;
- Connecting the ESP32 board to the container is not supported yet;
- Limited reproducibility of the building environment. The building environment
is reproducible as long as the Docker image is not updated. If the Docker image
is updated, it will pick up the latest version of the ESP-IDF and the toolchain,
which may create a different build environment.
