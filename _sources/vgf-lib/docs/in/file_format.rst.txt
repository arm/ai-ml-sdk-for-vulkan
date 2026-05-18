VGF File Format Notes
=====================

Section Alignment
-----------------

VGF files written with format version ``0.4.3`` or later align each section offset to an 8-byte boundary. Decoders
remain compatible with older files whose section offsets were not guaranteed to be 8-byte aligned.

Model Constants Section
-----------------------

New VGF files store the Model Constants Section as a compact raw byte section. Older files can still contain the
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
   The raw constants section stores fixed-width integer fields and payload bytes without endian conversion. The target
   host and the host that created the VGF file must use the same endianness.
