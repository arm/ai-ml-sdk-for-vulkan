Vulkan® Shader in TOSA Custom Operation Attributes
==================================================

Overview
--------

This schema defines the JSON attributes used to embed a **Vulkan® shader**
inside a **TOSA custom operation**.

It supports:

- Shader entry point definition
- Workgroup configuration
- Textual shader source (GLSL/HLSL)
- Binary SPIR-V™ (base64 encoded)
- Vulkan® resource binding metadata for inputs and outputs

The schema is designed to be:

- Strongly validated
- Vulkan® aligned
- Deterministic in key naming
- Forward-compatible


Top-Level Properties
--------------------

entry_point (required)
~~~~~~~~~~~~~~~~~~~~~~

**Type:** string

Name of the shader entry point.

.. code-block:: json

   "entry_point": "main"


workgroup_sizes (required)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** Array of exactly 3 positive integers

Represents the local workgroup size: [x, y, z]

Constraints:

- Exactly 3 elements
- Each value must be >= 1

Example:

.. code-block:: json

   "workgroup_sizes": [8, 8, 1]

Corresponds to:

.. code-block:: glsl

   layout(local_size_x = 8,
          local_size_y = 8,
          local_size_z = 1) in;


shader_language (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** Enum

Allowed values:

- "" (unspecified)
- "SPIR-V"
- "GLSL"
- "HLSL"

Example:

.. code-block:: json

   "shader_language": "GLSL"


shader_code (optional)
~~~~~~~~~~~~~~~~~~~~~~

**Type:** string

Validation depends on ``shader_language``.

If ``shader_language == "SPIR-V"``:

- Must be base64 encoded
- Represents raw SPIR-V™ binary

Example:

.. code-block:: json

   "shader_language": "SPIR-V",
   "shader_code": "AwIjBAAAAAEAAAABAAEAAAA..."

Otherwise (GLSL/HLSL):

- Treated as plain text shader source

Example:

.. code-block:: json

   "shader_language": "GLSL",
   "shader_code": "void main() { }"


push_constants (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** string

Comma-separated "name: size" pairs describing push constant layout.

Example:

.. code-block:: json

   "push_constants": "scale: 4, bias: 4"

Future versions may represent this as structured JSON.


Input / Output Resource Attributes
-----------------------------------

Resources are described using indexed attribute names.

Naming Convention
~~~~~~~~~~~~~~~~~

::

   input_<index>_<property>
   output_<index>_<property>

Where:

- ``<index>`` is a non-negative integer
- Leading zeros are not allowed
  - Valid: ``input_0``, ``input_1``, ``input_10``
  - Invalid: ``input_01``

Example:

.. code-block:: json

   "input_0_vkformat": "VK_FORMAT_R32_SFLOAT",
   "input_0_vkdescriptortype": "VK_DESCRIPTOR_TYPE_STORAGE_BUFFER",
   "input_0_binding": 0,
   "input_0_descriptorset": 0


Resource Properties
-------------------

Each indexed input/output may define the following.


_vkformat
~~~~~~~~~

**Type:** string

Vulkan® format (e.g., ``VK_FORMAT_R32_SFLOAT``).

Example:

.. code-block:: json

   "input_0_vkformat": "VK_FORMAT_R32G32B32A32_SFLOAT"


_vkdescriptortype
~~~~~~~~~~~~~~~~~

**Type:** string

Must follow Vulkan® naming convention:

::

   VK_DESCRIPTOR_TYPE_[A-Z0-9_]+

Examples:

- ``VK_DESCRIPTOR_TYPE_STORAGE_BUFFER``
- ``VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER``
- ``VK_DESCRIPTOR_TYPE_STORAGE_TENSOR_EXT``


_type
~~~~~

**Type:** string

Logical resource type.

Examples:

- "Tensor"
- "Image"
- "Buffer"


_binding
~~~~~~~~

**Type:** Integer >= 0

Vulkan® binding index.

Example:

.. code-block:: json

   "input_0_binding": 0


_descriptorset
~~~~~~~~~~~~~~

**Type:** Integer >= 0

Descriptor set index.

Example:

.. code-block:: json

   "input_0_descriptorset": 0


Complete Example — GLSL
------------------------

.. code-block:: json

   {
     "entry_point": "main",
     "workgroup_sizes": [8, 8, 1],
     "shader_language": "GLSL",
     "shader_code": "void main() { }",

     "input_0_vkformat": "VK_FORMAT_R32_SFLOAT",
     "input_0_vkdescriptortype": "VK_DESCRIPTOR_TYPE_STORAGE_BUFFER",
     "input_0_binding": 0,
     "input_0_descriptorset": 0,

     "output_0_vkformat": "VK_FORMAT_R32_SFLOAT",
     "output_0_vkdescriptortype": "VK_DESCRIPTOR_TYPE_STORAGE_BUFFER",
     "output_0_binding": 1,
     "output_0_descriptorset": 0
   }


Complete Example — SPIR-V™
--------------------------

.. code-block:: json

   {
     "entry_point": "main",
     "workgroup_sizes": [16, 16, 1],
     "shader_language": "SPIR-V",
     "shader_code": "AwIjBAAAAAEAAAABAAEAAAA...",

     "input_0_vkformat": "VK_FORMAT_R32G32B32A32_SFLOAT",
     "input_0_vkdescriptortype": "VK_DESCRIPTOR_TYPE_STORAGE_BUFFER",
     "input_0_binding": 0,
     "input_0_descriptorset": 0
   }
