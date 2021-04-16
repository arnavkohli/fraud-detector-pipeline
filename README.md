# Fraud Detector Pipeline

A pipeline designed using Apache Kafka to segregate fraudulent/ legitimate transactions.

## Features
- Bifurcate transactions into two types _(fraudulent/ legitimate_)_
- Provides insights over a socketio dashboard

## Services

### Dashboard
_Flask SocketIO Dashboard to provide real time insights._

### Detector
_Service to segregate the transactions on receiving them from the **subscribed** Kafka topic._

### Generator (_for testing_)
_Service to generate random transactions and populate the Kafka topic._

## References
https://florimond.dev/blog/articles/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/
