import json
from time import sleep

import pymysql
from confluent_kafka import Consumer, KafkaException

DB_CONFIG = {
    'host': 'mysql',
    'user': 'root',
    'password': 'example',
    'database': 'kafka_demo',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def insert_to_db(data):
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO insurance_applications (
                        application_id, agent_id, customer_name, plan, timestamp
                    ) VALUES (%s, %s, %s, %s, %s)
                ''', (
                    data['application_id'],
                    data['agent_id'],
                    data['customer_name'],
                    data['plan'],
                    data['timestamp']
                ))
            conn.commit()
    except pymysql.MySQLError as err:
        print(f"[DB ERROR] {err}")

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'notifier-group',
    'auto.offset.reset': 'earliest'
})

# Wait for topic to exist
for _ in range(10):
    md = consumer.list_topics(timeout=5.0)
    if 'insurance_applications' in md.topics:
        print("[Consumer] Topic ready.")
        break
    print("[Consumer] Waiting for topic...")
    sleep(2)
else:
    raise Exception("Topic 'insurance_applications' not found after retries.")

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
        print(f"[Consumer] Received: {data}")
        if data.get("init"):
            continue
        insert_to_db(data)
except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
