import json
import time
import pandas as pd
from kafka import KafkaProducer


INPUT_PATH = "data/raw/reddit_posts.csv"
KAFKA_TOPIC = "reddit-posts"
KAFKA_SERVER = "localhost:9092"


def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


def stream_posts_to_kafka(delay_seconds=0.2):
    df = pd.read_csv(INPUT_PATH)
    producer = create_producer()

    print(f"Streaming {len(df)} posts to Kafka topic: {KAFKA_TOPIC}")

    for _, row in df.iterrows():
        message = row.to_dict()
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Sent: {message['topic']} | {message['title'][:60]}")
        time.sleep(delay_seconds)

    producer.flush()
    producer.close()

    print("Kafka producer completed.")


if __name__ == "__main__":
    stream_posts_to_kafka()
