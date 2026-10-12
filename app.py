"""Interface visual em Streamlit para a Máquina Estatística."""

from pathlib import Path
import random

import pandas as pd
import streamlit as st

import maquina_estatistica as modelo


st.set_page_config(
    page_title="Máquina Estatística | IFES",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
RESULTADOS = ROOT / "resultados"

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --text-color: #17263a;
        --background-color: #f5f7fb;
        --secondary-background-color: #ffffff;
        --primary-color: #2463a5;
    }
    .stApp { background: linear-gradient(145deg, #f5f7fb 0%, #eef3f8 100%); color: #17263a; }
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"], .stApp [data-testid="stCaptionContainer"] {
        color: #17263a;
    }
    [data-testid="stSidebar"] { background: #e8eef5; }
    [data-testid="stMetric"] { background: white; color: #17263a; padding: 18px 20px; border-radius: 16px; border: 1px solid #d7e1ec; }
    [data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #17263a !important; }
    [data-testid="stAlert"] { color: #17263a; }
    [data-testid="stAlert"] p { color: inherit !important; }
    [data-baseweb="tab"] { color: #34465b; }
    [data-baseweb="tab"][aria-selected="true"] { color: #174f88; }
    [data-testid="stDataFrame"] { background: white; }
    .slot { background: #12243a; color: #f4f8ff; border-radius: 18px; padding: 20px; }
    .slot-row { display: flex; justify-content: center; gap: 12px; margin: 9px 0; }
    .symbol { width: 82px; height: 72px; display: grid; place-items: center; border-radius: 13px; background: #243d5c; font-size: 34px; font-weight: 800; }
    .payline { background: #f7c948; color: #17263a; }
    .caption { color: #d6e3f3; text-align: center; font-size: 13px; margin-top: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def ler_resultado(nome: str) -> pd.DataFrame | None:
    caminho = RESULTADOS / nome
    if not caminho.exists():
        return None
    return pd.read_csv(caminho)


def mostrar_maquina(tabuleiro: list[list[str]]) -> None:
    st.markdown('<div class="slot">', unsafe_allow_html=True)
    for linha_idx, linha in enumerate(tabuleiro):
        classe = "payline" if linha_idx == 1 else ""
        celulas = "".join(
            f'<div class="symbol {classe}">{simbolo}</div>' for simbolo in linha
        )
        st.markdown(f'<div class="slot-row">{celulas}</div>', unsafe_allow_html=True)
    st.markdown('<div class="caption">A linha dourada é a única que paga.</div></div>', unsafe_allow_html=True)


def tabuleiro_de_resultado(resultado: dict) -> list[list[str]]:
    return [
        resultado["topo"].split("-"),
        resultado["linha_central"].split("-"),
        resultado["base"].split("-"),
    ]


st.title("🎰 Máquina Estatística")
st.caption("Trabalho de Probabilidade e Estatística I · IFES")
st.warning("Simulador acadêmico — somente créditos fictícios.")

with st.sidebar:
    st.header("Navegação")
    st.write("Explore a máquina, rode simulações e consulte os experimentos do trabalho.")
    st.divider()
    st.caption("Aposta: 1 crédito · Chance de prêmio: 4% · RTP teórico: 84%")

aba_jogo, aba_simulacao, aba_estudos, aba_educativa = st.tabs([
    "🎮 Jogar", "📊 Simulação", "📚 Experimentos", "🌱 Entenda a máquina"
])

with aba_jogo:
    if "saldo" not in st.session_state:
        st.session_state.saldo = 100
        st.session_state.ultima_rodada = None
        st.session_state.historico = []

    lado_jogo, lado_info = st.columns([1.2, 1])
    with lado_jogo:
        st.subheader("Uma rodada de cada vez")
        if st.session_state.ultima_rodada is None:
            tabuleiro = [["A", "B", "C"], ["A", "B", "C"], ["C", "D", "E"]]
        else:
            tabuleiro = tabuleiro_de_resultado(st.session_state.ultima_rodada)
        mostrar_maquina(tabuleiro)
        botao_col, reiniciar_col = st.columns(2)
        with botao_col:
            girar = st.button("Girar rolos", type="primary", use_container_width=True, disabled=st.session_state.saldo < 1)
        with reiniciar_col:
            reiniciar = st.button("Reiniciar saldo", use_container_width=True)
        if reiniciar:
            st.session_state.saldo = 100
            st.session_state.ultima_rodada = None
            st.session_state.historico = []
            st.rerun()
        if girar:
            resultado = modelo.executar_rodada(random.Random())
            st.session_state.saldo += resultado["lucro"]
            st.session_state.ultima_rodada = resultado
            st.session_state.historico.append(resultado)
            st.rerun()

    with lado_info:
        st.subheader("Seu painel")
        st.metric("Saldo fictício", f"{st.session_state.saldo:.0f} créditos")
        atual = st.session_state.ultima_rodada
        if atual:
            if atual["premiada"]:
                st.success(f"Tripla {atual['linha_central']}! Prêmio de {atual['premio']:.0f} créditos · lucro líquido +{atual['lucro']:.0f}.")
            else:
                st.info(f"Sem prêmio nesta rodada · lucro líquido {atual['lucro']:.0f} crédito.")
        else:
            st.write("Clique em **Girar rolos** para começar.")
        st.markdown("**Pagamentos da linha central**")
        st.dataframe(pd.DataFrame([{"Tripla": f"{s}–{s}–{s}", "Prêmio": f"{p:.0f} créditos"} for s, p in modelo.PAGAMENTOS_BASE.items()]), hide_index=True, use_container_width=True)
        if st.session_state.historico:
            st.caption(f"Rodadas nesta sessão: {len(st.session_state.historico)}")

with aba_simulacao:
    st.subheader("Veja como os resultados se comportam")
    controles, explicacao = st.columns([1, 2])
    with controles:
        n = st.slider("Número de rodadas", min_value=100, max_value=50000, value=10000, step=100)
        seed = st.number_input("Semente aleatória", min_value=0, max_value=2_147_483_647, value=2026, step=1)
        executar = st.button("Executar simulação", type="primary")
    with explicacao:
        st.info("Cada rolo é sorteado de forma independente. Só há prêmio quando os três símbolos da linha central são iguais.")
    if executar or "dados_simulacao" not in st.session_state:
        st.session_state.dados_simulacao = modelo.simular(int(n), int(seed))
        st.session_state.param_simulacao = (int(n), int(seed))
    dados = st.session_state.dados_simulacao
    resumo = modelo.resumo_lucros(dados["lucro"], dados["premio"])
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rodadas", f"{resumo['rodadas']:,}".replace(",", "."))
    m2.metric("Prêmios observados", f"{resumo['proporcao_premiada'] * 100:.2f}%", "teórico: 4%")
    m3.metric("RTP observado", f"{resumo['rtp_observado_percentual']:.2f}%", "teórico: 84%")
    m4.metric("Lucro médio", f"{resumo['lucro_medio_creditos']:.3f} crédito/rodada", "teórico: −0,16")

    frequencias = dados["linha_central"].value_counts().rename_axis("Linha central").reset_index(name="Ocorrências")
    frequencias["Frequência (%)"] = frequencias["Ocorrências"] / len(dados) * 100
    frequencias = frequencias.sort_values("Linha central")
    dados_grafico = dados.assign(Rodada=range(1, len(dados) + 1))
    dados_grafico["Lucro médio acumulado"] = dados_grafico["lucro"].expanding().mean()
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("#### Frequência das linhas centrais")
        st.bar_chart(frequencias.set_index("Linha central")["Frequência (%)"], color="#3b82f6")
    with g2:
        st.markdown("#### Lucro médio acumulado")
        st.line_chart(dados_grafico.set_index("Rodada")["Lucro médio acumulado"], color="#13a38e")
    st.caption("A linha pontilhada de −0,16 crédito/rodada é a esperança teórica; amostras finitas oscilam em torno dela.")
    st.dataframe(frequencias, hide_index=True, use_container_width=True)
    st.download_button("Baixar resultados desta simulação (CSV)", dados.to_csv(index=False).encode("utf-8-sig"), "simulacao.csv", "text/csv")

with aba_estudos:
    st.subheader("Resultados dos experimentos E1–E5")
    st.write("Tabelas geradas pelo programa acadêmico e salvas na pasta `resultados`. Rode `python maquina_estatistica.py` uma vez para regenerá-las.")
    e1, e2 = st.columns(2)
    with e1:
        st.markdown("#### E1 · Distribuição dos resultados")
        frequencias_e1 = ler_resultado("e1_frequencias.csv")
        if frequencias_e1 is not None:
            colunas = [c for c in ["resultado", "probabilidade_teorica_percentual", "frequencia_relativa_percentual", "contagem_observada"] if c in frequencias_e1]
            st.dataframe(frequencias_e1[colunas], hide_index=True, use_container_width=True)
            st.bar_chart(frequencias_e1.set_index("resultado")[["probabilidade_teorica_percentual", "frequencia_relativa_percentual"]], color=["#94a3b8", "#3b82f6"])
        else:
            st.info("Ainda não há resultados E1. Execute o programa principal para gerar os arquivos.")
    with e2:
        st.markdown("#### E2 · Lei dos Grandes Números")
        media = ler_resultado("e2_medias_acumuladas.csv")
        if media is not None:
            st.line_chart(media.pivot(index="rodadas", columns="semente", values="media_acumulada"), color=["#f59e0b", "#3b82f6", "#13a38e"])
            st.dataframe(media, hide_index=True, use_container_width=True)
        else:
            st.info("Ainda não há resultados E2. Execute o programa principal para gerar os arquivos.")
    st.divider()
    colunas_estudos = st.columns(3)
    for coluna, (titulo, arquivo) in zip(colunas_estudos, [
        ("E3 · Saldo dos participantes", "e3_resumo.csv"),
        ("E4 · Probabilidade condicional", "e4_probabilidade_condicional.csv"),
        ("E5 · Comparação de pagamentos", "e5_comparacao_pagamentos.csv"),
    ]):
        with coluna:
            st.markdown(f"#### {titulo}")
            tabela = ler_resultado(arquivo)
            if tabela is not None:
                st.dataframe(tabela, hide_index=True, use_container_width=True)
            else:
                st.info("Execute o programa principal para gerar este experimento.")
    st.caption("Resultados são didáticos. Variabilidade amostral pode fazer os valores observados diferirem dos teóricos.")

with aba_educativa:
    st.title("Como funciona a Máquina Estatística?")
    st.write(
        "Este simulador transforma um jogo de rolos em um experimento de probabilidade. "
        "Abaixo explicamos as regras, as contas e o que encontramos nos nossos próprios dados, "
        "sem exigir conhecimento prévio de estatística."
    )
    st.warning("É um modelo acadêmico com créditos fictícios. Os resultados não são dinheiro real nem previsão do que acontecerá a uma pessoa.")

    st.subheader("1. O que acontece em um giro?")
    st.write(
        "Cada rolo usa a mesma sequência circular **A → B → C → D → E → A**. "
        "Ele sorteia uma posição inicial K entre 0 e 4. Essa letra aparece no topo; "
        "as duas seguintes aparecem no centro e na base. Por exemplo, se K = 3, "
        "a coluna fica **D / E / A**: depois de E, a sequência volta para A."
    )
    st.markdown(
        "**Apenas a fileira do meio conta.** Os três rolos são sorteados independentemente. "
        "Assim, o resultado de um rolo não altera a chance dos outros; já as três letras "
        "dentro de uma coluna são vizinhas da sequência e, portanto, não são sorteios independentes."
    )
    st.caption("O programa usa um gerador pseudoaleatório: uma semente fixa permite repetir a sequência no mesmo algoritmo e ambiente.")

    st.subheader("2. De onde vêm as probabilidades?")
    st.write(
        "Cada rolo pode mostrar qualquer uma das cinco letras no centro, com chance de 1/5. "
        "Como os três centros são independentes, há **5 × 5 × 5 = 125** trios centrais possíveis, "
        "todos com a mesma chance. Um trio específico, como A–A–A, tem chance "
        "(1/5) × (1/5) × (1/5) = **1/125 = 0,8%**."
    )
    st.success("Há cinco trios premiados (A–A–A até E–E–E). A chance de qualquer prêmio é 5/125 = 4%; a chance de não ganhar é 96%.")

    st.subheader("3. Prêmio bruto e lucro líquido")
    tabela_premios = pd.DataFrame([
        {"Centro": f"{s}–{s}–{s}", "Prêmio bruto (P)": p, "Lucro líquido (X = P − 1)": p - 1}
        for s, p in modelo.PAGAMENTOS_BASE.items()
    ])
    st.dataframe(tabela_premios, hide_index=True, use_container_width=True)
    st.markdown(
        "A aposta custa 1 crédito. **Prêmio bruto (P)** é o valor pago pelo trio; "
        "**lucro líquido (X)** desconta a aposta. Sem trio, P = 0 e X = −1. "
        "A média teórica do prêmio é (5 + 10 + 15 + 25 + 50) / 125 = **0,84 crédito**. "
        "Logo, o lucro líquido esperado é 0,84 − 1 = **−0,16 crédito por rodada**, e o retorno teórico (RTP) é 84%."
    )
    st.info("Esperança é uma média de longo prazo, não uma promessa para cada rodada ou para o saldo de uma pessoa. Uma rodada pode pagar muito, pouco ou nada.")

    st.subheader("4. O que observamos nos nossos experimentos?")
    dados_e1 = ler_resultado("e1_resumo.csv")
    frequencias_e1 = ler_resultado("e1_frequencias.csv")
    if dados_e1 is not None and not dados_e1.empty:
        r = dados_e1.iloc[0]
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Rodadas no E1", f"{int(r['rodadas']):,}".replace(",", "."))
        k2.metric("Prêmios observados", f"{r['proporcao_premiada'] * 100:.2f}%", "teórico: 4%")
        k3.metric("RTP observado", f"{r['rtp_observado_percentual']:.2f}%", "teórico: 84%")
        k4.metric("Lucro médio observado", f"{r['lucro_medio_creditos']:.4f}", "teórico: −0,16 por rodada")
        st.write(
            f"No E1, com {int(r['rodadas']):,} rodadas, a frequência de prêmios foi "
            f"**{r['proporcao_premiada'] * 100:.2f}%**, perto dos 4% previstos. "
            f"O lucro médio observado foi **{r['lucro_medio_creditos']:.4f} crédito por rodada**. "
            "A diferença para a média teórica é uma oscilação da amostra; não muda a probabilidade definida pelo modelo."
        )
        if frequencias_e1 is not None:
            st.markdown("**E1 — proporção teórica e observada por resultado**")
            st.bar_chart(
                frequencias_e1.set_index("resultado")[[
                    "probabilidade_teorica_percentual", "frequencia_relativa_percentual"
                ]],
                color=["#94a3b8", "#2463a5"],
            )
    else:
        st.info("Os arquivos de resultados ainda não foram gerados. Execute `python maquina_estatistica.py` para preencher esta página com os dados do projeto.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**E2 — médias em 10.000 rodadas**")
        e2 = ler_resultado("e2_medias_acumuladas.csv")
        if e2 is not None and not e2.empty:
            ultimos = e2[e2["rodadas"] == e2["rodadas"].max()][["semente", "media_acumulada"]]
            st.dataframe(ultimos.rename(columns={"semente": "Semente", "media_acumulada": "Lucro médio acumulado"}), hide_index=True, use_container_width=True)
            st.caption("As sementes produzem amostras diferentes; com mais rodadas, as médias tendem a se aproximar da esperança teórica.")
    with c2:
        st.markdown("**E3 — 100 participantes simulados**")
        e3 = ler_resultado("e3_resumo.csv")
        if e3 is not None and not e3.empty:
            r3 = e3.iloc[0]
            st.write(
                f"**{r3['perda_percentual']:.0f}%** terminaram com saldo menor que o inicial; "
                f"**{r3['ganho_percentual']:.0f}%** terminaram com mais e "
                f"**{r3['esgotamento_percentual']:.0f}%** ficaram sem crédito para continuar. "
                "É o resultado deste grupo simulado, com saldo inicial e limite de rodadas definidos no experimento."
            )

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**E4 — o giro anterior muda o próximo?**")
        e4 = ler_resultado("e4_probabilidade_condicional.csv")
        if e4 is not None and not e4.empty:
            st.dataframe(e4[["resultado_anterior", "proporcao_observada", "referencia_teorica"]].rename(columns={
                "resultado_anterior": "Resultado anterior",
                "proporcao_observada": "Prêmio observado no próximo giro",
                "referencia_teorica": "Referência teórica",
            }), hide_index=True, use_container_width=True)
            st.caption("No modelo, a rodada seguinte é sorteada de novo; um prêmio anterior não aumenta a chance do próximo.")
    with c4:
        st.markdown("**E5 — o que muda ao aumentar os pagamentos?**")
        e5 = ler_resultado("e5_comparacao_pagamentos.csv")
        if e5 is not None and not e5.empty:
            st.dataframe(e5[["tabela_pagamento", "rtp_teorico_percentual", "rtp_observado_percentual", "lucro_esperado_teorico"]].rename(columns={
                "tabela_pagamento": "Tabela de pagamento",
                "rtp_teorico_percentual": "RTP teórico (%)",
                "rtp_observado_percentual": "RTP observado (%)",
                "lucro_esperado_teorico": "Lucro esperado/rodada",
            }), hide_index=True, use_container_width=True)
            st.caption("O E5 reutiliza os mesmos giros e altera os pagamentos, isolando o efeito da tabela de prêmios.")

    st.subheader("5. Como interpretar — e quais são os limites")
    st.markdown(
        "A **lei dos grandes números** explica por que frequências e médias de muitas rodadas "
        "tendem a ficar mais próximas dos valores teóricos; ela não diz que isso ocorrerá em uma "
        "sessão curta. A simulação também não representa pessoas reais, não mede comportamento "
        "da população e não prevê resultados futuros. Saldo e perdas no E3 pertencem somente às "
        "regras e sementes escolhidas para este modelo."
    )
    st.subheader("Fontes para continuar estudando")
    st.markdown(
        "- [OpenStax — eventos independentes e regra do produto](https://openstax.org/books/statistics/pages/3-2-independent-and-mutually-exclusive-events)\n"
        "- [OpenStax — esperança matemática e desvio padrão](https://openstax.org/books/statistics/pages/4-2-mean-or-expected-value-and-standard-deviation)\n"
        "- [OpenStax — lei dos grandes números](https://openstax.org/books/statistics/pages/7-3-using-the-central-limit-theorem)\n"
        "- [Documentação oficial do Python — módulo `random` e reprodutibilidade](https://docs.python.org/3/library/random.html)\n"
        "- [NIST — intervalos de confiança para a média](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm)"
    )
