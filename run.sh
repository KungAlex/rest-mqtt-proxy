#!/usr/bin/env bash

docker build -t kungalex/rest-mqtt-proxy .
gnome-terminal -x sh -c "docker run -it \
    -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
    -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
    -v ${PWD}/config/prod/config.ini:/srv/rest-mqtt-proxy/config.ini:ro \
    -v ${PWD}/config/prod/mappings/:/srv/rest-mqtt-proxy/mappings/:ro \
    kungalex/rest-mqtt-proxy:latest"