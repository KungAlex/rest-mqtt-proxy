import json
import datetime
import logging


def default_output_handler(msg):

    try:
        output = json.loads(msg.payload.decode())

    except json.decoder.JSONDecodeError as e:
        logging.info(e)
        output = msg.payload.decode()

    logging.info("topic: " + msg.topic + " payload: " + str(output) + " Type: " + str(type(output)))


def push_influxdb_handler(msg, queue):
    logging.info("push_influxdb_handler: start callback")
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

    logging.info(json_body)
    queue.put(json_body)
