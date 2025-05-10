import json

from confluent_kafka import Consumer, KafkaException

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'notifier-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['insurance_applications'])

print("[Consumer] Listening for events...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        data = json.loads(msg.value().decode('utf-8'))
        print(f"[Consumer] Received event: {data}")
except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
