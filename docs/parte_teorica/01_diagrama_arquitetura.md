# Parte Teórica - Diagrama de Arquitetura

## Objetivo do diagrama
Representar a arquitetura proposta para detecção de fraude em tempo real, com:
- resposta imediata por blacklist;
- classificação de suspeita por trilha de ML;
- persistência para auditoria e histórico;
- observabilidade e operação sem ponto único de falha.

## Componentes principais
1. **Origem de transações**
- POS físico e API de pagamentos online.

2. **Ingestão de eventos**
- Kafka como barramento central de transações e eventos de decisão.

3. **Resposta imediata**
- Motor de decisão consulta blacklist de `user_id`, `card_id` e `site_id`.
- Em caso de correspondência, bloqueio imediato da transação.

4. **Enriquecimento e ML**
- Transações sem bloqueio imediato passam por enriquecimento de dados.
- Pipeline de features envia evento para inferência de suspeita.
- Resultado alimenta fila de revisão/confirmacão e retroalimentação.

5. **Feedback de fraude**
- Confirmações de fraude atualizam blacklist.
- Falsos positivos alimentam ajuste de regras/modelo.

6. **Persistência**
- Base transacional para auditoria e rastreabilidade.
- Camada histórica para treino e reprocessamento.

7. **Observabilidade**
- Prometheus + Grafana para saúde de componentes, latência e eventos.

## Artefato visual
- Imagem do diagrama: `docs/parte_teorica/imagens/01_diagrama_arquitetura.png`

