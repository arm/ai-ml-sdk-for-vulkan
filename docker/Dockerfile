#
# SPDX-FileCopyrightText: Copyright 2025-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
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
ENV ANDROID_HOME="/opt/android/sdk"
ENV PATH="/home/$user/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y \
    bash \
    bash-completion \
    build-essential \
    ca-certificates \
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
    openjdk-17-jdk \
    pkg-config \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    sudo \
    unzip \
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

# Install flatc v25.2.10
RUN git clone --depth 1 https://github.com/google/flatbuffers.git -b v25.2.10 && \
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

# Install uv
RUN curl -sSL -o /tmp/uv-installer.sh https://astral.sh/uv/install.sh && \
    UV_INSTALL_DIR=/home/$user/.local/bin sh /tmp/uv-installer.sh && \
    rm /tmp/uv-installer.sh

# Install Gradle 9.4.1
RUN wget https://services.gradle.org/distributions/gradle-9.4.1-bin.zip -O /tmp/gradle-9.4.1-bin.zip && \
    unzip /tmp/gradle-9.4.1-bin.zip -d /opt && \
    ln -sf /opt/gradle-9.4.1/bin/gradle /home/$user/.local/bin/gradle && \
    rm /tmp/gradle-9.4.1-bin.zip

# Install command-line tools
RUN mkdir -p /opt/android/sdk/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/commandlinetools-linux-11076708_latest.zip && \
    unzip -qo /tmp/commandlinetools-linux-11076708_latest.zip -d /opt/android/sdk/cmdline-tools && \
    mv /opt/android/sdk/cmdline-tools/cmdline-tools /opt/android/sdk/cmdline-tools/latest && \
    ln -sf /opt/android/sdk/cmdline-tools/latest/bin/sdkmanager /home/$user/.local/bin/sdkmanager && \
    ln -sf /opt/android/sdk/cmdline-tools/latest/bin/avdmanager /home/$user/.local/bin/avdmanager && \
    rm /tmp/commandlinetools-linux-11076708_latest.zip

COPY --chown=$user ../requirements.txt ./
COPY --chown=$user ../tooling-requirements.txt ./
RUN uv pip install --system -r requirements.txt
RUN uv pip install --system -r tooling-requirements.txt
RUN rm -f requirements.txt tooling-requirements.txt
RUN uv pip install --system twine "dohq-artifactory>=0.10.0,<0.11"

RUN git lfs install

RUN useradd -m -u $uid -U $user && \
    echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R $user:$user /opt/android

WORKDIR /home/$user
RUN chown -R $user:$user .

USER $user
CMD ["/bin/bash"]
