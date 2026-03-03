docker compose exec kafka1 kafka-topics --bootstrap-server kafka1:29092 --create --if-not-exists --topic driver-location-state --partitions 6 --replication-factor 3 --config cleanup.policy=compact --config min.cleanable.dirty.ratio=0.01 --config segment.ms=10000 --config delete.retention.ms=1000 --config min.insync.replicas=2

docker compose exec kafka1 kafka-topics --bootstrap-server kafka1:29092 --describe --topic driver-location-state
