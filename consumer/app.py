from services.consumer import KafkaConfig, KafkaSubscriberToTopic
import os
from helpers.logger import BaseLogger
import json
import time
from flask_socketio import SocketIO, emit, join_room, leave_room, send, close_room, rooms, disconnect
from flask import Flask, render_template
from threading import Thread
import eventlet
eventlet.monkey_patch()

async_mode = 'eventlet'
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
thread = None

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = 'transaction_queue'

baseLogger = BaseLogger()
logger = baseLogger.logger_instance()


def background_thread():

    KAFKA_SERVER_INSTANTIATE = KafkaConfig(bootstrap_servers=KAFKA_BROKER_URL,
                                       value_deserializer=lambda value: json.loads(value), api_version=(0, 10, 1))

    kafka_subscribe_to_topic = KafkaSubscriberToTopic(
        KAFKA_SERVER_INSTANTIATE, TRANSACTIONS_TOPIC)
    consumer = kafka_subscribe_to_topic.return_kafka_consumer()
    # consumer reading is a blocking code
    for message in consumer:
        socketio.emit('message',
                      {'data': message.value['name']}, broadcast=True)
        logger.debug('emitted')
        time.sleep(1)


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template("index.html")


@socketio.on('connect')
def connected():
    socketio.emit('message',
                      {'data': 'user connected'}, broadcast=True)
    # send('connected', broadcast=True)


@socketio.on('message')
def handleMessage(msg):
    emit(msg, broadcast=True)
    logger.debug('Message: ' + msg)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
