#
# SPDX-FileCopyrightText: Copyright 2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

# syntax=docker/dockerfile:1.10

ARG ubuntu_version=22.04
FROM ubuntu:$ubuntu_version
ARG user=mlsdkuser
ARG uid=1000

ARG BUILDPLATFORM

ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/home/$user/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y \
    android-sdk-platform-tools \
    bash \
    bash-completion \
    build-essential \
    clang-format \
    clang \
    cppcheck \
    curl \
    doxygen \
    g++-aarch64-linux-gnu \
    gcc-aarch64-linux-gnu \
    git \
    git-lfs \
    graphviz \
    jq \
    libc++-dev \
    libc++abi-dev \
    libvulkan-dev \
    lld \
    mesa-common-dev \
    mesa-utils \
    mesa-vulkan-drivers \
    ninja-build \
    pkg-config \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    sudo \
    vulkan-tools \
    wget \
    xmlstarlet

RUN mkdir -p /home/$user/.local/bin

RUN if [ "$BUILDPLATFORM" = "linux/amd64" ] ; then ARCH="x86_64"; else ARCH="aarch64"; fi && \
    curl -sSL -o cmake-3.25.3-linux-${ARCH}.sh https://github.com/Kitware/CMake/releases/download/v3.25.3/cmake-3.25.3-linux-${ARCH}.sh && \
    bash cmake-3.25.3-linux-${ARCH}.sh --prefix=/home/$user/.local --skip-license && \
    rm cmake-3.25.3-linux-${ARCH}.sh

RUN curl -sSL -o /home/$user/.local/bin/repo https://storage.googleapis.com/git-repo-downloads/repo && \
    chmod u+x . /home/$user/.local/bin/repo

# Install glslang 15.4.0
RUN git clone --depth 1 https://github.com/KhronosGroup/glslang.git -b 15.4.0 && \
    cd glslang && \
    python3 update_glslang_sources.py && \
    cmake -B build -S . -DCMAKE_BUILD_TYPE=Release -DENABLE_GLSLANG_BINARIES=ON -DENABLE_OPT=OFF -DBUILD_SHARED_LIBS=OFF && \
    cmake --build build --target glslang-standalone -j $(nproc) && \
    cp build/StandAlone/glslang /home/$user/.local/bin && \
    cd .. && rm -rf glslang

# Install flatc v23.5.26
RUN git clone --depth 1 https://github.com/google/flatbuffers.git -b v23.5.26 && \
    cd flatbuffers && \
    cmake -B build -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build -j $(nproc) && \
    cp build/flatc /home/$user/.local/bin && \
    cd .. && rm -rf flatbuffers

# Install sccache v0.12.0
RUN mkdir -p /home/$user/sccache
WORKDIR /home/$user/sccache
RUN if [ "$BUILDPLATFORM" = "linux/amd64" ] ; then ARCH="x86_64"; else ARCH="aarch64"; fi && \
    curl -sSL -o sccache-v0.12.0-${ARCH}-unknown-linux-musl.tar.gz  https://github.com/mozilla/sccache/releases/download/v0.12.0/sccache-v0.12.0-${ARCH}-unknown-linux-musl.tar.gz && \
    tar xvf sccache-v0.12.0-${ARCH}-unknown-linux-musl.tar.gz --strip-components=1 && \
    cp sccache /home/$user/.local/bin/ && \
    rm -rf /home/$user/sccache

COPY --chown=$user ../requirements.txt ./
COPY --chown=$user ../tooling-requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install -r tooling-requirements.txt
RUN rm -f requirements.txt tooling-requirements.txt

RUN git lfs install

RUN useradd -m -u $uid -U $user && \
    echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /home/$user
RUN chown -R $user:$user .

USER $user
CMD ["/bin/bash"]
