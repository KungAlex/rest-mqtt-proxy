#!/bin/bash

cat <<EOF
#####################################################
###                                               ###
###      Welcome to rest-mqtt-proxy               ###
###                                               ###
###                                               ###
###                                               ###
###  for more information see:                    ###
###  https://kungalex.github.io/rest-mqtt-proxy/  ###
###                                               ###
#####################################################
EOF


cd ${DOCKER_DEPLOY_DIR}

# Prepare log files and start outputting logs to stdout
mkdir -p logs
touch logs/gunicorn.log
touch logs/access.log
tail -n 0 -f logs/*.log &


# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn main:app \
    --name ${APP_NAME} \
    --bind 0.0.0.0:5000 \
    --pid=app.pid \
    --log-level=info \
    --log-file=${DOCKER_DEPLOY_DIR}/logs/gunicorn.log \
    --access-logfile=${DOCKER_DEPLOY_DIR}/logs/access.log
