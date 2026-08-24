FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    cmake gcc g++ vim ninja-build git wget sudo curl ca-certificates wget unzip build-essential \
    python3-pip pipx python3-venv \
    clang-format \
    help2man perl python3 make autoconf flex bison ccache libgoogle-perftools-dev numactl perl-doc libfl-dev zlib1g-dev \
    libsdl2-dev liblz4-dev \
    && rm -rf /var/lib/apt/lists/*

# Give the ubuntu user passwordless sudo access
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

# Start the dev container as ubuntu
USER ubuntu
WORKDIR /home/ubuntu

RUN pipx install ruff && pipx ensurepath
RUN wget -O verible.tar.gz https://github.com/chipsalliance/verible/releases/download/v0.0-4148-g1ea007ec/verible-v0.0-4148-g1ea007ec-linux-static-arm64.tar.gz \
    && sudo tar -xzf verible.tar.gz --strip-components=2 -C /usr/local/bin

RUN git clone -b v5.050 https://github.com/verilator/verilator.git \
    && cd verilator \
    && autoconf \
    && ./configure \
    && make -j4 \
    && sudo make install

# python virtual environment
RUN python3 -m venv /home/ubuntu/my_python_venv
ENV PATH="/home/ubuntu/my_python_venv/bin:$PATH"
# cocotb
ENV COCOTB_IGNORE_PYTHON_REQUIRES=1
RUN pip install cocotb
