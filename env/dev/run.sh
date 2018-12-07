#!/usr/bin/env bash
source ./common-vars.sh

case "$1" in
    tests|"")
        docker run --rm --volume ${REPO_ROOT}:/code ${IMAGE}
        ;;
    *)
        docker run --rm --volume ${REPO_ROOT}:/code -it ${IMAGE} "${@:1}"
        ;;
esac
