#
# SPDX-FileCopyrightText: Copyright 2022-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

cmake_minimum_required(VERSION 3.25)

project(MLSdkForVulkan
    DESCRIPTION "ML SDK for Vulkan®")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(ML_SDK_GENERATE_CPACK "Generate CPack artifacts" OFF)

list(APPEND CMAKE_MODULE_PATH
    ${CMAKE_CURRENT_LIST_DIR}/cmake
)

if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "${CMAKE_PROJECT_NAME} requires an out of source build.")
endif()

### Options
option(ML_SDK_BUILD_DOCS "Build project documentation" OFF)

# Path to ML SDK for Vulkan® root
set(ML_SDK_FOR_VULKAN_PATH           "${CMAKE_CURRENT_LIST_DIR}" CACHE PATH "Path to ML SDK for Vulkan®")

# Third party dependencies
set(ARGPARSE_PATH                    "${ML_SDK_FOR_VULKAN_PATH}/dependencies/argparse" CACHE PATH "Path to Argparse")
set(CATCH2_PATH                      "${ML_SDK_FOR_VULKAN_PATH}/dependencies/Catch2" CACHE PATH "Path to Catch2")
set(FLATBUFFERS_PATH                 "${ML_SDK_FOR_VULKAN_PATH}/dependencies/flatbuffers" CACHE PATH "Path to FlatBuffers")
set(JSON_PATH                        "${ML_SDK_FOR_VULKAN_PATH}/dependencies/json" CACHE PATH "Path to JSON")
set(LLVM_PATH                        "${ML_SDK_FOR_VULKAN_PATH}/dependencies/llvm-project" CACHE PATH "Path to LLVM")
set(TOSA_TOOLS_PATH                  "${ML_SDK_FOR_VULKAN_PATH}/dependencies/tosa-tools" CACHE PATH "Path to TOSA Tools")

# Khronos dependencies
set(GLSLANG_PATH                     "${ML_SDK_FOR_VULKAN_PATH}/dependencies/glslang" CACHE PATH "Path to GLSLang")
set(SPIRV_HEADERS_PATH               "${ML_SDK_FOR_VULKAN_PATH}/dependencies/SPIRV-Headers" CACHE PATH "Path to SPIRV Headers")
set(SPIRV_CROSS_PATH                 "${ML_SDK_FOR_VULKAN_PATH}/dependencies/SPIRV-Cross" CACHE PATH "Path to SPIRV Cross")
set(SPIRV_TOOLS_PATH                 "${ML_SDK_FOR_VULKAN_PATH}/dependencies/SPIRV-Tools" CACHE PATH "Path to SPIRV Tools")
set(VULKAN_HEADERS_PATH              "${ML_SDK_FOR_VULKAN_PATH}/dependencies/Vulkan-Headers" CACHE PATH "Path to Vulkan Headers")

macro(optional_add_subdirectory dir_path binary)
    if(EXISTS "${dir_path}/CMakeLists.txt")
        message(STATUS "Including component: ${dir_path}")
        add_subdirectory("${dir_path}" ${binary})
        if(ML_SDK_BUILD_DOCS)
            list(APPEND ML_SDK_COMPONENTS_DIRS ${binary})
        endif()
        if(ML_SDK_GENERATE_CPACK)
            cpack_add_component(${binary})
            list(APPEND CPACK_COMPONENTS_ALL ${binary})
        endif()
    elseif(${binary} STREQUAL "vgf-lib")
        message(WARNING "Component ${dir_path} not found. VGF Library is required by Model Converter and Scenario Runner.")
    else()
        message(WARNING "Optional component ${dir_path} not found. Skipping.")
    endif()
endmacro()

# SDK components
set(ML_SDK_MODEL_CONVERTER_PATH      "${ML_SDK_FOR_VULKAN_PATH}/sw/model-coverter" CACHE PATH "Path to the ML SDK Model Converter")
set(ML_SDK_EMULATION_LAYER_PATH      "${ML_SDK_FOR_VULKAN_PATH}/sw/emulation-layer" CACHE PATH "Path to the ML SDK Emulation Layer for Vulkan")
set(ML_SDK_SCENARIO_RUNNER_PATH      "${ML_SDK_FOR_VULKAN_PATH}/sw/scenario-runner" CACHE PATH "Path to the ML SDK Scenario Runner")
set(ML_SDK_VGF_LIB_PATH              "${ML_SDK_FOR_VULKAN_PATH}/sw/vgf-lib" CACHE PATH "Path to the ML SDK VGF Library")
set(ML_SDK_COMPONENTS_DIRS "")

optional_add_subdirectory("${ML_SDK_VGF_LIB_PATH}" vgf-lib)
optional_add_subdirectory("${ML_SDK_MODEL_CONVERTER_PATH}" model-converter)
optional_add_subdirectory("${ML_SDK_EMULATION_LAYER_PATH}" emulation-layer)
optional_add_subdirectory("${ML_SDK_SCENARIO_RUNNER_PATH}" scenario-runner)

if(ML_SDK_GENERATE_CPACK)
    set(CPACK_PACKAGE_NAME "ai_ml_sdk_for_vulkan")
    set(CPACK_GENERATOR "TGZ")
    include(cmake/package.cmake)
    mlsdk_package(
        PACKAGE_NAME ${CPACK_PACKAGE_NAME}
        NAMESPACE ${CPACK_PACKAGE_NAME}
        LICENSES
        "${CMAKE_SOURCE_DIR}/LICENSES/Apache-2.0.txt"
        )
    include(CPack)
endif()

###############################################################################
# Generate documentation
###############################################################################
if(ML_SDK_BUILD_DOCS)
    include(docs/docs.cmake)
endif()
unset(ML_SDK_BUILD_DOCS CACHE)
unset(ML_SDK_GENERATE_CPACK CACHE)
