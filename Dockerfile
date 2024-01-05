# Use an official Ubuntu runtime as a parent image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    cmake \
    wget flex bison python3-pip python3-venv ninja-build ccache \
    libffi-dev libssl-dev dfu-util libusb-1.0-0 vim

# Get the Espressif ESP-IDF
RUN mkdir -p ~/esp && \
    cd ~/esp && \
    git clone --recursive https://github.com/espressif/esp-idf.git

# set up the tools
RUN cd ~/esp/esp-idf && \
    ./install.sh all && \
    echo "source ~/esp/esp-idf/export.sh" >> ~/.bashrc

CMD "bash"
