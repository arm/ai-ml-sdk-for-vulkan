#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright 2024-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from executorch.backends.arm.vgf import VgfCompileSpec
from executorch.backends.arm.vgf import VgfPartitioner
from executorch.exir import EdgeCompileConfig
from executorch.exir import to_edge_transform_and_lower


# Define model
class MaxPoolModel(nn.Module):
    def __init__(self):
        super(MaxPoolModel, self).__init__()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        x = self.pool(x)
        return x


# Generate test input
example_input = torch.randn(1, 3, 64, 64)
np.save("input-0.npy", example_input.numpy())

model = MaxPoolModel().eval()

# Save the VGF model
compile_spec = VgfCompileSpec()
compile_spec.dump_intermediate_artifacts_to(".")

partitioner = VgfPartitioner(compile_spec)

exported_program = torch.export.export_for_training(model, (example_input,))

to_edge_transform_and_lower(
    exported_program,
    partitioner=[partitioner],
    compile_config=EdgeCompileConfig(
        _check_ir_validity=False,
    ),
)
