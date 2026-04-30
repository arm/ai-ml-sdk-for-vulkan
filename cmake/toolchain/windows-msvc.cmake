#
# SPDX-FileCopyrightText: Copyright 2024-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

# Use /Z7-style embedded debug info for MSVC debug-symbol configurations.
# This avoids compiler PDB contention when parallel launchers such as sccache
# are used during Windows builds.
set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT
    "$<$<OR:$<CONFIG:Debug>,$<CONFIG:RelWithDebInfo>>:Embedded>")

# Compilation warnings
set(ML_SDK_SCENARIO_RUNNER_COMPILE_OPTIONS /EHa /WX /W4)
