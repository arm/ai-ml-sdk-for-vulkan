# Workflows 

## docker build
See the workflow file [publish-linux-docker-image.yml](./workflows/publish-linux-docker-image.yml)
is using the [Dockerfile](../docker/Dockerfile) and [ci_build.sh](.workflows/scripts/ci_build.sh)

## save docker build cache to registry `ghcr.io`
In `docker build` is using `cache-from` and `cache-to` to save the docker build cache to registry.
this reduces the build time of docker build

## code build
to run code build run `/home/mlsdkuser/ci_build.sh` inside the docker container see see [build-with-manifest.yml](.workflows/build-with-manifest.yml)

