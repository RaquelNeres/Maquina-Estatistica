# Máquina Estatística — IFES

Simulador acadêmico para o Trabalho I de Probabilidade e Estatística I.

> **Simulador acadêmico — somente créditos fictícios.**

## Requisitos
- Python 3.10 ou superior recomendado
- `numpy`, `pandas` e `matplotlib`

Instale as dependências:
```bash
pip install numpy pandas matplotlib
```

## Como executar
Na pasta que contém `maquina_estatistica.py`, execute:
```bash
python maquina_estatistica.py
```
O programa cria/atualiza a pasta `resultados/`, com tabelas CSV, gráficos PNG e metadados do ambiente.

## Interface visual
Para abrir o simulador interativo no navegador:
```bash
pip install -r requirements.txt
streamlit run app.py

# se der erro no Device Guard
python -m streamlit run app.py 
```
### Para o Ubuntu no WSL (caso o Windows continue com restrições do Device Guard)
Caso as políticas de segurança do Windows (Device Guard / WDAC) impeçam o carregamento de binários `.pyd` (como o NumPy), execute a aplicação via WSL:
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip

python3 -m venv .venv_linux
source .venv_linux/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

As abas **Jogar**, **Simulação**, **Experimentos** e **Entenda a máquina** permitem brincar com a máquina, ajustar sementes e número de rodadas, visualizar gráficos e baixar resultados em CSV. A página educativa explica o modelo e os resultados E1–E5 em linguagem acessível, com fontes verificáveis. A aba de experimentos lê as tabelas já geradas em `resultados/`; rode `python maquina_estatistica.py` para atualizá-las.

## Conteúdo implementado
- Máquina de três rolos e avaliação exclusiva da linha central.
- Experimentos obrigatórios E1–E5, com sementes especificadas no enunciado.
- CSVs, gráficos e metadados para reprodução.
- Página educativa para público não especializado, com resultados próprios e fontes verificáveis.
- Extras: intervalo aproximado de 95% para a média do lucro, comparação de distribuições com mesmo RTP, limites de exposição, análise de sensibilidade e testes automatizados.

## Observações para o relatório
- O intervalo de confiança é uma aproximação normal para a média amostral, não um intervalo para resultados individuais.
- As simulações são didáticas e não estimam prevalência de transtornos ou perdas da população brasileira.
- Os resultados observados podem diferir dos valores teóricos por variabilidade aleatória.
- Antes da entrega, confira as tabelas e gráficos, redija as interpretações com suas próprias palavras e verifique as exigências completas do enunciado.

## Declaração de uso de IA — sugestão para revisar
"Foi utilizada uma ferramenta de IA como apoio à estruturação inicial do código e à organização de análises. O grupo revisou, executou e conferiu os cálculos, os resultados e as interpretações, responsabilizando-se pelo conteúdo final."

A declaração deve ser ajustada ao uso real feito pelo grupo e às regras do professor.
