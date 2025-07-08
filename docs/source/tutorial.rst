Converting and deploying a PyTorch model tutorial
=================================================

This tutorial describes how to convert and deploy a PyTorch model using the |SDK_project|.
In this tutorial, we generate a sample PyTorch file with a single MaxPool2D operation
to demonstrate each step of the end-to-end workflow.

1. Run the following python script to create a PyTorch model for a single MaxPool2D operation. For the
model input,use a NumPy file. To convert the model to TOSA FlatBuffers, use ExecuTorch:

.. literalinclude:: assets/MaxPool2DModel.py
    :language: python

.. code-block:: bash

   python MaxPool2DModel.py

This generates a TOSA Flatbuffers :code:`${NAME}.tosa`, where the tool generates :code:`${NAME}`

2. Convert the TOSA FlatBuffers file into a VGF file:

.. code-block:: bash

    model-converter --input ${NAME}.tosa --output maxpool.vgf

.. note::
   For more information about the ML SDK Model Converter, see: :ref:`ML SDK Model Converter`

3. Use the VGF Dump Tool to generate a Scenario Template. To run a scenario on the ML SDK Scenario Runner,
you must have a scenario specification in the form of a JSON file. Use the VGF file that was generated in the previous
step and pass it to the VGF Dump Tool:

.. code-block:: bash

    $vgf_dump --input maxpool.vgf --output scenario.json --scenario-template

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


5. Run the ML SDK Scenario Runner on the Emulation Layer:

.. code-block:: bash

    scenario-runner --scenario scenario.json

The output from the scenario is produced as a file named :code:`output-0.npy`. The file is specified in scenario.json.

.. note::
   For more information about building and running the ML SDK Scenario Runner, see: :ref:`ML SDK Scenario Runner`.

   For more information about building and setting up the Emulation Layer, see:
   :ref:`ML Emulation Layer for Vulkan®`
