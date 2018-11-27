.. rest-mqtt-proxy documentation master file, created by
   sphinx-quickstart on Fri Nov 16 00:53:16 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _my-reference-label:

=========
Config
=========

This section contains details about configuration and there default values.

There are to different config possibilities.

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





PRE_MAPPING_DIR
===============

To Subsrcibe on Topics you can use the follow yaml syntax to define some resources from kind MQTTSubscriptionV1
All files placed in the *PRE_MAPPING_DIR* will used to create resources.

Filename: example.yaml


.. code-block:: yaml

    kind: MQTTSubscriptionV1
    subregex: "test-a/topic/#"
    description: 'Test Topics'
    event_handlers:
        default_manager: default_output_handler
        persistent_manager: push_influxdb_handler

    ---

    kind: MQTTSubscriptionV1
    subregex: "test-b/topic/#"
    description: 'Test Topics'
    event_handlers:
        default_manager: default_output_handler
        persistent_manager: push_influxdb_handler




