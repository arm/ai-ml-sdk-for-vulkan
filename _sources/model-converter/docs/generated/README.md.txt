# ML SDK Model Converter

The ML SDK Model Converter is a command line application that translate TOSA ML
Models to VGF files. A VGF file is a model file containing SPIR-V™ modules and
constants that are required to execute the model through the ML extensions for
Vulkan®. The ML SDK Model Converter supports several different TOSA encodings
as inputs:

- TOSA FlatBuffers
- TOSA MLIR bytecode
- TOSA MLIR textual format

The ML SDK Model Converter can also produce TOSA FlatBuffers from its input,
without performing any conversion.

You can also use the ML SDK Model Converter to check that all tensors specified
in the input model are ranked and have fixed, non-dynamic shapes. If a dynamic
tensor is detected, the program will exit with an error.

The suggested workflow for this tool as part of the ML SDK for Vulkan® is:

1.  A TOSA MLIR file is converted to a VGF file using the ML SDK Model Converter
    (this project).
2.  The generated VGF file and VGF library VGF Dump Tool is used to create a
    JSON scenario template file. The template file is edited with the correct
    filenames and paths.
3.  Using the generated VGF file and scenario file, the ML SDK Scenario Runner
    then dispatches the contained SPIR-V™ modules to the ML extensions for
    Vulkan®.

### Cloning the repository

To clone the ML SDK Model Converter as a stand-alone repository, you can use
regular git clone commands. However, for better management of dependencies and
to ensure everything is placed in the appropriate directories, we recommend
using the `git-repo` tool to clone the repository as part of the ML SDK for
Vulkan® suite. The tool is available
[here](https://gerrit.googlesource.com/git-repo).

For a minimal build and to initialize only the ML SDK Model Converter and its
dependencies, run:

```bash
repo init -u https://github.com/arm/ai-ml-sdk-manifest -g model-converter
```

Alternatively, to initialize the repo structure for the entire ML SDK for
Vulkan®, including the ML SDK Model Converter, run:

```bash
repo init -u https://github.com/arm/ai-ml-sdk-manifest -g all
```

After the repo is initialized, you can fetch the contents with:

```bash
repo sync
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
python <path-to-git-repo>\git-repo\repo sync
```

Using **Git Bash**:

```powershell
cmd.exe "/c reg.exe add \"HKLM\System\CurrentControlSet\Control\FileSystem"" /v LongPathsEnabled /t REG_DWORD /d 1 /f"
git config --global core.longpaths true
git --version # Ensure you are using the Git for Windows, for example 2.50.1.windows.1
git clone <git-repo-tool-url>
python <path-to-git-repo>/git-repo/repo init -u <manifest-url> -g all
python <path-to-git-repo>/git-repo/repo sync
```

Due to a known issue in `git-repo`, nested submodules do not always update as
part of `repo sync` and need to be manually updated, for example:

```bash
cd dependencies/tosa_mlir_translator
git submodule update --init --recursive
```

After the sync command completes successfully, you can find the ML SDK Model
Converter in `<repo_root>/sw/model-converter/`. You can also find all the
dependencies required by the ML SDK Model Converter in
:`<repo_root>/dependencies/`.

### Building the ML SDK Model Converter from source

The build system must have:

- CMake 3.25 or later.
- C/C++ 17 compiler: GCC, or optionally Clang on Linux and MSVC on Windows®.
- Python 3.10 or later. Required python libraries for building are listed in
  `tooling-requirements.txt`.
- Flatbuffers flatc compiler 25.2.10 or later.

The following dependencies are also needed:

- [Argument Parser for Modern C++](https://github.com/p-ranav/argparse).
- [LLVM](https://github.com/llvm/llvm-project).
- [TOSA Serialization Library](https://review.mlplatform.org/plugins/gitiles/tosa/serialization_lib).
- [TOSA MLIR Translator](https://review.mlplatform.org/plugins/gitiles/tosa/tosa_mlir_translator).

For the preferred dependency versions see the manifest file.

### Providing Flatc

There are 3 options for providing the flatc binary and headers.

1.  Using the default path. When the repository is initialized using the repo
    manifest, the flatbuffers source is checked out in
    `<repo-root>/dependencies/flatbuffers/`. The VGF Library cmake scripts
    automatically find and build flatc in this location.

2.  Providing a custom flatc path. If flatc cannot be found in the default
    `<repo-root>/dependencies/flatbuffers` path, you can provide a custom binary
    file path to the build script using the `--flatc-path <path_to_flatc>`
    option, see [Building with the script](#building-with-the-script).

3.  Installing flatc to the system. If flatc cannot be found in the default path
    and no custom path is provided, it will be searched using `PATH`. To install
    flatc to the system and make it available on the searchable `PATH`, see the
    [flatbuffers documentation](https://flatbuffers.dev/). For example, on Linux
    navigate to the flatbuffers checkout location and run the following
    commands:

```bash
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build build --target install
```

### Building with the script

Arm® provides a python build script to make build configuration options easily
discoverable. When the script is run from a git-repo manifest checkout, the
script uses default paths and does not require any additional arguments.
Otherwise the paths to the dependencies must be specified.

To build on Linux, run:

```bash
SDK_PATH="path/to/sdk"
python3 ${SDK_PATH}/sw/scenario-runner/scripts/build.py -j $(nproc) \
    --vgf-lib-path ${SDK_PATH}/sw/vgf-lib \
    --flatbuffers-path ${SDK_PATH}/dependencies/flatbuffers \
    --argparse-path ${SDK_PATH}/dependencies/argparse \
    --tosa-mlir-translator-path ${SDK_PATH}/dependencies/tosa_mlir_translator \
    --external-llvm ${SDK_PATH}/dependencies/llvm-project
```

To build on Windows®, run:

```powershell
$env:SDK_PATH="path\to\sdk"
$cores = [System.Environment]::ProcessorCount
python3 "$env:SDK_PATH\sw\scenario-runner\scripts\build.py" -j $cores `
    --vgf-lib-path "$env:SDK_PATH\sw\vgf-lib" `
    --flatbuffers-path "$env:SDK_PATH\dependencies\flatbuffers" `
    --argparse-path "$env:SDK_PATH\dependencies\argparse" `
    --tosa-mlir-translator-path "$env:SDK_PATH\dependencies\tosa_mlir_translator" `
    --external-llvm "$env:SDK_PATH\dependencies\llvm-project"
```

If the components are in their default locations, it is not necessary to specify
the `--vgf-lib-path`, `--flatbuffers-path`, `--argparse-path`,
`--tosa-mlir-translator-path`, and `--external-llvm` options.

Tests can be enabled and run with `--test` and linting by `--lint`. The
documentation can be built with `--doc`. To build the documentation, sphinx and
doxygen must be installed on the machine.

You can install the project build artifacts into a specified location by passing
the option `--install` with the required path.

To create an archive with the build artifacts option, add `--package`. The
archive will be stored in the provided location."

For more information, see the help output:

```bash
python3 scripts/build.py --help
```

### Usage

To generate a VGF file, run:

```bash
./build/model-converter --input ${INPUT_TOSA} --output ${OUTPUT_VGF}
```

To generate a TOSA flatbuffer file, run:

```bash
./build/model-converter --tosa-flatbuffer --input ${INPUT_TOSA} --output ${OUTPUT_TOSA_FB}
```

For more information, see the help output:

```bash
./build/model-converter --help
```

## Known Limitations

- Usage of the `patches/llvm.patch` file is temporary until the required changes
  can be upstreamed to main LLVM Project
- The emit-debug-info cli option does not produce debug symbols for the
  SPV_ARM_graph and SPIR-V™ extended instructions for TOSA operators in the
  generated SPIR-V™ module.

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
