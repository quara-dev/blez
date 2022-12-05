FROM quara/blez-base:latest

COPY scripts /opt/blez-scripts

ARG BLUEZ_VERSION="5.66"
ENV BLUEZ_VERSION="$BLUEZ_VERSION"

RUN /opt/blez-scripts/install.sh "$BLUEZ_VERSION"
