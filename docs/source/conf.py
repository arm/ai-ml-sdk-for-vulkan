#
# SPDX-FileCopyrightText: Copyright 2022-2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
#
import os
import re
import sys
from importlib import import_module

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList

sys.path.insert(0, os.path.abspath("."))

# Main project config
SDK_project = "ML SDK for Vulkan®"
MC_project = "ML SDK Model Converter"
EL_project = "ML Emulation Layer for Vulkan®"
SR_project = "ML SDK Scenario Runner"
VGF_project = "ML SDK VGF Library"
WL_project = "ML Workload Library for Vulkan®"
copyright = "2022-2026, Arm Limited and/or its affiliates <open-source-office@arm.com>"
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
.. |WL_project| replace:: %s
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
    WL_project,
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
suppress_warnings = [
    "autosectionlabel.*",
    "toc.no_title",
    "myst.xref_missing",
    "myst.header",
]
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

exclude_patterns = [
    "**/glslang/**",
    "**/dependencies/**",
    "**/docs/generated/*.md",
    "**/generated/*.md",
]


class PyEnumTable(Directive):
    """Generate a compact table of enum members from the Python module."""

    has_content = False

    def run(self):
        module = import_module("vgfpy")
        enums = sorted(
            (name, value)
            for name, value in vars(module).items()
            if isinstance(value, type) and hasattr(value, "__members__")
        )
        lines = [
            ".. list-table::",
            "   :header-rows: 1",
            "   :widths: 30 70",
            "",
            "   * - Enumeration",
            "     - Members",
        ]
        for name, enum in enums:
            members = ", ".join(f"``{member}``" for member in enum.__members__)
            lines.extend([f"   * - ``{name}``", f"     - {members}"])

        container = nodes.container()
        self.state.nested_parse(StringList(lines), self.content_offset, container)
        return container.children


def normalize_pybind11_docstrings(app, what, name, obj, options, lines):
    """Render pybind11 overload signatures as literals in autodoc output."""
    if what not in {"function", "method"}:
        return

    for index, line in enumerate(lines):
        if re.match(r"^\d+\. [A-Za-z_][A-Za-z0-9_]*\(", line):
            lines[index] = f"``{line}``"


def hide_pybind11_wrapper_signature(
    app, what, name, obj, options, signature, return_annotation
):
    """Prefer pybind11's detailed overload signatures to its *args wrapper."""
    if signature == "(*args, **kwargs)":
        return "", return_annotation
    return signature, return_annotation


def setup(app):
    app.add_directive("py-enum-table", PyEnumTable)
    app.connect("autodoc-process-docstring", normalize_pybind11_docstrings)
    app.connect("autodoc-process-signature", hide_pybind11_wrapper_signature)
