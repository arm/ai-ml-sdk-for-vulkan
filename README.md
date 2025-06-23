# ML SDK for Vulkan®

The ML SDK for Vulkan® is an SDK to facilitate the development of projects
using the Arm® Vulkan® ML extensions.

## Content

This repository contains scripts to facilitate building all the ML SDK for
Vulkan® components, utilities, and documentation.

## Build all the ML SDK for Vulkan® components

The ML SDK for Vulkan® consists of four components:

- [VGF Library](https://github.com/arm/ai-ml-sdk-vgf-library)
- [Model Converter](https://github.com/arm/ai-ml-sdk-model-converter)
- [Scenario Runner](https://github.com/arm/ai-ml-sdk-scenario-runner)
- [Emulation Layer](https://github.com/arm/ai-ml-emulation-layer-for-vulkan)

These can be built from the ML SDK for Vulkan® root repository or individually
from their respective repositories.

The build system must have:

- CMake 3.25 or later.
- C/C++ 17 compiler: GCC, or optionally Clang on Linux and MSVC on Windows®.
- Python 3.10 or later. Required python libraries for building are listed in
  `tooling-requirements.txt`.
- Flatbuffers flatc compiler.

The following dependencies are also needed:

- [Argument Parser for Modern C++](https://github.com/p-ranav/argparse).
- [LLVM](https://github.com/llvm/llvm-project).
- [TOSA Serialization Library](https://review.mlplatform.org/plugins/gitiles/tosa/serialization_lib).
- [TOSA MLIR Translator](https://review.mlplatform.org/plugins/gitiles/tosa/tosa_mlir_translator).
- [JSON for Modern C++](https://github.com/nlohmann/json).
- [pybind11](https://github.com/pybind/pybind11).
- [GoogleTest](https://github.com/google/googletest). Optional, for testing.
- [glslang](https://github.com/KhronosGroup/glslang).
- [SPIRV-Headers](https://github.com/KhronosGroup/SPIRV-Headers).
- [SPIRV-Tools](https://github.com/KhronosGroup/SPIRV-Tools).
- [SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross).
- [Vulkan-Headers](https://github.com/KhronosGroup/Vulkan-Headers).

For building the ML SDK for Vulkan® components, run the following command:

```bash
./scripts/build.py
```

If the ML SDK for Vulkan® components are installed in custom locations, specify
their paths by adding the following command line option:

```bash
./scripts/build.py --$COMPONENT_NAME $PATH_TO_COMPONENT
```

COMPONENT_NAME, with the respective default relative locations within
paranthesis, can be:

- vgf-lib (sw/vgf-lib)
- model-converter (sw/model-converter)
- scenario-runner (sw/scenario-runner)
- emulation-layer (sw/emulation-layer)

Similarly, dependencies with custom install locations need to be specifed. For
instance if glslang was installed at `$GLSLANG_REPO_PATH`, use the following:

```bash
./scripts/build.py --glslang-path $GLSLANG_REPO_PATH
```

Upon a sparse checkout, missing components will be skipped during building. Note
that some components have strict dependencies on each other, with VGF Library
being required by Scenario Runner and Model Converter.

The build artifacts can be installed into a specified location by passing the
option `--install` with the required path.

To create an archive with the build artifacts, add the option `--package`. The
archive will be stored in the provided location.

## Build the documentation

To build the documentation, run the following command:

```bash
./scripts/build.py --doc
```

## More command line options

For more command line options, consult the program help:

```bash
./scripts/build.py --help
```

## License

[Apache-2.0](LICENSES/Apache-2.0.txt)

## Security

If you believe you have discovered a security issue please refer to the
[Security Section](SECURITY.md)

## Trademark notice

Arm® is a registered trademarks of Arm Limited (or its subsidiaries) in the US
and/or elsewhere.

Khronos®, Vulkan® and SPIR-V™ are registered trademarks of the
[Khronos® Group](https://www.khronos.org/legal/trademarks).
