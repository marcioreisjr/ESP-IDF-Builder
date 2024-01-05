# ESP-IDF-Builder
Builds the ESP-IDF development environment in a Docker container

## Introduction
This project aims to simplify the installation of the ESP-IDF development
environment by using a Docker container. The project builds on the instructions
provided on the [Espressif](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html)
web page.

Having the development environment in a container allows you to:
- Have a clean and automated installation of the ESP-IDF development
environment;
- Have a portable development environment;
- Have a development environment that is independent of the host system;
- Have a development environment that is easy to update;
- Easily remove the development environment from the host system.

> If you try and like [this project](https://github.com/marcioreisjr/ESP-IDF-Builder),
  please give it a star on GitHub.

## Installation
This system is containerized and requires the Docker app on your host
system before proceeding with the installation. If you need to install Docker,
please follow the instructions on the [Docker docs](https://docs.docker.com/get-docker/).

When Docker is running:
- Set the basis for your project development by either:
  - Downloading the latest version of these files from the release
    [page](https://github.com/marcioreisjr/ESP-IDF-Builder/releases) and
    extracting them to a directory of your choice or
  - Cloning this repository to get the latest version of these files and copying
    them to a directory of your choice;
- Build the container by running the following command:
    ```bash
    ./Docker-ESP-IDF.sh
    ```

> **Note:** A large count of files will be downloaded and built
during the first run of the script. It may take a while to complete. On my host
system, it took about 7 minutes to complete; it had a solid average network
throughput of 50 Mbps. Once the Docker image is built, it is reused on the next
runs of the script.

This script will:
- Build the Docker image (named `esp-idf`) if it does not exist;
- Create a container named `esp-idf-container` from the `esp-idf` image if it
does not exist;
- Start the `esp-idf-container` container;
- Attach the current terminal to the `esp-idf-container` container.
- After exiting the container, you can reconnect to it by running the
`./Docker-ESP-IDF.sh` script again.

> **Note:** You can exit the container by pressing `Ctrl + D` or by typing
`exit` in the terminal.

## Usage
Once the container is running, the local directory gets mounted in the
`/app` directory of the container, meaning you can edit the files in
your favorite editor on your host system and build the project in the container.

You can also use the `idf.py` tool in the container to create a new project or
to build an existing one.

## Removing the Container/Image
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
