# ML SDK for Vulkan® — Release Notes

---

## Version 2025.12.0 – *Expanded Platform & CI Coverage*

Changes since `v2025.10.0`.

### Highlights

- Linux AArch64 builds now supported end-to-end, including native
    builds and AArch64 Docker images.
- Windows® and Darwin coverage moved into CI using shared workflows and
    gated tests.
- Build tooling consolidated around ci_build.sh for determinism and
    improved diagnostics.

### Build & Github CI

- Added reusable workflows: trigger, manifest-build, and topic builds,
    with concurrency limits and multi-component checks.
- Manifest overrides handled safely to avoid config drift.
- Github CI workflows for Linux, Windows® and Darwin.
- Added ci_build.sh with debug tracing, faster repo sync, updated
    package commands, and Ninja as the default CMake generator.

### Tooling, Docker & Dependencies

- Expanded Linux AArch64 support and published refreshed Docker images.
- Images include sccache, tosa_tools, wget, and an updated FlatBuffers
    toolchain.
- Synced tooling versions across components; added
    tooling-requirements.txt and documented pip requirements.
- Refreshed SBOM data and adopted usage of `REUSE.toml`.

### Documentation & Tutorials

- Added end-to-end ONNX and VGF execution tutorials and refreshed
    walkthroughs (basic, Sobel, ExecuTorch) with install guidance and
    limitations.
- Updated platform support docs, README layout, and diagrams to match
    the expanded device matrix.

### Supported Platforms

The following platform combinations are supported:

- Linux - AArch64 and x86-64
- Windows® - x86-64
- Darwin - AArch64 via MoltenVK (experimental)
- Android™ - AArch64 (experimental)

## Version 2025.10.0 – *Initial Public Release*

## Overview

The ML SDK for Vulkan® helps integrate and deploy new ML extensions for Vulkan®.
It targets portability and hardware acceleration, using these extensions
and SPIR-V™ additions:

- `VK_ARM_data_graph`
- `VK_ARM_tensors`
- `SPV_ARM_graph`
- `SPV_ARM_tensors`

These are aligned with the **TOSA 1.x spec** for consistent operator semantics
across vendors. The SDK comprises four main components:

- **VGF Library**
- **Model Converter**
- **Scenario Runner**
- **Emulation Layer**

Please refer to the single components release notes for more details.

## Platform Support

The following platform combinations are supported:

- Linux - X86-64
- Windows® - X86-64

---
