---
name: descobrir-editais
description: Descobrir oportunidades de financiamento para jornalismo e áreas transversais, com fontes oficiais e rastreabilidade.
---

# descobrir-editais

Busque por financiadores e instrumentos, não apenas jornalismo: grants, chamadas públicas, fomento, bolsas, cultura, memória, direitos, socioambiental e educação. Cruze financiadores (Pulitzer, Fundo Brasil, fundos culturais, fundações e redes de jornalismo) com território e entidade elegível. Agregadores são pistas: abra a chamada original. Expanda fontes a partir de links descobertos. Registre queries, URLs e lacunas de cobertura. Não diga atualizado automaticamente sem execução recorrente real. Execute ../../run.py para um piloto delimitado com busca web e API; budget de piloto não é limite definitivo do produto.

## Modo atual: coleta sem IA
A pedido de Lucas em 13/11, a consulta automatizada não chama modelo. Use `../../collect_no_ai.py`: visita índices HTML de fontes conhecidas, descobre links concretos, coleta páginas e persiste observações. `run.py` é o experimento anterior baseado em IA e não deve ser usado para esta etapa. Não exclua chamadas por encaixe jornalístico. Mantenha abertas, encerradas, contínuas e sem status separadas. Agregadores ampliam descoberta, mas não substituem a verificação do financiador. A lista de fontes é expandível e a cobertura deve ser reportada, não chamada exaustiva.
