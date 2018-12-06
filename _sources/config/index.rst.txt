.. rest-mqtt-proxy documentation master file, created by
   sphinx-quickstart on Fri Nov 16 00:53:16 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _my-reference-label:

=========
Config
=========

This section contains details about configuration and their default values.
There are two necessary configs parts. The first configfile is for the basic connection Setup and the other for the Topic subscription.


.. _app-config-file-label:

APP_CONFIG_FILE
===============



For the basic MQTT-Broker Config use the this example and set env APP_CONFIG_FILE
to file path.

Filename: config.ini

.. code-block:: apacheconf

   # Base MQTT-Brocker
   [broker]
   host = iot.eclipse.org
   port = 1883
   user = None
   password = None

   # InfluxDB (optional)
   [influx]
   host = localhost
   host = influxdb
   port = 8086
   db = iot



.. _pre-mapping-dir-label:

PRE_MAPPING_DIR
===============
All files placed in the *PRE_MAPPING_DIR* will used to create resources.
To Subscribe some Topics you can use the follow yaml syntax to define some resources from kind MQTTSubscriptionV1.


Filename: example.yaml


.. code-block:: yaml

    kind: MQTTSubscriptionV1
    subregex: "test-a/topic/#"
    description: 'Test Topics'
    event_handlers:
        default_manager: default_output_handler
        persistent_manager: none

    ---

    kind: MQTTSubscriptionV1
    subregex: "test-b/topic/#"
    description: 'Test Topics'
    event_handlers:
        default_manager: default_output_handler
        persistent_manager: none




