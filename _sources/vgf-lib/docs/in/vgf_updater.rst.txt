VGF Updater Tool
==================

After you have built the VGF Library, a vgf_updater binary is produced as an artifact. The vgf_updater binary is a tool used to produce an up-to-date version of a given outdated VGF file.

An example usage of vgf_updater is the following:

.. code-block:: bash

   vgf_updater -i input.vgf -o output.vgf

This writes a new VGF file to output.vgf if the given input.vgf file is valid and outdated. If input.vgf is already at the latest version then the tool prints the current version and exits without writing the output file.

For more information the help output can be consulted:

.. code-block:: bash

   vgf_updater --help

.. literalinclude:: ../generated/vgf_updater_help.txt
    :language: text
