# Motor de descoberta: piloto de oficina

Não é um monitor recorrente em produção. Executa busca web via API, recolhe fontes e interpreta os documentos em etapas separadas. Sem endpoint público, sem inscrição ou envio de proposta.

## Executar
`python pipeline/run.py`, fornecer chave por stdin oculto ou variável de ambiente mantida pelo operador. Não pôr chave em comando, código, logs ou Git. Modelo configurável por MODEL; padrão gpt-4.1-mini.
`--reuse-discovery` repete coleta/análise dos candidatos guardados, sem nova busca paga.

## Artefatos
- output/search-trace.json: resposta da API com web_search_call real. queries_used do JSON do modelo não é log autoritativo: consultar action no rastro.
- output/discovery.json: candidatos, ainda não são editais verificados.
- output/catalog.sqlite: observações por URL e instante; falhas persistem como unknown para retomada.
- output/run.json: relatório de cobertura e consumo. Não representa verificação editorial concluída.
- Skills em skills/: descobrir, coletar, analisar. São recursos do projeto, não instaladas globalmente.

## Implementado e limites
Busca programática executada, coleta HTML, hash, extração por IA, conferência de citações no texto e persistência SQLite. Sem segredo persistido. Fonte inacessível não vira encerrada; necessidade de PDF fica pendente. Conteúdo bruto de página não é mantido, apenas hash e evidências. Máximo5 candidatos é orçamento do piloto, não regra de completude.
Ainda falta: extrair PDFs/retificações, resolver fontes JavaScript, expansão persistente da lista de financiadores, paginação por fonte, execução recorrente, revisão editorial, validação de elegibilidade por perfil e integração ao catálogo público. Busca que retorna prêmio/livro ou chamada antiga não equivale a oportunidade de financiamento aberta.

## Próxima evolução
Ciclo diário por financiador conhecido + descoberta exploratória em eixos alternados; uma fila persistente de fontes pendentes com tentativas e motivos. Editais futuros/contínuos são revisitados; encerrados permanecem no arquivo. Novos domínios são verificados e incorporados, não limitados para sempre à lista inicial. Campos desconhecidos ficam explícitos. Priorizar relevância e prova, não número de cartões.

## Revisão solicitada por Lucas: sem IA na consulta
Executar `python pipeline/collect_no_ai.py`. Não requer chave e não faz chamadas OpenAI. Descobre URLs percorrendo índices de financiadores e agregadores; coleta HTML, título, status explícito e referências a prazo. Histórico SQLite e relatório no-ai-run.json. Não julga adequação ao jornalismo. Limitação: índice sem paginação descoberta pode omitir arquivos; status aberto textual sem data deve ser conferido; datas relativas não são convertidas implicitamente; portal de terceiros permanece identificado como tal. Nenhuma rotina agendada está ativa.
