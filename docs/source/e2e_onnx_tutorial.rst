Converting and deploying an ONNX model tutorial
===============================================

This tutorial demonstrates how to convert and deploy an ONNX model using Torch-MLIR and the ML SDK for Vulkan®.
It walks through model conversion to TOSA MLIR, VGF file generation, and execution using the ML SDK Scenario Runner.

1. Install Torch-MLIR

.. code-block:: bash

    pip install --pre torch-mlir -f https://github.com/llvm/torch-mlir-release/releases/expanded_assets/dev-wheels

2. Download the ONNX Model:

.. code-block:: bash

   curl -LO https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-12.onnx

3. Generate input tensor:

.. code-block:: python

    import numpy
    data = numpy.random.rand(28,28).astype(numpy.float32)
    numpy.save("input-0.npy", data)

4. Convert the Model to TOSA MLIR Bytecode:

Convert the ONNX model to the Torch-MLIR ONNX MLIR dialect:

.. code-block:: bash

    torch-mlir-import-onnx mnist-12.onnx --data-prop --clear-domain -o mnist-12.torch.mlir

Convert the MLIR file to the Torch-MLIR backend dialect:

.. code-block:: bash

    torch-mlir-opt mnist-12.torch.mlir --torch-onnx-to-torch-backend-pipeline \
        --canonicalize -o mnist-12.torch.backend.mlir

Use the Torch-MLIR TOSA backend to convert the backend MLIR to the TOSA MLIR dialect:

.. code-block:: bash

    torch-mlir-opt mnist-12.torch.backend.mlir \
        --pass-pipeline="builtin.module(torch-backend-to-tosa-backend-pipeline{require-full-tosa-conversion})" \
        -o mnist-12.tosa.mlir

5. Generate the VGF File:

.. code-block:: bash

    model-converter --input mnist-12.tosa.mlir --output mnist-12.vgf

6. Run the VGF file with ML SDK Scenario Runner and ML Emulation Layer for Vulkan®

To execute the VGF file refer to :ref:`How to run a VGF file with ML SDK Scenario Runner and ML Emulation Layer for Vulkan®`.

After this executes, the MNIST model output will be stored in :code:`output-0.npy`.
