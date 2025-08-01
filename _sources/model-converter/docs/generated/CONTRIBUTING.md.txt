# Contributor Guide

The ML SDK Model Converter project is open for external contributors and
welcomes contributions. ML SDK Model Converter is licensed under the Apache-2.0
and all accepted contributions must have the same license.

## Developer Certificate of Origin (DCO)

Before the ML SDK Model Converter project accepts your contribution, you need to
certify its origin and give us your permission. To manage this process we use
Developer Certificate of Origin (DCO) V1.1
(<https://developercertificate.org/>).

To indicate that you agree to the the terms of the DCO, you "sign off" your
contribution by adding a line with your name and e-mail address to every git
commit message:

Signed-off-by: John Doe <john.doe@example.org>

You must use your real name, no pseudonyms or anonymous contributions are
accepted.

## C++ Coding Style

Changes to ML SDK Model Converter should follow the
[CppCoreGuidelines](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md)

Use clang-format to check your changes. It can be install by running:

```bash
apt-get install -y clang-format
```

The configuration file for this is present in the root folder of the project.

## Python Coding Style

[Black](https://github.com/psf/black) is the code style to use as defined in
`pyproject.toml`.

## Run pre-commit tests

Pre-commit tests can be run using the `pre-commit` hooks.

You can install the precommit hooks using the following command:

```bash
pre-commit install
```

The pre-commit tests will be run on each commit. You can run them manually as
follows:

```bash
pre-commit run --all-files --hook-stage commit
pre-commit run --all-files --hook-stage push
```

or run specific pre-commit hook as follow

```bash
pre-commit run <hook_id>
```
