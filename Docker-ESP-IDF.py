#!/usr/bin/env python3
# Description: This script will build the Docker Image and run the Docker
#              Container for the ESP-IDF development environment.
# Created: Jan 4, 2024
# Author: Marcio Reis

import os
import subprocess
import shutil
import sys
from random import randint
import json

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
MIN_LETTERS = 3
MAX_LETTERS = 8


def fake_a_name():
    """
    Generates a random name with alternating vowels and consonants; it is not
    a real name and sounds funny, like a name from a sci-fi movie.
    """
    n_len = randint(MIN_LETTERS, MAX_LETTERS)
    use_vowel = randint(0, 1) == 1
    name = ""
    for i in range(n_len):
        if use_vowel:
            name += VOWELS[randint(0, len(VOWELS) - 1)]
        else:
            name += CONSONANTS[randint(0, len(CONSONANTS) - 1)]
        use_vowel ^= True
    return name


def find_image(name):
    """
    Find the image with the given name. If the image is not found, return None.
    """
    cmd_output = subprocess.run(
        ["docker", "image", "ls", "--format", "json"],
        stdout=subprocess.PIPE,
    )
    images = list(
        map(
            json.loads,
            filter(len, str(cmd_output.stdout, encoding="utf-8").split("\n")),
        )
    )
    for image in images:
        if image["Repository"] == name:
            return image
    return None


def find_container(name):
    """
    Find the container with the given name. If the container is not found,
    return None, otherwise return the container status ('up', 'exited').

    param name: The name of the container to find.

    return: The status of the container, or None if the container is not found.
    """
    cmd_output = subprocess.run(
        [
            "docker",
            "ps",
            "-a",
            "--format",
            "json",
        ],
        stdout=subprocess.PIPE,
    )
    containers = list(
        map(
            json.loads,
            filter(len, str(cmd_output.stdout, encoding="utf-8").split("\n")),
        )
    )
    for container in containers:
        if container["Names"] == name:
            return container["Status"].split(" ")[0].lower()
    return None


# Check if the user is asking for help
if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print("Usage:./Docker-ESP-IDF.sh [container-name]")
    print("If no container-name is provided, a generic name will be used.")
    exit(0)

# Check if Docker is installed
docker_path = shutil.which("docker")
if docker_path is None:
    print("Docker is not installed or you are already in a Docker container.")
    print(
        "Please install Docker first if you want to build the ESP-IDF development environment."
    )
    exit(1)

# Check if the Dockerfile exists
if not os.path.isfile("Dockerfile"):
    print(
        "Dockerfile not found. Please run this script from the root of the ESP-IDF project."
    )
    exit(1)

# Build the Docker Image, if it doesn't exist
if find_image("esp-idf") is None:
    cmd_output = subprocess.run(
        ["docker", "build", "-t", "esp-idf", "."], stdout=subprocess.PIPE
    )
    if cmd_output.returncode != 0:
        print("Error building Docker image")
        exit(1)
else:
    print("Docker Image esp-idf already exists")

# Use provided name or generate a unique name for the container
container_name = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "esp-idf-" + "-".join((fake_a_name(), fake_a_name()))
)
print(f"Using {container_name} as container name")

# Run the Docker Container. If it does not exist, create it. If it exists and
# is stopped then start it. If it exists and is running, do nothing.
container_status = find_container(container_name)
if container_status is None:
    cmd_output = subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-it",
            "--name",
            container_name,
            "-v",
            f"{os.getcwd()}:/app",
            "esp-idf",
            "bash",
        ],
        stdout=subprocess.PIPE,
    )
    if cmd_output.returncode != 0:
        print("Error running Docker container")
        exit(1)
elif container_status == "exited":
    cmd_output = subprocess.run(
        ["docker", "start", "-itd", container_name], stdout=subprocess.PIPE
    )
    if cmd_output.returncode != 0:
        print("Error starting Docker container")
        exit(1)
else:
    print(f"Docker Container {container_name} already exists and is running")

# Connect to the container and start a bash session, allowing the user to
# interact with the container as if it was a virtual machine.
cmd_output = subprocess.call(["docker", "exec", "-it", container_name, "bash"])
