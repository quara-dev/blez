#!/usr/bin/env bash

BLEZ_VERSION="v0.2.0"
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
    BLUEZ_ARTIFACT="$BLUEZ_DIR-$(platform).tar.gz"
    BLUEZ_HOME="/opt/$BLUEZ_DIR"
    URL="https://github.com/charbonnierg/blez/releases/tag/$BLEZ_VERSION/bluez-$BLUEZ_VERSION-$(platform).tar.gz"
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
    cp $PARENT_DIR/profile.d/bluetooth.sh /etc/profile.d/bluetooth.sh
    sed -i "s@__MARKER__@$BLUEZ_HOME@" /etc/profile.d/bluetooth.sh
}

install $1
