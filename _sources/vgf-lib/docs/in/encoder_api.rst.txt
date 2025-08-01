VGF Encoder C++ API
===================

The Encoder Application Program Interface is an offline tool that provides a set of API calls for creating VGF files. The API calls allow you to specify the inputs, outputs, resources and modules required to represent a model in the VGF format. The following example outlines the usage of the API calls to create an output VGF file.

Encoder Example Usage
---------------------

After you create the encoder object, you can create resources for a given segment. The VGF Encoder stores these resources in a model resource table. Resources are defined for the segment inputs, outputs, and constants:


.. literalinclude:: ../sources/test/model_resource_tests.cpp
  :language: cpp
  :start-after: MrtEncodeInput begin
  :end-before: MrtEncodeInput end

For a constant resource, constant values are assigned to the created constant object. The resource reference is used to determine the index of the resource in the model resource table:

.. literalinclude:: ../sources/test/model_resource_tests.cpp
  :language: cpp
  :start-after: MrtEncodeConstant begin
  :end-before: MrtEncodeConstant end

Next, you can specify binding slots within the VGF. The assigned resources in the model resource table are then linked:

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotEncodingSample0 begin
  :end-before: BindingSlotEncodingSample0 end

You can add descriptor set information, which is linked to each of the created binding slots:

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotEncodingSample1 begin
  :end-before: BindingSlotEncodingSample1 end

You must then specify the module for the segment, containing the SPIR-V™ module. This can also be done prior to adding resources:

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: ModelSequenceTableEncodingSample0 begin
  :end-before: ModelSequenceTableEncodingSample0 end

Alternatively, you can add a placeholder module. The application provisions the SPIR-V™ binary data when the model is loaded.

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotEncodingSample2 begin
  :end-before: BindingSlotEncodingSample2 end

If required, you can specify push constants for the segment:


.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: PushConstRangesEncodingSample0 begin
  :end-before: PushConstRangesEncodingSample0 end


.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotEncodingSample3 begin
  :end-before: BindingSlotEncodingSample3 end

You must repeat this process for multiple segments in the model. After creating each of the model segments, you must specify the sequencing based on the binding slots inputs and outputs:

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotEncodingSample4 begin
  :end-before: BindingSlotEncodingSample4 end

You must indicate the end of the encoding sequence. Then, you can write the VGF file representing the model:

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotEncodingSample5 begin
  :end-before: BindingSlotEncodingSample5 end

Encoder API Reference
---------------------

.. doxygengroup:: encoderAPI
    :project: MLSDK
    :content-only:
    :members:
