docker compose exec redis redis-cli --scan --pattern "driver:location:*" | measure
docker compose exec redis redis-cli HGETALL "driver:location:driver_100"
docker compose exec redis redis-cli HGETALL "driver:location:driver_101"
