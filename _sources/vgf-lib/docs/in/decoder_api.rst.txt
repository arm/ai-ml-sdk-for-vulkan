VGF Decoder C++ API
===================


The VGF Library decoder enables the parsing of VGF files. The VGF Library contains different sections and the methods for each section. The important sections are the Header section, Model Sequence Table, Module Table, Model Resource Table and the Constant Section.

Header section decoding
```````````````````````

The header decoder allows you to verify the validity of the VGF file and the file version.
The header decoder also uses memory size and offset pairs to provide the location of the other sections within the VGF file.


To parse the VGF file header, you must load the file into memory and then create a header decoder. To create a header decoder, you must provide the VGF data-pointer:

.. literalinclude:: ../sources/test/header_tests.cpp
  :language: cpp
  :start-after: HeaderDecodingSample0 begin
  :end-before: HeaderDecodingSample0 end

After creating a header decoder, you can verify the validity of the VGF file and its compatibility with the library. To verify the validity of the VGF file, check if their versions match:

.. literalinclude:: ../sources/test/header_tests.cpp
  :language: cpp
  :start-after: HeaderDecodingSample1 begin
  :end-before: HeaderDecodingSample1 end

To further verify a potentially unsafe vgf file, use the verify functions for each section:

.. code-block:: cpp

  VerifyModuleTable(
      vgf_data.c_str() + headerDecoder->GetModuleTableOffset(),
      headerDecoder->GetModuleTableSize());

  VerifyModelResourceTable(
      vgf_data.c_str() + headerDecoder->GetModelResourceTableOffset(),
      headerDecoder->GetModelResourceTableSize());

  VerifyModelSequenceTable(
      vgf_data.c_str() + headerDecoder->GetModelSequenceTableOffset(),
      headerDecoder->GetModelSequenceTableSize());

  VerifyConstant(
      vgf_data.c_str() + headerDecoder->GetConstantsOffset(),
      headerDecoder->GetConstantsSize());


Model Sequence Table decoding
`````````````````````````````

The Model Sequence table contains all of the segments in the VGF file.
Each segment entry contains the input and output resources of the segment and their exposed bindings.
The Model sequence table also contains information about any constants that the segment uses and optional push constants.

For each resource, either input, output, or constant, a pointer into the Model Resource table is stored to access detailed information of the resource itself.
For example, if the resource is a tensor or an image, the Model Resource table holds its shape or dimension.

With the previously created header decoder, you must create a Model Sequence Table decoder.

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: ModelSequenceTableDecodingSample0 begin
  :end-before: ModelSequenceTableDecodingSample0 end

To extract all the relevant information of any segment, you can address each segment using the respective index. For example, you can create a binding slot decoder to extract the inputs or outputs to the segment.

Binding Slot decoding
`````````````````````

Each segment in the Model Sequence Table (MST) corresponds to a single Vulkan® pipeline object. You can use binding slots
to map how specific resources are to be bound to pipelines via one or more 'DescriptorSet' objects when using the Vulkan® API. Optionally, you can also use different views of
these slots to determine more optimal scheduling strategies. For example, by analyzing the graph connectivity between segments some platforms may enabled overlapped execution
where dependencies allow.

Most of the useful information required is contained in the Model Resource Table and each binding slot contains an index to an entry in the table.
Multiple Binding slots can reference a single Model Resource Table.

The segment contains 1 or more DescriptorSetInfos. Each DescriptorSetInfos correspond to a separate Vulkan® descriptor set object required by the associated Vulkan® pipeline.

Therefore, when you translate the VGF contents to Vulkan® API calls, there are 2 distinct stages where you need the binding slot information:

#. During creation of the descriptor set layout
#. During writing of the descriptor set

There are several routes to getting binding slot information depending on the required view.

#. The most common route is via DescriptorSetInfos on the 'Segment'. Each segment has a list of descriptor sets which themselves contain a view of the binding slots. There is a 1-1
   mapping between the DescriptorSetInfos in the Model Sequence Table and the Vulkan® API DescriptorSets.
#. The ModelSequenceTable has a list of binding slots that form the inputs and outputs to the entire model. This is useful when connecting game or app resources to the model.
#. Each segment has a list of input and output binding slots. You can use the binding slots for for graph connectivity analysis.

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotDecodingSample0 begin
  :end-before: BindingSlotDecodingSample0 end


To setup the corresponding resources for a segment, you can use the binding slot decoder together with the Model Resource table.


Push Constant decoding
``````````````````````

Vulkan® push constants are also supported in the VGF encoding. The push constants are available in the segment info.

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: PushConstRangesDecodingSample0 begin
  :end-before: PushConstRangesDecodingSample0 end

Model Resource Table decoding
`````````````````````````````

The Module Resource table stores information used to build up the resources which are needed by the model encoded in the VGF.
An entry in the table holds the type of the resource, which can be tensor, image, buffer, along with resource specific information.
For example, a tensor entry contains its element type, shape and stride. However, an image entry contains its image encoding and its dimension.

To find the correct MRT entry, for example, binding slot '0', you can use the previously acquired BindingSlotArrayHandle:

.. literalinclude:: ../sources/test/model_sequence_tests.cpp
  :language: cpp
  :start-after: BindingSlotDecodingSample1 begin
  :end-before: BindingSlotDecodingSample1 end

After you create a Model Resource Table decoder, you can use the obtained mrtIndex to extract information for that binding:

.. literalinclude:: ../sources/test/model_resource_tests.cpp
  :language: cpp
  :start-after: MrtDecodingSample0 begin
  :end-before: MrtDecodingSample0 end

Module Table decoding
`````````````````````

The API facilitates the extraction of each module which contains the module type, SPIR-V™ code existence and, if applicable, its corresponding code.

After you create a Module table decoder, you can extract the respective module of the segment. To extract the module, you can use the moduleIndex:

.. literalinclude:: ../sources/test/module_table_tests.cpp
  :language: cpp
  :start-after: ModuleTableDecodingSample0 begin
  :end-before: ModuleTableDecodingSample0 end

Decoder API reference
---------------------

.. doxygengroup:: VGFDecoderAPI
    :project: MLSDK
    :content-only:
    :members:
