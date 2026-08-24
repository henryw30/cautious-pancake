# ============================================================
# Verilator dependencies
# ============================================================
FROM ubuntu:latest AS verilator-base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git \
    autoconf \
    make \
    gcc \
    g++ \
    flex \
    bison \
    help2man \
    perl \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Build verilator
FROM verilator-base AS verilator-builder
ARG VERILATOR_VERSION=v5.050
WORKDIR /tmp
RUN git clone --depth 1 --branch ${VERILATOR_VERSION} \
        https://github.com/verilator/verilator.git \
    && cd verilator \
    && autoconf \
    && ./configure --prefix=/opt/verilator \
    && make -j4 \
    && make install

# ============================================================
# Development image
# ============================================================
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    cmake gcc g++ vim ninja-build git wget sudo curl ca-certificates wget unzip build-essential locales \
    python3-pip pipx python3-venv \
    clang-format \
    help2man perl python3 make autoconf flex bison ccache libgoogle-perftools-dev numactl perl-doc libfl-dev zlib1g-dev \
    libsdl2-dev liblz4-dev \
    && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8 && sudo update-locale LANG=en_US.UTF-8

# Copy verilator
COPY --from=verilator-builder /opt/verilator /opt/verilator
ENV PATH="/opt/verilator/bin:$PATH"

# sudo privileges
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

# Start the dev container as ubuntu
USER ubuntu
WORKDIR /home/ubuntu

# Verible
RUN pipx install ruff && pipx ensurepath
RUN wget -O verible.tar.gz https://github.com/chipsalliance/verible/releases/download/v0.0-4148-g1ea007ec/verible-v0.0-4148-g1ea007ec-linux-static-arm64.tar.gz \
    && sudo tar -xzf verible.tar.gz --strip-components=2 -C /usr/local/bin

# python virtual environment
RUN python3 -m venv /home/ubuntu/my_python_venv
ENV PATH="/home/ubuntu/my_python_venv/bin:$PATH"
# cocotb
ENV COCOTB_IGNORE_PYTHON_REQUIRES=1
RUN pip install cocotb
