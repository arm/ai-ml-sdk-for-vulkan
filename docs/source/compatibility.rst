Compatibility matrix
====================

Each |SDK_project| release has a tagged manifest that selects a coordinated set
of component versions. Use the tagged manifest when checking out a released
version of the |SDK_project|.

Release compatibility
---------------------

.. list-table::
   :header-rows: 1
   :width: 100%
   :widths: 15 12 16 14 15 12 16

   * - | ML SDK
       | release
     - Manifest
     - | Emulation
       | Layer
     - | Model
       | Converter
     - | Scenario
       | Runner
     - | VGF
       | Library
     - | Workload
       | Library
   * - 2025.10.0
     - `v2025.10.0
       <https://github.com/arm/ai-ml-sdk-manifest/blob/v2025.10.0/default.xml>`_
     - 0.7.0
     - 0.7.0
     - 0.7.0
     - 0.7.0
     - N/A
   * - 2025.12.0
     - `v2025.12.0
       <https://github.com/arm/ai-ml-sdk-manifest/blob/v2025.12.0/default.xml>`_
     - 0.8.0
     - 0.8.0
     - 0.8.0
     - 0.8.0
     - N/A
   * - 2026.03.0
     - `v2026.03.0
       <https://github.com/arm/ai-ml-sdk-manifest/blob/v2026.03.0/default.xml>`_
     - 0.9.0
     - 0.9.0
     - 0.9.0
     - 0.9.0
     - N/A
   * - 2026.06.0
     - `v2026.06.0
       <https://github.com/arm/ai-ml-sdk-manifest/blob/v2026.06.0/default.xml>`_
     - 0.10.0
     - 0.10.0
     - 0.10.0
     - 0.10.0
     - N/A
   * - 2026.09.0
     - `v2026.09.0
       <https://github.com/arm/ai-ml-sdk-manifest/blob/v2026.09.0/default.xml>`_
     - 0.11.0
     - 0.11.0
     - 0.11.0
     - 0.11.0
     - 0.11.0

VGF compatibility
-----------------

The VGF Library can read VGF files written using older versions of the VGF
format. Use the VGF Library version included in the selected |SDK_project|
release.

Use the :doc:`VGF Updater Tool <vgf-lib/docs/in/vgf_updater>` to migrate a
valid older VGF file to the format supported by the installed VGF Library.
