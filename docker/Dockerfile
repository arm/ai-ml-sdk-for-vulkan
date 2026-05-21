#
# SPDX-FileCopyrightText: Copyright 2025-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

# syntax=docker/dockerfile:1.10

ARG ubuntu_version=24.04
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
    abi-compliance-checker \
    abi-dumper \
    bash \
    bash-completion \
    build-essential \
    ca-certificates \
    clang \
    clang-format \
    clang-tidy \
    cmake \
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
    libgl1-mesa-dri \
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

RUN if getent passwd "$uid" >/dev/null; then \
        existing_user="$(getent passwd "$uid" | cut -d: -f1)" && \
        existing_group="$(id -gn "$existing_user")" && \
        if [ "$existing_group" != "$user" ]; then \
            groupmod -n "$user" "$existing_group"; \
        fi && \
        if [ "$existing_user" != "$user" ]; then \
            usermod -l "$user" "$existing_user"; \
        fi && \
        usermod -c "" -d "/home/$user" -m "$user"; \
    else \
        useradd -m -u "$uid" -U "$user"; \
    fi && \
    echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /home/$user/.local/bin

RUN curl -sSL -o /home/$user/.local/bin/repo https://storage.googleapis.com/git-repo-downloads/repo && \
    chmod u+x . /home/$user/.local/bin/repo

# Install glslang vulkan-sdk-1.4.341.0 (16.2.0) -- needed for compiling EL shaders when cross-compiling
RUN git clone --depth 1 https://github.com/KhronosGroup/glslang.git -b vulkan-sdk-1.4.341.0 && \
    cd glslang && \
    python3 update_glslang_sources.py && \
    cmake -B build -S . -DCMAKE_BUILD_TYPE=Release -DENABLE_GLSLANG_BINARIES=ON -DENABLE_OPT=OFF -DBUILD_SHARED_LIBS=OFF && \
    cmake --build build --target glslang-standalone -j $(nproc) && \
    cp build/StandAlone/glslang /home/$user/.local/bin && \
    cd .. && rm -rf glslang

# Install sccache v0.12.0 -- building cache to speed up builds
RUN mkdir -p /home/$user/sccache
WORKDIR /home/$user/sccache
RUN if [ "$BUILDPLATFORM" = "linux/amd64" ] ; then ARCH="x86_64"; else ARCH="aarch64"; fi && \
    curl -sSL -o sccache-v0.12.0-${ARCH}-unknown-linux-musl.tar.gz  https://github.com/mozilla/sccache/releases/download/v0.12.0/sccache-v0.12.0-${ARCH}-unknown-linux-musl.tar.gz && \
    tar xvf sccache-v0.12.0-${ARCH}-unknown-linux-musl.tar.gz --strip-components=1 && \
    cp sccache /home/$user/.local/bin/ && \
    rm -rf /home/$user/sccache

# Install uv - python package management and wheel creation
RUN curl -sSL -o /tmp/uv-installer.sh https://astral.sh/uv/install.sh && \
    UV_INSTALL_DIR=/home/$user/.local/bin sh /tmp/uv-installer.sh && \
    rm /tmp/uv-installer.sh

# Install Gradle 9.4.1 - needed for APK packaging for Android
RUN wget https://services.gradle.org/distributions/gradle-9.4.1-bin.zip -O /tmp/gradle-9.4.1-bin.zip && \
    unzip /tmp/gradle-9.4.1-bin.zip -d /opt && \
    ln -sf /opt/gradle-9.4.1/bin/gradle /home/$user/.local/bin/gradle && \
    rm /tmp/gradle-9.4.1-bin.zip

# Install command-line tools -- needed for Android build and testing
RUN mkdir -p /opt/android/sdk/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/commandlinetools-linux-11076708_latest.zip && \
    unzip -qo /tmp/commandlinetools-linux-11076708_latest.zip -d /opt/android/sdk/cmdline-tools && \
    mv /opt/android/sdk/cmdline-tools/cmdline-tools /opt/android/sdk/cmdline-tools/latest && \
    ln -sf /opt/android/sdk/cmdline-tools/latest/bin/sdkmanager /home/$user/.local/bin/sdkmanager && \
    ln -sf /opt/android/sdk/cmdline-tools/latest/bin/avdmanager /home/$user/.local/bin/avdmanager && \
    rm /tmp/commandlinetools-linux-11076708_latest.zip

RUN git lfs install

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install twine "dohq-artifactory>=1.0.1,<2"

COPY --chown=$user ../requirements.txt ./
COPY --chown=$user ../tooling-requirements.txt ./
RUN uv pip install -r requirements.txt
RUN uv pip install -r tooling-requirements.txt
RUN rm -f requirements.txt tooling-requirements.txt

RUN chown -R $user:$user /opt/android

WORKDIR /home/$user
RUN chown -R $user:$user .

USER $user
CMD ["/bin/bash"]
