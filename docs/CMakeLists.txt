#
# SPDX-FileCopyrightText: Copyright 2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
cmake_minimum_required(VERSION 3.25)
project(MLSdkForVulkan LANGUAGES NONE)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
    message(FATAL_ERROR "Documentation requires an out-of-source build. Use -B build-docs.")
endif()

# TODO(standalone-docs): Remove this mode flag once the native entry point is retired.
set(ML_SDK_DOCS_STANDALONE ON)
include("${CMAKE_CURRENT_LIST_DIR}/docs.cmake")
