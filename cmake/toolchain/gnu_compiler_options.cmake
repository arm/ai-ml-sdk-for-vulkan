#
# SPDX-FileCopyrightText: Copyright 2023-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

# Compilation warnings
set(ML_SDK_SCENARIO_RUNNER_COMPILE_OPTIONS -Werror -Wall -Wextra -Wsign-conversion -Wconversion -Wpedantic)

if(SCENARIO_RUNNER_GCC_SANITIZERS)
    message(STATUS "GCC Sanitizers enabled")
    add_compile_options(
        -fsanitize=undefined,address
        -fno-sanitize=vptr,alignment
        -fno-sanitize-recover=all
    )
    add_link_options(
        -fsanitize=undefined,address
    )
    unset(SCENARIO_RUNNER_GCC_SANITIZERS CACHE)
endif()
