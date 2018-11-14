############################################################
# Dockerfile for Flask-Application
# Based on python:3
############################################################

FROM python:3
ENV PYTHONUNBUFFERED 1

MAINTAINER KungAlex <alexander.kleinschmidt@smail.fh-koeln.de>

# Set Basic Environment vars
ENV APP_NAME='rest-mqtt-proxy'
ENV DOCKER_DEPLOY_DIR=/srv/${APP_NAME}/

# Create deployment dir
RUN mkdir -p ${DOCKER_DEPLOY_DIR}

# Install pip requirements
ADD requirements.txt ${DOCKER_DEPLOY_DIR}
WORKDIR ${DOCKER_DEPLOY_DIR}
RUN pip install -r requirements.txt

# Copy Source
COPY app ${DOCKER_DEPLOY_DIR}

EXPOSE 5000

# Run startScript.sh
CMD [ "./start-script.sh" ]