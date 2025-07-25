#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright 2024-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
import torch
import torch.nn as nn
import torch.nn.functional as F
from executorch.backends.arm.arm_backend import ArmCompileSpecBuilder
from executorch.backends.arm.tosa_partitioner import TOSAPartitioner
from executorch.exir import EdgeCompileConfig
from executorch.exir import to_edge_transform_and_lower

image_height = 480
image_width = 640

# Sobel filter definitions
def get_sobel_filters():
    x_filter = torch.tensor(
        [[-1, -2, 0, 2, 1]], dtype=torch.float32
    ).t() @ torch.tensor([[1, 4, 6, 4, 1]], dtype=torch.float32)
    y_filter = torch.tensor([[1, 4, 6, 4, 1]], dtype=torch.float32).t() @ torch.tensor(
        [[-1, -2, 0, 2, 1]], dtype=torch.float32
    )
    return x_filter.view(1, 1, 5, 5), y_filter.view(1, 1, 5, 5)


# Define model
class SobelFilteringModel(nn.Module):
    def __init__(self):
        super(SobelFilteringModel, self).__init__()
        x_filter, y_filter = get_sobel_filters()

        self.conv_x = nn.Conv2d(4, 1, 5, bias=False)
        self.conv_y = nn.Conv2d(4, 1, 5, bias=False)

        with torch.no_grad():
            self.conv_x.weight.zero_()
            self.conv_y.weight.zero_()
            self.conv_x.weight[:, :3, :, :] = x_filter
            self.conv_y.weight[:, :3, :, :] = y_filter

    def forward(self, x):
        gx = self.conv_x(x)
        gy = self.conv_y(x)
        return torch.sqrt(gx**2 + gy**2)


# Generate test input
example_input = torch.randn(1, 4, image_height, image_width)

model = SobelFilteringModel().eval()

# Save model intermediates
compile_spec = (
    ArmCompileSpecBuilder()
    .tosa_compile_spec("TOSA-1.0+FP")
    .dump_intermediate_artifacts_to(".")
    .build()
)
partitioner = TOSAPartitioner(compile_spec)

exported_program = torch.export.export_for_training(model, (example_input,))

to_edge_transform_and_lower(
    exported_program,
    partitioner=[partitioner],
    compile_config=EdgeCompileConfig(
        _check_ir_validity=False,
    ),
)
