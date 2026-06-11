import json
from kafka import KafkaConsumer


KAFKA_TOPIC = "reddit-posts"
KAFKA_SERVER = "localhost:9092"
OUTPUT_PATH = "data/processed/kafka_stream_log.jsonl"


def consume_posts_from_kafka(max_messages=50):
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        consumer_timeout_ms=10000,
    )

    count = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        for message in consumer:
            post = message.value
            file.write(json.dumps(post) + "\n")

            print(f"Received: {post['topic']} | {post['title'][:60]}")

            count += 1
            if count >= max_messages:
                break

    consumer.close()
    print(f"Kafka consumer saved {count} messages to {OUTPUT_PATH}")


if __name__ == "__main__":
    consume_posts_from_kafka()
