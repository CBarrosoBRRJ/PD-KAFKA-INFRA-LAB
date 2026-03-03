# PD-KAFKA-INFRA-LAB

Projeto da disciplina dividido em duas frentes:
- Parte teórica: arquitetura de detecção de fraude em tempo real.
- Parte prática: pipeline Kafka para rastreamento de entregadores com estado atual no Redis.

## Repositório
- URL: `https://github.com/CBarrosoBRRJ/PD-KAFKA-INFRA-LAB`

## Escopo
- Escopo consolidado: `docs/escopo_projeto.md`
- Parte teórica (artefatos):
  - `docs/parte_teorica/01_diagrama_arquitetura.md`
  - `docs/parte_teorica/02_casos_de_uso.md`
  - `docs/parte_teorica/03_tecnologias_justificativas.md`
  - `docs/parte_teorica/04_ml_monitoramento_spof.md`
  - `docs/parte_teorica/imagens/01_diagrama_arquitetura.png`
- Relatório final em HTML (com imagens): `relatorio/index.html`

## Arquitetura da parte prática
- Kafka (3 brokers)
- Kafka Connect (Redis Sink)
- Redis (estado atual por `driver_id`)
- Prometheus + Grafana
- Produtor Python com simulador de localização

## Estrutura principal
- `docker-compose.yml`
- `producer/tracking_simulator.py`
- `producer/kafka_producer.py`
- `connectors/redis-sink-driver-location.json`
- `scripts/create_topic.ps1`
- `scripts/create_connector.ps1`
- `scripts/validate_state.ps1`
- `relatorio/` (HTML + CSS + imagens de evidência)

## Pre-requisitos
- Docker Desktop
- Docker Compose v2

Observação: para execução local do produtor via Python, use `requirements.txt` (opcional).

## Execução rápida (100% Docker para infraestrutura)
1. Subir serviços:
```powershell
docker compose up -d
```

2. Verificar status:
```powershell
docker compose ps
```

3. Criar/validar tópico compactado:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create_topic.ps1
```

4. Criar/atualizar conector Redis Sink:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create_connector.ps1
```

5. Rodar produtor (opção A - local):
```powershell
pip install -r requirements.txt
python .\producer\kafka_producer.py --drivers 20 --updates 10 --topic driver-location-state
```

6. Rodar produtor (opção B - container):
```powershell
docker build -f .\producer\Dockerfile -t delivery-producer .
docker run --rm --network pd_kafka_infra_lab_default delivery-producer
```

## Validação funcional
- Validar estado no Redis:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate_state.ps1
```

Esperado:
- chaves no padrão `driver:location:<driver_id>`
- estado atualizado por entregador sem duplicidade lógica

## Observabilidade
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
  - usuário: `admin`
  - senha: `admin`
  - dashboard: `Kafka Delivery Tracking Overview`

## Resiliência (teste)
```powershell
docker stop kafka2
docker compose ps
docker start kafka2
docker compose ps
```

## Dependências Python
Arquivo `requirements.txt`:
- `confluent-kafka==2.6.1`

Usado apenas para execução local do produtor. Infra principal e validações rodam via Docker.

