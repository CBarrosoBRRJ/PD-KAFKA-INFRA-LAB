"""Delivery tracking event simulator used by the Kafka producer."""

import argparse
import json
import queue
import random
import threading
import time
from dataclasses import asdict, dataclass
from typing import Generator


@dataclass
class DeliveryPosition:
    """Represents a single real-time delivery location event."""

    timestamp: int
    driver_id: str
    delivery_id: str
    latitude: float
    longitude: float
    status: str


class DeliveryTrackingGenerator:
    """Generates driver position updates for a configurable fleet size and rate."""

    _LAT_START = -23.5505
    _LON_START = -46.6333
    _COORDINATE_DELTA = 0.001

    def __init__(self, updates_per_sec: float = 5.0, num_drivers: int = 20, max_queue_size: int = 1000) -> None:
        self._positions_queue: queue.Queue[DeliveryPosition] = queue.Queue(maxsize=max_queue_size)
        self._updates_per_sec = updates_per_sec
        self._num_drivers = num_drivers

        self._drivers_state: dict[str, dict[str, str | float]] = {}
        for index in range(self._num_drivers):
            driver_id = f"driver_{100 + index}"
            self._drivers_state[driver_id] = {
                "delivery_id": f"del_{1000 + index}",
                "lat": self._LAT_START + random.uniform(-0.05, 0.05),
                "lon": self._LON_START + random.uniform(-0.05, 0.05),
                "status": random.choice(["PICKING_UP", "DELIVERING"]),
            }

    def _update_driver_position(self, driver_id: str) -> DeliveryPosition:
        state = self._drivers_state[driver_id]

        state["lat"] = float(state["lat"]) + random.uniform(-self._COORDINATE_DELTA, self._COORDINATE_DELTA)
        state["lon"] = float(state["lon"]) + random.uniform(-self._COORDINATE_DELTA, self._COORDINATE_DELTA)

        if random.random() < 0.01:
            if state["status"] == "DELIVERING":
                state["status"] = "PICKING_UP"
                state["delivery_id"] = f"del_{random.randint(2000, 9999)}"
            else:
                state["status"] = "DELIVERING"

        return DeliveryPosition(
            timestamp=int(time.time()),
            driver_id=driver_id,
            delivery_id=str(state["delivery_id"]),
            latitude=round(float(state["lat"]), 6),
            longitude=round(float(state["lon"]), 6),
            status=str(state["status"]),
        )

    def _tracking_thread(self) -> None:
        delay = 1 / self._updates_per_sec
        driver_ids = list(self._drivers_state.keys())

        while True:
            driver_id = random.choice(driver_ids)
            position_update = self._update_driver_position(driver_id)
            self._positions_queue.put(position_update)
            time.sleep(delay)

    def generate_tracking_data(self) -> Generator[DeliveryPosition, None, None]:
        threading.Thread(target=self._tracking_thread, daemon=True).start()

        while True:
            position = self._positions_queue.get()
            yield position
            self._positions_queue.task_done()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a delivery tracking stream.")
    parser.add_argument("--drivers", type=int, default=10, help="Number of drivers to simulate (default: 10)")
    parser.add_argument("--updates", type=float, default=5.0, help="Updates per second (default: 5.0)")
    args = parser.parse_args()

    tracking_gen = DeliveryTrackingGenerator(updates_per_sec=args.updates, num_drivers=args.drivers)
    count = 0
    print(
        f"Starting Delivery Tracking Simulation for {args.drivers} drivers at {args.updates} updates/sec..."
        " (Press Ctrl+C to stop)"
    )
    try:
        for position in tracking_gen.generate_tracking_data():
            count += 1
            print(json.dumps(asdict(position)))
    except KeyboardInterrupt:
        print(f"\nSimulation stopped. {count} tracking updates generated.")
