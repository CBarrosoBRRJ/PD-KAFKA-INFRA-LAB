# Guia Rapido - Diagrama de Arquitetura (Parte Teorica)

Crie o diagrama em draw.io (ou similar) com os blocos abaixo:

1. **Origem**
- POS / API Online

2. **Ingestao**
- Kafka (topicos de transacao e eventos de decisao)

3. **Resposta imediata**
- Motor de blacklist (consulta user/card/site)
- Saidas: `APROVA` ou `BLOQUEIA`

4. **Enriquecimento e ML**
- Enriquecimento (dados de usuario + estabelecimento)
- Feature pipeline
- Servico de inferencia (suspeita)

5. **Decisao e feedback**
- Fila de revisao/confirmacao
- Atualizacao de blacklist
- Evento de falso positivo/reversao

6. **Persistencia**
- Banco transacional (auditoria)
- Data lake (historico/treino)
- Busca analitica (investigacao)

7. **Observabilidade**
- Prometheus
- Grafana
- Alertas

Salvar imagem final em:
- `evidencias/parte_teorica/imagens/01_diagrama_arquitetura.png`
