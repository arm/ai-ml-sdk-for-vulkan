.. _install-prebuilt-packages:

Install prebuilt packages
=========================

Prebuilt |SDK_project| packages are distributed through PyPI. These
instructions describe how to check package compatibility and install the
available packages.

For instructions on building components from source, see :doc:`building`.

Requirements
------------

Before installing a package, ensure that your system has:

* Python 3.10 or later.
* A supported operating system and architecture. See :ref:`Platforms`.
* A recent version of ``pip``.

Python 3.10 or later is the general Python requirement. However, this does not
mean that every package is available for every later Python version or
platform. A compatible wheel must also have been published for your Python
version, operating system, and architecture.

Create a virtual environment
----------------------------

Using a virtual environment is recommended:

.. code-block:: shell

   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip

On Windows®:

.. code-block:: powershell

   py -3 -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip

Check package availability
--------------------------

Before installing, open the package's PyPI page and select **Download files**.

Check that the release contains a wheel compatible with:

* Your operating system.
* Your processor architecture.
* Your Python version and ABI.

The Python requirement shown on the main PyPI page is not sufficient by
itself. A compatible wheel must also appear on the **Download files** page.

The release compatibility matrix maps |SDK_project| releases to coordinated
component versions. It does not describe the availability of Python package
files for particular platforms or Python versions.

Wheel availability can change between releases. For this reason, this page
does not provide a fixed wheel availability table. ``pip`` selects a compatible
wheel automatically when one is available.

Available packages
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Component
     - Install command
     - Package files
   * - Model Converter
     - ``python -m pip install ai-ml-sdk-model-converter``
     - `Model Converter files on PyPI
       <https://pypi.org/project/ai-ml-sdk-model-converter/#files>`_
   * - VGF Library
     - ``python -m pip install ai-ml-sdk-vgf-library``
     - `VGF Library files on PyPI
       <https://pypi.org/project/ai-ml-sdk-vgf-library/#files>`_
   * - Workload Library
     - ``python -m pip install ai-ml-workload-library-for-vulkan``
     - `Workload Library files on PyPI
       <https://pypi.org/project/ai-ml-workload-library-for-vulkan/#files>`_
   * - Scenario Runner
     - ``python -m pip install ai-ml-sdk-scenario-runner``
     - `Scenario Runner files on PyPI
       <https://pypi.org/project/ai-ml-sdk-scenario-runner/#files>`_
   * - Emulation Layer
     - ``python -m pip install ai-ml-emulation-layer-for-vulkan``
     - `Emulation Layer files on PyPI
       <https://pypi.org/project/ai-ml-emulation-layer-for-vulkan/#files>`_

If ``pip`` reports that no matching distribution is available, check the
package's **Download files** page. A wheel might not yet be available for your
combination of Python version, operating system, and architecture.

Vulkan® runtime requirements
----------------------------

The Model Converter and VGF Library do not execute Vulkan® workloads.

Running workloads with Scenario Runner or the Emulation Layer requires a
Vulkan® 1.3 or later implementation. There is no separately documented minimum
Vulkan® Loader version.

Linux®
~~~~~~

Use a Vulkan® 1.3-capable implementation with Mesa 23.x or later.

Windows®
~~~~~~~~

Windows® 11 with a current Vulkan®-capable GPU driver is recommended.

Use the Vulkan® Loader installed by the GPU driver's Vulkan® Runtime. The
LunarG Vulkan® SDK is not required when using prebuilt packages.

Darwin
~~~~~~

Scenario Runner and Emulation Layer support on Darwin is experimental.

Install the latest available LunarG Vulkan® SDK for Darwin. The SDK provides
the Vulkan® Loader and a Vulkan® implementation through a translation layer.

See :ref:`darwin-support` for driver selection, configuration, and current
limitations.

Verify the installation
-----------------------

Check that the installed packages have consistent dependencies:

.. code-block:: shell

   python -m pip check

You can also inspect an installed package:

.. code-block:: shell

   python -m pip show ai-ml-sdk-model-converter
   python -m pip show ai-ml-sdk-vgf-library
   python -m pip show ai-ml-workload-library-for-vulkan
   python -m pip show ai-ml-sdk-scenario-runner
   python -m pip show ai-ml-emulation-layer-for-vulkan

Next steps
----------

* :doc:`Convert a model <model-converter/docs/in/usage>`
* :doc:`Use the VGF Library <vgf-lib/docs/in/index>`
* :doc:`Use the Workload Library <workload-lib/docs/in/usage>`
* :doc:`Run a scenario <scenario-runner/docs/in/usage>`
* :doc:`Use the Emulation Layer <emulation-layer/docs/in/usage>`
