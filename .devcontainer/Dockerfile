FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    cmake gcc g++ vim ninja-build git wget sudo python3-pip curl ca-certificates wget unzip build-essential \
    python3-pip pipx \
    clang-format \
    libsdl2-dev \
    && rm -rf /var/lib/apt/lists/*

# Give the ubuntu user passwordless sudo access
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

# Start the dev container as ubuntu
USER ubuntu
WORKDIR /home/ubuntu

RUN pipx install ruff && pipx ensurepath
RUN wget -O verible.tar.gz https://github.com/chipsalliance/verible/releases/download/v0.0-4148-g1ea007ec/verible-v0.0-4148-g1ea007ec-linux-static-arm64.tar.gz \
    && tar -xzf verible.tar.gz \
    && sudo cp verible-v0.0-4148-g1ea007ec/bin/* /usr/local/bin