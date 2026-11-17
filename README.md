# Radar de editais

Lista de editais coletados via HTTP e classificados com evidências. Situação de inscrições deve ser revalidada na fonte; a captura publicada é histórica, não recorrente.

Projeto criado na oficina Codesinfo · REC’n’Play, Recife, 13 de novembro de 2026.

- [Demonstração da oficina](https://codesinfo-sustentabilidade.burgos.chatgpt.site/)
- Slug preservado: `codesinfo-sustentabilidade`.
- Esta cópia é independente do ambiente de hospedagem original. Não contém chaves de API nem o histórico privado de desenvolvimento.

## Instalação e execução

Requisito: Python 3 para servir os arquivos (nenhum pacote adicional).

```sh
git clone https://github.com/BurgosNY/codesinfo-sustentabilidade.git
cd codesinfo-sustentabilidade
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Abra http://localhost:8000. Para publicar, hospede o conteúdo de `dist/` em qualquer hospedagem estática.

## IA e chaves

A interface e o fluxo principal deste projeto **não precisam de chave de API**. Não adicione uma chave ao JavaScript do navegador. OpenAI não é uma dependência obrigatória.

## Atualizar a coleta

```sh
python3 pipeline/collect_no_ai.py
```

Consulta fontes públicas sem IA e grava `pipeline/output/no-ai-run.json` e `catalog.sqlite`. Revise manualmente os registros. Para atualizar a interface, copie o relatório aprovado: `cp pipeline/output/no-ai-run.json dist/catalog.json`. Não há cron nem execução automática; sites podem bloquear ou mudar a estrutura.

### Pipeline experimental com IA (opcional)

`pipeline/run.py` é o experimento anterior, separado do coletor determinístico. Exige `OPENAI_API_KEY` e aceita `MODEL` (padrão `gpt-4.1-mini`). Configure no ambiente e execute `python3 pipeline/run.py`; pode consumir créditos e fazer busca web. Não execute sem revisar o script e o custo. O `.env.example` é só documentação: Python não o carrega automaticamente.

Pode substituir OpenAI por outro motor adaptando `api()` em `pipeline/run.py`: endpoint Responses, autenticação, entrada, saída JSON e evidência de busca. Provedores só compatíveis com Chat Completions exigem adaptação; busca web e rastros de fontes precisam de equivalentes reais. Não há garantia de compatibilidade apenas mudando modelo/chave.

## Limites e uso editorial

Protótipo de oficina, não produto auditado para produção. Revise resultados, datas, contexto e fontes antes de publicar. Demonstrações históricas não indicam que a informação continua atual. Marcas e materiais de terceiros mantêm seus direitos; consulte `ASSETS.md`.
