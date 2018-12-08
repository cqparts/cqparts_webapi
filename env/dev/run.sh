#!/usr/bin/env bash
source ./common-vars.sh

port=8089

case "$1" in
    tests|"")
        docker run --rm \
            --volume ${REPO_ROOT}:/code \
            --publish ${port}:${port} \
            ${IMAGE}
        ;;
    *)
        docker run --rm \
            --volume ${REPO_ROOT}:/code \
            --publish ${port}:${port} \
            -it \
            ${IMAGE} \
            "${@:1}"
        ;;
esac
