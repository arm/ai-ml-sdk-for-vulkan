#!/usr/bin/env bash

# SPDX-FileCopyrightText: Copyright 2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0


set -euo pipefail

usage() {
  echo "Usage: $(basename "$0")"
  echo
  echo "Environment:"
  echo "  MANIFEST_URL   (optional)  default: https://github.com/arm/ai-ml-sdk-manifest.git"
  echo "  REPO_DIR       (optional)  default: ./sdk"
  echo "  INSTALL_DIR    (optional)  default: ./install"
  echo "  CHANGED_REPO   (optional)  manifest project name to pin and resync"
  echo "  CHANGED_SHA    (optional)  commit SHA to pin CHANGED_REPO to (required if CHANGED_REPO is set)"
  echo "  OVERRIDES      (optional)  JSON object: { \"org/repo\": \"40-char-sha\", ... }"
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

MANIFEST_URL="${MANIFEST_URL:-https://github.com/arm/ai-ml-sdk-manifest.git}"
REPO_DIR="${REPO_DIR:-$PWD/sdk}"
INSTALL_DIR="${INSTALL_DIR:-$PWD/install}"
CHANGED_REPO="${CHANGED_REPO:-}"
CHANGED_SHA="${CHANGED_SHA:-}"
OVERRIDES="${OVERRIDES:-}"

echo "Using manifest URL: $MANIFEST_URL"
echo "Using repo directory: $REPO_DIR"
echo "Using install directory: $INSTALL_DIR"
echo "find CHANGED_REPO: $CHANGED_REPO"
echo "find CHANGED_SHA: $CHANGED_SHA"
echo "find OVERRIDES: $OVERRIDES"

# for macOS compatibility
if ! command -v nproc >/dev/null 2>&1; then
  nproc() { sysctl -n hw.ncpu; }
fi

mkdir -p $REPO_DIR
REPO_DIR="$(realpath "$REPO_DIR")"
INSTALL_DIR="$(realpath "$INSTALL_DIR")"
pushd $REPO_DIR

repo init -u $MANIFEST_URL
# --force-sync to ensure we get latest even if there are local changes when re-running
repo sync --no-clone-bundle -j $(nproc) --force-sync

if [ -n "$OVERRIDES" ]; then
  mkdir -p .repo/local_manifests
  echo '<manifest>' > .repo/local_manifests/override.xml
  echo "$OVERRIDES" | jq -r 'to_entries[] | "<project name=\"\(.key)\" remote="github" revision=\"\(.value)\"/>"' >> .repo/local_manifests/override.xml
  echo '</manifest>' >> .repo/local_manifests/override.xml

  # Resolve each project's path from the active manifest and re-sync it
  for NAME in $(echo "$OVERRIDES" | jq -r 'keys[]'); do
    PROJECT_PATH=$(repo manifest -r | xmlstarlet sel -t -v "//project[@name='${NAME}']/@path")
    if [ -z "$PROJECT_PATH" ]; then
      echo "ERROR: project path for $NAME not found in manifest"
      exit 1
    fi
    echo "Syncing $NAME ($PROJECT_PATH)"
    repo sync -j"$(nproc)" --force-sync "$PROJECT_PATH"
  done

elif [ -n "$CHANGED_REPO" ]; then
  if [ -z "$CHANGED_SHA" ]; then
    echo "CHANGED_REPO is set but CHANGED_SHA is empty"
    exit 1
  fi

  # Find project path for changed repo
  PROJECT_PATH=$(repo manifest -r | xmlstarlet sel -t -v "//project[@name='${CHANGED_REPO}']/@path")
  if [ -z "$PROJECT_PATH" ]; then
    echo "Could not find project path for ${CHANGED_REPO} in manifest"
    exit 1
  fi
  echo "Changed project path: $PROJECT_PATH"

  # Create a local manifest override to pin the changed repo to the exact SHA
  mkdir -p .repo/local_manifests
  cat > .repo/local_manifests/override.xml <<EOF
<manifest>
  <project name="${CHANGED_REPO}" revision="${CHANGED_SHA}" remote="github"/>
</manifest>
EOF

  # Re-sync the changed project to the specified SHA
  repo sync -j $(nproc) --force-sync "$PROJECT_PATH"
fi

echo "Build VGF-Lib"
./sw/vgf-lib/scripts/build.py -j $(nproc) --doc --test

echo "Build Model Converter"
./sw/model-converter/scripts/build.py -j $(nproc) --doc --test

echo "Build Emulation Layer"
export VK_LAYER_PATH=$INSTALL_DIR/share/vulkan/explicit_layer.d
export LD_LIBRARY_PATH=$INSTALL_DIR/lib

if [ "$(uname)" = "Darwin" ]; then
    echo "macOS detected, skipping Emulation Layer tests"
    ./sw/emulation-layer/scripts/build.py -j $(nproc) --doc --install $INSTALL_DIR
else
    ./sw/emulation-layer/scripts/build.py -j $(nproc) --doc --test --install $INSTALL_DIR
fi

echo "Build Scenario Runner"
export VK_INSTANCE_LAYERS=VK_LAYER_ML_Graph_Emulation:VK_LAYER_ML_Tensor_Emulation

if [ "$(uname)" = "Darwin" ]; then
    echo "macOS detected, skipping Scenario Runner tests"
    ./sw/scenario-runner/scripts/build.py -j $(nproc) --doc
else
    ./sw/scenario-runner/scripts/build.py -j $(nproc) --doc --test
fi

echo "Build SDK Root"
./scripts/build.py -j $(nproc) --doc

popd
