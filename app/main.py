import queue
import configparser
import os
import threading
import json
import yaml

from influx_base_client import InfluxDBBaseClient
from mqtt_base_client import BaseClient
from paho.mqtt.client import topic_matches_sub
from flask import Flask, abort, url_for
from flask_restful import Api, Resource, reqparse, marshal

from models import TopicMappingV1, MQTTSubscriptionV1
from views import subscription_fields, topic_mapping_fields
import callbacks
from helper import run_async

import logging
log = logging.getLogger(__name__)


APP_CONFIG_FILE=(os.getenv('APP_CONFIG_FILE', '../config/dev/config.ini'))
PRE_MAPPING_DIR=(os.getenv('PRE_MAPPING_DIR', '../config/dev/mappings'))

# Read Config
config = configparser.ConfigParser()
log.info(APP_CONFIG_FILE)
config.read(APP_CONFIG_FILE)

# Define Queues
sub_queue = queue.Queue()  # Queue for all topic to sub
pub_queue = queue.Queue()  # Queue for msg to pub
msg_queue = queue.Queue()  # Queue with incoming messages
persistent_queue = queue.Queue() # Queue for influxDB persistent manager



def create_app():
    """

    :return:
    """
    log.info("run create_app()")
    app = Flask(__name__)
    create_persistent_client()
    create_mqtt_client()
    return app


def create_persistent_client():
    """

    :return:
    """
    log.info("run: create_persistent_client()")

    try:

        INFLUX_HOST = config['influx']['host']
        INFLUX_PORT = int(config['influx']['port'])
        INFLUX_DB = config['influx']['db']

        kwargs = {'host': INFLUX_HOST, 'port': INFLUX_PORT, 'database': INFLUX_DB, 'persistent_queue': persistent_queue}
        log.info(kwargs)

        t_influxdb_client = threading.Thread(name='influxdb-client', target=InfluxDBBaseClient, kwargs=kwargs)
        t_influxdb_client.setDaemon(True)
        t_influxdb_client.start()

    except KeyError as e:
        log.error(e)


def create_mqtt_client():
    """

    :return:
    """
    log.info("run: create_mqtt_client()")

    try:
        MQTT_HOST = config['broker']['host']
        MQTT_PORT = int(config['broker']['port'])
        MQTT_PASSWORD = config['broker']['password']
        MQTT_USER = config['broker']['user']

        kwargs = {'broker': MQTT_HOST, 'port': MQTT_PORT, 'sub_queue': sub_queue, 'pub_queue': pub_queue,
                  'msg_queue': msg_queue, 'username': MQTT_USER, 'password': MQTT_PASSWORD}

        log.info(kwargs)

        # Start MQTT-Client Thread
        t_mqtt_client = threading.Thread(name='MQTT-Client', target=BaseClient, kwargs=kwargs)
        t_mqtt_client.setDaemon(True)
        t_mqtt_client.start()

    except KeyError as e:
        log.error(e)


app = create_app()
api = Api(app)

topic_mapping_list = []
subscriptions_list = []


log.info(PRE_MAPPING_DIR)

# TODO
for file in os.listdir(PRE_MAPPING_DIR):
    print(file)
    if file.endswith(".yaml") or file.endswith(".yml"):
        yaml_file = (os.path.join(PRE_MAPPING_DIR, file))
        print(yaml_file)
        with open(yaml_file, 'r') as stream:
            yamls = yaml.load_all(stream)
            for y in yamls:

                try:

                    kind = y['kind']

                    # TODO switch case alternative!

                    if kind == "MQTTSubscriptionV1":
                        try:
                            sub = MQTTSubscriptionV1.load_yaml(yaml=y)
                            subscriptions_list.append(sub)

                        except yaml.YAMLError as exc:
                            log.error(exc)
                            # TODO exceptions description#

                    if kind == "MQTTSubscriptionV2":
                        try:
                            sub = MQTTSubscriptionV1.load_yaml(yaml=y)
                            subscriptions_list.append(sub)

                        except yaml.YAMLError as exc:
                            log.error(exc)
                            # TODO exceptions description#

                except KeyError as exc:
                    log.error("KeyError: " + str(exc))

for subscription in subscriptions_list:
    log.info(subscription.__repr__())
    sub_queue.put(subscription.subregex)


def run_event_handlers(subscribtion, msg):
    try:
        default_manager = getattr(callbacks, subscribtion.event_handlers['default_manager'])
        if default_manager is not None:
            default_manager(msg)
    except AttributeError:
        log.info("no default_manager function ")

    except KeyError:
        log.info("no default_manager function define ")

    try:
        persistent_manager = getattr(callbacks, subscribtion.event_handlers['persistent_manager'])
        if persistent_manager is not None:
            persistent_manager(msg=msg, queue=persistent_queue)

    except KeyError:
        log.info("no persistent_manager ")
    except AttributeError:
        log.info("no persistent_manager function define")


@run_async
def run_msq_queue():
    while True:
        to_add = True  # If True a new Topic mapping will be create and append to list
        msg = msg_queue.get()
        topic_sub = None

        for topic_mapping in topic_mapping_list:
            if topic_mapping.topic == msg.topic:

                to_add = False

                try:
                    topic_mapping.last_value = json.loads(msg.payload.decode())
                except json.decoder.JSONDecodeError as e:
                    log.info(e)
                    topic_mapping.last_value = msg.payload.decode()

                # TODO for all handlers in Event_handlers: do handler(msg)

                for subscription in subscriptions_list:
                    if subscription.uuid == topic_mapping.sub_uuid:
                        topic_sub = subscription

                run_event_handlers(topic_sub, msg)

        if to_add:

            for subscription in subscriptions_list:
                if topic_matches_sub(subscription.subregex, msg.topic):
                    topic_sub = subscription

            topic_mapping = TopicMappingV1(topic=msg.topic, sub_uuid=topic_sub.uuid)

            try:
                topic_mapping.last_value = json.loads(msg.payload.decode())
            except json.decoder.JSONDecodeError as e:
                log.info(e)
                topic_mapping.last_value = msg.payload.decode()

            topic_mapping_list.append(topic_mapping)

            # TODO run event_handlers (first time)
            run_event_handlers(topic_sub, msg)


class Home(Resource):
    def get(self):
        return {
            'msg': 'Welcome to a Python Http-Mqtt Proxy!',
            'urls':
                {
                    'api_v1': url_for('api_v1', _external=True),
                    'api_v2': 'TODO'
                }
        }


class ApiV1(Resource):
    def get(self):
        return {'api_version': 1, 'urls': {
            'topic_mapping_list': url_for('api_topic_mapping_list', _external=True),
            'subscriptions_list': url_for('api_subscription_list', _external=True)
        }}


class TopicMappingListApiV1(Resource):

    def get(self):
        return {'topic_mapping_list': [marshal(topic, topic_mapping_fields) for topic in topic_mapping_list]}


class SubscriptionsListApiV1(Resource):

    def get(self):
        return {'subscriptions_list': [marshal(subscription, subscription_fields) for subscription in
                                       subscriptions_list]}


class SubscriptionDetailsApiV1(Resource):

    def get(self, uuid):
        for subscription in subscriptions_list:
            if subscription.uuid == uuid:
                return marshal(subscription, subscription_fields),  # TODO use marshal

        abort(404)


class TopicValueApiV1(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('last_value', type=str, location='json')

        super(TopicValueApiV1, self).__init__()

    def get(self, uuid):
        for mapping in topic_mapping_list:
            if mapping.uuid == uuid:
                # return marshal(mapping, topic_fields),  # TODO use marshal
                return mapping.last_value, 200

        abort(404)

    def put(self, uuid):
        for mapping in topic_mapping_list:
            if mapping.uuid == uuid:
                args = self.reqparse.parse_args()

                if args['last_value']:
                    mapping.last_value = args['last_value']
                    message = dict()
                    message['topic'] = mapping.topic
                    message['payload'] = args['last_value']
                    pub_queue.put(message)

                return mapping.last_value, 200

        abort(404)

    def delete(self, uuid):
        for topic in topic_mapping_list:
            if topic.uuid == uuid:
                topic_mapping_list.remove(topic)
                return {'result': True}, 200

        abort(404)


class TopicDetailsApiV1(Resource):

    def get(self, uuid):
        for mapping in topic_mapping_list:
            if mapping.uuid == uuid:
                return marshal(mapping, topic_mapping_fields),  # TODO use marshal

        abort(404)


class MappingValueApiV1(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('last_value', type=str, location='json')
        super(MappingValueApiV1, self).__init__()

    def get(self, topic):

        for mapping in topic_mapping_list:
            if mapping.topic == topic:
                # return {'topic': marshal(mapping, topic_fields)}
                # return marshal(mapping, topic_fields), 200 # , envelope=str(mapping.uuid)
                return mapping.last_value, 200

        abort(404)


class MappingDetailsApiV1(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('last_value', type=str, location='json')
        super(MappingDetailsApiV1, self).__init__()

    def get(self, topic):

        for mapping in topic_mapping_list:
            if mapping.topic == topic:
                return marshal(mapping, topic_mapping_fields), 200  # , envelope=str(mapping.uuid)

        abort(404)


# Add API Resources
api.add_resource(Home, '/', endpoint='api_home')
api.add_resource(ApiV1, '/api/v1', endpoint='api_v1')

# Topics
api.add_resource(TopicMappingListApiV1, '/api/v1/topics', endpoint='api_topic_mapping_list')
api.add_resource(TopicDetailsApiV1, '/api/v1/topic/details/<uuid:uuid>', endpoint='api_topic_details')
api.add_resource(TopicValueApiV1, '/api/v1/topic/value/<uuid:uuid>', endpoint='api_topic_value')
api.add_resource(MappingDetailsApiV1, '/api/v1/topic/details/<path:topic>', endpoint='api_mapping_details')
api.add_resource(MappingValueApiV1, '/api/v1/topic/value/<path:topic>', endpoint='api_mapping_value')

# Subscription
api.add_resource(SubscriptionsListApiV1, '/api/v1/subscriptions', endpoint='api_subscription_list')
api.add_resource(SubscriptionDetailsApiV1, '/api/v1/subscription/details/<uuid:uuid>',
                 endpoint='api_subscription_details')

run_msq_queue()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
