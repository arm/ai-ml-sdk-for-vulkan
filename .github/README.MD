# Workflows 

## docker build
See the workflow file [publish-linux-docker-image.yml](./workflows/publish-linux-docker-image.yml)
is using the [Dockerfile](../docker/Dockerfile) and [ci_build.sh](.workflows/scripts/ci_build.sh)

## cache docker layers
In `docker build` is running the script [ci_build.sh](.workflows/scripts/ci_build.sh) to cache the `repo` build in docker layers.
this save time when running the `Build ML SDK` see [build-with-manifest.yml](.workflows/build-with-manifest.yml) and reduce the time to build the docker image by 50%.

## save docker build cache to registry `ghcr.io`
In `docker build` is using `cache-from` and `cache-to` to save the docker build cache to registry.
this reduce the build time of docker build

## weekly docker build
a cron job in [publish-linux-docker-image.yml](./workflows/publish-linux-docker-image.yml) is running weekly
and rebuilding the docker image without using `ghcr.io` cache
to reduce the gap of `repo sync` in the docker image.

## code build
to run code build run `/home/mlsdkuser/ci_build.sh` inside the docker container see see [build-with-manifest.yml](.workflows/build-with-manifest.yml)

