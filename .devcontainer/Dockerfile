ARG TARGETARCH

# ============================================================
# Verible Builder
# ============================================================
FROM mcr.microsoft.com/devcontainers/cpp:ubuntu26.04 AS verible-builder
ARG TARGETARCH
ARG VERIBLE_VERSION=v0.0-4281-gbfc19111

WORKDIR /opt/verible
RUN case "${TARGETARCH}" in \
      amd64) \
        VERIBLE_ARCH="linux-static-x86_64" ;; \
      arm64) \
        VERIBLE_ARCH="linux-static-arm64" ;; \
      *) \
        echo "Unsupported architecture: ${TARGETARCH}" && exit 1 ;; \
    esac && \
    curl -fL \
      "https://github.com/chipsalliance/verible/releases/download/${VERIBLE_VERSION}/verible-${VERIBLE_VERSION}-${VERIBLE_ARCH}.tar.gz" \
      -o /tmp/verible.tar.gz && \
    tar -xzf /tmp/verible.tar.gz --strip-components=1 && \
    chmod -R 755 /opt/verible/bin && \
    rm /tmp/verible.tar.gz

# ============================================================
# Verilator Builder
# ============================================================
FROM mcr.microsoft.com/devcontainers/cpp:ubuntu26.04 AS verilator-builder
ARG VERILATOR_VERSION=v5.050

RUN apt-get update && apt-get install -y \
    autoconf \
    flex \
    bison \
    help2man \
    perl \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch ${VERILATOR_VERSION} \
        https://github.com/verilator/verilator.git \
    && cd verilator \
    && autoconf \
    && ./configure --prefix=/opt/verilator \
    && make -j"$(nproc)" \
    && make install

# ============================================================
# Development image
# ============================================================
FROM mcr.microsoft.com/devcontainers/cpp:ubuntu26.04

RUN apt-get update && apt-get install -y \
    vim clang-format ccache \
    pipx python3-venv python3-dev \
    liblz4-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy verilator
COPY --from=verilator-builder /opt/verilator /opt/verilator
COPY --from=verible-builder /opt/verible /opt/verible
ENV PATH="/opt/verilator/bin:/opt/verible/bin:$PATH"

# Python setup
USER vscode
RUN pipx install ruff && pipx ensurepath
RUN python3 -m venv /home/vscode/my_python_venv
ENV PATH="/home/vscode/my_python_venv/bin:$PATH"
# cocotb
RUN pip install cocotb
