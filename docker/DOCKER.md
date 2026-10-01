# Build The Docker Image

To build the docker image run the following command from the folder containing
the `Dockerfile`:

```sh
docker build --tag ml-sdk-image --file Dockerfile --build-arg user=$(whoami) --build-arg uid=$(id -u) ..
```

The image uses `uv` 0.12.9 and installs the pinned Python dependencies in
`docker/requirements.txt`.
This file includes the SDK and the runtime, optional feature, build, test, and tooling dependencies
declared by all five components. It resolves one Python 3.12 Linux environment
from their declarations; each component's `uv.lock` still governs its own
development environment. Regenerate the image requirements from a complete
manifest checkout when a component dependency changes:

```sh
python docker/update_requirements.py
python docker/update_requirements.py --check
```

Both commands resolve against the package index with Python 3.12. `--check`
compares the complete pinned output. Pass `--python PATH` if Python 3.12 is not
on your PATH.

Commit the updated `docker/requirements.txt` in the SDK root repository. The
public image build uses this file because it checks out only the root repository.
