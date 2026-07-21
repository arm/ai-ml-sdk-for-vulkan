VGF File Format
===============

This page describes the VGF on-disk layout written by the current encoder and accepted by the current decoder.
The metadata tables are defined in ``schema/vgf.fbs``; the fixed header and raw constants section are defined by
the C++ layout constants in ``src/header.hpp`` and ``src/constant.hpp``.

VGF File Structure
------------------

The file starts with a fixed 128-byte header. The header records the file format version, the Vulkan header version
used by the encoder, and four file-relative section entries. Each section entry contains a ``uint64`` offset and a
``uint64`` size.

The current section order is:

1. Header
2. Module Table section
3. Model Sequence Table section
4. Model Resource Table section
5. Model Constants section

.. figure:: assets/vgf_file_structure.svg
   :alt: VGF file structure
   :align: center

   Current VGF file layout and cross-references between the header, FlatBuffers metadata tables, resources, segments,
   descriptor bindings, and constants.

Header Layout
-------------

New files use format version ``0.4.3`` and write the ``VGF1`` FourCC magic. The decoder still accepts the deprecated
pre-FourCC magic value for backward compatibility.

.. list-table::
   :header-rows: 1

   * - Offset
     - Size
     - Field
     - Description
   * - 0
     - 4
     - ``magic``
     - FourCC ``VGF1`` in new files.
   * - 4
     - 2
     - ``vk_header_version``
     - ``VK_HEADER_VERSION`` value used by the encoder. Consumers use this to interpret stored Vulkan enum values.
   * - 6
     - 2
     - ``reserved0``
     - Reserved; written as zero.
   * - 8
     - 3
     - ``version``
     - ``major``, ``minor``, and ``patch`` bytes. The current writer emits ``0.4.3``.
   * - 11
     - 1
     - ``reserved1``
     - Reserved; written as zero.
   * - 12
     - 4
     - ``reserved2``
     - Reserved; written as zero.
   * - 16
     - 16
     - ``moduleSection``
     - Offset and size for the Module Table section.
   * - 32
     - 16
     - ``sequenceSection``
     - Offset and size for the Model Sequence Table section.
   * - 48
     - 16
     - ``resourceSection``
     - Offset and size for the Model Resource Table section.
   * - 64
     - 16
     - ``constantSection``
     - Offset and size for the Model Constants section.
   * - 80
     - 48
     - ``reserved3`` ... ``reserved8``
     - Reserved; written as zero.

The decoder validates that the magic and major/minor version are supported and that every section range is contained
inside the file. ``IsLatestVersion`` additionally checks for an exact ``0.4.3`` match.

Section Alignment
-----------------

VGF files written with format version ``0.4.3`` or later align every section offset to an 8-byte boundary. Padding
between sections is written as zero bytes and is not included in the preceding section size. Decoders remain compatible
with older files whose section offsets were not guaranteed to be 8-byte aligned.

FlatBuffers Metadata Sections
-----------------------------

The Module Table, Model Sequence Table, and Model Resource Table sections are FlatBuffers buffers. Each section is
verified independently before decoding.

The Module Table stores ``Module`` entries:

* ``type`` is ``COMPUTE`` or ``GRAPH``.
* ``name`` and ``entry_point`` are strings.
* ``code`` is a ``ModuleCode`` union. Current code variants are SPIR-V ``uint32`` words, GLSL source, and HLSL source.

The Model Sequence Table stores model-level inputs and outputs plus ordered ``SegmentInfo`` entries. Segment metadata
links runtime execution state together:

* ``module_index`` indexes the Module Table.
* ``set_infos`` stores descriptor sets. ``DescriptorSetInfo.set_index`` is explicit when present; ``UINT32_MAX`` means
  it was omitted and decoders fall back to the descriptor's array position.
* ``inputs`` and ``outputs`` are ``BindingSlot`` arrays. Each binding slot records a descriptor ``binding`` and an
  ``mrt_index`` into the Model Resource Table.
* ``constants`` stores indexes into the Model Constants metadata records.
* ``dispatch_shape`` is expected to contain three elements when present.
* ``push_constant_ranges`` stores Vulkan stage flags, byte offsets, and byte sizes.

The Model Resource Table stores ``ModelResourceTableEntry`` records:

* ``vk_descriptor_type`` and ``vk_format`` are stored as opaque Vulkan enum values. ``vk_descriptor_type`` uses
  ``UINT32_MAX`` as the on-disk "not present" sentinel for resources such as constants.
* ``category`` is ``INPUT``, ``OUTPUT``, ``INTERMEDIATE``, or ``CONSTANT``.
* ``description`` stores tensor ``shape`` and ``strides`` arrays.
* ``extra_config`` is an extension point. The current supported variant is ``SamplerConfig``.
* ``alias_group_id`` uses ``UINT32_MAX`` as the "no alias group" sentinel. Non-constant resources may share a group id
  to indicate shared storage.

Model Constants Section
-----------------------

New VGF files store the Model Constants section as a compact raw byte section. Older files can still contain the
legacy FlatBuffers ``ConstantSection`` layout; the decoder keeps support for that legacy representation.

The current raw constants layout is version ``CONST00``:

.. list-table::
   :header-rows: 1

   * - Offset
     - Size
     - Field
     - Description
   * - 0
     - 8
     - ``version``
     - Fixed bytes ``C O N S T 0 0 \0``.
   * - 8
     - 8
     - ``count``
     - Number of constant metadata records.
   * - 16
     - ``count * 24``
     - ``metadata``
     - Fixed-size ``ConstantMetaDataV00`` records.
   * - ``16 + count * 24``
     - remaining bytes
     - ``payload``
     - Raw constant data bytes.

Each ``ConstantMetaDataV00`` record is 24 bytes:

.. list-table::
   :header-rows: 1

   * - Offset
     - Size
     - Field
     - Description
   * - 0
     - 4
     - ``mrt_index``
     - Model Resource Table index for the constant resource.
   * - 4
     - 4
     - ``sparsity_dimension``
     - Sparse dimension, or ``-1`` for a non-sparse constant. Values below ``-1`` are invalid.
   * - 8
     - 8
     - ``size``
     - Constant data size in bytes, excluding any padding.
   * - 16
     - 8
     - ``offset``
     - Offset in bytes from the start of the payload region.

Constant payload entries are stored as raw bytes. The encoder pads each payload entry to an 8-byte boundary, but
``size`` always describes the unpadded constant data length returned by the decoder.

.. caution::
   The fixed header and raw constants section store fixed-width integer fields without endian conversion. The target
   host and the host that created the VGF file must use the same endianness for these raw portions.
