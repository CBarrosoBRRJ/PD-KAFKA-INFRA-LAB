# Parte Teórica - Casos de Uso e Fluxos

## Caso 1 - Transacao legitima (sem historico de fraude)
1. Evento de transacao chega via POS/API e entra no Kafka.
2. Motor de resposta imediata consulta blacklist (user/card/site).
3. Sem match em blacklist, transacao segue para enriquecimento de dados.
4. Pipeline de features envia evento para modulo de scoring.
5. Se score abaixo do limiar, transacao aprovada.
6. Evento final e persistido para trilha de auditoria (retencao 180 dias).

## Caso 2 - Transacao com entidade ja fraudulenta
1. Evento chega no Kafka.
2. Motor de resposta imediata encontra `user_id`, `card_id` ou `site_id` na blacklist.
3. Transacao e bloqueada imediatamente.
4. Sistema publica evento de bloqueio e registra para auditoria/monitoramento.

## Caso 3 - Transacao suspeita por ML
1. Evento sem historico de fraude passa no filtro de blacklist.
2. Sistema enriquece dados (usuario, estabelecimento, contexto geografico/comportamental).
3. Modulo de ML gera score de suspeita.
4. Se score acima do limiar, transacao marcada como suspeita.
5. Resultado alimenta lista de revisao/confirmacao.
6. Transacoes suspeitas ficam armazenadas para retreino e analise.

## Caso 4 - Confirmacao de fraude
1. Time de risco ou regra externa confirma fraude.
2. Sistema atualiza blacklist (card/user/site).
3. Novas transações relacionadas passam a ser bloqueadas em resposta imediata.
4. Evento de confirmacao alimenta dataset supervisionado para treinamento futuro.

## Caso 5 - Falso positivo (reversao)
1. Caso suspeito e reavaliado e classificado como legitimo.
2. Sistema remove/ajusta bloqueio quando aplicavel.
3. Evento de reversao alimenta dataset para reduzir falsos positivos.
4. Monitoramento acompanha taxa de FP por janela de tempo.

