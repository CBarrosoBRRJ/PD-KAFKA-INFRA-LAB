# Escopo do Projeto - Disciplina Kafka

## Visão geral
O projeto possui duas partes:

1. Parte teórica: projeto de arquitetura para detecção de fraude em tempo real.
2. Parte prática: implementação de pipeline Kafka para rastreamento de entregadores com estado atual em Redis.

## Parte teórica - Detecção de fraude

### Objetivo
Analisar transações de cartão de crédito em tempo real e:
- responder imediatamente se `card_id`, `user_id` ou `site_id` estiver em lista de bloqueio;
- classificar suspeitas via ML para eventos sem histórico de fraude;
- retroalimentar lista de bloqueio com confirmações de fraude.

### Dados de entrada
- Transação: `timestamp`, `transaction_id`, `user_id`, `card_id`, `site_id`, `value`, `location_id`, `country`
- Usuário: `user_id`, `nome`, `endereco`, `email`
- Estabelecimento: `site_id`, `nome`, `endereco`, `categoria_produtos`

### Requisitos não funcionais
- Escalabilidade: até 10.000 TPS
- Disponibilidade: 99,9%
- Latência de resposta imediata: P50 <= 1s, P90 <= 5s
- Latência para identificação de suspeitas: P50 <= 10 min, P90 <= 30 min
- Retenção: 180 dias para transações e suspeitas
- Sem SPOF

### Entregáveis da parte teórica
- Diagrama de arquitetura
- Casos de uso e fluxos
- Justificativa de tecnologias
- Estratégia de ML (sem obrigação de definir algoritmo específico)
- Estratégia de monitoramento e métricas de saúde

## Parte prática - Rastreamento de entregadores

### Objetivo
Manter no Redis somente o estado mais recente por entregador.

### Requisitos técnicos
1. Cluster Kafka com 3 brokers.
2. Tópico configurado para comportamento de último estado por chave (compactação).
3. Produtor Python usando simulador de eventos.
4. Schema mínimo: `driver_id`, `latitude`, `longitude`, `timestamp`, `status`.
5. Integração automática Kafka Connect Sink -> Redis.
6. Prometheus e Grafana para monitoramento.

### Entregáveis da parte prática
- Topologia do ambiente (`docker-compose.yml`)
- Configuração dos tópicos
- Configuração do conector Redis Sink
- Evidências de monitoramento
- Validação de estado no Redis sem duplicidade por entregador
- Demonstração de resiliência com parada de 1 broker

## Implementação atual (resumo)
- Kafka: 3 brokers
- Tópico: `driver-location-state`
- Chave de mensagem: `driver_id`
- Connect: `com.redis.kafka.connect.RedisSinkConnector`
- Redis: chaves `driver:location:<driver_id>` com último estado
- Monitoramento: Prometheus + Grafana
