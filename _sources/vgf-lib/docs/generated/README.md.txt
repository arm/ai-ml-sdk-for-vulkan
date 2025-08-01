# ML SDK VGF Library

The VGF Library is a library that encodes and decodes VGF files. The VGF format
covers the entire model use cases. These use cases can be a combination of
SPIR-V™ module binary data, their constants, and compute shaders. The library
provides a suite of APIs and tools for working with VGF files. The library
includes the following:

- C++ encoder API
- C++ decoder API
- C decoder API
- VGF dumping tool: `vgf_dump`

The encoder provides a simple, high-level API for building up VGF files. It is
designed for easy integration into offline tooling.

The decoder is designed to be lightweight and to be included in high-performing
programs, for example game engines. Therefore, the decoder does not allocate any
dynamic memory on its own. To maintain full control, you must allocate the
memory required and provide it to this library. To minimize copies and peak
memory requirements, the format also supports mmap read operations on the
contents.

VGF Library also provides a dumping tool which is called vgf_dump. vgf_dump
prints the content of a VGF file into human-readable JSON format. You can also
use vgf_dump to generate scenario file templates. You can use the scenario file
templates with the
[Scenario Runner](https://github.com/arm/ai-ml-sdk-scenario-runner) tool.

### Building VGF Library from source

The build system must have:

- CMake 3.22 or later.
- C/C++ 17 compiler: GCC, or optionally Clang on Linux and MSVC on Windows®.
- Python 3.10 or later. Required python libraries for building are listed in
  `tooling-requirements.txt`.
- Flatbuffers flatc compiler 25.2.10 or later.

The following dependencies are also needed:

- [Argument Parser for Modern C++](https://github.com/p-ranav/argparse).
- [JSON for Modern C++](https://github.com/nlohmann/json).
- [pybind11](https://github.com/pybind/pybind11).
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

<a name="building-with-the-script"></a>

### Building with the script

To make the build configuration options easily discoverable, we provide a python
build script. When you run the script from a git-repo manifest checkout, the
script uses default paths and does not require any additional arguments. If you
do not use the script, you must specify paths to the dependencies.

To build on the current platform, for example on Linux or Windows®, run the
following command:

```bash
python3 $SDK_PATH/sw/vgf-lib/scripts/build.py -j $(nproc)
```

To cross compile for AArch64 architecture, add the following option:

```bash
python3 $SDK_PATH/sw/vgf-lib/scripts/build.py -j $(nproc) --target-platform aarch64
```

To enable and run tests, use the `--test` option. To lint the tests, use the
`--lint` option. To build the documentation, use the `--doc` option. To build
the documentation, you must have `sphinx` and `doxygen` installed on your
machine.

You can install the build artifacts for this project into a specified location.
To install the build artifacts, pass the `--install` option with the required
path.

To create an archive with the build artifacts option, you must add the
`--package` option. The archive is stored in the provided location.

For more command line options, see the help output:

```bash
python3 $SDK_PATH/sw/vgf-lib/scripts/build.py --help
```

## License

[Apache-2.0](LICENSES/Apache-2.0.txt)

## Security

If you have found a security issue, see the [Security Section](SECURITY.md)

## Trademark notice

Arm® is a registered trademarks of Arm Limited (or its subsidiaries) in the US
and/or elsewhere.

Khronos®, Vulkan® and SPIR-V™ are registered trademarks of the
[Khronos® Group](https://www.khronos.org/legal/trademarks).
