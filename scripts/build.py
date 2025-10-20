#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright 2024-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
import argparse
import os
import pathlib
import platform
import subprocess
import sys

try:
    import argcomplete
except:
    argcomplete = None

ML_SDK_FOR_VULKAN_DIR = pathlib.Path(__file__).resolve().parents[1]
ML_SDK_FOR_VULKAN_COMPONENTS_DIR = ML_SDK_FOR_VULKAN_DIR / "sw"
DEPENDENCIES_DIR = ML_SDK_FOR_VULKAN_DIR / "dependencies"
CMAKE_TOOLCHAIN_PATH = ML_SDK_FOR_VULKAN_DIR / "cmake" / "toolchain"


class Builder:
    """
    A class that builds all ML SDK for Vulkan® components

    Parameters
    ----------
    args: 'dict'
        Dictionary with arguments to build the ML SDK for Vulkan® components
    """

    def __init__(self, args) -> None:
        self.prefix_path = args.prefix_path
        self.build_dir = args.build_dir
        self.build_type = args.build_type

        self.model_converter = args.model_converter
        self.scenario_runner = args.scenario_runner
        self.vulkan_headers_path = args.vulkan_headers_path
        self.glslang_path = args.glslang_path
        self.spirv_headers_path = args.spirv_headers_path
        self.spirv_tools_path = args.spirv_tools_path
        self.spirv_cross_path = args.spirv_cross_path
        self.vgf_lib = args.vgf_lib
        self.emulation_layer = args.emulation_layer
        self.gtest_path = args.gtest_path
        self.argparse = args.argparse
        self.flatbuffers = args.flatbuffers
        self.json = args.json
        self.tosa_mlir_translator = args.tosa_mlir_translator
        self.llvm = args.external_llvm
        self.skip_llvm_patch = args.skip_llvm_patch
        self.threads = args.threads
        self.target_platform = args.target_platform

        self.doc = args.doc
        self.install = args.install

        self.package_dir = args.package_dir or self.build_dir
        self.package_tgz = "tgz" in args.package_type
        self.package_zip = "zip" in args.package_type

    def setup_platform_build(self, cmake_setup_cmd):
        system = platform.system()
        if self.target_platform == "host":
            if system == "Linux":
                cmake_setup_cmd.append(
                    f"-DCMAKE_TOOLCHAIN_FILE={CMAKE_TOOLCHAIN_PATH / 'gcc.cmake'}"
                )
                return True
            if system == "Darwin":
                cmake_setup_cmd.append(
                    f"-DCMAKE_TOOLCHAIN_FILE={CMAKE_TOOLCHAIN_PATH / 'clang.cmake'}"
                )
                return True
            if system == "Windows":
                cmake_setup_cmd.append(
                    f"-DCMAKE_TOOLCHAIN_FILE={CMAKE_TOOLCHAIN_PATH / 'windows-msvc.cmake'}"
                )
                cmake_setup_cmd.append("-DMSVC=ON")
                return True
            print(f"Unsupported host platform {system}", file=sys.stderr)
            return False
        if self.target_platform == "linux-clang":
            if system != "Linux":
                print(
                    f"ERROR: target {self.target_platform} only supported on Linux. Host platform {system}",
                    file=sys.stderr,
                )
                return False
            cmake_setup_cmd.append(
                f"-DCMAKE_TOOLCHAIN_FILE={CMAKE_TOOLCHAIN_PATH / 'clang.cmake'}"
            )
            return True

    def generate_cmake_package(self, generator):
        cmake_package_cmd = [
            "cpack",
            "--config",
            f"{self.build_dir}/CPackConfig.cmake",
            "-C",
            self.build_type,
            "-G",
            generator,
            "-B",
            self.package_dir,
            "-D",
            "CPACK_INCLUDE_TOPLEVEL_DIRECTORY=OFF",
        ]
        subprocess.run(cmake_package_cmd, check=True)

    def run(self):
        cmake_setup_cmd = [
            "cmake",
            "-S",
            str(ML_SDK_FOR_VULKAN_DIR),
            "-B",
            self.build_dir,
            f"-DCMAKE_BUILD_TYPE={self.build_type}",
            f"-DARGPARSE_PATH={self.argparse}",
            f"-DFLATBUFFERS_PATH={self.flatbuffers}",
            f"-DJSON_PATH={self.json}",
            f"-DGLSLANG_PATH={self.glslang_path}",
            f"-DSPIRV_HEADERS_PATH={self.spirv_headers_path}",
            f"-DSPIRV_TOOLS_PATH={self.spirv_tools_path}",
            f"-DSPIRV_CROSS_PATH={self.spirv_cross_path}",
            f"-DVULKAN_HEADERS_PATH={self.vulkan_headers_path}",
            f"-DLLVM_PATH={self.llvm}",
            f"-DTOSA_MLIR_TRANSLATOR_PATH={self.tosa_mlir_translator}",
            f"-DML_SDK_MODEL_CONVERTER_PATH={self.model_converter}",
            f"-DML_SDK_SCENARIO_RUNNER_PATH={self.scenario_runner}",
            f"-DML_SDK_VGF_LIB_PATH={self.vgf_lib}",
            f"-DML_SDK_EMULATION_LAYER_PATH={self.emulation_layer}",
        ]
        if not self.setup_platform_build(cmake_setup_cmd):
            return 1

        if self.package_tgz or self.package_zip:
            cmake_setup_cmd.append(f"-DML_SDK_GENERATE_CPACK=ON")

        if self.skip_llvm_patch:
            cmake_setup_cmd.append("-DMODEL_CONVERTER_APPLY_LLVM_PATCH=OFF")

        if self.prefix_path:
            cmake_setup_cmd.append(f"-DCMAKE_PREFIX_PATH={self.prefix_path}")

        if self.doc:
            cmake_setup_cmd.append("-DML_SDK_BUILD_DOCS=ON")

        cmake_setup_cmd.append(f"-DGTEST_PATH={self.gtest_path}")

        cmake_build_cmd = [
            "cmake",
            "--build",
            self.build_dir,
            "-j",
            str(self.threads),
            "--config",
            self.build_type,
        ]

        try:
            subprocess.run(cmake_setup_cmd, check=True)
            subprocess.run(cmake_build_cmd, check=True)

            if self.install:
                cmake_install_cmd = [
                    "cmake",
                    "--install",
                    self.build_dir,
                    "--prefix",
                    self.install,
                    "--config",
                    self.build_type,
                ]
                subprocess.run(cmake_install_cmd, check=True)

            if self.package_tgz:
                self.generate_cmake_package("TGZ")

            if self.package_zip:
                self.generate_cmake_package("ZIP")

        except ValueError as e:
            print(
                f"Exception caught in documentation build script: {e}", file=sys.stderr
            )
            return 1

        return 0


def parse_arguments():
    parser = argparse.ArgumentParser(description="Build ML SDK for Vulkan®")
    parser.add_argument(
        "--prefix-path",
        help="Path to prefix directory.",
    )
    parser.add_argument(
        "--build-dir",
        help="Name of folder where to build ML SDK for Vulkan® components. Default: build",
        default=f"{ML_SDK_FOR_VULKAN_DIR / 'build'}",
    )
    parser.add_argument(
        "--build-type",
        help="Type of build to perform. Default: %(default)s",
        default="Release",
    )
    parser.add_argument(
        "--threads",
        "-j",
        type=int,
        help="Number of threads to use for building. Default: %(default)s",
        default=16,
    )
    parser.add_argument(
        "--model-converter",
        help="Path to ML SDK Model Converter repo",
        default=f"{ML_SDK_FOR_VULKAN_COMPONENTS_DIR / 'model-converter'}",
    )
    parser.add_argument(
        "--scenario-runner",
        help="Path to ML SDK Scenario Runner repo",
        default=f"{ML_SDK_FOR_VULKAN_COMPONENTS_DIR / 'scenario-runner'}",
    )
    parser.add_argument(
        "--vulkan-headers-path",
        help="Path to Vulkan headers folder",
        default=f"{DEPENDENCIES_DIR /'Vulkan-Headers'}",
    )
    parser.add_argument(
        "--target-platform",
        help="Specify the target build platform",
        choices=["host", "linux-clang"],
        default="host",
    )
    parser.add_argument(
        "--glslang-path",
        help="Path to Glslang repo",
        default=f"{DEPENDENCIES_DIR / 'glslang'}",
    )
    parser.add_argument(
        "--spirv-headers-path",
        help="Path to SPIR-V headers repo",
        default=f"{DEPENDENCIES_DIR / 'SPIRV-Headers'}",
    )
    parser.add_argument(
        "--spirv-tools-path",
        help="Path to SPIR-V Tools repo",
        default=f"{DEPENDENCIES_DIR / 'SPIRV-Tools'}",
    )
    parser.add_argument(
        "--spirv-cross-path",
        help="Path to SPIR-V Cross repo",
        default=f"{DEPENDENCIES_DIR / 'SPIRV-Cross'}",
    )
    parser.add_argument(
        "--vgf-lib",
        help="Path to ML SDK VGF Library repo",
        default=f"{ML_SDK_FOR_VULKAN_COMPONENTS_DIR / 'vgf-lib'}",
    )
    parser.add_argument(
        "--emulation-layer",
        help="Path to Vulkan Emulation Layer",
        default=f"{ML_SDK_FOR_VULKAN_COMPONENTS_DIR / 'emulation-layer'}",
    )
    parser.add_argument(
        "--argparse",
        help="Path to Argparse",
        default=f"{DEPENDENCIES_DIR / 'argparse'}",
    )
    parser.add_argument(
        "--flatbuffers",
        help="Path to FlatBuffers",
        default=f"{DEPENDENCIES_DIR / 'flatbuffers'}",
    )
    parser.add_argument(
        "--json",
        help="Path to JSON",
        default=f"{DEPENDENCIES_DIR / 'json'}",
    )
    parser.add_argument(
        "--tosa-mlir-translator",
        help="Path to TOSA MLIR Translator",
        default=f"{DEPENDENCIES_DIR / 'tosa_mlir_translator'}",
    )
    parser.add_argument(
        "--external-llvm",
        help="Path to the LLVM repo and build",
        default=f"{DEPENDENCIES_DIR / 'llvm-project'}",
    )
    parser.add_argument(
        "--skip-llvm-patch",
        help="Skip applying LLVM patch. Default: %(default)s",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--gtest-path",
        help="Path to gtest repo",
        default=f"{DEPENDENCIES_DIR / 'googletest'}",
    )
    parser.add_argument(
        "--doc",
        help="Build documentation. Default: %(default)s",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--install",
        help="Install build artifacts into a provided location",
    )
    parser.add_argument(
        "--package-dir",
        help="Specify location for packages to be created. Default path is the build directory",
        default="",
    )
    parser.add_argument(
        "--package-type",
        choices=["zip", "tgz"],
        action="append",
        help="Create a package of a certain type",
        default=[],
    )
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()

    return args


def main():
    builder = Builder(parse_arguments())
    sys.exit(builder.run())


if __name__ == "__main__":
    main()
