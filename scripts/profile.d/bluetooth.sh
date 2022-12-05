# This variable is replaced using sed
# sed -i 's/__MARKER__/$BLUEZ_HOME/g'
export BLUEZ_HOME="__MARKER__"
# Export both bin directory and libexec/bluetooth directory
export PATH="__MARKER__/bin:__MARKER__/libexec/bluetooth:$PATH"
