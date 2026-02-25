#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR=$(dirname $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

function build {
    PYTHON_VERSION="$1"
    BUILD_IMAGE="quara/blez-build:${PYTHON_VERSION}"
    OUTPUT_DIR=$(mktemp -d)
    docker run -i --platform="$PLATFORM" -v "$ROOT_DIR:/build" -v "$OUTPUT_DIR:/dist" -e OUTPUT_DIR=/dist --workdir /build "$BUILD_IMAGE" scripts/build.sh ${@:2}
    mv "$OUTPUT_DIR" "$ROOT_DIR/dist/"
}

function main {
    export PLATFORM="$1"
    PYTHON_VERSION="$2"
    build "$PYTHON_VERSION" ${@:3}
    unset PLATFORM
}

main $@
