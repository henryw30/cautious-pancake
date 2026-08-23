FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    vim \
    ninja-build \
    git \
    libsdl2-dev \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Give the ubuntu user passwordless sudo access
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

# Start the dev container as ubuntu
USER ubuntu
WORKDIR /home/ubuntu