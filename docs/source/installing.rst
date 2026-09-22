.. _install-prebuilt-packages:

Install prebuilt packages
=========================

Prebuilt |SDK_project| packages are distributed as Python wheels through
PyPI and as binary tarballs and ZIP files through GitHub releases for Linux,
Windows®, and Darwin. These packages contain native tools and libraries, so
you can use the packaged components without compiling them. This guide
explains how to choose a package, check compatibility, install it, and
understand the scope of testing.

For instructions on building components from source, see :doc:`building`.

Package downloads and documentation
-----------------------------------

Use PyPI for Python wheels or GitHub releases for binary tarballs and ZIP
files:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Component
     - Python wheels
     - Binary archives
   * - Model Converter
     - `PyPI <https://pypi.org/project/ai-ml-sdk-model-converter/>`__
     - `GitHub releases <https://github.com/arm/ai-ml-sdk-model-converter/releases>`__
   * - VGF Library
     - `PyPI <https://pypi.org/project/ai-ml-sdk-vgf-library/>`__
     - `GitHub releases <https://github.com/arm/ai-ml-sdk-vgf-library/releases>`__
   * - Workload Library
     - `PyPI <https://pypi.org/project/ai-ml-workload-library-for-vulkan/>`__
     - `GitHub releases <https://github.com/arm/ai-ml-workload-library-for-vulkan/releases>`__
   * - Scenario Runner
     - `PyPI <https://pypi.org/project/ai-ml-sdk-scenario-runner/>`__
     - `GitHub releases <https://github.com/arm/ai-ml-sdk-scenario-runner/releases>`__
   * - Emulation Layer
     - `PyPI <https://pypi.org/project/ai-ml-emulation-layer-for-vulkan/>`__
     - `GitHub releases <https://github.com/arm/ai-ml-emulation-layer-for-vulkan/releases>`__

Select the binary archive for your operating system and architecture from
the release assets, then extract it and follow the component's usage
instructions. The platform and runtime requirements below still apply.

The `SDK GitHub releases
<https://github.com/arm/ai-ml-sdk-for-vulkan/releases>`_ also provide a ZIP
containing precompiled, versioned documentation. Download the documentation
for the SDK release you are using and extract it to browse locally without
building the documentation yourself.

Requirements for pip installation
---------------------------------

Before installing a package with ``pip``, ensure that your system has:

* Python 3.10 or later.
* A supported operating system and architecture. See :ref:`Platforms`.
* A recent version of ``pip``.

Python 3.10 or later is the general Python requirement. However, this does not
mean that every package is available for every later Python version or
platform. A compatible wheel must also have been published for your Python
version, operating system, and architecture.

Supported platforms
-------------------

The desktop platform support described in :ref:`Platforms` is summarized
below. Check the files for your selected package release before installing;
platform support does not guarantee that a wheel is available for every
component or Python version.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Operating system
     - Architecture
     - Support notes
   * - Linux
     - x86-64 and AArch64
     - All five components are supported. Check the wheel's Linux
       compatibility tag and the runtime requirements below.
   * - Windows®
     - x86-64
     - All five components are supported. Windows® on AArch64 is unsupported.
   * - Darwin
     - Arm64
     - Model Converter and VGF Library are supported. Workload Library,
       Scenario Runner, and Emulation Layer support is experimental.
       Darwin on x86-64 is unsupported.

The current Linux binary packages are built and tested on AlmaLinux 8.
Linux wheel builds target ``manylinux_2_28``, with a minimum requirement of
**glibc 2.28 or later** (``glibc >= 2.28``). You can use other compatible
Linux distributions; AlmaLinux is not required on the installation system.
The Python, architecture, and Vulkan® runtime requirements still apply.
See the `manylinux compatibility documentation
<https://github.com/pypa/manylinux#manylinux_2_28-almalinux-8-based>`_.

For an older package release, check its wheel tags because the compatibility
baseline can differ between releases.

Android™ AArch64 support is experimental and uses a separate native/APK
workflow for runtime components. The desktop ``pip`` instructions on this
page do not install Android™ packages. See :ref:`Platforms` and the component
documentation for Android™ support and build instructions.

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

Wheel filenames include compatibility tags. For example, ``win_amd64``
identifies Windows® x86-64, and ``aarch64`` identifies Linux AArch64 in a
Linux wheel tag. A ``cp310`` interpreter tag identifies CPython 3.10; a
``py3-none`` wheel has no Python-version-specific ABI dependency, but can
still contain native binaries and require a particular operating system.
Linux and Darwin platform tags also encode an operating-system compatibility
baseline. Let ``pip`` check these tags; renaming a wheel does not make it
compatible with another system.

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

Install the components needed for your workflow:

* **Model Converter** converts TOSA models into VGF artifacts.
* **VGF Library** provides VGF file handling and the ``vgf_dump`` tool.
* **Workload Library** provides a native library for applications that execute
  Vulkan® workloads.
* **Scenario Runner** executes workloads described by scenario files.
* **Emulation Layer** provides the Vulkan® ML emulation layers used when
  running workloads through emulation.

The commands below require binary wheels for the package and its dependencies.
This avoids falling back to a source build when a compatible wheel is missing.
See the `pip installation options
<https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-only-binary>`_.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Component
     - Install command
     - Package description
   * - Model Converter
     - ``python -m pip install --only-binary=:all: ai-ml-sdk-model-converter``
     - `Model Converter on PyPI
       <https://pypi.org/project/ai-ml-sdk-model-converter/>`_
   * - VGF Library
     - ``python -m pip install --only-binary=:all: ai-ml-sdk-vgf-library``
     - `VGF Library on PyPI
       <https://pypi.org/project/ai-ml-sdk-vgf-library/>`_
   * - Workload Library
     - ``python -m pip install --only-binary=:all: ai-ml-workload-library-for-vulkan``
     - `Workload Library on PyPI
       <https://pypi.org/project/ai-ml-workload-library-for-vulkan/>`_
   * - Scenario Runner
     - ``python -m pip install --only-binary=:all: ai-ml-sdk-scenario-runner``
     - `Scenario Runner on PyPI
       <https://pypi.org/project/ai-ml-sdk-scenario-runner/>`_
   * - Emulation Layer
     - ``python -m pip install --only-binary=:all: ai-ml-emulation-layer-for-vulkan``
     - `Emulation Layer on PyPI
       <https://pypi.org/project/ai-ml-emulation-layer-for-vulkan/>`_

If ``pip`` reports that no matching distribution is available, check the
package's **Download files** page. A wheel might not yet be available for your
combination of Python version, operating system, and architecture.
Check which package the error names: the missing wheel might belong to a
dependency. Use a combination listed in the release's available files, or
follow :doc:`building` to build from source.

Vulkan® runtime requirements
----------------------------

The Model Converter and VGF Library do not execute Vulkan® workloads.

Running workloads with Scenario Runner or the Emulation Layer requires a
Vulkan® 1.3 or later implementation. There is no separately documented minimum
Vulkan® Loader version.

Linux
~~~~~

Use a Vulkan® 1.3-capable implementation with Mesa 23.x or later.

Windows®
~~~~~~~~

The Windows® binary packages are built and tested on Windows® 11.
Use a current Vulkan®-capable GPU driver when running workloads.

Use the Vulkan® Loader installed by the GPU driver's Vulkan® Runtime. The
LunarG Vulkan® SDK is not required when using prebuilt packages.

Darwin
~~~~~~

Workload Library, Scenario Runner, and Emulation Layer support on Darwin is
experimental.

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

These checks confirm installed package metadata and dependency consistency.
To check execution, follow the component usage instructions below and run a
conversion or scenario. Running a Vulkan® workload also checks the driver and
layer configuration, which package installation alone does not validate.

Python versions and testing platforms
-------------------------------------

The current binary package build configuration targets CPython 3.10, 3.11,
3.12, 3.13, and 3.14 for VGF Library and Scenario Runner. Model Converter,
Emulation Layer, and Workload Library use Python 3.10 to produce
``py3-none`` wheels, with Python 3.10 or later declared as their requirement.
These are wheel build targets; check the selected release's files for actual
availability.

We test the pip packages for all five components on all platforms listed
below, using Python 3.12 only.

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Operating system
     - Architecture
     - Python used for testing
   * - AlmaLinux 8
     - x86-64 and AArch64
     - 3.12
   * - Windows® 11
     - x86-64
     - 3.12
   * - Darwin 25.5.0
     - Arm64
     - 3.12

Android™ AArch64 is also a testing target for native runtime components.

Testing on a platform does not establish support for every GPU, model,
operator, or tensor format. Darwin runtime support and Android™ support remain
experimental. See :ref:`Platforms`, :ref:`darwin-support`, and each component's
documented limitations for your intended workload.

Next steps
----------

* :doc:`Convert a model <model-converter/docs/in/usage>`
* :doc:`Use the VGF Library <vgf-lib/docs/in/index>`
* :doc:`Use the Workload Library <workload-lib/docs/in/usage>`
* :doc:`Run a scenario <scenario-runner/docs/in/usage>`
* :doc:`Use the Emulation Layer <emulation-layer/docs/in/usage>`
