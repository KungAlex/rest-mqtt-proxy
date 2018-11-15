import json
import datetime
import logging

log = logging.getLogger(__name__)


def default_output_handler(msg):

    try:
        output = json.loads(msg.payload.decode())

    except json.decoder.JSONDecodeError as e:
        log.info(e)
        output = msg.payload.decode()

        log.info("topic: " + msg.topic + " payload: " + str(output) + " Type: " + str(type(output)))


def push_influxdb_handler(msg, queue):
    log.info("push_influxdb_handler: start callback")
    value_output = msg.payload.decode()

    current_time = datetime.datetime.utcnow().isoformat()
    # TODO fix tag (get from client config)
    json_body = [

        {
            "measurement": msg.topic,
            "tags": {
                "host": "localhost",
                "broker": "mosquitto",
                "namespace": "iot.micronodes.io"
            },
            "time": current_time,
            "fields": {
                "value": value_output
            }
        }
    ]

    queue.put(json_body)
