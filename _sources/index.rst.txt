Welcome to the '|SDK_project|' documentation
============================================

The '|SDK_project|' is a collection of libraries and tools to assist with the
integration and deployment of ML use cases via the Vulkan® API. The ML SDK for Vulkan® makes use
of the new ML extensions for Vulkan® which provide a hardware abstraction to enable
deployment of ML workloads that are both portable and accelerable. The Vulkan®
extensions currently exposed are:

- `VK_ARM_data_graph <https://docs.vulkan.org/spec/latest/appendices/extensions.html#VK_ARM_data_graph>`_
- `VK_ARM_data_graph_instruction_set_tosa <https://docs.vulkan.org/spec/latest/appendices/extensions.html#VK_ARM_data_graph_instruction_set_tosa>`_
- `VK_ARM_data_graph_optical_flow <https://docs.vulkan.org/spec/latest/appendices/extensions.html#VK_ARM_data_graph_optical_flow>`_
- `VK_ARM_tensors <https://docs.vulkan.org/spec/latest/appendices/extensions.html#VK_ARM_tensors>`_

The corresponding SPIR-V™ extensions and extended instruction sets currently used are:

- `SPV_ARM_graph <https://github.khronos.org/SPIRV-Registry/extensions/ARM/SPV_ARM_graph.html>`_
- `SPV_ARM_tensors <https://github.khronos.org/SPIRV-Registry/extensions/ARM/SPV_ARM_tensors.html>`_
- `TOSA.001000.1 <https://github.khronos.org/SPIRV-Registry/extended/TOSA.001000.1.html>`_
- `Arm.MotionEngine.100 <https://github.com/KhronosGroup/SPIRV-Headers/blob/main/include/spirv/unified1/extinst.arm.motion-engine.100.grammar.json>`_

The tight integration of ML workloads into the rendering pipeline enables graphics
use cases at improved levels of performance and efficiency and by leveraging the
TOSA 1.x specification, you can expect consistent behavior
accross multiple vendor implementations.

.. toctree::
   :maxdepth: 1
   :caption: Overview

   introduction.rst
   cloning.rst
   building.rst
   tensor_aliasing_tutorial.rst
   e2e_pytorch_tutorial.rst
   e2e_tflite_tutorial.rst
   e2e_onnx_tutorial.rst
   vgf_run_tutorial.rst
   license.rst


.. toctree::
   :maxdepth: 2
   :caption: ML SDK Model Converter

   model-converter/docs/in/index.rst

.. toctree::
   :maxdepth: 2
   :caption: ML SDK VGF Library

   vgf-lib/docs/in/index.rst

.. toctree::
   :maxdepth: 2
   :caption: ML SDK Scenario Runner

   scenario-runner/docs/in/index.rst

.. toctree::
   :maxdepth: 2
   :caption: ML Emulation Layer for Vulkan®

   emulation-layer/docs/in/index.rst

.. toctree::
   :maxdepth: 1
   :caption: Contribution

   contribution/guidelines.rst
   contribution/security.rst
