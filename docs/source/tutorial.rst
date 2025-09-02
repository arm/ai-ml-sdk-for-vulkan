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

    pip install --upgrade --pre -f https://download.pytorch.org/whl/nightly/executorch/ "executorch==0.8.0.dev20250811"

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

3. Use the VGF Dump Tool to generate a Scenario Template. To run a scenario on the ML SDK Scenario Runner,
you must have a scenario specification in the form of a JSON file. Use the VGF file that was generated in the previous
step and pass it to the VGF Dump Tool:

.. code-block:: bash

    $vgf_dump --input ${NAME}.vgf --output scenario.json --scenario-template

.. note::
   For more information about VGF Library and the VGF Dump Tool, see: :ref:`ML SDK VGF Library`


4. The generated :code:`scenario.json` file contains placeholder names for input and output bindings
   for the scenario. You must replace these names with the actual input and output filenames that will
   be used when running the scenario. In the example :code:`scenario.json` file generated in the preceding step:

   a. Replace the name TEMPLATE_PATH_TENSOR_INPUT_0 with the actual input file :code:`input-0.npy`.

   b. Replace the name TEMPLATE_PATH_TENSOR_OUTPUT_0 with the actual output filename :code:`output-0.npy`.

.. note::
    For more information about the test description format, see:
    :ref:`JSON Test Description Specification`.


5. Run the ML SDK Scenario Runner on the ML Emulation Layer for Vulkan®:

.. code-block:: bash

    scenario-runner --scenario scenario.json

The output from the scenario is produced as a file named :code:`output-0.npy`. The file is specified in scenario.json.

.. note::
   For more information about building and running the ML SDK Scenario Runner, see: :ref:`ML SDK Scenario Runner`.

   For more information about building and setting up the Emulation Layer, see:
   :ref:`ML Emulation Layer for Vulkan®`
