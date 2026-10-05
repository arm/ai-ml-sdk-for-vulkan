# SPDX-FileCopyrightText: Copyright 2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: Apache-2.0
"""Checks for the Docker dependency snapshot maintenance command."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

SCRIPT = Path(__file__).with_name("update_requirements.py")
SPEC = importlib.util.spec_from_file_location("update_requirements", SCRIPT)
update_requirements = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(update_requirements)


def test_check_compares_resolved_requirements_even_when_inputs_match(tmp_path, capsys):
    output = tmp_path / "docker" / "requirements.txt"
    output.parent.mkdir()
    resolved = SimpleNamespace(returncode=0, stdout="example==1.2.3\n", stderr="")
    with (
        mock.patch.object(
            update_requirements,
            "collect_requirements",
            return_value=(["example"], "a" * 64),
        ),
        mock.patch.object(
            update_requirements.subprocess, "run", return_value=resolved
        ) as compile_run,
        mock.patch.object(
            update_requirements.sys,
            "argv",
            ["update_requirements.py", "--sdk-root", str(tmp_path)],
        ),
    ):
        assert update_requirements.main() == 0
        assert ("# SPDX-" "License-Identifier: Apache-2.0\n") in output.read_text()
        with mock.patch.object(
            update_requirements.sys,
            "argv",
            ["update_requirements.py", "--sdk-root", str(tmp_path), "--check"],
        ):
            assert update_requirements.main() == 0
            output.write_text(
                output.read_text().replace("example==1.2.3", "example==1.2.2")
            )
            assert update_requirements.main() == 1
    error = capsys.readouterr().err
    assert "-example==1.2.2" in error
    assert "+example==1.2.3" in error
    assert compile_run.call_count == 3
    assert (
        compile_run.call_args.args[0][
            compile_run.call_args.args[0].index("--python") + 1
        ]
        == "3.12"
    )


def test_collect_requirements_includes_all_optional_features(tmp_path):
    project = (
        '[project]\nname = "example"\nversion = "0.1"\n'
        '[project.optional-dependencies]\nfeature = ["example-extra==1.0"]\n'
    )
    (tmp_path / "pyproject.toml").write_text(project)
    for component in update_requirements.COMPONENTS:
        path = tmp_path / "sw" / component / "pyproject.toml"
        path.parent.mkdir(parents=True)
        path.write_text(project)
    requirements, _ = update_requirements.collect_requirements(tmp_path)
    assert requirements == ["example-extra==1.0"]


def test_clean_python_310_bootstraps_tomli_after_argument_parsing():
    with (
        mock.patch.object(update_requirements, "tomllib", None),
        mock.patch.object(
            update_requirements.subprocess, "call", return_value=7
        ) as run,
        mock.patch.object(
            update_requirements.sys,
            "argv",
            ["update_requirements.py", "--check", "--uv", "uv-custom"],
        ),
    ):
        assert update_requirements.main() == 7

    assert run.call_args.args[0] == [
        "uv-custom",
        "run",
        "--no-project",
        "--isolated",
        "--with",
        "tomli==2.4.1",
        "--python",
        update_requirements.sys.executable,
        str(SCRIPT.resolve()),
        "--check",
        "--uv",
        "uv-custom",
    ]
