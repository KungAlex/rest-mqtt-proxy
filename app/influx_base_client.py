from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from helper import run_async
import logging
import _thread

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class InfluxDBBaseClient(object):
    client = None
    host = None
    port = None
    database = None

    def __init__(self, host="localhost", port=8086, database="iot", persistent_queue=None):
        """

        :param host:
        :param port:
        :param database:
        :param persistent_queue:
        """
        log.info("run __init__")
        self.persistent_queue = persistent_queue
        self.host = host
        self.port = port
        self.database = database
        self.start_client()
        self.run_persistent_queue()

    def start_client(self):
        log.info("run start_client()")
        try:
            self.client = InfluxDBClient(host=self.host, port=self.port, database=self.database)

        except ConnectionRefusedError as e:
            log.error(e)
            log.info('Exiting main...')
            _thread.interrupt_main()
            exit(0)

    @run_async
    def run_persistent_queue(self):
        """
        Subscribe
        """
        logging.info("run run_persistent_queue")

        while True:
            json_body = self.persistent_queue.get()
            log.info(json_body)
            try:

                self.client.write_points(json_body)

            except ConnectionRefusedError as e:
                log.error(e)
                log.info('InfluxDBBaseClient: Exiting main...')
                _thread.interrupt_main()
                exit(0)

            except InfluxDBClientError as e:
                log.error(e)
                log.info('InfluxDBBaseClient: Exiting main...')
                _thread.interrupt_main()
                exit(0)
