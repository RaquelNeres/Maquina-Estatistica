"""Interface visual em Streamlit para a Máquina Estatística."""

from pathlib import Path
import base64
import html
import json
import random
import time

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import maquina_estatistica as modelo


st.set_page_config(
    page_title="Máquina Estatística | IFES",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
RESULTADOS = ROOT / "resultados"
ASSETS_PROFESSORES = ROOT / "assets" / "professores"
CAMPUS_IMAGE = ROOT / "assets" / "campus_serra.jpg"
IFES_LOGO = ROOT / "assets" / "logo_ifes.png"
AUDIO_JOGO = ROOT / "assets" / "audio" / "fortune_tiger_theme.m4a"
AUDIO_ROLETA = ROOT / "assets" / "audio" / "roleta_silvio.m4a"
DURACAO_GIRO = 5.0
DOCENTES = {
    "A": {"nome": "Giraldeli", "arquivo": "giraldeli.png"},
    "B": {"nome": "Calhau", "arquivo": "calhau.png"},
    "C": {"nome": "Graziela", "arquivo": "graziela.webp"},
    "D": {"nome": "Rapchan", "arquivo": "rapchan.png"},
    "E": {"nome": "Fidelis", "arquivo": "fidelis.png"},
}

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Jogar"
pagina_atual = st.session_state.pagina_atual
if "menu_direito_recolhido" not in st.session_state:
    st.session_state.menu_direito_recolhido = False
menu_direito_recolhido = st.session_state.menu_direito_recolhido
largura_menu_direito = 48 if menu_direito_recolhido else 220
largura_menu_direito_mobile = 48 if menu_direito_recolhido else 195
proporcao_menu_direito = 0.04 if menu_direito_recolhido else 0.17
logo_direito = max(0, (largura_menu_direito - 126) // 2)
logo_direito_mobile = max(0, (largura_menu_direito_mobile - 126) // 2)


@st.cache_data
def campus_fundo_data_uri() -> str:
    conteudo = base64.b64encode(CAMPUS_IMAGE.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{conteudo}"


@st.cache_data
def logo_ifes_data_uri() -> str:
    conteudo = base64.b64encode(IFES_LOGO.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{conteudo}"


@st.cache_data
def audio_jogo_data_uri() -> str:
    conteudo = base64.b64encode(AUDIO_JOGO.read_bytes()).decode("ascii")
    return f"data:audio/mp4;base64,{conteudo}"


@st.cache_data
def audio_roleta_data_uri() -> str:
    conteudo = base64.b64encode(AUDIO_ROLETA.read_bytes()).decode("ascii")
    return f"data:audio/mp4;base64,{conteudo}"


def animacao_roleta_html(resultado: dict) -> str:
    tabuleiro_final = tabuleiro_de_resultado(resultado)
    linhas_html = []
    for indice_linha, linha in enumerate(tabuleiro_final):
        celulas = []
        for simbolo in linha:
            docente = DOCENTES[simbolo]
            imagem = imagem_data_uri(docente["arquivo"])
            classe = "reel-cell payline" if indice_linha == 1 else "reel-cell"
            celulas.append(f'<div class="{classe}"><img alt=""></div>')
        linhas_html.append(f'<div class="slot-row">{"".join(celulas)}</div>')

    imagens = {simbolo: imagem_data_uri(docente["arquivo"]) for simbolo, docente in DOCENTES.items()}
    documento = """<!doctype html><html><head><meta charset="utf-8"><style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; overflow: hidden; background: transparent; }
body { display: grid; place-items: start center; }
.slot { position: relative; display: table; margin: 0 auto; padding: 22px; border-radius: 22px; background: #12243a; box-shadow: 0 12px 35px rgba(13,28,44,.28); }
.slot-row { display: flex; justify-content: center; gap: 14px; margin: 12px 0; }
.reel-cell { width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; padding: 6px; overflow: hidden; border-radius: 15px; background: white; }
.reel-cell img { width: 138px; height: 138px; object-fit: cover; object-position: center 28%; border-radius: 11px; background: white; }
.payline { border: 4px solid #f7c948; }
@media (max-width: 600px) { .slot { padding: 12px; } .reel-cell { width: 90px; height: 90px; } .reel-cell img { width: 82px; height: 82px; } .slot-row { gap: 8px; } }
</style></head><body><div class="slot" id="slot">__ROWS__</div>
<audio id="spin-audio" src="__AUDIO_SOURCE__" preload="auto"></audio>
<script>
const images = __IMAGES__;
const sequence = __SEQUENCE__;
const finalBoard = __FINAL_BOARD__;
const cells = Array.from(document.querySelectorAll('.reel-cell img'));
const audio = document.getElementById('spin-audio');
const durationMs = __DURATION__ * 1000;
audio.volume = 0.16;
function showBoard(board) {
    cells.forEach((cell, i) => { cell.src = images[board[Math.floor(i / 3)][i % 3]]; });
}
function randomBoard() {
    const board = Array.from({length: 3}, () => Array(3));
    for (let col = 0; col < 3; col++) {
        const start = Math.floor(Math.random() * sequence.length);
        for (let row = 0; row < 3; row++) board[row][col] = sequence[(start + row) % sequence.length];
    }
    return board;
}
function startSpin() {
    const startedAt = performance.now();
    let nextFrameAt = startedAt;
    function frame(now) {
        const elapsed = now - startedAt;
        if (elapsed >= durationMs) {
            showBoard(finalBoard);
            audio.pause();
            audio.currentTime = 0;
            return;
        }
        if (now >= nextFrameAt) {
            showBoard(randomBoard());
            nextFrameAt = now + 90;
        }
        requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
}
audio.play().then(startSpin).catch(startSpin);
</script></body></html>"""
    substituicoes = {
        "__ROWS__": "".join(linhas_html),
        "__AUDIO_SOURCE__": audio_roleta_data_uri(),
        "__IMAGES__": json.dumps(imagens),
        "__SEQUENCE__": json.dumps(list(modelo.SEQUENCIA_ROLO)),
        "__FINAL_BOARD__": json.dumps(tabuleiro_final),
        "__DURATION__": str(DURACAO_GIRO),
    }
    for marcador, valor in substituicoes.items():
        documento = documento.replace(marcador, valor)
    return documento


def cabecalho_jogo_html() -> str:
    html_cabecalho = """<!doctype html>
<html><head><meta charset="utf-8"><style>
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: transparent; overflow: hidden; }
    .heading { text-align: center; padding-top: 2px; }
    .title-row { display: flex; justify-content: center; align-items: center; gap: 14px; }
    h1 { margin: 0; color: #15263a; font: 600 clamp(2.4rem, 4.4vw, 3.5rem)/1.12 "Comic Sans MS", "Segoe Print", cursive; text-shadow: 0 1px 12px rgba(255,255,255,.8); }
    .sound { width: 46px; height: 46px; padding: 8px; display: grid; place-items: center; border: 0; border-radius: 50%; color: #583425; background: transparent; cursor: pointer; }
    .sound:hover { background: transparent; transform: scale(1.06); }
    .sound:focus-visible { outline: 3px solid #f08c00; outline-offset: 3px; }
    .sound svg { width: 28px; height: 28px; fill: currentColor; }
    .subtitle { margin: 3px 0 0; color: #f08c00; font: italic 600 1.25rem/1.35 "Comic Sans MS", "Segoe Print", cursive; text-shadow: 0 1px 8px rgba(255,255,255,.95); }
    @media (max-width: 700px) { h1 { font-size: 2rem; } .sound { width: 40px; height: 40px; } .subtitle { font-size: 1rem; } }
</style></head><body>
<div class="heading">
    <div class="title-row"><h1>🎰 Máquina Estatística</h1>
        <button class="sound" id="sound-toggle" type="button" aria-label="Ativando som" title="Ativando som"></button>
    </div>
    <p class="subtitle">Simulador acadêmico — somente créditos fictícios</p>
</div>
<audio id="game-audio" src="__AUDIO_SOURCE__" loop preload="auto" autoplay></audio>
<script>
    const audio = document.getElementById('game-audio');
    const button = document.getElementById('sound-toggle');
    const onIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a3.5 3.5 0 0 0-2-3.16v6.31a3.5 3.5 0 0 0 2-3.15zM14.5 3.23v2.06a7 7 0 0 1 0 13.42v2.06a9 9 0 0 0 0-17.54z"/></svg>';
    const offIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 4V5L7 9H3zm13.59 3 2.7 2.7-1.42 1.42-2.7-2.71-2.7 2.71-1.42-1.42 2.7-2.7-2.7-2.7 1.42-1.42 2.7 2.7 2.7-2.7 1.42 1.42-2.7 2.7z"/></svg>';
    function showState(playing) {
        button.innerHTML = playing ? onIcon : offIcon;
        button.setAttribute('aria-label', playing ? 'Desativar som' : 'Ativar som');
        button.title = playing ? 'Desativar som' : 'Ativar som';
    }
    audio.volume = 0.18;
    button.addEventListener('click', async () => {
        if (audio.paused) {
            try { await audio.play(); showState(true); } catch (_) { showState(false); }
        } else {
            audio.pause();
            showState(false);
        }
    });
    audio.addEventListener('play', () => showState(true));
    audio.addEventListener('pause', () => showState(false));
    audio.play().then(() => showState(true)).catch(() => showState(false));
</script></body></html>"""
    return html_cabecalho.replace("__AUDIO_SOURCE__", audio_jogo_data_uri())


background_css = ""
sidebar_css = ""
main_padding_css = "padding-top: 1.2rem;"
if pagina_atual == "Jogar":
    background_css = f"""
        background-image: linear-gradient(rgba(233, 241, 250, .24), rgba(16, 31, 47, .16)),
                          url('{campus_fundo_data_uri()}');
        background-size: cover;
        background-position: center 48%;
        background-attachment: fixed;
    """
    sidebar_css = ""
    main_padding_css = "padding-top: 1.7rem;"
else:
    sidebar_css = "display: none !important;"

st.markdown(
    f"""
    <style>
    :root {{ color-scheme: light; --primary-color: #a45c2f; }}
    .stApp {{ background-color: #eef2f7; background-image: none; color: #17263a; }}
    [data-testid="stAppViewContainer"] {{ {background_css} }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stMainBlockContainer"] {{ {main_padding_css} padding-bottom: 3rem; }}
    .stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"], .stApp [data-testid="stCaptionContainer"] {{ color: #17263a; }}
    section[data-testid="stSidebar"] {{ width: 250px !important; {sidebar_css} }}
    [data-testid="stSidebar"] > div:first-child {{ background: #583425; }}
    [data-testid="stSidebar"] * {{ color: #fff7ed !important; }}
    [data-testid="stSidebar"] input {{ color: #17263a !important; }}
    [data-testid="stSidebarContent"] {{ padding-top: 0 !important; }}
    [data-testid="stSidebarUserContent"] {{ padding-top: 0 !important; margin-top: -1.25rem; }}
    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] {{ gap: .5rem; }}
    [data-testid="stSidebar"] h2 {{ margin-top: 0; margin-bottom: .2rem; }}
    [data-testid="stSidebar"] h3 {{ margin-top: .25rem; margin-bottom: .2rem; }}
    [data-testid="stSidebar"] hr {{ margin: .35rem 0; }}
    [data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"] {{
        display: flex !important; visibility: visible !important; opacity: 1 !important;
        pointer-events: auto !important; z-index: 1101 !important;
    }}
    [data-testid="stMetric"] {{ background: white; color: #17263a; padding: 18px 20px; border-radius: 16px; border: 1px solid #d7e1ec; }}
    [data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: #17263a !important; }}
    [data-testid="stAlert"] {{ color: #17263a; }}
    [data-testid="stAlert"] p {{ color: inherit !important; }}
    [data-testid="stDataFrame"] {{ background: white; }}
    .prize-list {{ display: grid; gap: 7px; margin: 4px 0 8px; }}
    .prize-item {{ display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 8px; padding: 6px; border: 1px solid rgba(255,247,237,.22); border-radius: 12px; background: rgba(255,255,255,.07); }}
    .prize-description {{ color: #fff7ed; font-size: .78rem; font-weight: 600; margin: 4px 0 1px; }}
    .sidebar-note {{ color: rgba(255,247,237,.86); font-size: .72rem; line-height: 1.45; margin: 2px 0 6px; }}
    .chance-panel {{ padding: 12px; border: 1px solid rgba(255,247,237,.25); border-radius: 12px; background: rgba(255,255,255,.08); margin: 4px 0 8px; }}
    .chance-kicker {{ color: #f4a11a; font-size: .7rem; font-weight: 800; letter-spacing: .08em; margin-bottom: 4px; }}
    .chance-title {{ color: #fff7ed; font-size: 1rem; font-weight: 700; margin-bottom: 8px; }}
    .chance-summary {{ display: grid; gap: 6px; margin: 2px 0 0; }}
    .chance-row {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 7px 9px; border-radius: 9px; background: rgba(255,255,255,.08); font-size: .82rem; }}
    .chance-row strong {{ color: #f4a11a; white-space: nowrap; }}
    .st-key-session_rounds {{ margin-top: .65rem; margin-bottom: .15rem; }}
    .st-key-prizes_section {{ margin-top: 1.1rem; }}
    .prize-symbols {{ display: flex; align-items: center; gap: 4px; min-width: 0; }}
    .prize-symbols img {{ width: 36px; height: 36px; object-fit: cover; object-position: center 28%; border-radius: 8px; background: white; }}
    .prize-value {{ font-weight: 700; white-space: nowrap; color: #f4a11a; }}
    .balance-card {{ padding: 10px 14px; border-radius: 14px; background: #fff; color: #17263a !important; border: 1px solid #d7e1ec; margin: 2px 0 6px; }}
    .balance-label {{ color: #536579 !important; font-size: .82rem; }}
    .balance-value {{ color: #17263a !important; font-size: 1.8rem; line-height: 1.2; font-weight: 700; margin-top: 3px; }}
    .stButton button:focus-visible, [data-testid="stCheckbox"] input:focus-visible {{
        outline: 3px solid #8a4b00 !important; outline-offset: 3px !important;
        box-shadow: 0 0 0 2px #ffffff !important;
    }}
    .st-key-right_nav {{ position: fixed; z-index: 1000; top: 0; right: 0; bottom: 0; width: {largura_menu_direito}px; height: 100vh; min-height: 100vh; box-sizing: border-box; overflow-y: auto; background: #583425; border-radius: 0; padding: {"4rem .4rem 1rem" if menu_direito_recolhido else "5rem 1.1rem 2rem"}; }}
    .st-key-right_nav h3, .st-key-right_nav p {{ color: #fff7ed !important; }}
    .st-key-right_nav .stButton {{ display: flex; justify-content: center; }}
    .st-key-right_nav .stButton button {{ width: 90%; margin: 0 auto; color: #f4a11a; background: transparent; border: 1px solid rgba(255,255,255,.18); text-align: center; }}
    .st-key-right_nav .stButton button:hover {{ background: rgba(255,255,255,.12); border-color: #f4a11a; }}
    .st-key-right_nav .st-key-toggle_right_nav {{ position: absolute; z-index: 3; top: 2.4rem; right: .6rem; width: 36px; }}
    .st-key-right_nav .st-key-toggle_right_nav button {{ width: 36px; min-width: 36px; height: 36px; padding: 0; border: 0; background: transparent; color: #fff7ed; font-size: 1.35rem; }}
    .right-nav-settings-spacer {{ height: 1.15rem; }}
    .ifes-logo {{ position: fixed; z-index: 1002; right: {logo_direito}px; bottom: 1rem; width: 126px; padding: 0; background: transparent; border: 0; box-shadow: none; pointer-events: none; }}
    .ifes-logo img {{ display: block; width: 100%; height: auto; background: transparent; }}
    .st-key-game_machine {{ margin-top: -1.5rem; }}
    .st-key-game_panel {{ margin-top: 5rem; padding: 1.2rem 1.5rem; background: rgba(255,255,255,.95); border: 1px solid #d7e1ec; border-radius: 18px; box-shadow: 0 10px 35px rgba(15, 35, 55, .16); }}
    .slot {{ position: relative; background: #12243a; color: #f4f8ff; border-radius: 22px; padding: 22px; display: table; margin: 0 auto; box-shadow: 0 12px 35px rgba(13, 28, 44, .28); }}
    .round-payout {{ position: absolute; z-index: 5; left: 50%; top: 50%; transform: translate(-50%, -50%); padding: 0; background: transparent; border: 0; font-size: clamp(3rem, 7vw, 5rem); font-weight: 900; letter-spacing: .02em; animation: payout-pop 2.7s ease-out both; pointer-events: none; white-space: nowrap; }}
    .round-payout.negative {{ color: #ff3535; text-shadow: 0 2px 5px #fff, 0 0 16px rgba(120,0,0,.9); }}
    .round-payout.positive {{ color: #00db69; text-shadow: 0 2px 5px #fff, 0 0 16px rgba(0,80,30,.9); }}
    @keyframes payout-pop {{ 0% {{ opacity: 0; transform: translate(-50%, -50%) scale(.35) rotate(-8deg); }} 12% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.12) rotate(2deg); }} 22% {{ transform: translate(-50%, -50%) scale(1) rotate(0); }} 75% {{ opacity: 1; }} 100% {{ opacity: 0; transform: translate(-50%, -65%) scale(.9); }} }}
    .slot-row {{ display: flex; justify-content: center; gap: 14px; margin: 12px 0; }}
    .reel-cell {{ width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; border-radius: 15px; background: #ffffff; padding: 6px; overflow: hidden; }}
    .reel-cell img {{ width: 138px; height: 138px; object-fit: cover; object-position: center 28%; background: #ffffff; border-radius: 11px; }}
    .payline {{ border: 4px solid #f7c948; }}
    .controls-gap {{ height: 12px; }}
    @media (max-width: 900px) {{
        section[data-testid="stSidebar"] {{ width: 235px !important; }}
        .st-key-right_nav {{ width: {largura_menu_direito_mobile}px; padding: {"4rem .25rem 1rem" if menu_direito_recolhido else "4.5rem .7rem 1.5rem"}; }}
        .ifes-logo {{ right: {logo_direito_mobile}px; }}
        .slot {{ padding: 12px; }} .reel-cell {{ width: 90px; height: 90px; }}
        .reel-cell img {{ width: 82px; height: 82px; }} .slot-row {{ gap: 8px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def ler_resultado(nome: str) -> pd.DataFrame | None:
    caminho = RESULTADOS / nome
    if not caminho.exists():
        return None
    return pd.read_csv(caminho)


@st.cache_data
def imagem_data_uri(arquivo: str) -> str:
    caminho = ASSETS_PROFESSORES / arquivo
    mime = "image/webp" if caminho.suffix.lower() == ".webp" else "image/png"
    conteudo = base64.b64encode(caminho.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{conteudo}"


def nome_do_simbolo(simbolo: str, incluir_letra: bool = True) -> str:
    nome = DOCENTES[simbolo]["nome"]
    return f"{nome} ({simbolo})" if incluir_letra else nome


def nome_da_linha(linha: str, separador: str = " – ") -> str:
    return separador.join(nome_do_simbolo(simbolo, incluir_letra=False) for simbolo in linha.split("-"))


def categoria_visual(resultado: str) -> str:
    if resultado.lower().startswith("sem"):
        return "Sem prêmio"
    simbolo = resultado.split("-")[0]
    return f"{nome_do_simbolo(simbolo, incluir_letra=False)} × 3"


def mostrar_maquina(tabuleiro: list[list[str]], lucro: float | None = None) -> None:
    partes = ['<div class="slot">']
    for linha_idx, linha in enumerate(tabuleiro):
        celulas = []
        for simbolo in linha:
            docente = DOCENTES[simbolo]
            nome = html.escape(docente["nome"])
            letra = html.escape(simbolo)
            imagem = imagem_data_uri(docente["arquivo"])
            classe = "reel-cell payline" if linha_idx == 1 else "reel-cell"
            celulas.append(f'<div class="{classe}"><img src="{imagem}" alt="Retrato de {nome}, símbolo {letra}"></div>')
        partes.append(f'<div class="slot-row">{"".join(celulas)}</div>')
    if lucro is not None:
        classe = "positive" if lucro > 0 else "negative"
        sinal = "+" if lucro > 0 else ""
        partes.append(f'<div class="round-payout {classe}" role="status">{sinal}{lucro:.0f}</div>')
    partes.append('</div>')
    st.markdown("".join(partes), unsafe_allow_html=True)


def mostrar_frame(container, tabuleiro: list[list[str]], lucro: float | None = None) -> None:
    with container.container():
        mostrar_maquina(tabuleiro, lucro)


def tabuleiro_de_resultado(resultado: dict) -> list[list[str]]:
    return [
        resultado["topo"].split("-"),
        resultado["linha_central"].split("-"),
        resultado["base"].split("-"),
    ]


if "semente_jogo" not in st.session_state:
    st.session_state.semente_jogo = random.SystemRandom().randrange(0, 2_147_483_648)

with st.sidebar:
    if pagina_atual == "Jogar":
        st.header("Seu painel")
        if "saldo" not in st.session_state:
            st.session_state.saldo = 100
            st.session_state.ultima_rodada = None
            st.session_state.historico = []
        st.markdown(
            f'<div class="balance-card"><div class="balance-label">Créditos disponíveis</div>'
            f'<div class="balance-value">{st.session_state.saldo:.0f} créditos</div></div>',
            unsafe_allow_html=True,
        )
        with st.container(key="session_rounds"):
            st.caption(f"Rodadas nesta sessão: {len(st.session_state.historico)}")
        st.markdown(
            '<div class="sidebar-note">Somente a linha central paga.<br><br>'
            'Lucro líquido = prêmio − aposta.</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        with st.container(key="prizes_section"):
            st.markdown("### Combinações premiadas")
            itens_premio = []
            for simbolo, premio in modelo.PAGAMENTOS_BASE.items():
                docente = DOCENTES[simbolo]
                imagem = imagem_data_uri(docente["arquivo"])
                descricao = html.escape(f"Três retratos de {docente['nome']}")
                retratos = "".join(f'<img src="{imagem}" alt="{descricao}">' for _ in range(3))
                itens_premio.append(
                    f'<div class="prize-item"><div><div class="prize-symbols" role="img" aria-label="{descricao}">{retratos}</div>'
                    f'<div class="prize-description">{html.escape(docente["nome"])}</div></div>'
                    f'<span class="prize-value">{premio:.0f} cr.</span></div>'
                )
            st.markdown('<div class="prize-list">' + "".join(itens_premio) + '</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown(
            '<div class="chance-panel"><div class="chance-kicker">ANTES DE GIRAR</div>'
            '<div class="chance-title">Entenda as chances</div><div class="chance-summary">'
            '<div class="chance-row"><span>Chance de prêmio</span><strong>4%</strong></div>'
            '<div class="chance-row"><span>Chance sem prêmio</span><strong>96%</strong></div>'
            '<div class="chance-row"><span>RTP teórico</span><strong>84%</strong></div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        st.divider()
if st.session_state.get("semente_ativa") != int(st.session_state.semente_jogo):
    st.session_state.semente_ativa = int(st.session_state.semente_jogo)
    st.session_state.rng_jogo = random.Random(st.session_state.semente_ativa)

main_col, nav_col = st.columns([1, proporcao_menu_direito], gap="large")
with nav_col:
    with st.container(key="right_nav"):
        if st.button("»" if menu_direito_recolhido else "«", key="toggle_right_nav", help="Expandir navegação" if menu_direito_recolhido else "Minimizar navegação"):
            st.session_state.menu_direito_recolhido = not menu_direito_recolhido
            st.rerun()
        if not menu_direito_recolhido:
            st.markdown("### Páginas")
            for nome, rotulo in [
                ("Jogar", "🎮  Jogar"),
                ("Simulação", "📊  Simulação"),
                ("Experimentos", "📚  Experimentos"),
                ("Entenda a máquina", "🌱  Entenda a máquina"),
            ]:
                if st.button(rotulo, key=f"nav_{nome}", use_container_width=True):
                    st.session_state.pagina_atual = nome
                    st.rerun()
            st.markdown('<div class="right-nav-settings-spacer"></div>', unsafe_allow_html=True)
            st.number_input(
                "Semente do jogo",
                min_value=0,
                max_value=2_147_483_647,
                step=1,
                key="semente_jogo",
                help="A semente identifica a sequência pseudoaleatória desta sessão. Troque-a para iniciar outra sequência.",
            )
            st.caption("Teclado: use Tab para focar um botão e Enter ou Espaço para acioná-lo.")

if not menu_direito_recolhido:
    st.markdown(
        f'<div class="ifes-logo"><img src="{logo_ifes_data_uri()}" alt="Instituto Federal do Espírito Santo"></div>',
        unsafe_allow_html=True,
    )

with main_col:
    if pagina_atual == "Jogar":
        components.html(cabecalho_jogo_html(), height=110, scrolling=False)
        if "saldo" not in st.session_state:
            st.session_state.saldo = 100
            st.session_state.ultima_rodada = None
            st.session_state.historico = []

        lado_jogo = st.container(key="game_machine")
        with lado_jogo:
            if st.session_state.ultima_rodada is None:
                tabuleiro = [["A", "B", "C"], ["A", "B", "C"], ["C", "D", "E"]]
            else:
                tabuleiro = tabuleiro_de_resultado(st.session_state.ultima_rodada)
            margem_esquerda, coluna_maquina, margem_direita = st.columns([1, 2.4, 1], gap="small")
            with coluna_maquina:
                area_tabuleiro = st.empty()
                lucro_animacao = st.session_state.pop("animar_lucro", None)
                mostrar_frame(area_tabuleiro, tabuleiro, lucro_animacao)
            st.markdown('<div class="controls-gap"></div>', unsafe_allow_html=True)
            margem_botoes, coluna_botoes, margem_botoes_direita = st.columns([1, 2.2, 1], gap="small")
            with coluna_botoes:
                botao_col, reiniciar_col = st.columns(2, gap="small")
                with botao_col:
                    girar = st.button("Girar rolos", type="primary", use_container_width=True, disabled=st.session_state.saldo < 1, help="Execute uma rodada aleatória. Também pode ser acionado pelo teclado.")
                with reiniciar_col:
                    reiniciar = st.button("Reiniciar saldo", use_container_width=True)
            if reiniciar:
                st.session_state.saldo = 100
                st.session_state.ultima_rodada = None
                st.session_state.historico = []
                st.session_state.rng_jogo = random.Random(int(st.session_state.semente_jogo))
                st.rerun()
            if girar:
                status_giro = st.empty()
                resultado = modelo.executar_rodada(st.session_state.rng_jogo)
                with area_tabuleiro.container():
                    components.html(animacao_roleta_html(resultado), height=580, scrolling=False)
                time.sleep(DURACAO_GIRO + 0.25)
                mostrar_frame(area_tabuleiro, tabuleiro_de_resultado(resultado))
                status_giro.success("Giro concluído.")
                st.session_state.saldo += resultado["lucro"]
                st.session_state.ultima_rodada = resultado
                st.session_state.historico.append(resultado)
                valor_animado = resultado["premio"] if resultado["premiada"] else resultado["lucro"]
                st.session_state.animar_lucro = valor_animado
                st.rerun()

    elif pagina_atual == "Simulação":
        st.title("Simulação")
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

        dados["resultado_visual"] = dados.apply(
            lambda r: f"{DOCENTES[r['linha_central'][0]]['nome']} × 3" if r["premiada"] else "Sem prêmio",
            axis=1,
        )
        frequencias = dados["resultado_visual"].value_counts().rename_axis("Resultado").reset_index(name="Ocorrências")
        frequencias["Frequência (%)"] = frequencias["Ocorrências"] / len(dados) * 100
        frequencias = frequencias.sort_values("Resultado")
        dados_grafico = dados.assign(Rodada=range(1, len(dados) + 1))
        dados_grafico["Lucro médio acumulado"] = dados_grafico["lucro"].expanding().mean()
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("#### Frequência dos resultados")
            st.bar_chart(frequencias.set_index("Resultado")["Frequência (%)"], color="#3b82f6")
        with g2:
            st.markdown("#### Lucro médio acumulado")
            st.line_chart(dados_grafico.set_index("Rodada")["Lucro médio acumulado"], color="#13a38e")
        st.caption("A linha pontilhada de −0,16 crédito/rodada é a esperança teórica; amostras finitas oscilam em torno dela.")
        st.dataframe(frequencias, hide_index=True, use_container_width=True)
        dados_download = dados.copy()
        dados_download["professores_linha_central"] = dados_download["linha_central"].map(nome_da_linha)
        st.download_button("Baixar resultados desta simulação (CSV)", dados_download.to_csv(index=False).encode("utf-8-sig"), "simulacao.csv", "text/csv")

    elif pagina_atual == "Experimentos":
        st.title("Experimentos")
        st.subheader("Resultados dos experimentos E1–E5")
        st.write("Tabelas geradas pelo programa acadêmico e salvas na pasta `resultados`. Rode `python maquina_estatistica.py` uma vez para regenerá-las.")
        e1, e2 = st.columns(2)
        with e1:
            st.markdown("#### E1 · Distribuição dos resultados")
            frequencias_e1 = ler_resultado("e1_frequencias.csv")
            if frequencias_e1 is not None:
                frequencias_e1["resultado_visual"] = frequencias_e1["resultado"].map(categoria_visual)
                tabela_e1 = frequencias_e1[["resultado_visual", "probabilidade_teorica_percentual", "frequencia_relativa_percentual", "contagem_observada"]].rename(columns={
                    "resultado_visual": "Resultado",
                    "probabilidade_teorica_percentual": "Teórico (%)",
                    "frequencia_relativa_percentual": "Observado (%)",
                    "contagem_observada": "Ocorrências",
                })
                st.dataframe(tabela_e1, hide_index=True, use_container_width=True)
                st.bar_chart(tabela_e1.set_index("Resultado")[["Teórico (%)", "Observado (%)"]], color=["#94a3b8", "#3b82f6"])
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

    else:
        st.title("Entenda a máquina")
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
        st.caption("O gerador pseudoaleatório usa a semente da barra lateral, inicializada uma vez por sessão; no mesmo algoritmo e ambiente, ela permite repetir a sequência.")
        st.caption("Legenda: A = Giraldeli · B = Calhau · C = Graziela · D = Rapchan · E = Fidelis.")

        st.subheader("2. De onde vêm as probabilidades?")
        st.write(
            "Cada rolo pode mostrar qualquer um dos cinco símbolos no centro, com chance de 1/5. "
            "Como os três centros são independentes, há **5 × 5 × 5 = 125** trios centrais possíveis, "
            "todos com a mesma chance. Um trio específico, como Giraldeli–Giraldeli–Giraldeli, tem chance "
            "(1/5) × (1/5) × (1/5) = **1/125 = 0,8%**."
        )
        st.success("Há cinco trios premiados, um para cada professor. A chance de qualquer prêmio é 5/125 = 4%; a chance de não ganhar é 96%.")

        st.subheader("3. Prêmio bruto e lucro líquido")
        tabela_premios = pd.DataFrame([
            {
                "Professor": DOCENTES[s]["nome"],
                "Símbolo": s,
                "Trio premiado": f"{DOCENTES[s]['nome']} × 3",
                "Prêmio bruto (P)": p,
                "Lucro líquido (X = P − 1)": p - 1,
            }
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
                frequencias_e1["resultado_visual"] = frequencias_e1["resultado"].map(categoria_visual)
                st.bar_chart(
                    frequencias_e1.set_index("resultado_visual")[[
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
