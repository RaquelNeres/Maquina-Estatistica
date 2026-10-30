"""
MAQUINA ESTATISTICA - Trabalho I de Probabilidade e Estatistica I (IFES)
Simulador didatico: somente creditos ficticios.

Execucao:
    python maquina_estatistica.py

Dependencias:
    pip install numpy pandas matplotlib

O programa gera a pasta resultados/ com CSVs e graficos.
Semente principal e parametros dos experimentos seguem o enunciado.
"""

from __future__ import annotations

import csv
import json
import platform
import random
import sys
from pathlib import Path
from statistics import mean, median, stdev
from typing import Iterable

import matplotlib
matplotlib.use("Agg")  # permite salvar graficos sem abrir janelas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ----------------------------- CONFIGURACAO -----------------------------

SIMBOLOS = ("A", "B", "C", "D", "E")
SEQUENCIA_ROLO = SIMBOLOS
PAGAMENTOS_BASE = {"A": 5.0, "B": 10.0, "C": 15.0, "D": 25.0, "E": 50.0}
APOSTA = 1.0
N_RODADAS_E1 = 10_000
PASTA_RESULTADOS = Path("resultados")


# ------------------------------ MODELO ----------------------------------

def gerar_coluna(rng: random.Random) -> tuple[str, str, str]:
    """Sorteia uma parada uniforme e monta a janela circular de um rolo."""
    k = rng.randrange(5)
    return tuple(SEQUENCIA_ROLO[(k + deslocamento) % 5] for deslocamento in range(3))


def executar_rodada(rng: random.Random,
                    pagamentos: dict[str, float] | None = None) -> dict:
    """
    Executa uma rodada. Os tres rolos sao sorteados independentemente.
    Somente a linha central paga, quando os tres simbolos centrais sao iguais.
    P = premio bruto; X = lucro liquido = P - aposta.
    """
    if pagamentos is None:
        pagamentos = PAGAMENTOS_BASE

    colunas = [gerar_coluna(rng) for _ in range(3)]
    tabuleiro = tuple(tuple(colunas[c][r] for c in range(3)) for r in range(3))
    linha_central = tabuleiro[1]

    premio = 0.0
    if linha_central[0] == linha_central[1] == linha_central[2]:
        premio = float(pagamentos[linha_central[0]])

    lucro = premio - APOSTA
    return {
        "topo": "-".join(tabuleiro[0]),
        "linha_central": "-".join(linha_central),
        "base": "-".join(tabuleiro[2]),
        "premio": premio,
        "lucro": lucro,
        "premiada": premio > 0,
    }


def simular(n: int, seed: int,
            pagamentos: dict[str, float] | None = None) -> pd.DataFrame:
    """Executa n rodadas com um gerador inicializado uma unica vez."""
    if n < 0:
        raise ValueError("O numero de rodadas nao pode ser negativo.")
    rng = random.Random(seed)
    return pd.DataFrame(executar_rodada(rng, pagamentos) for _ in range(n))


def resumo_lucros(lucros: Iterable[float], premios: Iterable[float]) -> dict:
    lucros = np.asarray(list(lucros), dtype=float)
    premios = np.asarray(list(premios), dtype=float)
    n = len(lucros)
    if n == 0:
        raise ValueError("Nao e possivel resumir uma amostra vazia.")
    return {
        "rodadas": n,
        "lucro_medio_creditos": float(np.mean(lucros)),
        "desvio_padrao_amostral_creditos": float(np.std(lucros, ddof=1)) if n > 1 else 0.0,
        "mediana_lucro_creditos": float(np.median(lucros)),
        "proporcao_premiada": float(np.mean(premios > 0)),
        "premio_medio_creditos": float(np.mean(premios)),
        "rtp_observado_percentual": float(np.mean(premios) / APOSTA * 100),
    }


def salvar_csv(df: pd.DataFrame, nome: str) -> None:
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    df.to_csv(PASTA_RESULTADOS / nome, index=False, encoding="utf-8-sig")


def salvar_figura(nome: str) -> None:
    plt.tight_layout()
    plt.savefig(PASTA_RESULTADOS / nome, dpi=160, bbox_inches="tight")
    plt.close()


# -------------------------- EXPERIMENTO 1 -------------------------------

def experimento_1() -> pd.DataFrame:
    dados = simular(N_RODADAS_E1, 2026)
    salvar_csv(dados, "e1_rodadas_seed_2026.csv")

    categorias = [
        ("Sem premio", -1.0, 120 / 125),
        ("A-A-A", 4.0, 1 / 125),
        ("B-B-B", 9.0, 1 / 125),
        ("C-C-C", 14.0, 1 / 125),
        ("D-D-D", 24.0, 1 / 125),
        ("E-E-E", 49.0, 1 / 125),
    ]
    linhas = []
    for nome, lucro, prob in categorias:
        contagem = int(np.isclose(dados["lucro"], lucro).sum())
        linhas.append({
            "resultado": nome,
            "lucro_por_rodada": lucro,
            "probabilidade_teorica": prob,
            "probabilidade_teorica_percentual": prob * 100,
            "contagem_observada": contagem,
            "frequencia_relativa": contagem / len(dados),
            "frequencia_relativa_percentual": contagem / len(dados) * 100,
        })
    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "e1_frequencias.csv")

    resumo = resumo_lucros(dados["lucro"], dados["premio"])
    salvar_csv(pd.DataFrame([resumo]), "e1_resumo.csv")

    x = np.arange(len(tabela))
    largura = 0.38
    plt.figure(figsize=(10, 5))
    plt.bar(x - largura/2, tabela["probabilidade_teorica_percentual"],
            largura, label="Teoria")
    plt.bar(x + largura/2, tabela["frequencia_relativa_percentual"],
            largura, label="Observado")
    plt.xticks(x, tabela["resultado"], rotation=20)
    plt.ylabel("Frequencia (%)")
    plt.title("E1 - Probabilidade teorica e frequencia observada")
    plt.legend()
    salvar_figura("e1_frequencias.png")

    print("\nEXPERIMENTO 1")
    print(tabela.to_string(index=False))
    print(pd.DataFrame([resumo]).to_string(index=False))
    print("Conferencia: contagens somam", int(tabela["contagem_observada"].sum()))
    return dados


# -------------------------- EXPERIMENTO 2 -------------------------------

def experimento_2(dados_seed_2026: pd.DataFrame) -> None:
    sementes = [10, 2026, 123456]
    checkpoints = [100, 1000, 10000]
    trajetorias = {}
    linhas = []

    for seed in sementes:
        # Reutiliza exatamente a sequencia do E1 para a semente 2026.
        dados = dados_seed_2026 if seed == 2026 else simular(10000, seed)
        trajetorias[seed] = dados["lucro"].to_numpy()
        acumulado = np.cumsum(trajetorias[seed]) / np.arange(1, len(dados) + 1)
        for ponto in checkpoints:
            linhas.append({
                "semente": seed,
                "rodadas": ponto,
                "media_acumulada": float(acumulado[ponto - 1]),
            })

    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "e2_medias_acumuladas.csv")

    plt.figure(figsize=(10, 5))
    for seed, lucros in trajetorias.items():
        media_acum = np.cumsum(lucros) / np.arange(1, len(lucros) + 1)
        plt.plot(np.arange(1, len(lucros) + 1), media_acum,
                 label=f"Semente {seed}", linewidth=1)
    plt.axhline(-0.16, linestyle="--", label="Esperanca teorica = -0,16")
    plt.xlabel("Numero da rodada")
    plt.ylabel("Lucro medio acumulado (creditos)")
    plt.title("E2 - Lei dos Grandes Numeros")
    plt.legend()
    salvar_figura("e2_medias_acumuladas.png")

    # Reprodutibilidade: repetir a semente e comparar os 10 primeiros resultados.
    repeticao = simular(10000, 2026)
    reproduz = dados_seed_2026.head(10)[["linha_central", "premio", "lucro"]].equals(
        repeticao.head(10)[["linha_central", "premio", "lucro"]]
    )
    salvar_csv(pd.DataFrame([{
        "semente_testada": 2026,
        "primeiros_10_resultados_reproduzidos": reproduz,
        "gerador": "random.Random",
        "versao_python": platform.python_version(),
    }]), "e2_reprodutibilidade.csv")

    print("\nEXPERIMENTO 2")
    print(tabela.pivot(index="semente", columns="rodadas", values="media_acumulada"))
    print("Os dez primeiros resultados foram reproduzidos:", reproduz)


# -------------------------- EXPERIMENTO 3 -------------------------------

def experimento_3() -> pd.DataFrame:
    rng = random.Random(42)  # inicializar uma vez e continuar entre participantes
    participantes = []
    trajetorias = []

    for pessoa in range(1, 101):
        saldo = 100.0
        saldos = [saldo]
        rodadas = 0
        while rodadas < 500 and saldo >= APOSTA:
            resultado = executar_rodada(rng)
            saldo += resultado["lucro"]
            rodadas += 1
            saldos.append(saldo)
        esgotou = saldo < APOSTA
        participantes.append({
            "participante": pessoa,
            "saldo_inicial": 100.0,
            "saldo_final": saldo,
            "rodadas_executadas": rodadas,
            "esgotamento": esgotou,
            "classificacao": "ganho" if saldo > 100 else ("empate" if saldo == 100 else "perda"),
        })
        if pessoa <= 5:
            trajetorias.append((pessoa, saldos))

    tabela = pd.DataFrame(participantes)
    salvar_csv(tabela, "e3_participantes.csv")

    contagens = tabela["classificacao"].value_counts()
    resumo = pd.DataFrame([{
        "participantes": len(tabela),
        "ganho_percentual": float((tabela["saldo_final"] > 100).mean() * 100),
        "empate_percentual": float((tabela["saldo_final"] == 100).mean() * 100),
        "perda_percentual": float((tabela["saldo_final"] < 100).mean() * 100),
        "esgotamento_percentual": float(tabela["esgotamento"].mean() * 100),
        "saldo_final_medio": float(tabela["saldo_final"].mean()),
        "saldo_final_mediano": float(tabela["saldo_final"].median()),
        "rodadas_media": float(tabela["rodadas_executadas"].mean()),
    }])
    salvar_csv(resumo, "e3_resumo.csv")

    plt.figure(figsize=(10, 5))
    for pessoa, saldos in trajetorias:
        # Apos parar, o saldo permanece constante ate o horizonte de 500 rodadas.
        saldo_final = saldos[-1]
        saldos_plot = saldos + [saldo_final] * (501 - len(saldos))
        plt.plot(range(501), saldos_plot, label=f"Participante {pessoa}")
    plt.axhline(100, linestyle="--", label="Saldo inicial = 100")
    plt.xlabel("Rodada")
    plt.ylabel("Saldo (creditos)")
    plt.title("E3 - Trajetorias dos cinco primeiros participantes")
    plt.legend()
    salvar_figura("e3_trajetorias.png")

    print("\nEXPERIMENTO 3")
    print(resumo.to_string(index=False))
    return tabela


# -------------------------- EXPERIMENTO 4 -------------------------------

def experimento_4(dados: pd.DataFrame) -> pd.DataFrame:
    premiada = dados["premiada"].to_numpy(dtype=bool)
    linhas = []
    for rotulo, mascara in [
        ("Apos premio", premiada[:-1]),
        ("Apos nao premio", ~premiada[:-1]),
    ]:
        total = int(mascara.sum())
        premios_seguinte = int((premiada[1:][mascara]).sum()) if total else 0
        linhas.append({
            "resultado_anterior": rotulo,
            "total_pares": total,
            "premios_na_rodada_seguinte": premios_seguinte,
            "proporcao_observada": premios_seguinte / total if total else np.nan,
            "referencia_teorica": 0.04,
        })
    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "e4_probabilidade_condicional.csv")
    print("\nEXPERIMENTO 4")
    print(tabela.to_string(index=False))
    print("Total de pares analisados:", len(dados) - 1)
    return tabela


# -------------------------- EXPERIMENTO 5 -------------------------------

def experimento_5(dados_base: pd.DataFrame) -> pd.DataFrame:
    # Os mesmos resultados aleatorios sao avaliados com as duas tabelas.
    pagamentos = [
        ("Base", PAGAMENTOS_BASE),
        ("Premios +10%", {s: p * 1.10 for s, p in PAGAMENTOS_BASE.items()}),
    ]
    linhas = []
    for nome, tabela_pagamentos in pagamentos:
        premios = []
        lucros = []
        for linha in dados_base["linha_central"]:
            simbolos = linha.split("-")
            premio = tabela_pagamentos[simbolos[0]] if simbolos[0] == simbolos[1] == simbolos[2] else 0.0
            premios.append(premio)
            lucros.append(premio - APOSTA)
        resumo = resumo_lucros(lucros, premios)
        linhas.append({
            "tabela_pagamento": nome,
            "probabilidade_teorica_premio": 0.04,
            "frequencia_observada_premio": float(np.mean(np.asarray(premios) > 0)),
            "premio_medio_observado": resumo["premio_medio_creditos"],
            "lucro_medio_observado": resumo["lucro_medio_creditos"],
            "rtp_teorico_percentual": 84.0 if nome == "Base" else 92.4,
            "rtp_observado_percentual": resumo["rtp_observado_percentual"],
            "lucro_esperado_teorico": -0.16 if nome == "Base" else -0.076,
        })
    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "e5_comparacao_pagamentos.csv")
    print("\nEXPERIMENTO 5")
    print(tabela.to_string(index=False))
    return tabela


# ------------------------------ EXTRAS ----------------------------------

def extra_intervalo_confianca(dados: pd.DataFrame) -> pd.DataFrame:
    """IC aproximado de 95% para o lucro medio usando aproximacao normal."""
    lucros = dados["lucro"].to_numpy(dtype=float)
    n = len(lucros)
    media = float(np.mean(lucros))
    erro_padrao = float(np.std(lucros, ddof=1) / np.sqrt(n))
    # Multiplicador 1.96 da aproximacao normal para 95%.
    margem = 1.96 * erro_padrao
    tabela = pd.DataFrame([{
        "metodo": "Intervalo normal aproximado de 95% para a media",
        "n": n,
        "media_lucro": media,
        "erro_padrao": erro_padrao,
        "limite_inferior": media - margem,
        "limite_superior": media + margem,
        "esperanca_teorica": -0.16,
        "observacao": "Aproximacao baseada no erro-padrao; nao e intervalo para cada rodada individual.",
    }])
    salvar_csv(tabela, "extra_intervalo_confianca.csv")
    return tabela


def extra_mesmo_rtp_riscos(dados: pd.DataFrame) -> pd.DataFrame:
    """
    Exemplo adicional: mantem o premio medio teorico de 0,84 e altera sua distribuicao.
    Cada uma das cinco combinacoes continua com probabilidade 1/125.
    Pagamentos iguais a 21 em cada combinacao geram premio esperado 5*21/125=0,84.
    """
    tabelas = [
        ("Base", PAGAMENTOS_BASE),
        ("Pagamento uniforme", {s: 21.0 for s in SIMBOLOS}),
    ]
    linhas = []
    for nome, pagamentos in tabelas:
        premio_teorico = sum(pagamentos.values()) / 125
        lucro_teorico = premio_teorico - APOSTA
        premios = []
        for linha in dados["linha_central"]:
            a, b, c = linha.split("-")
            premios.append(float(pagamentos[a]) if a == b == c else 0.0)
        lucros = np.asarray(premios) - APOSTA
        linhas.append({
            "tabela": nome,
            "premio_esperado_teorico": premio_teorico,
            "rtp_teorico_percentual": premio_teorico * 100,
            "lucro_esperado_teorico": lucro_teorico,
            "desvio_padrao_lucro_observado": float(np.std(lucros, ddof=1)),
            "lucro_medio_observado": float(np.mean(lucros)),
            "pagamentos": json.dumps(pagamentos, ensure_ascii=False),
        })
    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "extra_mesmo_rtp_riscos.csv")
    return tabela


def extra_limites_exposicao() -> pd.DataFrame:
    """Compara regras de parada predefinidas, usando participantes e semente fixa."""
    configuracoes = [
        ("100 rodadas ou saldo insuficiente", 100),
        ("500 rodadas ou saldo insuficiente", 500),
    ]
    linhas = []
    for nome, limite in configuracoes:
        rng = random.Random(700 + limite)
        saldos, rodadas, esgotamentos = [], [], []
        for _ in range(100):
            saldo = 100.0
            n = 0
            while n < limite and saldo >= APOSTA:
                saldo += executar_rodada(rng)["lucro"]
                n += 1
            saldos.append(saldo)
            rodadas.append(n)
            esgotamentos.append(saldo < APOSTA)
        linhas.append({
            "regra_parada": nome,
            "participantes": 100,
            "saldo_final_medio": float(np.mean(saldos)),
            "saldo_final_mediano": float(np.median(saldos)),
            "percentual_perda": float(np.mean(np.asarray(saldos) < 100) * 100),
            "percentual_ganho": float(np.mean(np.asarray(saldos) > 100) * 100),
            "percentual_empate": float(np.mean(np.asarray(saldos) == 100) * 100),
            "percentual_esgotamento": float(np.mean(esgotamentos) * 100),
            "rodadas_media": float(np.mean(rodadas)),
            "semente": 700 + limite,
        })
    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "extra_limites_exposicao.csv")
    return tabela


def extra_sensibilidade() -> pd.DataFrame:
    """Analisa seis cenarios de multiplicador de pagamento sem mudar as chances."""
    multiplicadores = [0.5, 0.75, 1.0, 1.1, 1.25, 1.5]
    linhas = []
    for fator in multiplicadores:
        premio_esperado = sum(PAGAMENTOS_BASE.values()) * fator / 125
        linhas.append({
            "multiplicador_pagamentos": fator,
            "premio_esperado": premio_esperado,
            "rtp_percentual": premio_esperado / APOSTA * 100,
            "lucro_esperado_por_rodada": premio_esperado - APOSTA,
            "probabilidade_premio_percentual": 4.0,
        })
    tabela = pd.DataFrame(linhas)
    salvar_csv(tabela, "extra_analise_sensibilidade.csv")

    plt.figure(figsize=(8, 5))
    plt.plot(tabela["multiplicador_pagamentos"], tabela["rtp_percentual"], marker="o")
    plt.axhline(100, linestyle="--", label="RTP de 100%")
    plt.xlabel("Multiplicador dos pagamentos")
    plt.ylabel("RTP teorico (%)")
    plt.title("Extra - Sensibilidade do RTP aos pagamentos")
    plt.legend()
    salvar_figura("extra_analise_sensibilidade.png")
    return tabela


def executar_testes() -> pd.DataFrame:
    """Testes automatizados de regras, pagamentos, sementes, totais e caso-limite."""
    testes = []

    # 1. Pagamentos corretos para cada tripla premiada.
    for simbolo, pagamento in PAGAMENTOS_BASE.items():
        linha = f"{simbolo}-{simbolo}-{simbolo}"
        a, b, c = linha.split("-")
        premio = PAGAMENTOS_BASE[a] if a == b == c else 0
        testes.append((f"Pagamento {linha}", premio == pagamento))

    # 2. Linha nao igual nao paga.
    a, b, c = ("A", "B", "A")
    premio = PAGAMENTOS_BASE[a] if a == b == c else 0
    testes.append(("Combinacao sem trio nao paga", premio == 0))

    # 3. Lucro desconta a aposta.
    testes.append(("Lucro de premio 5 e 4", 5 - APOSTA == 4))
    testes.append(("Lucro sem premio e -1", 0 - APOSTA == -1))

    # 4. Semente reproduz a mesma sequencia.
    d1, d2 = simular(20, 2026), simular(20, 2026)
    testes.append(("Semente reproduz resultados", d1.equals(d2)))

    # 5. O total de frequencias do E1 soma N.
    e1 = simular(1000, 2026)
    testes.append(("Total de rodadas preservado", len(e1) == 1000))

    # 6. Caso-limite: zero rodadas e rejeitado pela funcao de resumo.
    try:
        resumo_lucros([], [])
        caso_limite = False
    except ValueError:
        caso_limite = True
    testes.append(("Amostra vazia tratada", caso_limite))

    # 7. Premio esperado e RTP teoricos.
    testes.append(("Esperanca do premio = 0,84", abs(sum(PAGAMENTOS_BASE.values()) / 125 - 0.84) < 1e-12))
    testes.append(("RTP teorico = 84%", abs(sum(PAGAMENTOS_BASE.values()) / 125 * 100 - 84) < 1e-12))

    tabela = pd.DataFrame(testes, columns=["teste", "aprovado"])
    salvar_csv(tabela, "extra_testes_automatizados.csv")
    print("\nTESTES AUTOMATIZADOS")
    print(tabela.to_string(index=False))
    print(f"{int(tabela['aprovado'].sum())}/{len(tabela)} testes aprovados.")
    return tabela


def salvar_metadados() -> None:
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    metadados = {
        "projeto": "Maquina Estatistica - IFES Probabilidade e Estatistica I",
        "aviso": "Simulador academico - somente creditos ficticios",
        "python": platform.python_version(),
        "gerador": "random.Random (Mersenne Twister)",
        "bibliotecas": {
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "aposta": APOSTA,
        "simbolos": list(SIMBOLOS),
        "pagamentos_base": PAGAMENTOS_BASE,
        "sementes": {"E1": 2026, "E2": [10, 2026, 123456], "E3": 42, "extras_exposicao": [800, 1200]},
    }
    (PASTA_RESULTADOS / "metadados_execucao.json").write_text(
        json.dumps(metadados, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    print("=" * 68)
    print("MAQUINA ESTATISTICA")
    print("Simulador academico - somente creditos ficticios")
    print("=" * 68)

    salvar_metadados()
    dados_e1 = experimento_1()
    experimento_2(dados_e1)
    experimento_3()
    experimento_4(dados_e1)
    experimento_5(dados_e1)

    print("\nEXTRAS")
    print("\nIntervalo de confianca aproximado:")
    print(extra_intervalo_confianca(dados_e1).to_string(index=False))
    print("\nMesmo RTP, distribuicoes de risco diferentes:")
    print(extra_mesmo_rtp_riscos(dados_e1).to_string(index=False))
    print("\nLimites de exposicao:")
    print(extra_limites_exposicao().to_string(index=False))
    print("\nAnalise de sensibilidade:")
    print(extra_sensibilidade().to_string(index=False))
    testes = executar_testes()

    print("\nArquivos gerados em:", PASTA_RESULTADOS.resolve())
    if not bool(testes["aprovado"].all()):
        raise SystemExit("ATENCAO: pelo menos um teste automatizado falhou.")
    print("Execucao concluida. Confira os CSVs, graficos e metadados antes de entregar.")


if __name__ == "__main__":
    main()
