Converting and deploying a TFLite model tutorial
================================================

This tutorial demonstrates how to convert and deploy a TFLite model
using the TOSA converter for TFLite and the ML SDK for Vulkan®.
It walks through model conversion to TOSA MLIR, VGF file generation, and execution using the ML SDK Scenario Runner.

1. Install the TOSA converter for TFLite:

The repo is available at: `TOSA converter for TFLite <https://gitlab.arm.com/tosa/tosa-converter-for-tflite>`_.

To install the tool, run:

.. code-block:: bash

    pip install "tosa-converter-for-tflite==2025.11.0"

2. Download the TFLite Model:

In this tutorial, we will use the SESR (super-efficient super resolution) model from the `Arm® Model Zoo <https://github.com/Arm-Examples/ML-zoo>`_.
To clone the entire Arm® Model Zoo repository into your current working directory, run:

.. code-block:: bash

    git clone https://github.com/Arm-Examples/ML-zoo.git

The model includes both the quantized `.tflite` file and corresponding `.npy` input/output test data, which we will use in later steps.

3. Convert the Model to TOSA MLIR Bytecode:

Run the following command to convert the SESR model from TFLite to TOSA in the form of MLIR bytecode:

.. code-block:: bash

    tosa-converter-for-tflite ./ML-zoo/models/superresolution/SESR/tflite_int8/SESR_1080p_to_4K_withD2S_full_int8.tflite \
        -o SESR_1080p_to_4K_withD2S_full_int8.mlirbc

4. Generate the VGF File:

Similarly as for deploying the PyTorch files (:ref:`Converting and deploying a PyTorch model tutorial`),
to generate the VGF file and Scenario Template, use the TOSA MLIR bytecode file:

.. code-block:: bash

    model-converter --input SESR_1080p_to_4K_withD2S_full_int8.mlirbc --output SESR_1080p_to_4K_withD2S_full_int8.vgf

3. Run the VGF file with ML SDK Scenario Runner and ML Emulation Layer for Vulkan®

To execute the VGF file refer to :ref:`How to run a VGF file with ML SDK Scenario Runner and ML Emulation Layer for Vulkan®`.

After the run, the contents of :code:`ML-zoo/models/superresolution/SESR/tflite_int8/testing_output/net_output/0.npy`
and :code:`output-0.npy` should be identical.

To verify the output matches the reference output, save the following script into :code:`compare_numpy.py`:

.. literalinclude:: ../generated/scripts/compare_numpy.py
    :language: python

Then run the following command:

.. code-block:: bash

    python3 compare_numpy.py ML-zoo/models/superresolution/SESR/tflite_int8/testing_output/net_output/0.npy output-0.npy

An exit status of 0 indicates that the contents of the two files are identical.
