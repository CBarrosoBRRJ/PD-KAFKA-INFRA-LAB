"""Kafka producer for delivery tracking events."""

import argparse
import json
import logging
from dataclasses import asdict

from confluent_kafka import Producer

from tracking_simulator import DeliveryTrackingGenerator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("delivery-kafka-producer")


def delivery_report(error: object, message: object) -> None:
    """Callback invoked for each produced message."""

    if error is not None:
        logger.error("Delivery failed for key=%s: %s", message.key(), error)
    else:
        logger.debug(
            "Delivered to %s[%s] at offset %s",
            message.topic(),
            message.partition(),
            message.offset(),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce delivery location events to Kafka.")
    parser.add_argument(
        "--bootstrap-servers",
        type=str,
        default="localhost:9092,localhost:9093,localhost:9094",
        help="Kafka bootstrap servers",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="driver-location-state",
        help="Kafka topic for driver state events",
    )
    parser.add_argument(
        "--drivers",
        type=int,
        default=10,
        help="Number of drivers to simulate",
    )
    parser.add_argument(
        "--updates",
        type=float,
        default=5.0,
        help="Updates per second",
    )
    args = parser.parse_args()

    producer_config = {
        "bootstrap.servers": args.bootstrap_servers,
        "acks": "all",
        "enable.idempotence": True,
        "retries": 10,
        "linger.ms": 10,
        "compression.type": "lz4",
    }
    producer = Producer(producer_config)

    generator = DeliveryTrackingGenerator(updates_per_sec=args.updates, num_drivers=args.drivers)
    total_published = 0

    logger.info(
        "Starting producer for topic=%s with bootstrap_servers=%s",
        args.topic,
        args.bootstrap_servers,
    )

    try:
        for position in generator.generate_tracking_data():
            payload = asdict(position)
            key = payload["driver_id"]
            value = json.dumps(payload)

            producer.produce(
                topic=args.topic,
                key=key,
                value=value,
                callback=delivery_report,
            )
            producer.poll(0)

            total_published += 1
            if total_published % 100 == 0:
                logger.info("Published %s events", total_published)
    except KeyboardInterrupt:
        logger.info("Stopping producer by user interruption")
    finally:
        producer.flush(timeout=30)
        logger.info("Producer flushed. Total events published: %s", total_published)
