#
# SPDX-FileCopyrightText: Copyright 2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#

find_package(Git)
if(Git_FOUND)
    execute_process(
        COMMAND ${GIT_EXECUTABLE} ls-files --others --directory
        WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/.."
        RESULT_VARIABLE RESULT
        OUTPUT_VARIABLE GIT_UNTRACKED_FILES
        ERROR_QUIET
        OUTPUT_STRIP_TRAILING_WHITESPACE)
    string(REPLACE "\n" ";" GIT_UNTRACKED_FILES ${GIT_UNTRACKED_FILES})
    list(TRANSFORM GIT_UNTRACKED_FILES PREPEND ${CMAKE_INSTALL_PREFIX})
endif()
