Converting and deploying a PyTorch model tutorial
=================================================

.. note::
    For details on platform support, installation, and usage of ExecuTorch, please refer to the official documentation:

    - `Getting Started with ExecuTorch <https://docs.pytorch.org/executorch/stable/getting-started.html>`_
    - `Arm® Backend Tutorial <https://github.com/pytorch/executorch/blob/main/docs/source/tutorial-arm.md>`_

This tutorial describes how to convert and deploy a PyTorch model using the |SDK_project|.
In this tutorial, we generate a sample PyTorch file with a single MaxPool2D operation
to demonstrate each step of the end-to-end workflow.

ExecuTorch can be installed via prebuilt wheels:

.. note::
    Here we are installing from a developmental wheel.
    In the future, replace it with an official release.

.. code-block:: bash

    pip install --upgrade --pre -f https://download.pytorch.org/whl/nightly/executorch/ "executorch==1.0.0.dev20250916"

Download the ExecuTorch repo, and install the required dependencies using the script.

.. note::
    In order to run the setup script, Git username and email need to be configured.
    For example:

    .. code-block:: bash

        git config --global user.name "Your Name"
        git config --global user.email "you@example.com"

.. code-block:: bash

    git clone https://github.com/pytorch/executorch.git
    ./executorch/examples/arm/setup.sh --disable-ethos-u-deps

1. Add the ML SDK Model Converter to :code:`PATH`:

The ExecuTorch backend relies on the ML SDK Model Converter.

.. code-block:: bash

    export PATH=/path/containing/model-converter/:$PATH
    which model-converter

This should print out the path to the `model-converter` binary.

2. Run the following python script to create a PyTorch model for a single MaxPool2D operation.

.. literalinclude:: assets/MaxPool2DModel.py
    :language: python

.. code-block:: bash

   python MaxPool2DModel.py

This generates a VGF file :code:`${NAME}.vgf` in the current working directory,
where the tool generates :code:`${NAME}`.
A matching example input is also generated in the same directory for testing.

3. Run the VGF file with ML SDK Scenario Runner and ML Emulation Layer for Vulkan®

To execute the VGF file refer to :ref:`How to run a VGF file with ML SDK Scenario Runner and ML Emulation Layer for Vulkan®`.
