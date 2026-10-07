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


def test_existing_output_pins_are_preferences(tmp_path, capsys):
    output = tmp_path / "docker" / "requirements.txt"
    output.parent.mkdir()
    existing_outputs = []
    compile_inputs = []
    resolved_versions = iter(["1.2.3", "1.2.3", "2.0.0", "2.1.0"])

    def compile_requirements(command, **_kwargs):
        output_argument = command.index("--output-file") + 1
        resolved_output = Path(command[output_argument])
        compile_inputs.append(_kwargs["input"])
        existing_outputs.append(
            resolved_output.read_text() if resolved_output.is_file() else None
        )
        resolved_output.write_text(f"example=={next(resolved_versions)}\n")
        return SimpleNamespace(returncode=0, stderr="")

    with (
        mock.patch.object(
            update_requirements,
            "collect_requirements",
            return_value=(["example"], "a" * 64),
        ) as collect_requirements,
        mock.patch.object(
            update_requirements.subprocess,
            "run",
            side_effect=compile_requirements,
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
            collect_requirements.return_value = (["example>=2"], "b" * 64)
            assert update_requirements.main() == 1
        with mock.patch.object(
            update_requirements.sys,
            "argv",
            [
                "update_requirements.py",
                "--sdk-root",
                str(tmp_path),
                "--upgrade",
            ],
        ):
            assert update_requirements.main() == 0
    error = capsys.readouterr().err
    assert "-example==1.2.3" in error
    assert "+example==2.0.0" in error
    assert compile_run.call_count == 4
    for call in compile_run.call_args_list:
        assert "--constraint" not in call.args[0]
        assert "--output-file" in call.args[0]
    for call in compile_run.call_args_list[:3]:
        assert "--upgrade" not in call.args[0]
    assert "--upgrade" in compile_run.call_args_list[3].args[0]
    assert existing_outputs[0] is None
    assert "example==1.2.3" in existing_outputs[1]
    assert "example==1.2.3" in existing_outputs[2]
    assert "example==1.2.3" in existing_outputs[3]
    assert compile_inputs[2] == "example>=2\n"
    assert (
        compile_run.call_args.args[0][
            compile_run.call_args.args[0].index("--python") + 1
        ]
        == "3.12"
    )


def test_removed_dependencies_are_dropped_from_output(tmp_path):
    output = tmp_path / "docker" / "requirements.txt"
    output.parent.mkdir()
    output.write_text("removed-direct==1.0\nremoved-transitive==1.0\nretained==2.0\n")

    def compile_requirements(command, **_kwargs):
        output_argument = command.index("--output-file") + 1
        resolved_output = Path(command[output_argument])
        assert resolved_output.read_text() == output.read_text()
        resolved_output.write_text("retained==2.0\n")
        return SimpleNamespace(returncode=0, stderr="")

    with (
        mock.patch.object(
            update_requirements,
            "collect_requirements",
            return_value=(["retained"], "a" * 64),
        ),
        mock.patch.object(
            update_requirements.subprocess,
            "run",
            side_effect=compile_requirements,
        ),
        mock.patch.object(
            update_requirements.sys,
            "argv",
            ["update_requirements.py", "--sdk-root", str(tmp_path)],
        ),
    ):
        assert update_requirements.main() == 0

    generated = output.read_text()
    assert "retained==2.0" in generated
    assert "removed-direct" not in generated
    assert "removed-transitive" not in generated


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
