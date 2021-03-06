#!/usr/bin/env bash
source ./common-vars.sh

port=8089

case "$1" in
    "")
        docker run --rm \
            --volume ${REPO_ROOT}:/code \
            --publish ${port}:${port} \
            -it \
            ${IMAGE}
        ;;
    *)
        docker run --rm \
            --volume ${REPO_ROOT}:/code \
            -it \
            ${IMAGE} \
            "${@:1}"
        ;;
esac
