#
# SPDX-FileCopyrightText: Copyright 2023-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
# TODO(standalone-docs): Remove legacy branches below once scripts/build.py
# --doc/--doc-only use the standalone project and the native CMakeLists.txt no
# longer includes this file. Then remove ML_SDK_DOCS_STANDALONE and its guards,
# retaining standalone setup and making the staging-manifest check unconditional.
get_filename_component(ML_SDK_REPO_ROOT "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)
set(ML_SDK_DOCS_DIR "${CMAKE_CURRENT_BINARY_DIR}/docs")
set(SPHINX_SRC_DIR_IN "${ML_SDK_REPO_ROOT}/docs/source")
set(SPHINX_SRC_DIR "${ML_SDK_DOCS_DIR}/in")
set(SPHINX_BLD_DIR "${ML_SDK_DOCS_DIR}/out")
set(SPHINX_GEN_DIR "${ML_SDK_DOCS_DIR}/generated")
set(SPHINX_INDEX_HTML "${SPHINX_BLD_DIR}/index.html")
set(DOXYGEN_XML_GEN "${ML_SDK_DOCS_DIR}/doxygen/xml")

list(APPEND CMAKE_MODULE_PATH "${ML_SDK_REPO_ROOT}/cmake")
if(ML_SDK_DOCS_STANDALONE)
    find_package(Doxygen 1.9.1 REQUIRED)
    find_package(Sphinx REQUIRED)
else()
    # TODO(standalone-docs): Remove this optional-tool branch with the native
    # documentation entry point; standalone documentation requires both tools.
    find_package(Doxygen)
    find_package(Sphinx)
    if(NOT DOXYGEN_FOUND OR NOT SPHINX_FOUND)
        message(STATUS "Doxygen or Sphinx is not available. Cannot generate documentation.")
        return()
    endif()
endif()

set(SPHINX_DEPENDS)
if(ML_SDK_DOCS_STANDALONE)
    set(ML_SDK_DOC_COMPONENT_BINARY_ROOT "${SPHINX_SRC_DIR}")
    set(ML_SDK_COMPONENTS_DIRS)
    set(SDK_COMPONENT_NAMES vgf-lib model-converter emulation-layer workload-lib scenario-runner)
    foreach(COMPONENT IN LISTS SDK_COMPONENT_NAMES)
        string(TOUPPER "${COMPONENT}" COMPONENT_KEY)
        string(REPLACE "-" "_" COMPONENT_KEY "${COMPONENT_KEY}")
        set(COMPONENT_PATH_VAR "ML_SDK_${COMPONENT_KEY}_PATH")
        set(${COMPONENT_PATH_VAR} "${ML_SDK_REPO_ROOT}/sw/${COMPONENT}" CACHE PATH "Path to ${COMPONENT}")
        set(COMPONENT_ROOT "${${COMPONENT_PATH_VAR}}")
        set(COMPONENT_BINARY "${ML_SDK_DOC_COMPONENT_BINARY_ROOT}/${COMPONENT}")
        file(GLOB COMPONENT_ENTRY CONFIGURE_DEPENDS "${COMPONENT_ROOT}/CMakeLists.txt")
        if(NOT COMPONENT_ENTRY)
            message(STATUS "Optional documentation component ${COMPONENT} is absent")
            # This exact child subtree belongs to this component; retain no stale pages.
            file(REMOVE_RECURSE "${COMPONENT_BINARY}")
            continue()
        endif()
        if(NOT EXISTS "${COMPONENT_ROOT}/docs/CMakeLists.txt")
            message(FATAL_ERROR "${COMPONENT} requires its standalone docs/CMakeLists.txt")
        endif()

        add_subdirectory("${COMPONENT_ROOT}/docs" "${COMPONENT_BINARY}" EXCLUDE_FROM_ALL)
        list(APPEND ML_SDK_COMPONENTS_DIRS "${COMPONENT}")
    endforeach()

else()
    # TODO(standalone-docs): Remove this native-layout symlink adapter when the
    # native entry point is retired. Standalone children stage directly in docs/in.
    set(ML_SDK_DOC_COMPONENT_BINARY_ROOT "${CMAKE_CURRENT_BINARY_DIR}")
    file(MAKE_DIRECTORY "${SPHINX_SRC_DIR}")
    foreach(COMPONENT IN LISTS ML_SDK_COMPONENTS_DIRS)
        execute_process(
            COMMAND "${CMAKE_COMMAND}" -E create_symlink
                "${ML_SDK_DOC_COMPONENT_BINARY_ROOT}/${COMPONENT}" "${SPHINX_SRC_DIR}/${COMPONENT}"
            COMMAND_ERROR_IS_FATAL ANY)
    endforeach()
endif()

foreach(COMPONENT IN LISTS ML_SDK_COMPONENTS_DIRS)
    set(COMPONENT_BINARY "${ML_SDK_DOC_COMPONENT_BINARY_ROOT}/${COMPONENT}")
    get_directory_property(COMPONENT_FILES DIRECTORY "${COMPONENT_BINARY}" DEFINITION DOC_STAGED_FILES)
    get_directory_property(COMPONENT_MANIFEST DIRECTORY "${COMPONENT_BINARY}" DEFINITION DOC_STAGED_MANIFEST)
    if(ML_SDK_DOCS_STANDALONE AND (NOT COMPONENT_FILES OR NOT EXISTS "${COMPONENT_MANIFEST}"))
        message(FATAL_ERROR "${COMPONENT} does not provide a documentation staging manifest")
    endif()
    list(APPEND SPHINX_DEPENDS ${COMPONENT_FILES} ${COMPONENT_MANIFEST})
endforeach()

# Only SDK-owned files belong to this manifest; child projects own their files.
set(SDK_STAGED_FILES)
foreach(SOURCE README.md CONTRIBUTING.md SECURITY.md scripts/compare_numpy.py)
    configure_file("${ML_SDK_REPO_ROOT}/${SOURCE}" "${SPHINX_GEN_DIR}/${SOURCE}" COPYONLY)
    list(APPEND SDK_STAGED_FILES "${SPHINX_GEN_DIR}/${SOURCE}")
endforeach()
configure_file("${ML_SDK_REPO_ROOT}/LICENSES/Apache-2.0.txt"
    "${SPHINX_GEN_DIR}/Apache-2.0.txt" COPYONLY)
list(APPEND SDK_STAGED_FILES "${SPHINX_GEN_DIR}/Apache-2.0.txt")
file(GLOB_RECURSE SDK_SOURCES CONFIGURE_DEPENDS FOLLOW_SYMLINKS LIST_DIRECTORIES false
    RELATIVE "${SPHINX_SRC_DIR_IN}" "${SPHINX_SRC_DIR_IN}/*")
foreach(SOURCE IN LISTS SDK_SOURCES)
    configure_file("${SPHINX_SRC_DIR_IN}/${SOURCE}" "${SPHINX_SRC_DIR}/${SOURCE}" COPYONLY)
    list(APPEND SDK_STAGED_FILES "${SPHINX_SRC_DIR}/${SOURCE}")
endforeach()

set(SDK_MANIFEST "${ML_SDK_DOCS_DIR}/sdk-staged-files.txt")
if(EXISTS "${SDK_MANIFEST}")
    file(STRINGS "${SDK_MANIFEST}" PREVIOUS_FILES)
    foreach(PREVIOUS_FILE IN LISTS PREVIOUS_FILES)
        cmake_path(IS_PREFIX ML_SDK_DOCS_DIR "${PREVIOUS_FILE}" NORMALIZE SDK_OWNED)
        if(SDK_OWNED AND NOT PREVIOUS_FILE IN_LIST SDK_STAGED_FILES)
            file(REMOVE "${PREVIOUS_FILE}")
        endif()
    endforeach()
endif()
list(JOIN SDK_STAGED_FILES "\n" SDK_MANIFEST_CONTENT)
file(CONFIGURE OUTPUT "${SDK_MANIFEST}" CONTENT "${SDK_MANIFEST_CONTENT}\n" @ONLY)
list(APPEND SPHINX_DEPENDS ${SDK_STAGED_FILES} "${SDK_MANIFEST}")

# TODO(standalone-docs): Remove this entire block with the native entry point:
# standalone docs use checked-in snapshots, so need neither native Python imports
# nor component HTML builds (deps_doc and its target-name mapping).
if(NOT ML_SDK_DOCS_STANDALONE)
    set(SPHINX_COMMAND ${SPHINX_EXECUTABLE})
    set(SPHINX_PYTHONPATH)
    if(EXISTS "${ML_SDK_SCENARIO_RUNNER_PATH}/CMakeLists.txt")
        list(APPEND SPHINX_PYTHONPATH $<TARGET_FILE_DIR:scenario_runner_py>)
        list(APPEND SPHINX_DEPENDS scenario_runner_py)
    endif()
    if(TARGET vgfpy)
        list(APPEND SPHINX_PYTHONPATH $<TARGET_FILE_DIR:vgfpy>)
        list(APPEND SPHINX_DEPENDS vgfpy)
    endif()
    if(SPHINX_PYTHONPATH)
        cmake_path(CONVERT "${SPHINX_PYTHONPATH}" TO_NATIVE_PATH_LIST SPHINX_PYTHONPATH)
        string(REPLACE ";" "\\;" SPHINX_PYTHONPATH "${SPHINX_PYTHONPATH}")
        list(PREPEND SPHINX_COMMAND
            ${CMAKE_COMMAND} -E env "PYTHONPATH=${SPHINX_PYTHONPATH}")
    endif()

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
            list(APPEND ML_SDK_DOC_DEP_TARGETS mlel_doc)
        elseif(component STREQUAL "model-converter")
            list(APPEND ML_SDK_DOC_DEP_TARGETS model_converter_doc)
        elseif(component STREQUAL "workload-lib")
            list(APPEND ML_SDK_DOC_DEP_TARGETS mlworkloadlib_doc)
        endif()
    endforeach()
    add_dependencies(deps_doc ${ML_SDK_DOC_DEP_TARGETS})

endif()

# Renderers receive fully prepared paths, inputs, and command requirements.
include("${ML_SDK_REPO_ROOT}/cmake/doxygen.cmake")
include("${ML_SDK_REPO_ROOT}/cmake/sphinx.cmake")
# TODO(standalone-docs): Remove these deps_doc edges with the legacy block above.
if(NOT ML_SDK_DOCS_STANDALONE)
    add_dependencies(sdk_sphx_doc deps_doc)
    add_dependencies(sdk_doxy_doc deps_doc)
endif()
add_custom_target(sdk_doc ALL DEPENDS sdk_sphx_doc sdk_doxy_doc SOURCES "${SPHINX_SRC_DIR}/index.rst")
