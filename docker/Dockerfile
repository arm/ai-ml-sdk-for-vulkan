#
# SPDX-FileCopyrightText: Copyright 2025-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

# syntax=docker/dockerfile:1.10

ARG almalinux_version=8.10
FROM almalinux:${almalinux_version}

SHELL ["/bin/bash", "-o", "errexit", "-o", "pipefail", "-c"]

ARG TARGETARCH
ARG user=mlsdkuser
ARG uid=1000

ENV LANG=C.UTF-8
ENV ANDROID_HOME=/opt/android/sdk
ENV PATH=/opt/rh/gcc-toolset-14/root/usr/bin:/opt/cppcheck/bin:/opt/venv/bin:/home/${user}/.local/bin:${PATH}

# RHEL and AlmaLinux disable the Lavapipe software Vulkan driver unless this variable is set.
ENV RH_SW_VULKAN=1

# Base development tools
# PowerTools supplies Ninja; EPEL supplies the ABI tools.
ARG CLANG_VERSION=20.1.8-2.module_el8.10.0+4062+b20d4441
RUN dnf install -y \
      dnf-plugins-core \
      epel-release && \
    dnf config-manager --set-enabled powertools && \
    dnf install -y \
      abi-compliance-checker \
      abi-dumper \
      autoconf \
      automake \
      bash \
      bash-completion \
      binutils \
      bison \
      ca-certificates \
      cmake \
      "clang-${CLANG_VERSION}" \
      "clang-tools-extra-${CLANG_VERSION}" \
      curl \
      elfutils \
      findutils \
      flex \
      gcc-toolset-14-binutils \
      gcc-toolset-14-gcc \
      gcc-toolset-14-gcc-c++ \
      gcc-toolset-14-libasan-devel \
      gcc-toolset-14-libubsan-devel \
      git \
      git-lfs \
      glx-utils \
      graphviz \
      gzip \
      jq \
      "lld-${CLANG_VERSION}" \
      make \
      mesa-dri-drivers \
      mesa-libGL-devel \
      mesa-libGLU-devel \
      mesa-vulkan-drivers \
      ninja-build \
      patch \
      pkgconf-pkg-config \
      procps-ng \
      python3.12 \
      python3.12-devel \
      python3.12-pip \
      shadow-utils \
      sudo \
      tar \
      unzip \
      vulkan-headers \
      vulkan-loader-devel \
      vulkan-tools \
      wget \
      which \
      xmlstarlet \
      xz && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# Build Universal Ctags because AlmaLinux 8 ships only Exuberant Ctags.
ARG UNIVERSAL_CTAGS_VERSION=6.2.1
RUN git clone --depth 1 --branch "v${UNIVERSAL_CTAGS_VERSION}" \
      https://github.com/universal-ctags/ctags.git /tmp/universal-ctags && \
    cd /tmp/universal-ctags && \
    ./autogen.sh && \
    ./configure --prefix=/usr/local && \
    make -j "$(nproc)" && \
    make install && \
    rm -rf /tmp/universal-ctags

# AlmaLinux 8's Doxygen 1.8.14 does not support
# WARN_AS_ERROR=FAIL_ON_WARNINGS. Build a pinned version for both architectures.
ARG DOXYGEN_VERSION=1.9.8
RUN git clone --depth 1 --branch "Release_${DOXYGEN_VERSION//./_}" \
      https://github.com/doxygen/doxygen.git /tmp/doxygen && \
    cmake \
      -S /tmp/doxygen \
      -B /tmp/doxygen/build \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr/local && \
    cmake --build /tmp/doxygen/build -j "$(nproc)" && \
    cmake --install /tmp/doxygen/build && \
    rm -rf /tmp/doxygen

RUN git lfs install

# AArch64 GNU cross-toolchain - amd64 only.
ARG ARM_GNU_TOOLCHAIN_VERSION=14.3.rel1
ARG ARM_GNU_TOOLCHAIN_SHA256=ddeaff1ea60d4135acba271b0143d9f5add02b68ab9e9be39672d1965c12e82f
RUN if [ "${TARGETARCH}" = amd64 ]; then \
      toolchain="arm-gnu-toolchain-${ARM_GNU_TOOLCHAIN_VERSION}-x86_64-aarch64-none-linux-gnu"; \
      curl -fsSL -o "/tmp/${toolchain}.tar.xz" \
        "https://developer.arm.com/-/media/Files/downloads/gnu/${ARM_GNU_TOOLCHAIN_VERSION}/binrel/${toolchain}.tar.xz"; \
      echo "${ARM_GNU_TOOLCHAIN_SHA256}  /tmp/${toolchain}.tar.xz" | sha256sum -c -; \
      mkdir -p /opt/arm-gnu-toolchain; \
      tar -xJf "/tmp/${toolchain}.tar.xz" \
        --strip-components=1 \
        -C /opt/arm-gnu-toolchain; \
      for tool_path in /opt/arm-gnu-toolchain/bin/aarch64-none-linux-gnu-*; do \
        tool="${tool_path##*/aarch64-none-linux-gnu-}"; \
        ln -s "${tool_path}" "/usr/local/bin/aarch64-linux-gnu-${tool}"; \
      done; \
      ln -s /opt/arm-gnu-toolchain/aarch64-none-linux-gnu/libc \
        /usr/aarch64-linux-gnu; \
      rm "/tmp/${toolchain}.tar.xz"; \
    fi

# libc++ and libc++abi are not packaged for AlmaLinux 8.
ARG LLVM_VERSION=20.1.8
RUN git clone --depth 1 --branch "llvmorg-${LLVM_VERSION}" \
      https://github.com/llvm/llvm-project.git /tmp/llvm-project && \
    cmake \
      -S /tmp/llvm-project/runtimes \
      -B /tmp/llvm-project/build \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_COMPILER=clang \
      -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_INSTALL_LIBDIR=lib64 \
      -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi" \
      -DLIBCXX_INCLUDE_TESTS=OFF \
      -DLIBCXXABI_INCLUDE_TESTS=OFF \
      -DLIBCXXABI_USE_LLVM_UNWINDER=OFF \
      -DPython3_EXECUTABLE=/usr/bin/python3.12 && \
    cmake --build /tmp/llvm-project/build --target install-cxx install-cxxabi -j "$(nproc)" && \
    rm -rf /tmp/llvm-project

# Non-root development user
RUN if getent passwd "${uid}" >/dev/null; then \
      old_user="$(getent passwd "${uid}" | cut -d: -f1)"; \
      old_group="$(id -gn "${old_user}")"; \
      if [ "${old_group}" != "${user}" ]; then \
        groupmod -n "${user}" "${old_group}"; \
      fi; \
      if [ "${old_user}" != "${user}" ]; then \
        usermod -l "${user}" "${old_user}"; \
      fi; \
      usermod -c "" -d "/home/${user}" -m "${user}"; \
    else \
      useradd -m -u "${uid}" -U "${user}"; \
    fi && \
    echo "${user} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/${user}" && \
    chmod 0440 "/etc/sudoers.d/${user}" && \
    install -d -o "${user}" -g "${user}" "/home/${user}/.local/bin"

# cppcheck - AlmaLinux 8's cppcheck package is too old, compile it from source
ARG CPPCHECK_VERSION=2.13.0
RUN git clone --depth 1 --branch "${CPPCHECK_VERSION}" \
      https://github.com/cppcheck-opensource/cppcheck.git /tmp/cppcheck && \
    cmake \
      -S /tmp/cppcheck \
      -B /tmp/cppcheck/build \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_GUI=OFF \
      -DCMAKE_INSTALL_PREFIX=/opt/cppcheck && \
    cmake --build /tmp/cppcheck/build -j "$(nproc)" && \
    cmake --install /tmp/cppcheck/build && \
    rm -rf /tmp/cppcheck

# Repo
RUN curl -fsSL -o "/home/${user}/.local/bin/repo" \
      https://storage.googleapis.com/git-repo-downloads/repo && \
    chmod 0755 "/home/${user}/.local/bin/repo"

# glslang from latest sdk
ARG GLSLANG_VERSION=vulkan-sdk-1.4.357.0
RUN git clone --depth 1 --branch "${GLSLANG_VERSION}" \
      https://github.com/KhronosGroup/glslang.git /tmp/glslang && \
    cd /tmp/glslang && \
    /usr/bin/python3.12 update_glslang_sources.py && \
    cmake \
      -S /tmp/glslang \
      -B /tmp/glslang/build \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DENABLE_GLSLANG_BINARIES=ON \
      -DENABLE_OPT=OFF \
      -DBUILD_SHARED_LIBS=OFF && \
    cmake --build /tmp/glslang/build --target glslang-standalone -j "$(nproc)" && \
    install -m 0755 /tmp/glslang/build/StandAlone/glslang \
      "/home/${user}/.local/bin/glslang" && \
    rm -rf /tmp/glslang

# sccache
ARG SCCACHE_VERSION=0.17.0
RUN case "${TARGETARCH}" in \
      amd64) architecture=x86_64 ;; \
      arm64) architecture=aarch64 ;; \
      *) \
        echo "Unsupported TARGETARCH: ${TARGETARCH}" >&2; \
        exit 1 \
        ;; \
    esac && \
    archive="sccache-v${SCCACHE_VERSION}-${architecture}-unknown-linux-musl.tar.gz" && \
    curl -fsSLO \
      "https://github.com/mozilla/sccache/releases/download/v${SCCACHE_VERSION}/${archive}" && \
    tar -xzf "${archive}" && \
    install -m 0755 \
      "sccache-v${SCCACHE_VERSION}-${architecture}-unknown-linux-musl/sccache" \
      "/home/${user}/.local/bin/sccache" && \
    rm -rf "${archive}" \
      "sccache-v${SCCACHE_VERSION}-${architecture}-unknown-linux-musl"

# uv
ARG UV_VERSION=0.12.9
RUN curl --proto '=https' --tlsv1.2 -fsSL -o /tmp/uv-installer.sh \
      "https://releases.astral.sh/github/uv/releases/download/${UV_VERSION}/uv-installer.sh" && \
    UV_INSTALL_DIR="/home/${user}/.local/bin" sh /tmp/uv-installer.sh && \
    rm /tmp/uv-installer.sh

# Android development tools - amd64 only.
ARG GRADLE_VERSION=9.4.1
ARG ANDROID_COMMAND_LINE_TOOLS_VERSION=11076708
RUN if [ "${TARGETARCH}" = amd64 ]; then \
      dnf install -y java-17-openjdk-devel; \
      dnf clean all; \
      rm -rf /var/cache/dnf; \
      gradle_archive="gradle-${GRADLE_VERSION}-bin.zip"; \
      wget -q -O "/tmp/${gradle_archive}" \
        "https://services.gradle.org/distributions/${gradle_archive}"; \
      wget -q -O "/tmp/${gradle_archive}.sha256" \
        "https://services.gradle.org/distributions/${gradle_archive}.sha256"; \
      echo "$(< "/tmp/${gradle_archive}.sha256")  /tmp/${gradle_archive}" | sha256sum -c -; \
      unzip -q "/tmp/${gradle_archive}" -d /opt; \
      ln -s "/opt/gradle-${GRADLE_VERSION}/bin/gradle" \
        "/home/${user}/.local/bin/gradle"; \
      android_archive="commandlinetools-linux-${ANDROID_COMMAND_LINE_TOOLS_VERSION}_latest.zip"; \
      wget -q -O "/tmp/${android_archive}" \
        "https://dl.google.com/android/repository/${android_archive}"; \
      mkdir -p "${ANDROID_HOME}/cmdline-tools"; \
      unzip -q "/tmp/${android_archive}" -d "${ANDROID_HOME}/cmdline-tools"; \
      mv "${ANDROID_HOME}/cmdline-tools/cmdline-tools" \
        "${ANDROID_HOME}/cmdline-tools/latest"; \
      ln -s "${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager" \
        "/home/${user}/.local/bin/sdkmanager"; \
      ln -s "${ANDROID_HOME}/cmdline-tools/latest/bin/avdmanager" \
        "/home/${user}/.local/bin/avdmanager"; \
      rm -f "/tmp/${gradle_archive}" "/tmp/${gradle_archive}.sha256" \
        "/tmp/${android_archive}"; \
    fi

# Python development environment
RUN uv venv --python /usr/bin/python3.12 /opt/venv
COPY requirements.txt tooling-requirements.txt /tmp/requirements/
RUN uv pip install \
      twine "dohq-artifactory>=1.0.1,<2" && \
    uv pip install -r /tmp/requirements/requirements.txt && \
    uv pip install -r /tmp/requirements/tooling-requirements.txt && \
    rm -rf /tmp/requirements

# File ownership
RUN if [ -d "${ANDROID_HOME}" ]; then \
      chown -R "${user}:${user}" "${ANDROID_HOME}"; \
    fi && \
    chown -R "${user}:${user}" "/home/${user}"

# Build a headless Lavapipe alongside AlmaLinux's other Mesa drivers and Vulkan loader.
# Install, build and clean up in one layer, retaining the original SDK packages.
# System Mesa uses LLVM 17. Link LLVM 20 statically and hide its archive symbols
# so normal multi-driver discovery cannot mix incompatible LLVM implementations.
# This makes Lavapipe larger, but avoids forcing CPU-only discovery through ENV.
ARG MESA_VERSION=25.2.8
ARG MESA_SHA256=097842f3e49d996868b38688db87b006f7d4541e93ce86d2f341d8b3e7be7c93
ARG LAVAPIPE_BUILD_JOBS=12
RUN lavapipe_tmp="$(mktemp -d /tmp/lavapipe-build-XXXXXX)" && \
    cd "${lavapipe_tmp}" && \
    rpm -qa | sort > packages-before.txt && \
    dnf install -y \
      "llvm-devel-${CLANG_VERSION}" \
      zlib-devel \
      libxml2-devel \
      elfutils-libelf-devel && \
    python3.12 -m venv build-tools && \
    build-tools/bin/pip install --no-cache-dir \
      meson==1.9.1 Mako==1.3.10 packaging==25.0 PyYAML==6.0.3 && \
    install -m 0755 "/home/${user}/.local/bin/glslang" \
      build-tools/bin/glslangValidator && \
    export PATH="${lavapipe_tmp}/build-tools/bin:${PATH}" CC=clang CXX=clang++ && \
    llvm_archives="$(llvm-config --link-static --libnames | tr ' ' ':')" && \
    export LDFLAGS="-Wl,--exclude-libs,${llvm_archives}" && \
    curl --fail --location --retry 3 \
      "https://archive.mesa3d.org/mesa-${MESA_VERSION}.tar.xz" \
      --output mesa.tar.xz && \
    echo "${MESA_SHA256}  mesa.tar.xz" | sha256sum --check - && \
    tar -xf mesa.tar.xz && \
    meson setup mesa-build "mesa-${MESA_VERSION}" \
      --prefix=/opt/mesa-lavapipe --libdir=lib64 --buildtype=release \
      --wrap-mode=nofallback \
      -Dvulkan-drivers=swrast -Dgallium-drivers=[] -Dvulkan-layers=[] \
      -Dplatforms=[] -Dglx=disabled -Degl=disabled -Dgbm=disabled \
      -Dopengl=false -Dgles1=disabled -Dgles2=disabled \
      -Dgallium-va=disabled -Dgallium-vdpau=disabled \
      -Dllvm=enabled -Dshared-llvm=disabled \
      -Dxmlconfig=disabled -Dexpat=disabled -Dbuild-tests=false && \
    meson compile -C mesa-build -j "${LAVAPIPE_BUILD_JOBS}" && \
    meson install -C mesa-build --strip && \
    mv /opt/mesa-lavapipe/share/vulkan/icd.d/lvp_icd.*.json \
      /opt/mesa-lavapipe/share/vulkan/icd.d/lvp_icd.json && \
    install -d /opt/mesa-lavapipe/share/licenses/mesa && \
    cp -r "mesa-${MESA_VERSION}/licenses/." /opt/mesa-lavapipe/share/licenses/mesa/ && \
    install -m 0644 "mesa-${MESA_VERSION}/docs/license.rst" \
      /opt/mesa-lavapipe/share/licenses/mesa/ && \
    comm -13 packages-before.txt <(rpm -qa | sort) > packages-added.txt && \
    xargs -r dnf remove -y --noautoremove < packages-added.txt && \
    # AlmaLinux's LLVM 20 uninstall script leaves this alternative behind.
    if grep -q '^llvm-devel-' packages-added.txt; then \
      update-alternatives --remove llvm-config-20 /usr/lib64/llvm20/bin/llvm-config; \
    fi && \
    rpm -qa | sort > packages-after.txt && \
    diff -u packages-before.txt packages-after.txt && \
    dnf clean all && \
    cd / && \
    rm -rf "${lavapipe_tmp}" /var/cache/dnf

# Replace only the existing system Lavapipe ICD registration, not the GPU ICDs.
# Reusing its filename avoids exposing both old and new CPU drivers to applications.
# The new manifest points to /opt/mesa-lavapipe; other Mesa libraries stay in place.
# Do not set VK_DRIVER_FILES or VK_ICD_FILENAMES here: either would restrict normal
# driver discovery and make GPU CI jobs compensate for an image-wide CPU override.
# CPU-only hosts discover the new Lavapipe; GPU hosts retain application device selection.
# A later mesa-vulkan-drivers package update may restore its manifest; reapply this step.
RUN set -- /usr/share/vulkan/icd.d/lvp_icd.*.json && \
    test "$#" -eq 1 && test -f "$1" && \
    install -m 0644 /opt/mesa-lavapipe/share/vulkan/icd.d/lvp_icd.json "$1"

WORKDIR /home/${user}
USER ${user}

CMD ["/bin/bash"]
