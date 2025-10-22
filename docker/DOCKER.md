# Build The Docker Image

To build the docker image run the following command from the folder containing
the `Dockerfile`:

```sh
docker buildx build --tag ml-sdk-image --file Dockerfile --build-arg user=$(whoami) --build-arg uid=$(id -u) ..
```

# Troubleshooting
## Error `did not complete successfully: cannot allocate memory`
increase the memory by running 

```sh
docker buildx build --memory=64g --tag ml-sdk-image --file Dockerfile --build-arg user=$(whoami) --build-arg uid=$(id -u) ..
```