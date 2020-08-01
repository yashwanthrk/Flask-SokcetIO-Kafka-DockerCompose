import os
import json
import threading

from kafka import KafkaConsumer, KafkaProducer, TopicPartition


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = 'transaction_queue'


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """ Singelton Design Pattern  """
        if cls not in cls._instance:
            cls._instance[cls] = super(
                MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class KafkaConfig():
    def __init__(self, bootstrap_servers, value_deserializer, api_version):
        # threading.Thread.__init__(self)
        # self.daemon = True
        """ Configure Kafka Server  """
        self.bootstrap_servers = bootstrap_servers,
        self.value_deserializer = value_deserializer,
        self.api_version = api_version


class KafkaSubscriberToTopic():

    def __init__(self, server, topic):
        """
        :param server: Object of class KafkaConfig
        """
        # threading.Thread.__init__(self)
        # self.daemon = True
        self.server = server
        self._consumer = KafkaConsumer(
            topic,
            # group_id='consumer-1',
            bootstrap_servers=self.server.bootstrap_servers,
            # Encode all values as JSON
            value_deserializer=lambda value: json.loads(value),
            # api_version=(0, 10, 1)
            enable_auto_commit=False,
            # consumer_timeout_ms=1000
        )
        

    def return_kafka_consumer(self):
        return self._consumer
