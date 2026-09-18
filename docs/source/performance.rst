Performance data and analysis
=============================

Scenario Runner provides several methods for collecting timing and diagnostic
information.

.. list-table::
   :header-rows: 1

   * - Method
     - Use it for
     - Output
   * - Runtime profiling
     - Measuring Vulkan® command execution
     - JSON
   * - Performance counters
     - Measuring host-side setup and preparation
     - JSON
   * - Emulation Layer graph profiling
     - Measuring individual operators inside the Emulation Layer
     - JSON
   * - Neural accelerator statistics
     - Collecting implementation-specific accelerator statistics
     - Binary
   * - Neural accelerator debug database
     - Driver-specific advanced debugging
     - Binary

Runtime profiling
-----------------

Use ``--profiling-dump-path`` to collect Vulkan® timestamp information:

.. code-block:: console

   scenario-runner \
       --scenario scenario.json \
       --profiling-dump-path profiling.json

The output contains the command name and type, timestamp values, timestamp
period, execution time in milliseconds, and iteration number.

``Total execution time [ms]`` records the total execution time across all
iterations.

For data graph pipelines, the output can also contain ``Memory Usage`` entries.
``Session memory [bytes]`` is the session-memory requirement reported for the
pipeline, not the total or peak GPU memory usage.

When ``--dry-run`` is used, Scenario Runner can report session-memory
requirements, but it does not produce execution timestamps.

Host-side performance counters
------------------------------

Use ``--perf-counters-dump-path`` to collect host-side timings:

.. code-block:: console

   scenario-runner \
       --scenario scenario.json \
       --perf-counters-dump-path counters.json

The output uses microseconds and groups measurements into categories such as
scenario setup, pipeline setup, running the scenario, loading or saving the
pipeline cache, and saving results.

``Time to Inference`` is the preparation time before the first inference starts.

``Total Scenario Time`` is the sum of all performance counters recorded by
Scenario Runner.

These counters measure host-side time rather than individual GPU command
execution. Use runtime profiling for command-level Vulkan® execution times.

Emulation Layer graph profiling
-------------------------------

Enable Emulation Layer graph profiling before starting Scenario Runner:

.. code-block:: console

   export VMEL_GRAPH_PROFILING=1

Then provide an existing output directory:

.. code-block:: console

   scenario-runner \
       --scenario scenario.json \
       --emulation-layer-profiling-dump-dir profiling-output

Scenario Runner writes one JSON file per graph pipeline:

.. code-block:: text

   EmulationLayerPipeline_0.json
   EmulationLayerPipeline_1.json

Each sample contains:

- The submission and graph-dispatch indexes.
- The internal pipeline index and kind.
- The operator name.
- Timestamp values and their difference.
- The calculated execution time in milliseconds.

The ``by_operator`` section groups samples by pipeline kind and operator name.
It provides the dispatch count and the total, average, minimum, and maximum
execution times.

Graph profiling requires a Vulkan® queue family with non-zero
``timestampValidBits``. If timestamp queries are unavailable, graph execution
can continue, but no profiling samples are collected.

These results describe execution inside the Emulation Layer and are not
representative of native neural accelerator performance.

Neural accelerator statistics
------------------------------

Scenario Runner supports
``VK_ARM_data_graph_neural_accelerator_statistics`` for data graph pipelines.
When this extension and its ``dataGraphNeuralAcceleratorStatistics`` feature
are available, Scenario Runner can request neural accelerator debug database
and statistics output from graph pipelines. Scenario Runner fails before
creating the Vulkan® device if either dump is requested without both.

Use ``--neural-statistics-dump-dir`` to enable statistics collection and dump
the resulting statistics memory after execution.

``--neural-statistics-mode`` selects the statistics mode, using ``0`` for
``VK_NEURAL_ACCELERATOR_STATISTICS_MODE_STATISTICS_0_ARM`` and ``1`` for
``VK_NEURAL_ACCELERATOR_STATISTICS_MODE_STATISTICS_1_ARM``.

For example:

.. code-block:: console

   scenario-runner \
       --scenario scenario.json \
       --neural-statistics-dump-dir statistics-output \
       --neural-statistics-mode 0

Scenario Runner writes files such as:

.. code-block:: text

   Graph_Pipeline_0_Statistics_0.bin
   Graph_Pipeline_0_Statistics_1.bin

The contents and interpretation of these dumps are implementation-specific.
Scenario Runner writes the data returned by the Vulkan® implementation to disk
without interpreting it.

The Emulation Layer does not implement this hardware-specific extension.

Neural accelerator debug database
---------------------------------

Use ``--neural-debug-database-dump-dir`` to dump the neural accelerator debug
database for graph pipelines that expose one:

.. code-block:: console

   scenario-runner \
       --scenario scenario.json \
       --neural-debug-database-dump-dir debug-output

Scenario Runner writes files such as:

.. code-block:: text

   Graph_Pipeline_0_Debug_Database.bin

The debug database is supplied by the driver and saved without interpretation.
If a pipeline does not expose a debug database, no file is created.

Choosing a measurement
----------------------

Use runtime profiling for command-level Vulkan® execution times.

Use performance counters for host-side setup, pipeline creation, caching, and
other Scenario Runner operations.

Use Emulation Layer graph profiling for per-operator measurements while using
the Emulation Layer.

Use neural accelerator statistics and debug databases for hardware-specific
diagnostic data.
