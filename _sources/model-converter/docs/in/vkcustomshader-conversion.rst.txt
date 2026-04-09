Vulkan® Custom Shader Conversion to VGF
=======================================

Overview
--------

A TOSA custom operation is interpreted as a Vulkan® compute shader and
converted into a VGF representation when all of the following conditions
are met:

- Domain Name (``domain_name``) is set to:

  ::

     "com.arm.VulkanCustomShader"

- Operator Name (``operator_name``) encodes the logical name of the shader.
- Implementation Attributes (``implementation_attrs``) follow the schema defined in:

  :doc:`vkshader-custom-op-encoding`

When these conditions are satisfied, the custom operation is treated as a
Vulkan® compute shader node during VGF generation.

This section defines both the semantic contract and the partitioning
behavior required to correctly lower mixed ML and shader models.


Required TOSA Fields
--------------------

Domain Name (``domain_name``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Must be:**

::

   com.arm.VulkanCustomShader

This value acts as the feature gate that enables Vulkan® shader lowering.


Operator Name (``operator_name``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** string

Encodes the logical name of the shader.

This name is used to identify the shader during conversion and may be used
for:

- Debug labeling
- Pipeline identification
- Symbol naming in generated artifacts


Implementation Attributes (``implementation_attrs``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Type:** JSON object

Must conform to the schema defined in:

::

   docs/source/vkshader-custom-op-encoding.rst

This schema defines:

- Entry point
- Workgroup sizes
- Shader source or SPIR-V™ binary
- Descriptor bindings
- Resource formats
- Push constant layout


Model Partitioning
------------------

ML models are represented as directed acyclic graphs (DAGs),
where nodes are operations and edges represent data dependencies.

Models may contain a mix of:

- Regular ML operations
- Shader custom operations (as defined above)

Vulkan® execution constraints require that:

- ML workloads cannot be dispatched in the same pipeline call
  as shader workloads.
- Neural Engine accelerators and classical GPU engines must be
  scheduled through separate Vulkan® pipelines.

Therefore, before VGF generation, the model is partitioned into
sub-models that can be executed independently.


Partitioning Strategy
---------------------

The partitioning follows these principles:

- Each shader custom operation forms its own partition.
- Regular ML operations occurring:
  - before the first shader custom operation,
  - between two shader custom operations,
  - or after the last shader custom operation,
  are grouped into ML partitions.
- Connections crossing partition boundaries become explicit
  inputs and outputs of the generated sub-models.

This transforms a single model DAG into a sequence (or DAG)
of sub-graphs, each mapped to an independent Vulkan® pipeline.


Execution Correctness
---------------------

Partitioning preserves the semantics of the original model by:

- Respecting all data dependencies.
- Ensuring that an operation executes only after its inputs are produced.
- Introducing synchronization between partitions where required
  (e.g., memory barriers and cache invalidation).

A partition cannot execute until all partitions producing its
required inputs have completed.

This guarantees ordering correctness while allowing execution
on heterogeneous GPU engines.


Partitioning Algorithm (Conceptual)
-----------------------------------

The model is traversed in breadth-first order.
Each operation is assigned a ``partition_id``.

- Shader custom operations always receive a new partition.
- Regular ML operations inherit or create partitions based on
  the partitions of their parent operations.

All operations sharing the same ``partition_id`` belong to the same
sub-model.

The algorithm ensures:

- Parent operations are processed before their children.
- Shader and ML operations never coexist in the same partition.
- Partition identifiers increase monotonically.


Conversion Semantics
--------------------

When a TOSA custom operation satisfies the required constraints:

1. The operation is isolated into its own partition.
2. A VGF compute node is generated for that partition.
3. The shader is materialized as:
   - SPIR-V™ binary (decoded from base64 if necessary), or
   - Compiled from textual source if GLSL or HLSL.
4. Descriptor sets and bindings are created according to the indexed
   ``input_<index>_*`` and ``output_<index>_*`` attributes.
5. Workgroup sizes are mapped to the compute dispatch configuration.
6. Synchronization is inserted between adjacent partitions as required.

The conversion is deterministic and fully driven by the schema-defined
attributes.


Minimal Example
---------------

.. code-block:: json

   {
     "domain_name": "com.arm.VulkanCustomShader",
     "operator_name": "MyComputeKernel",
     "implementation_attrs": {
       "entry_point": "main",
       "workgroup_sizes": [8, 8, 1],
       "shader_language": "GLSL",
       "shader_code": "void main() { }",

       "input_0_vkformat": "VK_FORMAT_R32_SFLOAT",
       "input_0_vkdescriptortype": "VK_DESCRIPTOR_TYPE_STORAGE_BUFFER",
       "input_0_binding": 0,
       "input_0_descriptorset": 0
     }
   }


Design Notes
------------

- Domain name (``domain_name``) acts as an explicit opt-in mechanism.
- The schema ensures that only well-formed Vulkan®-compatible shaders
  are converted.
- The conversion assumes compute shader semantics.
- Partitioning enables efficient scheduling across GPU engines
  while preserving correctness.

Any custom operation not satisfying these constraints is not interpreted
as a Vulkan® shader and is handled according to the default custom
operation path.
