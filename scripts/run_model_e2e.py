#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright 2024-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
import argparse
import pathlib
import shutil
import subprocess

try:
    import argcomplete
except:
    argcomplete = None

SDK_DIR = pathlib.Path(__file__).resolve().parent / ".."
SDK_COMPONENTS_DIR = SDK_DIR / ".."


class ModelRunner:
    """
    A class that runs the input model end-to-end using ML SDK for Vulkan®.

    Parameters
    ----------
    args : 'dict'
        Dictionary with arguments to run tests.
    """

    def __init__(self, args) -> None:
        self.out_dir = pathlib.Path(args.out_dir)
        self.model_filename = args.model
        self.inputs = args.inputs
        self.outputs = args.outputs
        self.shaders = args.shaders
        self.shape_override = args.shape_override
        self.scenario_runner_path = args.scenario_runner_path
        self.model_converter_path = args.model_converter_path
        self.vgf_dump_path = args.vgf_dump_path

    def run(self):
        """Runs the steps to convert the TOSA model to VGF and execute the ML SDK Scenario Runner"""
        try:
            self.out_dir.mkdir(parents=True, exist_ok=True)
            for file in [self.model_filename] + self.inputs + self.shaders:
                shutil.copy(file, self.out_dir)

            self.run_model_converter()
            self.generate_scenario_json()
            self.run_scenario_runner()

        except Exception as e:
            print(f"An error occurred during execution: {e}")
            return 1

        return 0

    def run_model_converter(self):
        """Run ML SDK Model Converter to convert Tosa MLIR to VGF"""
        self.vgf_filename = self.out_dir.joinpath(self.model_filename).with_suffix(
            ".vgf"
        )
        cmd = [
            self.model_converter_path,
            "--input",
            self.model_filename,
            "--output",
            self.vgf_filename,
            "--require-static-shape",
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command '{cmd}' failed with error: {e}")

    def run_scenario_runner(self):
        """Execute ML SDK Scenario Runner"""
        try:
            subprocess.run(
                [
                    self.scenario_runner_path,
                    "--scenario",
                    self.scenario_filename.name,
                ],
                cwd=self.out_dir,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Scenario Runner execution failed with error: {e}")

    def generate_scenario_json(self):
        """Create scenario JSON template using vgf_dump and replace template names with actual scenario files"""
        self.scenario_filename = self.out_dir.joinpath(self.model_filename).with_suffix(
            ".json"
        )

        template_replacements = []
        for i, input_name in enumerate(self.inputs):
            template_replacements.append(
                (f"TEMPLATE_PATH_TENSOR_INPUT_{i}", input_name)
            )

        for i, output_name in enumerate(self.outputs):
            template_replacements.append(
                (f"TEMPLATE_PATH_TENSOR_OUTPUT_{i}", output_name)
            )

        for i, shader_name in enumerate(self.shaders):
            template_replacements.append(
                (f"TEMPLATE_PATH_SHADER_GLSL_{i}", shader_name)
            )

        cmd = [
            self.vgf_dump_path,
            "--input",
            self.vgf_filename,
            "--output",
            self.scenario_filename,
            "--scenario-template",
        ]
        try:
            subprocess.run(cmd, check=True)
            scenario = self.scenario_filename.read_text()
            for old, new in template_replacements:
                scenario = scenario.replace(old, new)
            self.scenario_filename.write_text(scenario)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate JSON scenario with error: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        help="Path to the TOSA model file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--inputs",
        help="Space separated list of model input files",
        type=str,
        nargs="+",
        required=True,
    )
    parser.add_argument(
        "--outputs",
        help="Space separated list of model output files",
        type=str,
        nargs="+",
        required=True,
    )
    parser.add_argument(
        "--shaders",
        help="Space separated list of shader files used in the model",
        type=str,
        nargs="+",
        default=[],
    )
    parser.add_argument(
        "--out-dir",
        help="Name of folder where to generate the output files.",
        type=str,
        default="out",
    )
    parser.add_argument(
        "--scenario-runner-path",
        help="Path to the ML SDK Scenario Runner binary",
        type=str,
        default=f"{SDK_COMPONENTS_DIR / 'ml-sdk-scenario-runner' /'build' / 'scenario-runner'}",
    )
    parser.add_argument(
        "--model-converter-path",
        help="Path to the ML SDK Model Converter binary",
        type=str,
        default=f"{SDK_COMPONENTS_DIR / 'ml-sdk-model-converter' /'build' / 'model-converter'}",
    )
    parser.add_argument(
        "--vgf-dump-path",
        help="Path to the VGF dump binary",
        type=str,
        default=f"{SDK_COMPONENTS_DIR / 'ml-sdk-vgf-lib' /'build' / 'vgf_dump' / 'vgf_dump'}",
    )
    return parser.parse_args()


def main():
    runner = ModelRunner(parse_arguments())
    exit(runner.run())


if __name__ == "__main__":
    main()
