#
# SPDX-FileCopyrightText: Copyright 2022-2025 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
import os
import sys

sys.path.insert(0, os.path.abspath("."))

# Main project config
SDK_project = "ML SDK for Vulkan®"
MC_project = "ML SDK Model Converter"
EL_project = "ML SDK Emulation Layer for Vulkan®"
SR_project = "ML SDK Scenario Runner"
VGF_project = "ML SDK VGF Library"
copyright = "2022-2025, Arm Limited and/or its affiliates <open-source-office@arm.com>"
author = "Arm Limited"

# Set home project name
project = SDK_project

# Enable keywords for substitution
cross_uni = "❌"
tick_uni = "✅"
dash_uni = "N/A"
git_repo_tool_url = "https://gerrit.googlesource.com/git-repo"

rst_epilog = """
.. |SDK_project| replace:: %s
.. |MC_project| replace:: %s
.. |EL_project| replace:: %s
.. |SR_project| replace:: %s
.. |VGF_project| replace:: %s
.. |/| replace:: %s
.. |x| replace:: %s
.. |-| replace:: %s
.. |git_repo_tool_url| replace:: %s
""" % (
    SDK_project,
    MC_project,
    EL_project,
    SR_project,
    VGF_project,
    tick_uni,
    cross_uni,
    dash_uni,
    git_repo_tool_url,
)

# Disable converting double-dash to typographical en-dash
smartquotes_action = "qe"

# Enabled extensions
extensions = [
    "breathe",
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "myst_parser",
    "sphinxcontrib.plantuml",
]

# Disable superfluous warnings
suppress_warnings = ["autosectionlabel.*", "toc.no_title"]
autosectionlabel_prefix_document = False

# Breathe Configuration
breathe_projects = {"MLSDK": "../generated/xml"}
breathe_default_project = "MLSDK"
breathe_domain_by_extension = {"h": "c"}

# HTML Options
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",  # Enable custom formatting for tables
]

# Enable RTD theme
html_theme = "sphinx_rtd_theme"
