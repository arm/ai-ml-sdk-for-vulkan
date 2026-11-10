#
# SPDX-FileCopyrightText: Copyright 2023-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
set(BREATHE_PROJECT_ARGS "-Dbreathe_projects.MLSDK=${DOXYGEN_XML_GEN}")
if("scenario-runner" IN_LIST ML_SDK_COMPONENTS_DIRS)
    set(SCENARIO_XML "${ML_SDK_DOC_COMPONENT_BINARY_ROOT}/scenario-runner/docs/doxygen")
    list(APPEND BREATHE_PROJECT_ARGS "-Dbreathe_projects.ScenarioRunner=${SCENARIO_XML}/xml")
    list(APPEND SPHINX_DEPENDS scenario_runner_doxy_doc
        "${SCENARIO_XML}/doxygen.stamp" "${SCENARIO_XML}/xml/index.xml")
endif()

set(SPHINX_WARN_ARGS)
list(LENGTH ML_SDK_COMPONENTS_DIRS COMPONENT_COUNT)
if(COMPONENT_COUNT EQUAL 5)
    list(APPEND SPHINX_WARN_ARGS -W)
else()
    message(STATUS "Sparse checkout detected, allowing doc warnings")
endif()
set(CLEANUP_DIRS)
foreach(COMPONENT vgf-lib model-converter emulation-layer workload-lib scenario-runner)
    list(APPEND CLEANUP_DIRS "${SPHINX_BLD_DIR}/${COMPONENT}/docs/generated")
endforeach()
set(SPHINX_STAMP "${ML_SDK_DOCS_DIR}/sphinx.stamp")
add_custom_command(OUTPUT "${SPHINX_STAMP}" "${SPHINX_INDEX_HTML}"
    DEPENDS ${SPHINX_DEPENDS} ${DOXYGEN_DEPENDS}
    COMMAND "${CMAKE_COMMAND}" -E rm -f "${SPHINX_STAMP}"
    COMMAND "${CMAKE_COMMAND}" -E rm -rf "${SPHINX_BLD_DIR}"
    COMMAND "${SPHINX_EXECUTABLE}" -b html ${SPHINX_WARN_ARGS} ${BREATHE_PROJECT_ARGS}
        "${SPHINX_SRC_DIR}" "${SPHINX_BLD_DIR}"
    COMMAND "${CMAKE_COMMAND}" -E rm -rf ${CLEANUP_DIRS}
    COMMAND "${CMAKE_COMMAND}" -E touch "${SPHINX_STAMP}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    COMMENT "Generating combined SDK documentation with Sphinx" VERBATIM)
add_custom_target(sdk_sphx_doc DEPENDS "${SPHINX_STAMP}" "${SPHINX_INDEX_HTML}" sdk_doxy_doc)
