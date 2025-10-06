# ML SDK for Vulkan® — Release Notes

---

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
