JSON Test Description Specification
===================================

Notation
--------

The following section describes the notation in the Scenario Runner.

A class defines a structured type in C terms with typed parameters. The comma separates the typed parameters:

  .. code-block::

      my_class: {
          my_parameter1: its_type,
          my_parameter2: another_type
      }

  The previous example defines a class called my_class with two parameters,
  ``my_parameter1`` of type ``its_type``, and ``my_parameter2`` of type
  ``another_type``.

Parameter types can be regular types, for example, int, float, string, path, enum or boolean. Parameters can also be other user-defined classes. For class types that are defined later in the spec, the class name is prefixed with class. For
example:

  .. code-block::

      some_parameter: class some_new_type,
      some_new_type: {

      }

Arrays of items are wrapped in [] and lists of allowed types are separated with
``|``.

  .. code-block::

    my_array_of_ints: [int],
    my_array_of_things: [int | float]

In the previous example, each element in ``my_array_of_things`` is a union of int and float types but can also be a union of different classes.

Parameters that are optional have (default=value) postfix decoration on the
type. Parameters that are not optional are required to be specified in the JSON
file.

Parameters that have a limited set of allowed values are postfixed with =
followed by a | separated list of the allowed values. default values must match
existing allowed constraints. For example, to define an optional parameter than
can only be a value of red, green or blue, we do:

  .. code-block::

    my_parameter:string(default="red")=("red"|"green"|"blue")

Enumerations are similarly specified but without the "".

  .. code-block::

    my_enum_param:enum = (clockwise | counterclockwise)

Comments in the specification are inlined after //

  .. code-block::

    my_param:int // this param is used by things

Specification
-------------

.. note::
  * You can use absolute paths. If you do not use absolute paths, all paths are relative to the input scenario JSON file parent directory.
  * All parameters defined in the specification are required unless annotated as
    optional with default=

The root of the JSON file has two blocks.

.. code-block::

  root: {
      resources: [ class image | class tensor | class buffer | class raw_data |
                   class graph | class shader | class memory_barrier | class buffer_barrier |
                   class buffer_barrier | class tensor_barrier | class image_barrier ],
      commands: [ class dispatch_compute | class dispatch_graph | class dispatch_barrier |
                  class mark_boundary ]
  }

``resources`` lists all the resources in the test case and each item in the
array can be any of the following types:

* :ref:`image`
* :ref:`tensor`
* :ref:`buffer`
* :ref:`raw_data`
* :ref:`graph`
* :ref:`shader`
* :ref:`Barriers`

``commands`` lists all the commands in order of execution or dispatch:

* :ref:`dispatch_compute`
* :ref:`dispatch_graph`
* :ref:`dispatch_barrier`
* :ref:`mark_boundary`


Resources
^^^^^^^^^

image
"""""

The ``image`` resource has the following properties:

.. code-block::

  image: {
      uid:string, // globally unique identifier for the resource
      format:string, // string name of the VkFormat enum.
      dims:[int], // n-length array of sized for an n-dimension image
      shader_access:enum = (readonly|writeonly|readwrite|image_read) // type of access required by the shader/graph
      mips:int(default=1), // Number of mipmaps. Create an Image with memory allocated for this many level of details. Mipmaps levels are automatically generated.
      src:path(default=""), // optional path to the DDS file to initialize the resource from
      dst:path(default=""), // optional path to the DDS file to write contents to (post execution of commands)
      min_filter:enum = (NEAREST|LINEAR) // sampler setting
      mag_filter:enum = (NEAREST|LINEAR) // sampler setting
      mip_filter:enum = (NEAREST|LINEAR) // sampler setting
      border_address_mode:enum = (CLAMP_EDGE|CLAMP_BORDER|REPEAT|MIRRORED_REPEAT) // sampler setting
      border_color:enum = (FLOAT_TRANSPARENT_BLACK|FLOAT_OPAQUE_BLACK|FLOAT_OPAQUE_WHITE|INT_TRANSPARENT_BLACK|INT_OPAQUE_BLACK|INT_OPAQUE_WHITE|INT_CUSTOM_EXT|FLOAT_CUSTOM_EXT) // sampler setting
      custom_border_color:[int|float], // length 4 array of integer or float values representing an RGBA color value for a custom border.
      memory_group, // optional memory group to share memory object between resources
      tiling:enum = (OPTIMAL|LINEAR), // optional "Tiling" arrangement info of the image resource
  }

For a complete list of VkFormat entries, see
https://www.khronos.org/registry/vulkan/specs/1.3-extensions/man/html/VkFormat.html
however, we will only support those which line up with the DDS format
described here:
https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide.

The following image formats are supported and have corresponding DDS equivalents:
``VK_FORMAT_R8_SNORM``, ``VK_FORMAT_R8G8_SINT``, ``VK_FORMAT_R8G8_UNORM``, ``VK_FORMAT_R8G8B8_SINT``,
``VK_FORMAT_R32_SFLOAT``, ``VK_FORMAT_R8G8B8A8_UNORM``, ``VK_FORMAT_R8G8B8A8_SNORM``, ``VK_FORMAT_R8G8B8_SNORM``,
``VK_FORMAT_R8G8B8A8_SINT``, ``VK_FORMAT_R16G16B16A16_SFLOAT``, ``VK_FORMAT_R32G32B32A32_SFLOAT``,
``VK_FORMAT_R16G16_SFLOAT``, ``VK_FORMAT_B10G11R11_UFLOAT_PACK32``, ``VK_FORMAT_D32_SFLOAT_S8_UINT``, ``VK_FORMAT_B8G8R8A8_UNORM``,
``VK_FORMAT_R8_UNORM``, ``VK_FORMAT_R32_UINT``

The following formats have no corresponding DDS equivalents.
They may still be used for intermediate images or via memory aliasing:
``VK_FORMAT_R16G16B16A16_UNORM``, ``VK_FORMAT_R16G16B16A16_SNORM``, ``VK_FORMAT_R16G16B16A16_SINT``,
``VK_FORMAT_R8_BOOL_ARM``, ``VK_FORMAT_R8_UINT``, ``VK_FORMAT_R8_SINT``, ``VK_FORMAT_R16_UINT``,
``VK_FORMAT_R16_SINT``, ``VK_FORMAT_R32_SINT``, ``VK_FORMAT_R64_SINT``, ``VK_FORMAT_R16_SFLOAT``,
``VK_FORMAT_R8G8B8_UNORM``, ``VK_FORMAT_B8G8R8_UNORM``

tensor
""""""

The ``tensor`` resources have the following properties:

.. code-block::

  tensor: {
      uid:string, // globally unique identifier for the resource
      dims:[int], // n-length array of sized for an n-dimension tensor
      format:string, // string name of the VkFormat enum.
      shader_access:enum = (readonly|writeonly|readwrite) // type of access required by the shader/graph
      src:path(default=""), // optional path to the NumPy file to initialize the resource from
      dst:path(default=""), // optional path to the NumPy file to write contents to (post execution of commands)
      memory_group, // optional memory group to share memory object between resources
      tiling:enum = (OPTIMAL|LINEAR), // optional "Tiling" arrangement info of the tensor resource
  }

Supported formats for tensors are limited to a subset of the single channel
types defined in the VkFormat enum. Currently supported formats are:

.. code-block::

  bool: VK_FORMAT_R8_BOOL_ARM
  uint8: VK_FORMAT_R8_UINT
  int8: VK_FORMAT_R8_SINT
  uint16: VK_FORMAT_R16_UINT
  int16: VK_FORMAT_R16_SINT
  uint32: VK_FORMAT_R32_UINT
  int32: VK_FORMAT_R32_SINT
  int64: VK_FORMAT_R64_SINT
  float16: VK_FORMAT_R16_SFLOAT
  float32: VK_FORMAT_R32_SFLOAT

To allow for memory aliasing, the following object is needed in each resource:
.. code-block::

  struct MemoryGroup {
      uid:string(default=""), // unique string defining the shared memory object
  }

buffer
""""""

The ``buffer`` resources map to Storage Buffers in Vulkan®:

.. code-block::

  buffer: {
      uid:string, // globally unique identifier for the resource
      size:int, // total size of buffer in bytes
      shader_access:enum = (readonly|writeonly|readwrite) // type of access required by the shader/graph
      src:path(default=""), // optional path to the NumPy file to initialize the resource from
      dst:path(default=""), // optional path to the NumPy file to write contents to (post execution of commands)
      memory_group, // optional memory group to share memory object between resources
  }

Buffers do not have a format and it is up to the shader to interpret the data
in the correct manner.

raw_data
""""""""

The ``raw_data`` represents some data in host memory that is fed to the
dispatches via means other than standard resource binding mechanisms for
example, push constant or specialization constants.

.. code-block::

  raw_data: {
      uid:string, // globally unique identifier for the resource
      src:path, // path to the NumPy file to initialize the resource from
  }

shader
""""""

The ``shader`` resource references a SPIR-V™ or GLSL shader file. The runner
loads the GLSL and compiles it to SPIR-V™ before handing it to the Vulkan®
Runtime.

.. code-block::

  shader: {
      uid:string, // globally unique identifier for the resource
      src:path, // path to a shader source file
      entry:string(default="main"), // entry point into the shader
      type: enum = (GLSL | SPIR-V), // Type of shader source to expect
      build_options:string(default=""), // Build options to be used when compiling a GLSL shader source
      include_dirs:[string](default=[]), // Shaders include directories
      push_constants_size:int(default=0), // Size in bytes of the push constants used by the shader. Must be a multiple of 4
      specialization_constants: [class specialization_constant](default=), // n-dimension array
  }

  specialization_constant: {
      id: int,    // id of the specialization constant in the shader
      value: int|float // float or integer value to set the constant to
  }

graph
"""""

The ``graph`` resource is loaded from a VGF file via the
SDK parser API.

.. code-block::

  graph: {
      uid:string, // globally unique identifier for the resource
      src:path, // path to the VGF file to initialize the resource from
      specialization_constants_map: [class specialization_constant_map](default=), // array containing all the specialization constants referenced within a graph.
      shader_substitutions:[class shader_substitutions](default=) // array containing all the shaders to substitute within the graph.
      push_constants_size:int(default=0), // Size in bytes of the push constants used in the graph. Must be a multiple of 4
  }

The specialization constant map allows to map specialization constants to
multiple shaders within a graph.

.. code-block::

  specialization_constant_map: {
      specialization_constants:[specialization_constant], // array of specialization constants id-value pair
      shader_target:string // name of the shader node in the graph on which to apply the constants
  }

The ``shader_substitutions`` parameter is an array of shader_substitution objects. Each shader_substitution describes a placeholder shader node in the
graph that will be substituted with an actual shader implementation. The shader
substitution occurs during graph parsing and before graph compilation.

.. code-block::

  shader_substitutions: {
      {
          shader_ref: string, // reference to the shader resource (by UID) to use for the substitution
          target: string, // name of the placeholder shader node in the graph to replace
      }
  }

Barriers
""""""""

The barrier type resources represents memory, image, tensor and buffer barriers in Vulkan® which are inserted
by the dispatch_barrier command. You must ensure that implicit barriers are disabled for the target pipeline in
the corresponding dispatch command.

.. code-block::

  memory_barrier: {
      uid:string, // globally unique identifier for the resource
      src_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the source
      dst_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the destination
      src_stage:[enum(GRAPH|COMPUTE|ALL)], // source pipeline stages
      dst_stage:[enum(GRAPH|COMPUTE|ALL)], // destination pipeline stages
  }

.. code-block::

  buffer_barrier: {
      uid:string, // globally unique identifier for the resource
      buffer_resource:string, // reference to the buffer resource
      size:int // total size of the buffer affected by this barrier in bytes
      src_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the source
      dst_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the destination
      src_stage:[enum(GRAPH|COMPUTE|ALL)], // source pipeline stages
      dst_stage:[enum(GRAPH|COMPUTE|ALL)], // destination pipeline stages
      offset:int(default=0), // the offset in bytes into the backing memory for the buffer affected by this barrier
  }

.. code-block::

  image_barrier: {
      uid:string, // globally unique identifier for the resource
      src_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the source
      dst_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the destination
      old_layout:enum = (IMAGE_LAYOUT_TENSOR_ALIASING|IMAGE_LAYOUT_GENERAL|IMAGE_LAYOUT_UNDEFINED), // the old image layout in an image layout transition
      new_layout:enum = (IMAGE_LAYOUT_TENSOR_ALIASING|IMAGE_LAYOUT_GENERAL|IMAGE_LAYOUT_UNDEFINED), // the new image layout in an image layout transition
      image_resource:string, // reference to the image resource
      subresource_range: class subresource_range // the subresource range within the image affected by this barrier
      src_stage:[enum(GRAPH|COMPUTE|ALL)], // source pipeline stages
      dst_stage:[enum(GRAPH|COMPUTE|ALL)], // destination pipeline stages
  }

The subresource_range resource maps the image subresources of an image affected by an image barrier:

.. code-block::

  subresource_range: {
      base_mip_level:int (default=0), // the first mipmap level accessible to view
      level_count:int (default=1), // number of mipmap levels accessible
      base_array_layer:int (default=0), // the first array layer accessible to view
      layer_count:int (default=1) // the number of array layers accessible
  }

.. code-block::

  tensor_barrier: {
      uid:string, // globally unique identifier for the resource
      tensor_resource:string, // reference to the tensor resource
      src_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the source
      dst_access:enum(ACCESS_MEMORY_WRITE|ACCESS_MEMORY_READ|ACCESS_GRAPH_WRITE|ACCESS_GRAPH_READ|ACCESS_COMPUTE_SHADER_WRITE|ACCESS_COMPUTE_SHADER_READ), // memory access type from the destination
      src_stage:[enum(GRAPH|COMPUTE|ALL)], // source pipeline stages
      dst_stage:[enum(GRAPH|COMPUTE|ALL)], // destination pipeline stages
  }

Commands
^^^^^^^^

``Commands`` are executed in order of appearance in the JSON file. Initial
implementation will execute in-order with no overlap.

dispatch_compute
""""""""""""""""

The ``dispatch_compute`` command dispatches a compute shader to execute.

.. code-block::

  dispatch_compute: {
      shader_ref: string, // reference to the shader resource
      push_data_ref: string(default=""), // reference to raw_data resource containing the push_constants data
      rangeND: [int], // 3-dimension dispatch range expressed as number of local workgroups per dimension
      bindings: [class binding] // array of bindings mapping a resource reference to a descriptor set and id
      implicit_barrier:boolean(default=true) // inclusion of implicit memory barrier
  }

While ``push_constants`` can technically support other stages, we focus on
a single ``push_constant`` buffer for the compute stage only.

.. code-block::

  binding: {
      set: int, // descriptor set id
      id: int, // descriptor id in the set
      resource_ref: string // named reference to the resource to bind
      lod: int(default=0) // Optional. Level of details index. In case of an Image resource with mipmaps could be used to bind specific level of details.
      descriptor_type:enum(default=VK_DESCRIPTOR_TYPE_AUTO) = (VK_DESCRIPTOR_TYPE_AUTO|VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // descriptor type for the resource in current dispatch. Needed only when descriptor type cannot be correctly inferred
  }

dispatch_graph
""""""""""""""

The ``dispatch_graph`` command dispatches a compiled graph using the proposed
ML extensions for Vulkan®.

.. code-block::

  dispatch_graph: {
      graph_ref: string, // reference to the graph resource
      push_constants: [class push_constant_map](default=), // mappings between push constants data and the target shader node.
      bindings: [class binding] // array of bindings mapping a resource reference to a descriptor set and id. These bindings describe the inputs and outputs to the graph.
      implicit_barrier:boolean(defualt=true) // inclusion of implicit memory barrier
  }

  push_constant_map: {
      push_data_ref: string, // reference to raw_data resource containing the push_constants data
      shader_target: string, // name of the shader node in the graph to apply the push constants to
  }

dispatch_barrier
""""""""""""""""

The ``dispatch_barrier`` command dispatches memory, image and buffer barriers.

.. code-block::

  dispatch_barrier: {
      image_barrier_refs:[string] (default=[]), // array of image barrier uids
      tensor_barrier_refs:[string] (default=[]), // array of tensor barrier uids
      memory_barrier_refs:[string] (default=[]), // array of memory barrier uids
      buffer_barrier_refs:[string] (default=[]) // array of buffer barrier uids
  }

mark_boundary
"""""""""""""

The ``mark_boundary`` command defines the end of a 'frame' and explicitly submits
JSON commands in the frame. Tools can use this information to identify frames and
capture targeted resources specified in the command options. The end of a 'frame'
implicitly marks the start of the next frame.

.. code-block::

  mark_boundary: {
      resources:[string] // array of named references to the resources to capture
  }


Examples
--------

Example resource descriptors:

.. code-block::

  "resources": [
      "image": {
          "uid": "InputColorBuffer0",
          "dims": [256, 256],
          "mips": "false",
          "format": "VK_FORMAT_R8G8B8A8_SRGB",
          "src": "./color.dds",
          "dst": "",
          "shader_access": "readonly",
          "border_color": "INT_TRANSPARENT_BLACK"
       },
      "tensor": {
          "uid": "intermediate0",
          "dims" : [256,256],
          "data_type": "VK_FORMAT_R32_SFLOAT",
          "shader_access": "readwrite",
      },
      "tensor": {
          "uid": "weights0",
          "dims" : [10,10],
          "data_type": "VK_FORMAT_R32_SFLOAT",
          "src": "./weights.npy",
          "shader_access": "readonly",
      }
  ]

Shader modules that are used in dispatch commands can be defined as resources.
They can have associated ``push_constants`` which are also provided via
``raw_data`` resource definitions.

Shader resource example:

.. code-block::

  "raw_data": {
      "uid": "prep_push_constants",
      "src": "./prep_pc.npy"
  },
  "shader": {
      "uid": "prep_shader_8x8",
      "src": "preprocess.glsl",
      "type": "GLSL",
      "push_constants_size": 16,
      "specialization_constants": [
          {
              id: 0,
              value: 8
          },
          {
              id: 1,
              value: 8
          }
      ]
      //...
  }

You can load complete graphs via the VGF Library Decoder. The complete graphs are specified as
VGF files. For some use cases, you should substitute placeholder shader
nodes in the graph for specific shaders.

.. code-block::

  "graph": {
      "uid": "graph_file"
      "src": "./graph_file.vgf",
      "shader_substitutions" : [
          {"shader_ref":"prep_shader", "target": "tfl_custom_pre_node"}
          {"shader_ref":"post_shader", "target": "tfl_custom_post_node"}
      ],
      //...
  }

The behavior of the scenario is defined with the ``Commands`` section. These
commands are processed in order of appearance in the file.

.. code-block::

  "commands" : [
      "dispatch_compute": {
          "shader_ref": "degamma_shader",
          "push_data_ref": "gamma_consts",
          "bindings": [
              {"set": 0, "id": 0, "resource_ref":"InputColorBuffer0"},
              {"set": 0, "id": 1, "resource_ref":"intermediate0"}
          ],
          "rangeND": [32, 32]
      },
      "dispatch_graph": {
          "graph_ref": "NN_graph",
          "bindings": [
              {"set": 0, "id": 0, "resource_ref":"intermediate0"},
              {"set": 0, "id": 1, "resource_ref":"vectors"},
              {"set": 0, "id": 2, "resource_ref":"depth"},
              {"set": 0, "id": 3, "resource_ref":"upscaled0"}
          ]
      },
      "dispatch_compute": {
          "shader_ref": "post_shader",
          "push_data_ref: "inv_projection",
          "bindings": [
              {"set": 0, "id": 0, "resource_ref":"upscaled0"},
              {"set": 0, "id": 1, "resource_ref":"result0"},
          ],
          "rangeND": [64, 64]
      }
  ]

You can use the ``mark_boundary`` command to signal the completion of a frame and explicitly
submit all commands in this frame.

.. code-block::

        "commands": [
            {
                "dispatch_compute": {
                    "bindings": [
                        {
                            "id": 0,
                            "set": 0,
                            "resource_ref": "inBufferA"
                        },
                        {
                            "id": 1,
                            "set": 0,
                            "resource_ref": "inBufferB"
                        },
                        {
                            "id": 2,
                            "set": 1,
                            "resource_ref": "outBufferAdd"
                        }
                    ],
                    "rangeND": [10],
                    "shader_ref": "add_shader"
                }
            },
            {
                "mark_boundary":{
                    "resources": [
                      "inBufferA",
                      "inBufferB"
                    ]
                }
            }
        ],
        "resources": [
            {
                "shader": {
                    "src": "path/to/add_shader.spv",
                    "type": "SPIR-V",
                    "uid": "add_shader"
                }
            },
            {
                "buffer": {
                    "shader_access": "readonly",
                    "size": 40,
                    "src": "path/to/inBufferA.npy",
                    "uid": "inBufferA"
                }
            },
            {
                "buffer": {
                    "shader_access": "readonly",
                    "size": 40,
                    "src": "path/to/inBufferB.npy",
                    "uid": "inBufferB"
                }
            },
            {
                "buffer": {
                    "dst": "path/to/outBufferAdd.npy",
                    "shader_access": "readwrite",
                    "size": 40,
                    "uid": "outBufferAdd"
                }
            }
        ]
