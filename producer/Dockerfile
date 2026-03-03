FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY producer/tracking_simulator.py /app/tracking_simulator.py
COPY producer/kafka_producer.py /app/kafka_producer.py

CMD ["python", "/app/kafka_producer.py", "--bootstrap-servers", "kafka1:29092,kafka2:29092,kafka3:29092", "--topic", "driver-location-state", "--drivers", "20", "--updates", "10"]
