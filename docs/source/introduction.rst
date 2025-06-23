Introduction
============

The |SDK_project| is a collection of libraries and tools consisting of various components.

The components are:

Model Converter
    Converts TOSA models into SPIR-V™ graphs and packages the whole use case into a
    VGF file. The Model Converter must be used as part of an asset pipeline
    deployment flow and is separated into two stages:

    1. The framework specific conversion mechanism lowers the framework model to a TOSA intermediate representation
    (not part of the |SDK_project|).

    2. The Model Converter applies additional transforms and optimizations before lowering to SPIR-V™ graph
    intermediate representation (IR) and then packaging the use case into a :code:`.vgf` file.

VGF Library
    A simple, efficient container format for ML use cases consisting of SPIR-V™ graphs, custom shaders,
    and constant data. This component provides:

    - A C++ encoder and decoder API for writing and efficiently reading VGF files.
    - A C decoder wrapper API to provide stable ABI bindings.
    - A VGF Dump Tool for working with VGF files.

The VGF Library is intended for integration into game engines. The library has been designed around
efficient decoding of the VGF file at runtime by supporting memory mapped file access (optional). The
library requires user managed memory allocation to minimise copying and in-memory duplication of
potentially large constant data.

Scenario Runner
    A data driven test and validation tool for executing ML workloads described in
    JSON scenario files.

Emulation layer
    A TOSA compliant, compute-based implementation of the graph and tensor extensions which is exposed
    using Vulkan® Layers.

In addition to these components, you will find documentation, tutorials, samples, and tests.

Platforms
---------

This table represents the status of platform support. We will increase support in the upcoming releases.

+------------------+-----------+----------+----------+-----------+
| Platforms        | ML SDK    |  ML SDK  | ML SDK   | ML SDK    |
|                  | Model     |  VGF     | Scenario | Emulation |
|                  | Converter |  Library | Runner   | Layer     |
+========+=========+===========+==========+==========+===========+
| Linux  | AArch64 | |/|       | |/|      | |/|      | |/|       |
+        +---------+-----------+----------+----------+-----------+
|        | X86-64  | |/|       | |/|      | |/|      | |/|       |
+--------+---------+-----------+----------+----------+-----------+
| Windows| AArch64 | |x|       | |x|      | |x|      | |x|       |
+        +---------+-----------+----------+----------+-----------+
|        | X86-64  | |/|       | |/|      | |/|      | |/|       |
+--------+---------+-----------+----------+----------+-----------+
| MacOS  | AArch64 | |x|       | |x|      | |-|      | |-|       |
+        +---------+-----------+----------+----------+-----------+
|        | X86-64  | |x|       | |x|      | |-|      | |-|       |
+--------+---------+-----------+----------+----------+-----------+
| Android| AArch64 | |-|       | |/|      | |/|      | |/|       |
+        +---------+-----------+----------+----------+-----------+
|        | X86-64  | |-|       | |x|      | |x|      | |x|       |
+--------+---------+-----------+----------+----------+-----------+
