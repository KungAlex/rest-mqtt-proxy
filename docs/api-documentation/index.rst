.. rest-mqtt-proxy documentation master file, created by
   sphinx-quickstart on Fri Nov 16 00:53:16 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



=================
API Documentation
=================

This section contains the full API-Documentation.


REST Resource: API
------------------

* List all API versions:
   http://0.0.0.0:5000/

.. code-block:: json

   {
      "msg": "Welcome to rest-mqtt-proxy prototype!",
      "urls":
         {
            "api_v1": "http://0.0.0.0:5000/api/v1",
            "api_v2": "TODO"
         }

   }


* Entry Point API V1:
   http://0.0.0.0:5000/api/v1

.. code-block:: json

   {
      "api_version": 1,
      "urls":
      {
         "topic_mapping_list": "http://0.0.0.0:5000/api/v1/topics",
         "subscriptions_list": "http://0.0.0.0:5000/api/v1/subscriptions"
      }

   }




REST Resource: Subscriptions
----------------------------

* List all Topic-Subscriptions:
   http://0.0.0.0:5000/api/v1/subscriptions

.. code-block:: json

   {
      "subscriptions_list":
      [
         {
            "kind": "MQTTSubscriptionV1",
            "uuid": "ac106f72-7801-5cdb-9c01-031e3bdac474",
            "subregex": "test-a/topic/#",
            "description": "Test Topics",
            "labels": {},
            "event_handlers":
               {
                  "default_manager": "default_output_handler",
                  "persistent_manager": "push_influxdb_handler"
               },
            "uri": "http://0.0.0.0:5000/api/v1/subscription/details/ac106f72-7801-5cdb-9c01-031e3bdac474"
         },

         {
            "kind": "MQTTSubscriptionV1",
            "uuid": "4259fc75-2ba6-56c2-902b-a88b8990bd49",
            "subregex": "test-b/topic/#",
            "description": "Test Topics",
            "labels": {},
            "event_handlers":
               {
                  "default_manager": "default_output_handler",
                  "persistent_manager": "push_influxdb_handler"
               },
            "uri": "http://0.0.0.0:5000/api/v1/subscription/details/4259fc75-2ba6-56c2-902b-a88b8990bd49"
            }
         ]
   }


* Get details about a specify Topic-Subscription
   http://0.0.0.0:5000/api/v1/subscription/details/<uuid>

.. code-block:: json


   [{
      "kind": "MQTTSubscriptionV1",
      "uuid": "ac106f72-7801-5cdb-9c01-031e3bdac474",
      "subregex": "test-a/topic/#",
      "description": "Test Topics",
      "labels": {},
      "event_handlers":
         {
            "default_manager": "default_output_handler",
            "persistent_manager": "push_influxdb_handler"
         },
      "uri": "http://0.0.0.0:5000/api/v1/subscription/details/ac106f72-7801-5cdb-9c01-031e3bdac474"
   }]


REST Resource: Mappings
-----------------------


* List all Topic-Mappings
   http://0.0.0.0:5000/api/v1/topics

.. code-block:: json


   {
     "topic_mapping_list": [
       {
         "kind": "TopicMappingV1",
         "topic": "test-a/topic/test",
         "uuid": "69e0fbc7-4596-54d9-a874-2bcfeadec724",
         "sub_uuid": "ac106f72-7801-5cdb-9c01-031e3bdac474",
         "last_value": "123.123",
         "details": "http://0.0.0.0:5000/api/v1/topic/details/69e0fbc7-4596-54d9-a874-2bcfeadec724",
         "uri": "http://0.0.0.0:5000/api/v1/topic/value/69e0fbc7-4596-54d9-a874-2bcfeadec724"
       },
       {
         "kind": "TopicMappingV1",
         "topic": "test-b/topic/test",
         "uuid": "7516ef28-4509-5f16-802b-6af81c55bc9b",
         "sub_uuid": "4259fc75-2ba6-56c2-902b-a88b8990bd49",
         "last_value": "123.123",
         "details": "http://0.0.0.0:5000/api/v1/topic/details/7516ef28-4509-5f16-802b-6af81c55bc9b",
         "uri": "http://0.0.0.0:5000/api/v1/topic/value/7516ef28-4509-5f16-802b-6af81c55bc9b"
       },
       {
         "kind": "TopicMappingV1",
         "topic": "test-b/topic/test-other",
         "uuid": "65085844-d7d4-55aa-877e-694fb387e488",
         "sub_uuid": "4259fc75-2ba6-56c2-902b-a88b8990bd49",
         "last_value": "Hello World",
         "details": "http://0.0.0.0:5000/api/v1/topic/details/65085844-d7d4-55aa-877e-694fb387e488",
         "uri": "http://0.0.0.0:5000/api/v1/topic/value/65085844-d7d4-55aa-877e-694fb387e488"
       }
     ]
   }

* Get details about a specify Topic-Mapping
   + by uuid: http://0.0.0.0:5000/api/v1/topic/details/<uuid>
   + by Topic: http://0.0.0.0:5000/api/v1/topic/details/<topic>

.. code-block:: json

   [
     {
       "kind": "TopicMappingV1",
       "topic": "test-a/topic/test",
       "uuid": "69e0fbc7-4596-54d9-a874-2bcfeadec724",
       "sub_uuid": "ac106f72-7801-5cdb-9c01-031e3bdac474",
       "last_value": "123.12",
       "details": "http://0.0.0.0:5000/api/v1/topic/details/69e0fbc7-4596-54d9-a874-2bcfeadec724",
       "uri": "http://0.0.0.0:5000/api/v1/topic/value/69e0fbc7-4596-54d9-a874-2bcfeadec724"
     }
   ]

* Get value of a specify Topic-Mapping
   + by uuid: http://0.0.0.0:5000/api/v1/topic/value/<uuid>
   + by Topic: http://0.0.0.0:5000/api/v1/topic/value/<topic>

.. code-block:: json

   123.123

