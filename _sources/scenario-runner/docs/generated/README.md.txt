# ML SDK Scenario Runner

The Scenario Runner is an application that executes shader and neural network
graph workloads through Vulkan® or the ML extensions for Vulkan®. The Scenario
Runner acts as a validation and performance exploration vehicle. The Scenario
Runner also acts as a mechanism to define test-cases called scenarios in a
declarative way via a JSON description. The Scenario Runner can parse the JSON,
load the input stimulus that is described in the JSON, execute the scenario and
produce output artifacts.

### Cloning the repository

To clone the ML SDK Scenario Runner as a stand-alone repository, you can use
regular git clone commands. However, for better management of dependencies and
to ensure everything is placed in the appropriate directories, we recommend
using the `git-repo` tool to clone the repository as part of the ML SDK for
Vulkan® suite. The tool is available
[here](https://gerrit.googlesource.com/git-repo).

For a minimal build and to initialize only the Scenario Runner and its
dependencies, run:

```bash
repo init -u https://github.com/arm/ai-ml-sdk-manifest -g scenario-runner
```

Alternatively, to initialize the repo structure for the entire ML SDK for
Vulkan®, including the Scenario Runner, run:

```bash
repo init -u https://github.com/arm/ai-ml-sdk-manifest -g all
```

Once the repo is initialized, you can fetch the contents:

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

```bash
cmd.exe "/c reg.exe add \"HKLM\System\CurrentControlSet\Control\FileSystem"" /v LongPathsEnabled /t REG_DWORD /d 1 /f"
git config --global core.longpaths true
git --version # Ensure you are using the Git for Windows, for example 2.50.1.windows.1
git clone <git-repo-tool-url>
python <path-to-git-repo>/git-repo/repo init -u <manifest-url> -g all
python <path-to-git-repo>/git-repo/repo sync
```

After the sync command completes successfully, you can find the ML SDK Scenario
Runner in `<repo_root>/sw/scenario-runner/`. You can also find all the
dependencies required by the ML SDK Scenario Runner in
`<repo_root>/dependencies/`.

### Building Scenario Runner from source

The build system must have:

- CMake 3.25 or later.
- C/C++ 17 compiler: GCC, or optionally Clang on Linux and MSVC on Windows®.
- Python 3.10 or later. Required python libraries for building are listed in
  `tooling-requirements.txt`.
- Flatbuffers flatc compiler 25.2.10 or later.

The following dependencies are also needed:

- [Argument Parser for Modern C++](https://github.com/p-ranav/argparse).
- [glslang](https://github.com/KhronosGroup/glslang).
- [JSON for Modern C++](https://github.com/nlohmann/json).
- [SPIRV-Headers](https://github.com/KhronosGroup/SPIRV-Headers).
- [SPIRV-Tools](https://github.com/KhronosGroup/SPIRV-Tools).
- [Vulkan-Headers](https://github.com/KhronosGroup/Vulkan-Headers).
- [GoogleTest](https://github.com/google/googletest). Optional, for testing.

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

To build on Linux, run the following command:

```bash
SDK_PATH="path/to/sdk"
python3 ${SDK_PATH}/sw/scenario-runner/scripts/build.py -j $(nproc) \
    --flatbuffers-path ${SDK_PATH}/dependencies/flatbuffers \
    --argparse-path ${SDK_PATH}/dependencies/argparse \
    --json-path ${SDK_PATH}/dependencies/json \
    --vulkan-headers-path ${SDK_PATH}/dependencies/Vulkan-Headers \
    --glslang-path ${SDK_PATH}/dependencies/glslang \
    --spirv-headers-path ${SDK_PATH}/dependencies/SPIRV-Headers \
    --spirv-tools-path ${SDK_PATH}/dependencies/SPIRV-Tools \
    --vgf-lib-path ${SDK_PATH}/sw/vgf-lib \
    --gtest-path ${SDK_PATH}/dependencies/googletest
```

To build on Windows®, run the following command:

```powershell
$env:SDK_PATH="path\to\sdk"
$cores = [System.Environment]::ProcessorCount
python "$env:SDK_PATH\sw\scenario-runner\scripts\build.py" -j $cores  `
    --flatbuffers-path "$env:SDK_PATH\dependencies\flatbuffers" `
    --argparse-path "$env:SDK_PATH\dependencies\argparse" `
    --json-path "$env:SDK_PATH\dependencies\json" `
    --vulkan-headers-path "$env:SDK_PATH\dependencies\Vulkan-Headers" `
    --glslang-path "$env:SDK_PATH\dependencies\glslang" `
    --spirv-headers-path "$env:SDK_PATH\dependencies\SPIRV-Headers" `
    --spirv-tools-path "$env:SDK_PATH\dependencies\SPIRV-Tools" `
    --vgf-lib-path "$env:SDK_PATH\sw\vgf-lib" `
    --gtest-path "$env:SDK_PATH\dependencies\googletest"
```

To cross compile for AArch64 architecture, you can add the following option:

```bash
SDK_PATH="path/to/sdk"
python3 $SDK_PATH/sw/scenario-runner/scripts/build.py -j $(nproc) \
    --flatbuffers-path ${SDK_PATH}/dependencies/flatbuffers \
    --argparse-path ${SDK_PATH}/dependencies/argparse \
    --json-path ${SDK_PATH}/dependencies/json \
    --vulkan-headers-path ${SDK_PATH}/dependencies/Vulkan-Headers \
    --glslang-path ${SDK_PATH}/dependencies/glslang \
    --spirv-headers-path ${SDK_PATH}/dependencies/SPIRV-Headers \
    --spirv-tools-path ${SDK_PATH}/dependencies/SPIRV-Tools \
    --vgf-lib-path ${SDK_PATH}/sw/vgf-lib \
    --gtest-path ${SDK_PATH}/dependencies/googletest \
    --target-platform aarch64
```

To enable and run tests, use the `--test` flag. To lint the tests, use the
`--lint` flag. To build the documentation, use the `--doc` flag. To build the
documentation, you must have `sphinx` and `doxygen` installed on your machine.

You can install the build artifacts for this project into a specified location.
To install the build artifacts, pass the `--install` option with the required
path.

To create an archive with the build artifacts, you must add `--package`. The
archive is stored in the provided location.

For more command line options, consult the program help:

```bash
python3 $SDK_PATH/sw/scenario-runner/scripts/build.py --help
```

### Usage

To run a scenario file, use the following command:

```bash
./scenario-runner --scenario ${SCENARIO_JSON_FILE}
```

Where:

- `--scenario`: File to load the scenario from. The file must be in JSON format.
  If the resources in the SCENARIO_JSON_FILE are not specified with absolute
  paths, their relative paths will be resolved against the parent directory of
  the SCENARIO_JSON_FILE.

For more details, see the help output:

```bash
./scenario-runner --help
```

## Known Limitations

- Resources created with `Optimal` tiling cannot be used with memory aliasing.

## License

[Apache-2.0](LICENSES/Apache-2.0.txt)

## Security

If you have found a security issue, see [Security Section](SECURITY.md)

## Trademark notice

Arm® is a registered trademarks of Arm Limited (or its subsidiaries) in the US
and/or elsewhere.

Khronos®, Vulkan® and SPIR-V™ are registered trademarks of the
[Khronos® Group](https://www.khronos.org/legal/trademarks).
