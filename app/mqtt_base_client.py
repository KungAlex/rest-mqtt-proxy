"""
mqtt_base_client.py
====================================
Main entry-point of this project
"""

import paho.mqtt.client as mqtt
from helper import run_async
import _thread
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def on_subscribe_callback(client, userdata, mid, granted_qos):
    """
    on_subscribe callback

    :param client:
    :param userdata:
    :param mid:
    :param granted_qos:
    :return:
    """
    log.info("subscribe topic")


def on_connect_callback(client, userdata, flags, rc):
    """
    on_connect callback

    :param client: 
    :param userdata: 
    :param flags: 
    :param rc: 
    :return: 
    """
    log.info("Connected with result code " + str(rc))


def on_message_callback(client, userdata, msg):
    """
    on_message callback

    :param client: 
    :param userdata: 
    :param msg: 
    :return: 
    """
    # logging.info("on_message_callback:" + str(msg))
    client.msg_queue.put(msg)


def on_publish_callback(client, userdata, mid):
    """
    on_publish Callback

    :param client: 
    :param userdata: 
    :param mid: 
    :return: 
    """
    log.info('on_publish_callback')


class BaseClient(object):
    """
    Base Class for MQTT-Client

    """
    client = None

    def __init__(self, broker="iot.eclipse.org", port=1883, sub_queue=None, pub_queue=None, msg_queue=None, password=None, username=None):
        """
        Init BaseClient

        :param broker:
        :param port:
        :param sub_queue:
        :param pub_queue:
        :param msg_queue:
        :param password:
        :param username:
        """

        log.info("run: __init__()")
        self.client = mqtt.Client()
        self.client.sub_queue = sub_queue
        self.client.pub_queue = pub_queue
        self.client.msg_queue = msg_queue
        self.client.on_connect = on_connect_callback
        self.client.on_message = on_message_callback
        self.client.on_publish = on_publish_callback
        self.client.on_subscribe = on_subscribe_callback

        if (password is not None) and (username is not None):
            self.client.username_pw_set(username=username,password=password)


        try:

            self.client.connect(broker, port)
            self.client.loop_start()
            self.start_sub_queue()
            self.start_pub_queue()

        except ConnectionRefusedError as e:
            log.error(e)
            log.info('Exiting main...')
            _thread.interrupt_main()
            exit(0)

        except OSError as e:
            log.error(e)
            log.info('Exiting main ...')
            _thread.interrupt_main()
            exit(0)


    @run_async
    def start_sub_queue(self):
        """
        Start subscribe queue for handel asynchronous callbacks

        :return:
        """

        log.info("run: start_sub_queue()")

        while True:
            topic = self.client.sub_queue.get()
            self.client.subscribe(topic)

    @run_async
    def start_pub_queue(self):
        """
        Start publish queue for handel asynchronous callbacks

        :return:
        """
        log.info("run: start_pub_queue()")

        while True:
            msg = self.client.pub_queue.get()
            self.client.publish(topic=msg['topic'], payload=msg['payload'])
