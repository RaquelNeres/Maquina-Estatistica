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
    .stApp { background: linear-gradient(145deg, #f5f7fb 0%, #eef3f8 100%); }
    [data-testid="stMetric"] { background: white; padding: 18px 20px; border-radius: 16px; border: 1px solid #e3eaf2; }
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

aba_jogo, aba_simulacao, aba_estudos = st.tabs(["🎮 Jogar", "📊 Simulação", "📚 Experimentos"])

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
