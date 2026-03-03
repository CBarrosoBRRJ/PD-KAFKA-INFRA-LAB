# Parte Teórica - Estrategia de ML, Monitoramento e Anti-SPOF

## Estrategia de ML (sem definir modelo especifico)

### Fluxo de dados para ML
1. Coletar transações rotuladas (fraude confirmada, legitima, falso positivo).
2. Enriquecer com dados de usuario, estabelecimento, geografia e historico.
3. Gerar features comportamentais por janela temporal.
4. Treinar periodicamente com validação offline.
5. Publicar versao aprovada para inferencia em producao.
6. Medir drift e performance para disparar retreino.

### Janelas de SLA
- Resposta imediata: P50 <= 1s, P90 <= 5s.
- Deteccao de suspeita por ML: P50 <= 10 min, P90 <= 30 min.

### Realimentacao
- Confirmacoes de fraude e reversoes (falso positivo) voltam para dataset.
- Blacklist e atualizada por eventos confirmados.

## Anti-SPOF (sem ponto único de falha)

- Kafka com 3 brokers e replicacao de tópicos criticos.
- `min.insync.replicas` configurado para evitar escrita insegura.
- Servicos stateless com replicas multiplas.
- Banco e cache em alta disponibilidade.
- Monitoramento e alertas de indisponibilidade por componente.

## Monitoramento de saude do sistema

### Plataforma
- Uptime por servico.
- Saude de brokers Kafka.
- Lag de consumidores por tópico/grupo.
- Taxa de erro de conectores/jobs.

### Negocio
- TPS processado.
- Latencia P50/P90 da resposta imediata.
- Latencia P50/P90 do fluxo de suspeita ML.
- Taxa de transações bloqueadas/suspeitas/confirmadas.
- Taxa de falso positivo e falso negativo (quando disponivel).

### Dados e ML
- Volume diario de eventos ingeridos.
- Taxa de enriquecimento com sucesso.
- Drift de dados e estabilidade de score.
- Recall/precision em validação periodica.

