
=================
rest-mqtt-proxy
=================

rest-mqtt-proxy's is a flask prototype application that act as mqtt/rest proxy.

For the full technical documentation visit: https://kungalex.github.io/rest-mqtt-proxy/


.. inclusion-marker-do-not-remove


Getting-Started
===============
This section contains a Quick-Start Example that cover basic use cases of rest-mqtt-proxy.
You can use prebuild Docker image or build from source.


Requirements
------------


Please make sure you have Docker installed.

.. code-block:: bash

    alex@alex-ThinkPad-L480:~$ docker version
    Client:
     Version:           18.06.1-ce
     API version:       1.38
     Go version:        go1.10.3
     Git commit:        e68fc7a
     Built:             Tue Aug 21 17:24:51 2018
     OS/Arch:           linux/amd64
     Experimental:      false

    Server:
     Engine:
      Version:          18.06.1-ce
      API version:      1.38 (minimum version 1.12)
      Go version:       go1.10.3
      Git commit:       e68fc7a
      Built:            Tue Aug 21 17:23:15 2018
      OS/Arch:          linux/amd64
      Experimental:     false



For more information about Docker Container and their usage see: https://docs.docker.com/


Build from Source
-----------------

clone or copy this repo and use the makefile to build this project from source.

.. code-block:: bash

    git clone git@github.com:KungAlex/rest-mqtt-proxy.git
    cd rest-mqtt-proxy
    make build
    make run

to see all available commands type: make help



Docker
-------


All configs can be made by mount local config files to the Docker-Container.

In *APP_CONFIG_FILE* are base config for the MQTT-Broker Connection and optional the InfluxDB config used for persistent Manager.

To configure what topics will be Subscribe by the Client-Thread use yaml files in *PRE_MAPPING_DIR*.


.. code-block:: bash

    docker pull kungalex/rest-mqtt-proxy:latest
    docker run -it \
        -p=5000:5000 \
        -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
        -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
        -v ${PWD}/config/dev/config.ini:/srv/rest-mqtt-proxy/config.ini:ro \
        -v ${PWD}/config/dev/mappings/:/srv/rest-mqtt-proxy/mappings/:ro \
        kungalex/rest-mqtt-proxy:latest

For an full config example please see :ref:`my-reference-label`.

Docker-Compose
--------------

For an Base integration test there is docker-compose script that starts all Services like Mosquitto and InfluxDB as Docker on your localhost.


.. code-block:: bash

    docker-compose up

    or

    make compose

For more information about Docker-Compose see: https://docs.docker.com/compose/



Kubernetes
----------

.. code-block:: bash

    kubectl apply -f k8s-example/


For more information about kubernetes see: https://kubernetes.io/


License (MIT)
-------------

This project is licensed under the terms of the MIT license.

Copyright (c) 2018 Alexander Kleinschmidt
