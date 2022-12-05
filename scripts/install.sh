#!/usr/bin/env bash

function installDependencies {
    apt-get update
    apt-get install -y --no-install-recommends libglib2.0-0 dbus
}
