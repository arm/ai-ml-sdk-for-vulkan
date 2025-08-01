VGF Logging C++ API
===================


The VGF Library produces logging messages. The Logging C++ API allows you to process these logging messages. To enable the logging functionality, you must provide the callback function. The callback function accepts log level and message as input parameters:

.. code-block:: cpp

  #include "vgf/logging.hpp"

  using namespace mlsdk::vgflib::logging;

  void loggingCallback(LogLevel logLevel, const std::string& message) {
    // Implementation of the logging callback
  }

  EnableLogging(loggingCallback);

To disable logging, use the following function:

.. code-block:: cpp

  #include "vgf/logging.hpp"

  using namespace mlsdk::vgflib::logging;

  DisableLogging();

Logging API reference
---------------------

.. doxygengroup:: VGFLoggingAPI
    :project: MLSDK
    :content-only:
