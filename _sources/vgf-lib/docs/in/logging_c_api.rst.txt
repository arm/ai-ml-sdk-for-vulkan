VGF Logging C API
===================

The VGF Library produces logging messages. The Logging C API allows you to process these logging messages. To enable the logging functionality, you must provide the callback function. The callback function accepts log level and message as input parameters:

.. code-block:: cpp

  #include "vgf/logging.h"

  void loggingCallback(mlsdk_logging_log_level logLevel, const char* message) {
    // Implementation of the logging callback
  }

  mlsdk_logging_enable(loggingCallback);

To disable logging, use the following function:

.. code-block:: cpp

    #include "vgf/logging.h"

    mlsdk_logging_disable();

C Logging API Reference
-----------------------

.. doxygengroup:: VGFLOGGINGCAPI
    :project: MLSDK
    :content-only:
