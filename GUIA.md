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

# Relatorio 

Os CSVs mostram os resultados, mas não escrevem a interpretação por vocês. Por exemplo: no E1, a simulação observou 4,12% de prêmios e lucro médio de −0,1315 crédito por rodada, contra −0,16 teórico. No E3, 75% terminaram com perda e 67% esgotaram o saldo. Esses números precisam ser comentados no relatório, inclusive explicando que diferenças entre simulação e teoria podem ocorrer por variabilidade amostral.

<br>
<br>
<br>

# 🌟 Atividades extras — até 20 pontos
As atividades abaixo podem render **até 20 pontos adicionais**. Para pontuar, implemente cada proposta e registre evidências no projeto.

| Atividade | Valor | O que fazer |
|---|:---:|---|
| **Validação automatizada** | Até 3 pontos | **O que fazer:** Acrescentar pelo menos **cinco verificações/testes automatizados** relevantes no código (ex.: checagem automática de pagamentos, cálculo do lucro, controle de semente, totais acumulados e um caso-limite) e explicar como executá-los |
| **Intervalos de confiança** | Até 4 pontos | **O que fazer:** Estimar um intervalo de confiança para o lucro médio ou para o RTP, explicando o método estatístico utilizado, as hipóteses e o significado da incerteza. Usar execuções independentes ou justificar o uso de reamostragem. |
| **Mesma média, riscos diferentes** | Até 4 pontos | **O que fazer:** Construir uma tabela alternativa de pagamentos que possua **exatamente o mesmo RTP** da tabela base (84%), mas com uma **dispersão (variância/desvio-padrão) diferente**. Comparar as distribuições e os saldos simulações. |
| **Limites de exposição** | Até 3 pontos | **O que fazer:** Comparar duas regras de parada predefinidas antes de simular. Analisar perdas, ganhos e o número de rodadas jogadas, diferenciando *tempo de exposição* de *esperança por rodada*. |
| **Auditoria de uma afirmação pública** | Até 3 pontos | **O que fazer:** Verificar uma alegação quantitativa na sua fonte original (analisando definição, população, período, método e limitações), indo além da contextualização básica exigida no relatório. |
| **Educação científica** | Até 3 pontos | **O que fazer:** Produzir um material de divulgação científica (uma página web ou um vídeo de até 3 minutos) direcionado ao público não especializado, apresentando os resultados próprios da simulação, conceitos explicados e fontes verificáveis. |
| **Interface acessível** | Até 3 pontos | **O que fazer:** Implementar recursos de acessibilidade no programa (interação via teclado, contraste adequado de cores, informações visuais que não dependam apenas de cor) e demonstrar um teste de uso. |
| **Análise de sensibilidade** | Até 3 pontos | **O que fazer:** Variar os valores de pagamentos ou probabilidades em **pelo menos cinco cenários diferentes** (indo além das duas tabelas do Experimento 5) e explicar como a esperança matemática e o RTP se alteram em cada cenário. |

### 📐 Regras de pontuação

- **Cálculo:** `Extras = min(20, soma dos pontos adicionais)`.
- **Registro das evidências:** O grupo deve especificar no relatório e no `README` quais extras foram implementados e em qual parte do projeto/código se encontram as evidências.
- **Pontuação parcial:** Itens incompletos ou meramente descritivos recebem nota parcial. Um mesmo resultado não é pontuado em duas opções diferentes.

<br>
<br>

# Pontos Extras - Localização
| Extra | Situação |
|---|---|
| Intervalo de confiança | **Parcial.** O cálculo em [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:346) e o resultado em [extra_intervalo_confianca.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_intervalo_confianca.csv) usam aproximação normal de 95% para a média de uma sequência do E1, com multiplicador 1,96. Não é um intervalo para resultados individuais. |
| Mesmo RTP, riscos diferentes | **Parcial.** [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:368) e [extra_mesmo_rtp_riscos.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_mesmo_rtp_riscos.csv) comparam pagamentos e dispersão dos lucros. Saldos finais dos participantes não são calculados; portanto, a conclusão deve se limitar a essas medidas. |
| Limites de exposição | **Implementado.** [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:401) e [extra_limites_exposicao.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_limites_exposicao.csv) comparam 100 e 500 rodadas e registram percentuais de ganho, empate, perda e esgotamento, além dos saldos e rodadas médias. |
| Auditoria de afirmação pública | **Não encontrei no projeto.** |
| Educação científica — página ou vídeo | **Implementada.** Há uma secção dentro de app.py com a explicação implementada |
| Interface acessível | **Parcial.** O Streamlit tem contraste ajustado e a linha premiada é indicada por cor e legenda, mas não encontrei uma verificação documentada de uso por teclado/acessibilidade. |
| Validação automatizada | **Implementada.** Há 13 verificações em [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:461), com resultados registrados em [extra_testes_automatizados.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_testes_automatizados.csv). Elas rodam ao executar `python maquina_estatistica.py` ([chamada no fluxo principal](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:554)); o README descreve esse procedimento. |
| Análise de sensibilidade | **Cálculo implementado; interpretação escrita pendente.** Há seis cenários em [maquina_estatistica.py](/D:/PROJETOS/maquina_estatistica/maquina_estatistica.py:432) e [extra_analise_sensibilidade.csv](/D:/PROJETOS/maquina_estatistica/resultados/extra_analise_sensibilidade.csv). |


