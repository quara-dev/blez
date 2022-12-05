#!/usr/bin/env bash

set -euo pipefail

BLEZ_VERSION="2022-12-05"
DEFAULT_BLUEZ_VERSION="${BLUEZ_VERSION:-5.66}"

PARENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#
# Find host platform
#
function platform {
    case $(arch) in
        x86_64)
            echo "linux-amd64"
            ;;
        aarch64)
            echo "linux-arm64"
            ;;
        armv7l)
            echo "linux-arm-v7"
            ;;
        *)
            >&2 echo "Architecture not supported: $(arch)"
            exit 1
            ;;
    esac
}

#
# Download and install bluez
#
function install {
    BLUEZ_VERSION="$1"
    BLUEZ_DIR="bluez-$BLUEZ_VERSION"
    BLUEZ_HOME="/opt/$BLUEZ_DIR"
    BLUEZ_ARTIFACT="$BLUEZ_DIR-$(platform).tar.gz"
    URL="https://github.com/charbonnierg/blez/releases/download/$BLEZ_VERSION/$BLUEZ_ARTIFACT"
    # Download build artifact from URL
    curl -O -q "$URL"
    # Uncompress artifact
    tar -xzf "$BLUEZ_ARTIFACT"
    # Install bluez into /opt directory
    mv "./opt/$BLUEZ_DIR/" "$BLUEZ_HOME"
    # Remove empty directory
    rmdir ./opt
    # Move configuration files to /etc directory
    if [ ! -f "/etc/dbus-1/system.d/org.bluez.conf" ]; then
        mv "$BLUEZ_HOME/etc/dbus-1/bluetooth.conf" /etc/dbus-1/system.d/org.bluez.conf
    fi
    if [ ! -f "/etc/bluetooth/main.conf" ]; then
        mv "$BLUEZ_HOME/etc/bluetooth/main.conf" /etc/bluetooth/main.conf
    fi
    # Remove etc dir once files are used
    rm -rf "$BLUEZ_HOME/etc"
    # Add bluez directories to PATH through profile
    if [ ! -f "/etc/profile.d/bluetooth.sh" ]; then
        cp $PARENT_DIR/profile.d/bluetooth.sh /etc/profile.d/bluetooth.sh
        sed -i "s@__MARKER__@$BLUEZ_HOME@" /etc/profile.d/bluetooth.sh
    fi
}

install "${1:-DEFAULT_BLUEZ_VERSION}"
