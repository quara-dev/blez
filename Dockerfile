FROM quara/blez-base:latest

COPY scripts /opt/blez-scripts

ARG BLUEZ_VERSION="5.66"
ENV BLUEZ_VERSION="$BLUEZ_VERSION"
ENV SUPERVISOR_HOME="/etc/supervisor"
ENV DBUS_HOME="/etc/dbus-1"

RUN /opt/blez-scripts/install.sh "$BLUEZ_VERSION"

# Copy default configurations
COPY configs/dbus-1/org.bluez.conf /etc/dbus-1/system.d/org.bluez.conf
COPY configs/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
