# Máquina Estatística — IFES

Simulador acadêmico para o Trabalho I de Probabilidade e Estatística I.

> **Simulador acadêmico — somente créditos fictícios.**

## Requisitos
- Python 3.10 ou superior recomendado
- `numpy`, `pandas`, `streamlit` e `matplotlib`

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como executar
Na pasta que contém `maquina_estatistica.py`, execute:
```bash
python maquina_estatistica.py
```
O programa cria/atualiza a pasta `resultados/`, com tabelas CSV, gráficos PNG e metadados do ambiente.

<br>

## Interface visual
Para abrir o simulador interativo no navegador:
```bash
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

As páginas **Jogar**, **Simulação**, **Experimentos** e **Entenda a máquina** permitem brincar com a máquina, ajustar sementes e número de rodadas, visualizar gráficos e baixar resultados em CSV. A página educativa explica o modelo e os resultados E1–E5 em linguagem acessível, com fontes verificáveis. Em **Jogar**, os retratos representam os símbolos A–E; a tabela mostra os pagamentos e a legenda associa cada professor à sua letra. A música de `assets/audio/fortune_tiger_theme.m4a` toca em loop e pode ser ligada ou desligada pelo ícone ao lado do título. O efeito sonoro da roleta toca ao girar. Se o navegador bloquear a reprodução automática, clique no ícone para ativar a música. Use Tab e Enter ou Espaço para operar os controles. O painel de verificação acessível permite registrar a checagem de foco, operação por teclado, contraste e informação textual. A página de experimentos lê as tabelas já geradas em `resultados/`; rode `python maquina_estatistica.py` para atualizá-las.

## Conteúdo implementado
- Máquina de três rolos e avaliação exclusiva da linha central.
- Experimentos obrigatórios E1–E5, com sementes especificadas no enunciado.
- CSVs, gráficos e metadados para reprodução.
- Página educativa para público não especializado, com resultados próprios e fontes verificáveis.
- Interface de jogo com retratos dos professores: A = Giraldeli, B = Calhau, C = Graziela, D = Rapchan, E = Fidelis.
- Controles de teclado, foco visível, texto com contraste e verificação de uso por checklist.
- Extras: intervalo aproximado de 95% para a média do lucro, comparação de distribuições com mesmo RTP, limites de exposição, análise de sensibilidade e testes automatizados.

## Observações para o relatório
- O intervalo de confiança é uma aproximação normal para a média amostral, não um intervalo para resultados individuais.
- As simulações são didáticas e não estimam prevalência de transtornos ou perdas da população brasileira.
- Os resultados observados podem diferir dos valores teóricos por variabilidade aleatória.
- Antes da entrega, confira as tabelas e gráficos, redija as interpretações com suas próprias palavras e verifique as exigências completas do enunciado.

## Ferramentas e declaração de uso de IA

O layout visual foi elaborado no **Excalidraw**. Ferramentas de IA foram usadas como apoio à implementação do código e da interface, e para revisar o projeto com base na lista de requisitos obrigatórios e extras do enunciado. O **NotebookLM** foi usado para pesquisar materiais e esclarecer dúvidas pontuais que surgiram durante o desenvolvimento.

![alt text](image-1.png)

![alt text](image.png)

![alt text](image-2.png)