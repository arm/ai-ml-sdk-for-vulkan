#
# SPDX-FileCopyrightText: Copyright 2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

# syntax=docker/dockerfile:1.10

ARG ubuntu_version=22.04
FROM ubuntu:$ubuntu_version
ARG user=myuser
ARG uid=1000

ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/home/$user/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y \
    bash \
    bash-completion \
    build-essential \
    clang-format \
    clang \
    cppcheck \
    curl \
    doxygen \
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
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    sudo \
    vulkan-tools \
    gcc-aarch64-linux-gnu \
    g++-aarch64-linux-gnu \
    android-sdk-platform-tools

RUN mkdir -p /home/$user/.local/bin

RUN curl -sSL -o cmake-3.25.3-linux-x86_64.sh https://github.com/Kitware/CMake/releases/download/v3.25.3/cmake-3.25.3-linux-x86_64.sh && \
    bash cmake-3.25.3-linux-x86_64.sh --prefix=/home/$user/.local --skip-license && \
    rm cmake-3.25.3-linux-x86_64.sh

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
