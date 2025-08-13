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

RUN apt-get update
RUN apt-get install -y \
    bash-completion \
    build-essential \
    clang-format \
    clang \
    curl \
    doxygen \
    git \
    git-lfs \
    jq \
    libc++-dev \
    libc++abi-dev \
    ninja-build \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    vulkan-tools

RUN curl -sSL -o cmake-3.25.3-linux-x86_64.sh https://github.com/Kitware/CMake/releases/download/v3.25.3/cmake-3.25.3-linux-x86_64.sh && \
    bash cmake-3.25.3-linux-x86_64.sh --prefix=/usr/local --skip-license && \
    rm cmake-3.25.3-linux-x86_64.sh

RUN curl -sSL --create-dirs -o /home/$user/.local/bin/repo https://storage.googleapis.com/git-repo-downloads/repo

RUN pip install \
    build \
    setuptools \
    wheel

COPY --chown=$user ../requirements.txt ./
COPY --chown=$user ../tooling-requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install -r tooling-requirements.txt
RUN rm -f requirements.txt tooling-requirements.txt

RUN git lfs install

RUN useradd -m -u $uid -U $user && \
    echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $user
WORKDIR /home/$user
CMD ["bash"]
