# Modelo e cinco experimentos - Localização

| Item | Onde está | Situação |
|---|---|---|
| Parâmetros, sequência dos símbolos e pagamentos | [maquina_estatistica.py (line 35)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:35) | Implementados. |
| Sorteio circular, usando posições de 0 a 4 e retorno com módulo 5 | [maquina_estatistica.py (line 45)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:45) | Implementado. |
| Três rolos e pagamento apenas da linha central | [maquina_estatistica.py (line 51)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:51) | Implementado. A função descreve sorteios independentes entre rolos. |
| Sementes, gerador e versões do ambiente | [maquina_estatistica.py (line 507)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:507) e [metadados_execucao.json](/D:/PROJETOS/maquina_estatistica/resultados/metadados_execucao.json) | Registrados: E1=2026, E2=10/2026/123456, E3=42, gerador `random.Random` e versões de Python, NumPy, pandas e Matplotlib. |
| E1 — frequências observadas versus teóricas | [maquina_estatistica.py (line 119)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:119) e [e1_frequencias.csv](/D:/PROJETOS/maquina_estatistica/resultados/e1_frequencias.csv) | Procedimento e resultados presentes. |
| E2 — médias acumuladas e reprodutibilidade | [maquina_estatistica.py (line 171)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:171) e [e2_medias_acumuladas.csv](/D:/PROJETOS/maquina_estatistica/resultados/e2_medias_acumuladas.csv) | Presente; compara três sementes e verifica a repetição dos primeiros resultados. |
| E3 — saldos dos participantes | [maquina_estatistica.py (line 223)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:223) e [e3_resumo.csv](/D:/PROJETOS/maquina_estatistica/resultados/e3_resumo.csv) | Presente: 100 participantes, até 500 rodadas ou saldo insuficiente. |
| E4 — prêmio na rodada seguinte | [maquina_estatistica.py (line 282)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:282) e [e4_probabilidade_condicional.csv](/D:/PROJETOS/maquina_estatistica/resultados/e4_probabilidade_condicional.csv) | Presente; compara a proporção observada com a referência teórica de 4%. |
| E5 — comparação de pagamentos | [maquina_estatistica.py (line 308)](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:308) e [e5_comparacao_pagamentos.csv](/D:/PROJETOS/maquina_estatistica/resultados/e5_comparacao_pagamentos.csv) | Presente: tabela base versus pagamentos aumentados em 10%. |

<br>
<br>
<br>

# Relatorio 

Os CSVs mostram os resultados, mas não escrevem a interpretação por vocês. Por exemplo: no E1, a simulação observou 4,12% de prêmios e lucro médio de −0,1315 crédito por rodada, contra −0,16 teórico. No E3, 75% terminaram com perda e 67% esgotaram o saldo. Esses números precisam ser comentados no relatório, inclusive explicando que diferenças entre simulação e teoria podem ocorrer por variabilidade amostral.

<br>
<br>
<br>

# Pontos Extras - Localização
| Extra | Situação |
|---|---|
| Intervalo de confiança | **Parcial.** O cálculo está em [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:343) e o resultado em [extra_intervalo_confianca.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_intervalo_confianca.csv). Faltam explicar melhor hipóteses e interpretação; há ainda uma pequena inconsistência: o docstring menciona intervalo *t*, mas o cálculo usa 1,96, aproximação normal. |
| Mesmo RTP, riscos diferentes | **Parcial.** [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:365) e [extra_mesmo_rtp_riscos.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_mesmo_rtp_riscos.csv) comparam pagamentos e dispersão. O critério também pede comparar saldos, o que não está calculado nessa análise. |
| Limites de exposição | **Parcial.** [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:398) e [extra_limites_exposicao.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_limites_exposicao.csv) comparam 100 e 500 rodadas. Há saldo, perdas, esgotamento e rodadas médias, mas falta apresentar separadamente o percentual de participantes com ganho. |
| Auditoria de afirmação pública | **Não encontrei no projeto.** |
| Educação científica — página ou vídeo | **Implementada.** Há uma secção dentro de app.py com a explicação implementada |
| Interface acessível | **Parcial.** O Streamlit tem contraste ajustado e a linha premiada é indicada por cor e legenda, mas não encontrei uma verificação documentada de uso por teclado/acessibilidade. |
| Validação automatizada | **Implementada.** Há 13 verificações em [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:459), com resultados em [extra_testes_automatizados.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_testes_automatizados.csv). Elas rodam ao executar `python maquina_estatistica.py` ([chamada no fluxo principal](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:552)); o README poderia explicar isso explicitamente. |
| Análise de sensibilidade | **Cálculo implementado; interpretação escrita pendente.** Há seis cenários em [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:432) e [extra_analise_sensibilidade.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_analise_sensibilidade.csv). |