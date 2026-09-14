Frequently asked questions
==========================

This FAQ provides quick, task-oriented answers. The linked platform, release,
and component documentation remains authoritative for complete procedures,
current requirements, and version-specific details.

.. contents:: On this page
   :local:
   :depth: 1

.. _faq-platform-support:

Which host and target platforms are supported?
----------------------------------------------

Linux AArch64 and x86-64, and Windows x86-64, are supported. Windows AArch64
and Darwin x86-64 are unsupported. Darwin AArch64 supports Model Converter and
VGF Library, with experimental Workload Library, Scenario
Runner, and Emulation Layer support. Android™ AArch64 support is experimental
for VGF Library, Workload Library, Scenario Runner, and
Emulation Layer, while Model Converter is not an Android™ target. Android™
x86-64 runtime components are unsupported.

Use the authoritative :ref:`Platforms` table for the component-by-component
status and :doc:`Building the ML SDK for Vulkan® <building>` for current host
prerequisites and component build documentation.

.. _faq-version-compatibility:

How do I choose compatible ML SDK, VGF and component versions?
--------------------------------------------------------------

Start from a `tagged ai-ml-sdk-manifest release
<https://github.com/arm/ai-ml-sdk-manifest/tags>`_. It pins the coordinated ML
SDK components and dependencies. Prefer revisions from the same coordinated
release.

To migrate a valid older VGF file to the format supported by the installed VGF
Library, run:

.. code-block:: bash

    vgf_updater -i input.vgf -o output.vgf

Use the tagged manifest together with the `ML SDK release notes
<https://github.com/arm/ai-ml-sdk-for-vulkan/blob/main/RELEASE_NOTES.md>`_, the
:ref:`Platforms` guidance, and the :doc:`VGF Updater documentation
<vgf-lib/docs/in/vgf_updater>`.

.. _faq-prebuilt-packages:

Where can I find supported prebuilt packages, and how do I get started?
-----------------------------------------------------------------------

Supported prebuilt ML SDK packages are distributed through PyPI. Install the
component you need. See :doc:`Install prebuilt packages <installing>` for the
available packages, host requirements, platform guidance, and instructions for
checking wheel compatibility.

.. _faq-darwin-support:

What is supported on Darwin, and how should it be configured?
-------------------------------------------------------------

Darwin support is limited to Apple silicon. Model Converter and VGF Library are
supported, while Workload Library, Scenario Runner, and
Emulation Layer are experimental.

Applications using the Workload Library and Scenario Runner
both use the Vulkan® Loader. The Emulation Layer can be enabled on either path,
with MoltenVK or KosmicKrisp providing the underlying Vulkan® implementation.
MoltenVK is the default compatibility option. KosmicKrisp is an optional
technical preview in recent Vulkan® SDK releases.

After sourcing the Vulkan® SDK environment, select exactly one driver by
setting ``VK_DRIVER_FILES`` to its manifest. After enabling the graph and
tensor layers, run ``vulkaninfo --summary``. Confirm that it reports the
selected MoltenVK or KosmicKrisp driver and lists
``VK_LAYER_ML_Graph_Emulation`` and ``VK_LAYER_ML_Tensor_Emulation``.

Check the authoritative :ref:`Platforms` table and follow the canonical
:ref:`Darwin build, driver, and layer setup <darwin-support>` for prerequisites,
driver selection, layer configuration, and validation.

.. _faq-android-build-run:

How do I build and run ML SDK components on Android™?
-----------------------------------------------------

Build the VGF Library, Workload Library, Scenario Runner, and
Emulation Layer for Android™ AArch64 with the Android™ NDK toolchain. On a
device with Vulkan® 1.3 support, run scenarios with Scenario Runner or run an
application linked with the Workload Library. APK packaging
also requires Gradle 8.4 or later on ``PATH``.
``ANDROID_HOME`` should point to an Android™ SDK containing the platform package
for API level 34 and Build Tools 34.0.0, or compatible versions.

For the Scenario Runner APK, install the generated package and start its
foreground service with:

.. code-block:: bash

    adb install -r build/scenario-runner-debug.apk

    adb shell am start-foreground-service \
        -n com.arm.ai_ml_sdk_scenario_runner/.Main \
        --esa args --scenario,/data/user/0/com.arm.ai_ml_sdk_scenario_runner/scenario.json

The scenario, VGF, and input files must already be accessible at the paths
passed to Scenario Runner. Deploy the Emulation Layer either as an APK-packaged
Vulkan® layer or by placing its layer libraries under
``/data/local/debug/vulkan``. Then enable the graph and tensor layers through
Android™'s GPU debug-layer settings.

See the complete documented :doc:`Scenario Runner Android™ build
<scenario-runner/docs/in/build>` and :doc:`execution
<scenario-runner/docs/in/usage>` flows, and the Emulation Layer sections for
:ref:`Building for Android™`, :ref:`Usage on Android™`, and
:ref:`APK Packaging`. The `Android™ Vulkan layer deployment guide
<https://developer.android.com/ndk/guides/graphics/validation-layer>`_ covers
the platform's layer file-transfer and enablement procedures.

.. note::
   Android™ AArch64 support is experimental for the VGF Library, Workload
   Library, Scenario Runner, and Emulation Layer. Model Converter is an offline
   host tool and is not an Android™ target. Behavior depends on the device, API
   level, app permissions, and whether the build is debuggable.

.. _faq-sample-models-vgfs-workloads:

Where can I find sample models, VGFs and workload examples?
------------------------------------------------------------

Use one of the end-to-end tutorials for :doc:`PyTorch
<e2e_pytorch_tutorial>`, :doc:`TensorFlow Lite <e2e_tflite_tutorial>`, or
:doc:`ONNX <e2e_onnx_tutorial>` to generate VGF files and Scenario Runner
workloads. The TensorFlow Lite tutorial uses the SESR super-resolution example
from the `Arm® Model Zoo <https://github.com/Arm-Examples/ML-zoo>`_, including
its model and NumPy reference data.

For C++ application integration, see the :doc:`ML Workload Library for Vulkan®
usage guide <workload-lib/docs/in/usage>` and its complete programs for VGF
inspection and execution, standalone workloads, runtime allocations, and
wrapped Vulkan® contexts.

For an existing VGF, generate a scenario template:

.. code-block:: bash

    vgf_dump --input model.vgf --output scenario.json --scenario-template

Before running the scenario, edit ``scenario.json`` and replace the generated
input and output path placeholders with paths to your files:

.. code-block:: bash

    scenario-runner --scenario scenario.json

Use the :doc:`VGF execution tutorial <vgf_run_tutorial>` for the full
scenario-editing and execution procedure.

.. _faq-vgf-tools:

What tools can create or inspect VGF files?
-------------------------------------------

- :doc:`Model Converter <model-converter/docs/in/usage>` converts supported
  TOSA FlatBuffer or MLIR input into VGF.
- The :doc:`VGF Library <vgf-lib/docs/in/index>` provides :doc:`C++ encoder
  <vgf-lib/docs/in/encoder_api>`, :doc:`C encoder
  <vgf-lib/docs/in/encoder_c_api>`, :doc:`C++ decoder
  <vgf-lib/docs/in/decoder_api>`, and :doc:`C decoder
  <vgf-lib/docs/in/decoder_c_api>` APIs for programmatic encoding and decoding.
- :doc:`vgf_dump <vgf-lib/docs/in/vgf_dump>` produces a human-readable view,
  extracts embedded data, and generates Scenario Runner templates.
- :doc:`vgf_updater <vgf-lib/docs/in/vgf_updater>` migrates a valid older file
  to the format supported by that VGF Library version.
- The :doc:`ML Workload Library for Vulkan®
  <workload-lib/docs/in/usage>` loads VGF content into inspectable workload,
  resource, module, and executable views and can prepare that workload for
  Vulkan® execution.
- The `VGF Adapter for Model Explorer
  <https://github.com/arm/vgf-adapter-model-explorer>`_ provides graphical
  inspection of VGF inputs, outputs, constants, and graphs.

The linked pages contain each tool's complete build, API, and command-line
documentation.

.. _faq-performance-data:

How do I collect and interpret performance data?
------------------------------------------------

Use Scenario Runner dump options for runtime profiling, performance counters,
neural statistics, and debug databases:

- ``--profiling-dump-path FILE`` for runtime profiling
- ``--perf-counters-dump-path FILE`` for performance counters
- ``--neural-statistics-dump-dir DIR`` with
  ``--neural-statistics-mode 0|1`` for neural statistics
- ``--neural-debug-database-dump-dir DIR`` for the accelerator debug database

Neural-statistics and debug-database dumps require both the
``VK_ARM_data_graph_neural_accelerator_statistics`` extension and its
``dataGraphNeuralAcceleratorStatistics`` feature. Scenario Runner fails before
creating the Vulkan® device if either dump is requested without both.

.. important::

   Neural-statistics and debug-database dumps are native-driver diagnostics whose
   contents and interpretation depend on the target hardware and driver. The
   Emulation Layer does not implement this hardware-specific extension, so these
   dumps are unavailable with it.

See the :doc:`Scenario Runner CLI <scenario-runner/docs/in/usage>` and
:ref:`Neural accelerator statistics` for complete details.

.. _faq-optical-flow-compatibility:

Which versions support Optical Flow?
------------------------------------

Support for ``VK_ARM_data_graph_optical_flow`` starts with ML SDK 2026.06.0.
That coordinated release uses Scenario Runner 0.10.0 and Emulation Layer
0.10.0.

See the tagged `ML SDK 2026.06.0 release notes
<https://github.com/arm/ai-ml-sdk-for-vulkan/blob/v2026.06.0/RELEASE_NOTES.md>`_,
the `2026.06.0 manifest
<https://github.com/arm/ai-ml-sdk-manifest/blob/v2026.06.0/default.xml>`_, and
the `Scenario Runner 0.10.0
<https://github.com/arm/ai-ml-sdk-scenario-runner/blob/v0.10.0/RELEASE_NOTES.md>`_
and `Emulation Layer 0.10.0
<https://github.com/arm/ai-ml-emulation-layer-for-vulkan/blob/v0.10.0/RELEASE_NOTES.md>`_
release notes for details.
