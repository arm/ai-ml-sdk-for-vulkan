#!/usr/bin/env bash

# SPDX-FileCopyrightText: Copyright 2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0


set -o errexit
set -o pipefail
set -o errtrace
set -o nounset
set -o xtrace

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

# for Darwin compatibility
if ! command -v nproc >/dev/null 2>&1; then
  nproc() { sysctl -n hw.ncpu; }
fi

mkdir -p $REPO_DIR
mkdir -p $INSTALL_DIR
REPO_DIR="$(realpath "$REPO_DIR")"
INSTALL_DIR="$(realpath "$INSTALL_DIR")"
pushd $REPO_DIR

repo init -u $MANIFEST_URL --depth=1
repo sync --no-clone-bundle -j $(nproc)

mkdir -p .repo/local_manifests

if [ -n "$OVERRIDES" ]; then
  MANIFEST_XML=$(repo manifest -r)

  # Resolve each project's path from the active manifest and re-sync it
  for NAME in $(echo "$OVERRIDES" | jq -r 'keys[]'); do
    REVISION=$(echo "$OVERRIDES" | jq -r --arg name "$NAME" '.[$name]')

    PROJECT_PATH=$(echo "$MANIFEST_XML" | xmlstarlet sel -t -v "//project[@name='${NAME}']/@path")
    if [ -z "$PROJECT_PATH" ]; then
      echo "ERROR: project path for $NAME not found in manifest"
      exit 1
    fi

    rm -f .repo/local_manifests/override.xml
    cat > .repo/local_manifests/override.xml <<EOF
<manifest>
  <project name="${NAME}" revision="${REVISION}" remote="github"/>
</manifest>
EOF

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
  cat > .repo/local_manifests/override.xml <<EOF
<manifest>
  <project name="${CHANGED_REPO}" revision="${CHANGED_SHA}" remote="github"/>
</manifest>
EOF

  # Re-sync the changed project to the specified SHA
  repo sync -j $(nproc) --force-sync "$PROJECT_PATH"
fi

run_checks() {
  pushd "${1}"
  echo "Current commit: $(git rev-parse HEAD)"
  git show -s --format=%B HEAD | grep "Signed-off-by:"
  pre-commit run --all-files --hook-stage commit --show-diff-on-failure
  pre-commit run --all-files --hook-stage push --show-diff-on-failure
  popd
}

echo "Build VGF-Lib"
run_checks ./sw/vgf-lib
./sw/vgf-lib/scripts/build.py -j $(nproc) --doc --test

echo "Build Model Converter"
run_checks ./sw/model-converter
./sw/model-converter/scripts/build.py -j $(nproc) --doc --test

export VK_LAYER_PATH=$INSTALL_DIR/share/vulkan/explicit_layer.d
export VK_INSTANCE_LAYERS=VK_LAYER_ML_Graph_Emulation:VK_LAYER_ML_Tensor_Emulation
export LD_LIBRARY_PATH=$INSTALL_DIR/lib

echo "Build Emulation Layer"
run_checks ./sw/emulation-layer
./sw/emulation-layer/scripts/build.py -j $(nproc) --doc --test --install $INSTALL_DIR

echo "Build Scenario Runner"
run_checks ./sw/scenario-runner
./sw/scenario-runner/scripts/build.py -j $(nproc) --doc --test

echo "Build SDK Root"
run_checks .
./scripts/build.py -j $(nproc) --doc

popd
