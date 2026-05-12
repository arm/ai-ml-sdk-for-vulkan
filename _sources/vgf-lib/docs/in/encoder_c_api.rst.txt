VGF Encoder C API
=================

The Encoder C API is a thin C wrapper over the C++ VGF Encoder API. It allows C callers to create VGF files by adding
modules, resources, resource alias groups, sampler metadata, constants, binding slots, descriptor set information,
segments, model inputs and model outputs.

The API owns an encoder object returned by ``mlsdk_encoder_create``. Destroy the encoder with
``mlsdk_encoder_destroy``. After all entries have been added, call ``mlsdk_encoder_finish`` and then
``mlsdk_encoder_write_to_file``.

C Encoder API Reference
-----------------------

.. doxygengroup:: VGFCEncoderAPI
    :project: MLSDK
    :content-only:
