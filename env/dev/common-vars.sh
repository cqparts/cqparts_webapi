# Environment variables common to all scripts in this folder
export IMAGE_BASE=cqparts-webapi
export IMAGE_VER=${PWD##*/}
export IMAGE=${IMAGE_BASE}:${IMAGE_VER}

export REPO_ROOT=$(git rev-parse --show-toplevel)
