VGF Dump Tool
=============

After you have built the VGF Library, a vgf_dump binary is produced as an artifact. The vgf_dump binary is a tool with multiple functions:

- You can use the vgf_dump tool to inspect the contents of the .vgf files.
- The tool can dump SPIR-V™ module binary data embedded in the VGF.
- The tool can dump constant buffers data embedded in the VGF.
- You can use vgf_dump to generate a scenario description JSON file
  template to use with `Scenario Runner`. The scenario template sets up all the input
  and output resource bindings which are setup with placeholder filenames. Therefore, you
  only need to point the resources to the actual file paths.

An example usage of vgf_dump is the following:

.. code-block:: bash

  vgf_dump input.vgf

Which outputs the human-readable json representation of the VGF file.

For more information the help output can be consulted:

.. code-block:: bash

  vgf_dump --help

.. literalinclude:: ../generated/vgf_dump_help.txt
    :language: text

`--dump-spirv`
--------------

This option outputs the raw SPIR-V™ data of the given module index to stdout. `--dump-spirv` is incompatible with `--dump-constant` and `--scenario-template` options.


`--dump-constant`
-----------------

This option outputs the contents of the constant at the given index to stdout.
If the `--output <file.npy>` option is provided, the contents will be saved to the specified NumPy file.

`--dump-constant` is incompatible with `--dump-spirv` and `--scenario-template` options.

`--scenario-template`
---------------------

This option outputs a template scenario file. The ML SDK Scenario Runner uses the template scenario file as an input file. The template scenario file describes what the scenario runner must execute. You must manually edit some file paths in the template scenario file. However, the `--scenario-template` is incompatible with `--dump-spirv` and `--dump-constant` options. For example, after creating a simple VGF file, the `--scenario-template` option produces:

.. code-block:: json

  {
      "commands": [
          {
              "dispatch_graph": {
                  "bindings": [
                      {
                          "id": 0,
                          "resource_ref": "input_0_ref",
                          "set": 0
                      },
                      {
                          "id": 1,
                          "resource_ref": "output_0_ref",
                          "set": 0
                      }
                  ],
                  "graph_ref": "vgf_graph_ref",
                  "shader_substitutions": []
              }
          }
      ],
      "resources": [
          {
              "graph": {
                  "src": "maxpool.vgf",
                  "uid": "vgf_graph_ref"
              }
          },
          {
              "tensor": {
                  "dims": [
                      1,
                      16,
                      16,
                      16
                  ],
                  "format": "VK_FORMAT_R8_SINT",
                  "shader_access": "readonly",
                  "src": "TEMPLATE_PATH_TENSOR_INPUT_0",
                  "uid": "input_0_ref"
              }
          },
          {
              "tensor": {
                  "dims": [
                      1,
                      8,
                      8,
                      16
                  ],
                  "dst": "TEMPLATE_PATH_TENSOR_OUTPUT_0",
                  "format": "VK_FORMAT_R8_SINT",
                  "shader_access": "writeonly",
                  "uid": "output_0_ref"
              }
          }
      ]
  }
