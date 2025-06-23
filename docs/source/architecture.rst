Architecture
============

The following shows how each of the ML SDK for Vulkan® components can be used in a larger system:

.. figure:: assets/ml_sdk_for_vulkan_components.svg
   :align: center
   :width: 85%

Production
----------

The proposed production workflow involves integrating the ML SDK Model Converter into the
application or game :code:`asset deployment pipeline`. The pipeline needs a TOSA intermediate
representation of a framework specific native model file. To obtain such a TOSA intermediate
representation, a specific framework to TOSA converter should be used (not depicted here).

The TOSA intermediate representation is then passed to the ML SDK Model Converter
to produce a :code:`.vgf` file. The VGF file contents can then be:

• Embedded into the game or application's native packaging format.
• Distributed as a file on disk as part of the normal platform specific application deployment flow.

.. tip::
    When exploring the API, such a tight integration is not necessary as the Model Converter can work directly
    with the framework files. The ML SDK Scenario Runner can also parse the VGF file directly. Passing the TOSA intermediate
    representation to the ML SDK Model Converter is recommended for smoother Model Authoring workflows when in
    production.

The application or game component that runs on the device, must integrate the
:code:`ML SDK VGF Library decoder` library to parse the VGF file contents so that the application or
game code can set up the required Vulkan® state.

.. note::
    The ML SDK VGF Library does not make any calls into the Vulkan® API. The integration must translate the parsed
    information directly into Vulkan® API calls, for example, allocating memory and creating resources,
    pipelines, synchronisation, and session objects.

Exploration
-----------

When exploring the viability of a ML use case or API integration, it can be useful to first explore the use
case using the ML SDK Scenario Runner. The ML SDK Scenario Runner allows running use cases in a declarative manner before
working on more complicated feature integrations.

.. tip::
    While the API is relatively new, we recommend you use the ML SDK Emulation Layer for Vulkan® for exploration. The Emulation Layer
    provides a TOSA conformant software implementation of the Vulkan® graph and tensor extensions. The Emulation
    Layer is enabled by the Vulkan® Layer mechanism.

    Another useful tool for exploration and debugging is the VGF Dump Tool. The VGF Dump Tool allows a developer
    to extract specific elements of the VGF file or even generate a template scenario description for a VGF file.
