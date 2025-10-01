## ML SDK for Vulkan® — Release Notes

---

## Version 0.7.0 – *Initial Public Release*

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

---
