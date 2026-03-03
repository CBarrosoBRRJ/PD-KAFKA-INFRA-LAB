# Parte Teórica - Tecnologias e Justificativas

## Mensageria e streaming
- **Apache Kafka**
  - Motivo: alto throughput, desacoplamento entre produtores/consumidores e boa tolerancia a falhas.
  - Aderencia ao requisito: suporta alta taxa de eventos e arquitetura distribuida sem SPOF.

## Resposta imediata (bloqueio por blacklist)
- **Servico stateless em containers (API/rules engine)**
  - Motivo: escala horizontal e baixa latencia para decisao de bloqueio.
  - Armazenamento de consulta rapida: Redis ou banco chave-valor para blacklist.

## Persistência transacional e auditoria
- **Banco relacional (PostgreSQL)**
  - Motivo: consistencia, integridade e auditoria de eventos e decisoes.
  - Uso: trilha transacional, historico de decisoes, dados de compliance.

## Features e historico para ML
- **Data lake/objeto (S3/MinIO/HDFS)**
  - Motivo: armazenamento historico de grande volume com custo eficiente.
  - Uso: treinamento, reprocessamento e analises offline.

## Busca e analise investigativa
- **Mecanismo de busca/analytics (OpenSearch/Elasticsearch)**
  - Motivo: consultas investigativas rapidas, filtros e agregacoes para analistas de fraude.

## Observabilidade
- **Prometheus + Grafana**
  - Motivo: padrao de mercado para metricas e dashboards operacionais.
  - Uso: saude da plataforma, latencia, erro, lag de consumo e disponibilidade.

## Orquestracao e deploy
- **Docker + orquestrador (Kubernetes ou equivalente)**
  - Motivo: padronizacao, portabilidade, escalabilidade e isolamento de serviços.

