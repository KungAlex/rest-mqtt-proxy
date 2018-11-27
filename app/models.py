"""
models.py
====================================
All Model Classes for Resources
"""


import uuid
import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class MQTTSubscriptionV1(object):
    """
    MQTTSubscriptionV1: Model Class to handle all MQTT-Subscriptions
    """
    kind = "MQTTSubscriptionV1"
    uuid = None
    subregex = None
    description = None
    event_handlers = dict()
    labels = dict()

    def __init__(self, subregex=None, description=None):
        if (subregex is not None) and (description is not None):
            self.uuid = uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=subregex)
            self.subregex = subregex
            self.description = description

    @staticmethod
    def load_yaml(yaml):
        instance = MQTTSubscriptionV1()
        for key in yaml:
            if hasattr(instance, 'set_' + key):
                setter_method = getattr(instance, 'set_' + key)
                setter_method(yaml[key])
        instance.uuid = uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=instance.subregex)
        return instance

    def set_subregex(self, subregex):
        self.subregex = subregex

    def set_description(self, description):
        self.description = description

    def set_event_handlers(self, event_handlers):
        self.event_handlers = event_handlers

    def set_labels(self, labels):
        self.labels = labels

    def __repr__(self):
        return json.dumps(self.__dict__, cls=UUIDEncoder)


class TopicMappingV1(object):
    """
    TopicMappingV1: Model Class to handle all Topic-Mappings
    """
    kind = "TopicMappingV1"
    uuid = None
    topic = None
    sub_uuid = None
    last_value = None

    def __init__(self, topic , sub_uuid):

        self.uuid = uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=topic)
        self.topic = topic
        self.sub_uuid = sub_uuid




