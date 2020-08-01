import os
from time import sleep
import json

from kafka import KafkaProducer
from faker import Faker
import random


TRANSACTIONS_TOPIC = 'transaction_queue'
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')



class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """ Singelton Design Pattern  """
        if cls not in cls._instance:
            cls._instance[cls] = super(
                MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class KafkaConfig():
    def __init__(self, bootstrap_servers, value_serializer, api_version):
        """ Configure Kafka Server  """
        self.bootstrap_servers = bootstrap_servers,
        self.value_serializer = value_serializer,
        self.api_version = api_version


class KafkaPublisher():

    def __init__(self, server):
        """
        :param server: Object of class KafkaConfig
        """

        self.server = server
        self._producer = KafkaProducer(
            bootstrap_servers=self.server.bootstrap_servers,
            # Encode all values as JSON
            value_serializer=lambda value: json.dumps(value).encode(),
            api_version=(0, 10, 1)
        )

    def publish(self, topic, payload={}):
        """
        :param payload: JSON payload
        :return: None
        """
        self._producer.send(topic, payload)
        print("Published Message: {}".format(payload))
        # flush the message buffer to force message delivery to broker on each iteration
        # self._producer.flush()


if __name__ == '__main__':
    kafka_server = KafkaConfig(bootstrap_servers=KAFKA_BROKER_URL, value_serializer=lambda value: json.dumps(
        value).encode(), api_version=(0, 10, 1))
    kafka_publisher = KafkaPublisher(kafka_server)
    while True:
        fake = Faker()
        transaction: dict = {
            'name': fake.name(), 'amount': random.randint(1000, 9999)}
        kafka_publisher.publish(TRANSACTIONS_TOPIC, transaction)
        # ten seconds
        sleep(10)
