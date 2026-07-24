.. _darwin-support:

Using the |SDK_project| on Darwin
=================================

The |SDK_project| supports native builds on Darwin. The Model
Converter and ML SDK VGF Library run as native tools. Running a workload with
the ML SDK Scenario Runner and ML Emulation Layer for Vulkan® additionally
requires a Vulkan® implementation over a translation layer.

Darwin support for the Scenario Runner and Emulation Layer is experimental.

Vulkan® driver options
----------------------

The Darwin Vulkan® SDK can provide two translation drivers:

``MoltenVK``
    The compatibility option and current default.

``KosmicKrisp``
    An opt-in technical preview included in recent Vulkan® SDK releases.

Prerequisites
-------------

The following prerequisites apply when using either MoltenVK or KosmicKrisp:

* Xcode Command Line Tools, including Clang.
* Python 3.10 or later, CMake 3.25 or later, and Ninja 1.10 or later.
* The `LunarG Vulkan® SDK for Darwin <https://vulkan.lunarg.com/sdk/home#mac>`_.
* The normal |SDK_project| source dependencies. Using the Repo tool as described
  in :doc:`cloning` obtains the preferred dependency versions.

The driver-specific requirements are:

``MoltenVK``
    Use the MoltenVK driver included in the standard Vulkan® SDK installation.
    No additional SDK component is required.

``KosmicKrisp``
    Select the KosmicKrisp component in the Vulkan® SDK installer. Check the requirements for the SDK
    version you install because they may change while KosmicKrisp remains a
    technical preview.

Build and install
-----------------

Set paths for the |SDK_project| checkout and the installed Vulkan® SDK version. The
Vulkan® SDK path in this example is the version directory containing
``setup-env.sh``, not its platform-specific child directory.

.. code-block:: shell

   export ML_SDK="$HOME/ml-sdk"
   export VULKAN_SDK_ROOT="$HOME/VulkanSDK/1.4.350.1"

Source the Vulkan® SDK environment, install the Python requirements, and build
the |SDK_project| into a local deployment directory:

.. code-block:: shell

   source "$VULKAN_SDK_ROOT/setup-env.sh"
   cd "$ML_SDK"
   python3 -m pip install -r requirements.txt
   python3 -m pip install -r tooling-requirements.txt
   ./scripts/build.py --install "$ML_SDK/deploy"

The setup script sets ``VULKAN_SDK`` to the SDK's platform-specific directory
and adds the Vulkan® tools and libraries to the current shell.

Select a Vulkan® driver
-----------------------

Select exactly one driver after sourcing ``setup-env.sh``. Sourcing the setup
script again can reset the selection.

For MoltenVK:

.. code-block:: shell

   export VK_DRIVER_FILES="$VULKAN_SDK/share/vulkan/icd.d/MoltenVK_icd.json"
   unset VK_ICD_FILENAMES

For KosmicKrisp:

.. code-block:: shell

   export VK_DRIVER_FILES="$VULKAN_SDK/share/vulkan/icd.d/libkosmickrisp_icd.json"
   unset VK_ICD_FILENAMES

``VK_DRIVER_FILES`` is the current Vulkan® Loader driver override.
``VK_ICD_FILENAMES`` is deprecated; clearing it prevents a stale value from
making the intended configuration unclear.

If the KosmicKrisp manifest is absent, reopen the Vulkan® SDK installer and add
the KosmicKrisp component, or install an SDK release that includes it.

Enable the graph and tensor layers
----------------------------------

Add the installed layer libraries and manifests to the environment, then
enable the Graph layer before the Tensor layer:

.. code-block:: shell

   export DYLD_LIBRARY_PATH="$ML_SDK/deploy/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
   export VK_LAYER_PATH="$ML_SDK/deploy/share/vulkan/explicit_layer.d${VK_LAYER_PATH:+:$VK_LAYER_PATH}"
   export VK_INSTANCE_LAYERS="VK_LAYER_ML_Graph_Emulation:VK_LAYER_ML_Tensor_Emulation"

The Vulkan® SDK setup script normally defines ``VK_LAYER_PATH`` for its own
layers. Prepending the |SDK_project| directory keeps those SDK layers discoverable.

Verify the configuration
------------------------

Run the Vulkan® information utility in the configured shell:

.. code-block:: shell

   vulkaninfo --summary

Check that:

* ``VK_LAYER_ML_Graph_Emulation`` and ``VK_LAYER_ML_Tensor_Emulation`` are
  listed as instance layers.
* The reported driver name is ``MoltenVK`` or ``KosmicKrisp``, matching the
  selected manifest.

Do not continue if the output reports a different driver or no Vulkan® device.

Run a scenario
--------------

Keep the same terminal environment and run the installed Scenario Runner:

.. code-block:: shell

   "$ML_SDK/deploy/bin/scenario-runner" \
       --scenario "/absolute/path/to/scenario.json"

Driver limitations
------------------

MoltenVK and KosmicKrisp do not support exactly the same optional Vulkan®
features. Select the driver by setting ``VK_DRIVER_FILES`` as described above
before starting Scenario Runner. Scenario Runner then uses the selected driver
through the Vulkan® Loader. Keep these runtime limitations in mind:

* Optical-flow scenarios are not currently supported on Darwin.
* A scenario can require an optional Vulkan® extension that is absent from the
  selected driver. Check ``vulkaninfo`` and the driver's release notes when an
  ``ErrorExtensionNotPresent`` error occurs.
* Timestamp-based graph profiling requires a queue with non-zero
  ``timestampValidBits``. Profiling is unavailable when the selected driver
  does not expose timestamp support; normal inference does not depend on it.

Troubleshooting
---------------

Wrong driver is reported
~~~~~~~~~~~~~~~~~~~~~~~~

Set ``VK_DRIVER_FILES`` after sourcing ``setup-env.sh``, unset
``VK_ICD_FILENAMES``, and rerun ``vulkaninfo --summary`` in the same shell.

No Vulkan® device is reported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Confirm that the selected manifest and driver library exist and that the host
meets that driver's requirements:

.. code-block:: shell

   test -f "$VK_DRIVER_FILES"
   uname -m

For KosmicKrisp, also confirm that the Vulkan® SDK installer included the
KosmicKrisp component.

Graph and tensor layers are not found
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Confirm that the installation contains both manifests and both libraries:

.. code-block:: shell

   ls "$ML_SDK/deploy/share/vulkan/explicit_layer.d/VkLayer_Graph.json"
   ls "$ML_SDK/deploy/share/vulkan/explicit_layer.d/VkLayer_Tensor.json"
   ls "$ML_SDK/deploy/lib/libVkLayer_Graph.dylib"
   ls "$ML_SDK/deploy/lib/libVkLayer_Tensor.dylib"

Then check ``VK_LAYER_PATH``, ``VK_INSTANCE_LAYERS``, and
``DYLD_LIBRARY_PATH`` in the terminal that starts Scenario Runner.

Further reading
---------------

* `LunarG Vulkan SDK: Getting Started on Darwin <https://vulkan.lunarg.com/doc/view/1.4.350.1/mac/getting_started.html>`_
* `Vulkan Loader driver interface <https://github.com/KhronosGroup/Vulkan-Loader/blob/main/docs/LoaderDriverInterface.md>`_
* `Vulkan Loader layer interface <https://github.com/KhronosGroup/Vulkan-Loader/blob/main/docs/LoaderLayerInterface.md>`_
* `MoltenVK runtime user guide <https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/MoltenVK_Runtime_UserGuide.md>`_
