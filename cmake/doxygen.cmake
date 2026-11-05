#
# SPDX-FileCopyrightText: Copyright 2023-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
set(DOXYGEN_INPUT_DIRS)
set(DOXYGEN_STRIP_DIRS)
if("vgf-lib" IN_LIST ML_SDK_COMPONENTS_DIRS)
    set(VGF_SOURCES "${ML_SDK_DOC_COMPONENT_BINARY_ROOT}/vgf-lib/docs/sources")
    list(APPEND DOXYGEN_INPUT_DIRS "${VGF_SOURCES}/include/vgf" "${VGF_SOURCES}/include-c/vgf")
    list(APPEND DOXYGEN_STRIP_DIRS "${VGF_SOURCES}/include/" "${VGF_SOURCES}/include/vgf")
endif()
if("workload-lib" IN_LIST ML_SDK_COMPONENTS_DIRS)
    set(WORKLOAD_SOURCES "${ML_SDK_DOC_COMPONENT_BINARY_ROOT}/workload-lib/docs/sources")
    list(APPEND DOXYGEN_INPUT_DIRS "${WORKLOAD_SOURCES}/include/mlworkloadlib")
    list(APPEND DOXYGEN_STRIP_DIRS "${WORKLOAD_SOURCES}/include")
endif()

set(DOXYGEN_INPUT_PATHS)
set(DOXYGEN_STRIP_PATHS)
set(DOXYGEN_FILES)
foreach(INPUT_DIR IN LISTS DOXYGEN_INPUT_DIRS)
    string(APPEND DOXYGEN_INPUT_PATHS " \"${INPUT_DIR}\"")
    file(GLOB INPUT_FILES CONFIGURE_DEPENDS LIST_DIRECTORIES false
        "${INPUT_DIR}/*.c" "${INPUT_DIR}/*.cpp" "${INPUT_DIR}/*.h"
        "${INPUT_DIR}/*.hpp" "${INPUT_DIR}/*.md" "${INPUT_DIR}/*.dox")
    list(APPEND DOXYGEN_FILES ${INPUT_FILES})
endforeach()
foreach(STRIP_DIR IN LISTS DOXYGEN_STRIP_DIRS)
    string(APPEND DOXYGEN_STRIP_PATHS " \"${STRIP_DIR}\"")
endforeach()
set(DOXYGEN_MANIFEST "${ML_SDK_DOCS_DIR}/doxygen-inputs.txt")
list(JOIN DOXYGEN_FILES "\n" DOXYGEN_MANIFEST_CONTENT)
file(CONFIGURE OUTPUT "${DOXYGEN_MANIFEST}" CONTENT "${DOXYGEN_MANIFEST_CONTENT}\n" @ONLY)
set(DOXYGEN_OUTPUT_DIR "${ML_SDK_DOCS_DIR}/doxygen")
set(DOXYGEN_STAMP "${DOXYGEN_OUTPUT_DIR}/doxygen.stamp")
set(DOXYGEN_INDEX_XML "${DOXYGEN_OUTPUT_DIR}/xml/index.xml")
set(DOXYGEN_DEPENDS "${DOXYGEN_MANIFEST}")
if(DOXYGEN_INPUT_DIRS)
    set(DOXYFILE_GEN "${CMAKE_CURRENT_BINARY_DIR}/Doxyfile")
    configure_file("${ML_SDK_REPO_ROOT}/docs/Doxyfile" "${DOXYFILE_GEN}" @ONLY)
    add_custom_command(OUTPUT "${DOXYGEN_STAMP}" "${DOXYGEN_INDEX_XML}"
        DEPENDS "${DOXYFILE_GEN}" "${DOXYGEN_MANIFEST}" ${DOXYGEN_FILES}
        COMMAND "${CMAKE_COMMAND}" -E rm -f "${DOXYGEN_STAMP}"
        COMMAND "${CMAKE_COMMAND}" -E rm -rf "${DOXYGEN_OUTPUT_DIR}/xml"
        COMMAND "${DOXYGEN_EXECUTABLE}" "${DOXYFILE_GEN}"
        COMMAND "${CMAKE_COMMAND}" -E touch "${DOXYGEN_STAMP}"
        WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
        COMMENT "Generating combined SDK API XML" VERBATIM)
    list(APPEND DOXYGEN_DEPENDS "${DOXYGEN_STAMP}" "${DOXYGEN_INDEX_XML}")
else()
    file(REMOVE_RECURSE "${DOXYGEN_OUTPUT_DIR}/xml")
    file(REMOVE "${DOXYGEN_STAMP}")
endif()
add_custom_target(sdk_doxy_doc DEPENDS ${DOXYGEN_DEPENDS})
