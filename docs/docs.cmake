#
# SPDX-FileCopyrightText: Copyright 2023-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
include(cmake/doxygen.cmake)
include(cmake/sphinx.cmake)

if(NOT DOXYGEN_FOUND OR NOT SPHINX_FOUND)
    return()
endif()

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/README.md ${SPHINX_GEN_DIR}/README.md COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/CONTRIBUTING.md ${SPHINX_GEN_DIR}/CONTRIBUTING.md COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/SECURITY.md ${SPHINX_GEN_DIR}/SECURITY.md COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/LICENSES/Apache-2.0.txt ${SPHINX_GEN_DIR}/Apache-2.0.txt COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/scripts/compare_numpy.py ${SPHINX_GEN_DIR}/scripts/compare_numpy.py COPYONLY)

execute_process(
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${SPHINX_SRC_DIR}"
    COMMAND_ERROR_IS_FATAL ANY)

foreach(SDK_COMPONENT_DIR ${ML_SDK_COMPONENTS_DIRS})
    execute_process(
        COMMAND "${CMAKE_COMMAND}" -E create_symlink "${CMAKE_CURRENT_BINARY_DIR}/${SDK_COMPONENT_DIR}" "${SPHINX_SRC_DIR}/${SDK_COMPONENT_DIR}"
        COMMAND_ERROR_IS_FATAL ANY)
endforeach()

# set source inputs list
file(GLOB_RECURSE  DOC_SRC_FILES CONFIGURE_DEPENDS FOLLOW_SYMLINKS RELATIVE ${SPHINX_SRC_DIR_IN} ${SPHINX_SRC_DIR_IN}/*)
set(DOC_SRC_FILES_FULL_PATHS "")
foreach(SRC_IN IN LISTS DOC_SRC_FILES)
    set(DOC_SOURCE_FILE_IN "${SPHINX_SRC_DIR_IN}/${SRC_IN}")
    set(DOC_SOURCE_FILE "${SPHINX_SRC_DIR}/${SRC_IN}")
    configure_file(${DOC_SOURCE_FILE_IN} ${DOC_SOURCE_FILE} COPYONLY)
    list(APPEND DOC_SRC_FILES_FULL_PATHS ${DOC_SOURCE_FILE})
endforeach()

add_custom_command(
    OUTPUT ${SPHINX_INDEX_HTML}
    DEPENDS ${DOC_SRC_FILES_FULL_PATHS}
    COMMAND ${SPHINX_EXECUTABLE} -b html -Dbreathe_projects.MLSDK=${DOXYGEN_XML_GEN} ${SPHINX_SRC_DIR} ${SPHINX_BLD_DIR}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Generating API documentation with Sphinx"
    VERBATIM
)

# Workaround sphinx leaking documentation source file in the target documentation folder
add_custom_command(
    OUTPUT SYMBOLIC cleanup_target_html
    DEPENDS ${SPHINX_INDEX_HTML}
    COMMAND rm -rf ${SPHINX_BLD_DIR}/model-converter/docs/generated
    COMMAND rm -rf ${SPHINX_BLD_DIR}/emulation-layer/docs/generated
    COMMAND rm -rf ${SPHINX_BLD_DIR}/scenario-runner/docs/generated
    COMMAND rm -rf ${SPHINX_BLD_DIR}/vgf-lib/docs/generated
    COMMENT "Remove all component/docs/generated folders"
    VERBATIM
)

# build components documentation first to avoid sphinx warnings that
# generated files with help messages are not found
set(ML_SDK_DOC_DEP_TARGETS "")
add_custom_target(deps_doc)
foreach(component IN LISTS ML_SDK_COMPONENTS_DIRS)
    if(component STREQUAL "vgf-lib")
        list(APPEND ML_SDK_DOC_DEP_TARGETS vgf_doc)
    elseif(component STREQUAL "scenario-runner")
        list(APPEND ML_SDK_DOC_DEP_TARGETS scenario_runner_doc)
    elseif(component STREQUAL "emulation-layer")
        message("EMULATION LAYER ADDED")
        list(APPEND ML_SDK_DOC_DEP_TARGETS mlel_doc)
    elseif(component STREQUAL "model-converter")
        list(APPEND ML_SDK_DOC_DEP_TARGETS model_converter_doc)
    endif()
endforeach()
add_dependencies(deps_doc ${ML_SDK_DOC_DEP_TARGETS})
add_dependencies(sdk_sphx_doc deps_doc)
add_dependencies(sdk_doxy_doc deps_doc)

# main target to build the docs
add_custom_target(sdk_doc ALL DEPENDS sdk_sphx_doc sdk_doxy_doc SOURCES "${SPHINX_SRC_DIR}/index.rst" cleanup_target_html)
