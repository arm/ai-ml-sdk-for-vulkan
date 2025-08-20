# Build The Docker Image

To build the docker image run the following command from the folder containing
the `Dockerfile`:

```sh
docker build --tag ml-sdk-image --file Dockerfile --build-arg user=$(whoami) --build-arg uid=$(id -u) ..
```
