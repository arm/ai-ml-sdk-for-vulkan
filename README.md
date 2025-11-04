# ML SDK for Vulkan®

The ML SDK for Vulkan® is an SDK to facilitate the development of projects
using the ML extensions for Vulkan®.

## Content

This repository contains scripts to facilitate building all the ML SDK for
Vulkan® components, utilities, and documentation.

## Cloning the repository

To clone the ML SDK for Vulkan® repository, you can use the
[Repo tool](https://gerrit.googlesource.com/git-repo). Cloning using Repo tool
ensures all components and dependencies are fetched and in a suitable default
location on the file system. To initialize the repo structure for the entire ML
SDK for Vulkan®, including all components, run:

```bash
repo init -u https://github.com/arm/ai-ml-sdk-manifest.git -g all
```

After the repository is initialized, fetch the contents with:

```bash
repo sync --no-clone-bundle
```

### Cloning on Windows®

To ensure nested submodules do not exceed the maximum long path length, you must
enable long paths on Windows®, and you must clone close to the root directory
or use a symlink. Make sure to use Git for Windows.

Using **PowerShell**:

```powershell
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
git config --global core.longpaths true
git --version # Ensure you are using Git for Windows, for example 2.50.1.windows.1
git clone <git-repo-tool-url>
python <path-to-git-repo>\git-repo\repo init -u <manifest-url> -g all
python <path-to-git-repo>\git-repo\repo sync --no-clone-bundle
```

Using **Git Bash**:

```bash
cmd.exe "/c reg.exe add \"HKLM\System\CurrentControlSet\Control\FileSystem"" /v LongPathsEnabled /t REG_DWORD /d 1 /f"
git config --global core.longpaths true
git --version # Ensure you are using the Git for Windows, for example 2.50.1.windows.1
git clone <git-repo-tool-url>
python <path-to-git-repo>/git-repo/repo init -u <manifest-url> -g all
python <path-to-git-repo>/git-repo/repo sync --no-clone-bundle
```

Due to a known issue in `git-repo`, nested submodules do not always update as
part of `repo sync` and need to be manually updated, for example:

```bash
cd dependencies/tosa_mlir_translator
git submodule update --init --recursive
```

After the sync command completes successfully, you can find the individual
components in `<repo_root>/sw/`. You can also find all the required dependencies
in `<repo_root>/dependencies/`.

You can initialize the repository with only the components that you need. This
also fetches only the dependencies required by the selected components. The
`-g all` in the preceding initialization command is equivalent to
`-g model-converter vgf-lib scenario-runner emulation-layer`. Some components
may also force other components to be included. For example, `scenario-runner`
automatically includes `vgf-lib` because `vgf-lib` is required.

Although we do not recommend this method, you can check out the components using
`git clone` commands directly. This requires checking out each component and
dependency manually. The custom location to each dependency needs to be
configured explicitly by options to the build command for each component which
results in a more complicated workflow.

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
- Doxygen 1.9.1 or later. (When building documentation)

The following dependencies are also needed:

- [Argument Parser for Modern C++](https://github.com/p-ranav/argparse).
- [LLVM](https://github.com/llvm/llvm-project).
- [TOSA Serialization Library](https://gitlab.arm.com/tosa/tosa-serialization).
- [TOSA MLIR Translator](https://gitlab.arm.com/tosa/tosa-mlir-translator).
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

The ML SDK for Vulkan® is distributed under the software licenses in LICENSES
directory.

## Trademark notice

Arm® is a registered trademarks of Arm Limited (or its subsidiaries) in the US
and/or elsewhere.

Khronos®, Vulkan® and SPIR-V™ are registered trademarks of the
[Khronos® Group](https://www.khronos.org/legal/trademarks).
