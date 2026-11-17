---
name: coletar-editais
description: Coletar fontes oficiais de editais e seus anexos preservando versão, datas e falhas para nova tentativa.
---

# coletar-editais

Abra documento principal, regulamento, anexos e retificações. Colete prazo de inscrição e fuso, não data de resultado. Preserve URL, instante de consulta e hash. Deduplicate por financiador+edição+instrumento, sem fundir edições diferentes. Falha de fetch, bloqueio ou PDF não extraído vira pendência com motivo, nunca edital encerrado. O piloto run.py lista PDFs mas ainda não extrai anexos; não promova ficha a verificada enquanto exigências estiverem nesses anexos. Retenção: somente evidências necessárias e campos, sem armazenar cópias volumosas indefinidamente.
