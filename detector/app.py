import os
import json
import socketio, time
from kafka import KafkaConsumer, KafkaProducer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")
LEGIT_TOPIC = os.environ.get("LEGIT_TOPIC")
FRAUD_TOPIC = os.environ.get("FRAUD_TOPIC")
CONN_URL = os.environ.get("CONN_URL")


def is_suspicious(transaction: dict) -> bool:
    """Determine whether a transaction is suspicious."""
    return transaction["amount"] >= 5000


# *** Write code to retrieve data from topics to get the latest stats.


sio = socketio.Client() # This is sync client, test & compare this against async client.


@sio.event
def connect():
    '''
        Function triggered on 'connect' event. Subscribes to topic
        and starts processing data. 

        TODO:
            - Add functionality to push data (num_legit, num_fraud, etc) to a Kafka topic.
    '''
    print('connected to server')
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value),
        auto_offset_reset='earliest'
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    TOTAL, NUM_LEGIT, NUM_FRAUD = 0, 0, 0
    AVG_AMT, AVG_LEGIT_AMT, AVG_FRAUD_AMT = 0, 0, 0
    for message in consumer:
        transaction: dict = message.value
        if is_suspicious(transaction):
            NUM_FRAUD += 1
            AVG_FRAUD_AMT = (AVG_FRAUD_AMT * (NUM_FRAUD - 1) + transaction['amount']) / (NUM_FRAUD)

            topic = FRAUD_TOPIC
            transaction['type'] = 'fraud'
        else:
            NUM_LEGIT += 1
            AVG_LEGIT_AMT = (AVG_FRAUD_AMT * (NUM_LEGIT - 1) + transaction['amount']) / (NUM_LEGIT)

            topic = LEGIT_TOPIC
            transaction['type'] = 'legit'
        TOTAL += 1
        AVG_AMT = (AVG_AMT * (TOTAL - 1) + transaction['amount']) / (TOTAL)
        transaction['num_legit'] = NUM_LEGIT
        transaction['num_fraud'] = NUM_FRAUD
        transaction['avg_legit_amt'] = int(AVG_LEGIT_AMT)
        transaction['avg_fraud_amt'] = int(AVG_FRAUD_AMT)
        transaction['num_total'] = TOTAL
        transaction['avg_total'] = int(AVG_AMT)

        transaction['amount'] = int(transaction['amount'])
        producer.send(topic, value=transaction)
        sio.emit(topic, transaction)
        time.sleep(1)


@sio.event
def disconnect():
    print('disconnected from server')


if __name__ == '__main__':
    sio.connect(CONN_URL) #('http://fraud-detector-pipeline_dashboard_1:5000')
    sio.wait()

