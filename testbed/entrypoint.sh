#!/bin/sh
# Applies the link profile of this container, then starts the service.
if [ -n "$NETEM_DELAY" ]; then
  tc qdisc add dev eth0 root netem delay "${NETEM_DELAY}ms" rate "${NETEM_RATE}mbit" 2>/dev/null \
    || echo "warning: tc unavailable (NET_ADMIN?), running without link shaping"
fi
exec "$@"
