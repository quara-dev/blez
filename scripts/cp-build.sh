#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR=$(dirname $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ))

function build {
    OUTPUT_DIR=$(mktemp)
    docker run -it --platform="$PLATFORM" -v "$ROOT_DIR:/build" -v "$OUTPUT_DIR:/opt/bluez" --workdir /scripts debian:oldoldstable scripts/build.sh $@
    mv "$OUTPUT_DIR" "$ROOT_DIR/dist/"
}

function main {
    export PLATFORM="$1"
    build ${@:2}
    unset PLATFORM
}

main $@
