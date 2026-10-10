import tkinter as tk
from tkinter import ttk, messagebox
import random

# Sequência circular dos rolos (posições 0 a 4)
ROLO = ['A', 'B', 'C', 'D', 'E']

# Tabela de pagamentos base
PAGAMENTOS = {
    ('A', 'A', 'A'): 5,
    ('B', 'B', 'B'): 10,
    ('C', 'C', 'C'): 15,
    ('D', 'D', 'D'): 25,
    ('E', 'E', 'E'): 50
}

saldo = 100

def girar_rodada():
    global saldo
    if saldo < 1:
        messagebox.showwarning("Aviso", "Saldo insuficiente para jogar!")
        return
    
    # Custo da aposta
    saldo -= 1
    
    # Sorteio uniforme de K em {0, 1, 2, 3, 4} para cada rolo
    k1 = random.randrange(5)
    k2 = random.randrange(5)
    k3 = random.randrange(5)
    
    # Montagem da janela 3x3: [Topo, Centro, Base]
    col1 = [ROLO[k1], ROLO[(k1 + 1) % 5], ROLO[(k1 + 2) % 5]]
    col2 = [ROLO[k2], ROLO[(k2 + 1) % 5], ROLO[(k2 + 2) % 5]]
    col3 = [ROLO[k3], ROLO[(k3 + 1) % 5], ROLO[(k3 + 2) % 5]]
    
    # Atualização da interface visual
    grade = [col1, col2, col3]
    for lin in range(3):
        for col in range(3):
            labels_grade[lin][col].config(text=grade[col][lin])
            
    # Avaliação apenas da linha central
    linha_central = (col1[1], col2[1], col3[1])
    premio = PAGAMENTOS.get(linha_central, 0)
    saldo += premio
    lucro = premio - 1
    
    # Atualização de rótulos de estado
    lbl_saldo.config(text=f"Saldo atual: {saldo} créditos")
    if premio > 0:
        lbl_resultado.config(text=f"Parabéns! Tripla {linha_central[0]}-{linha_central[1]}-{linha_central[2]} paga {premio} créditos (Lucro: +{lucro})", fg="green")
    else:
        lbl_resultado.config(text=f"Sem prémio na linha central ({linha_central[0]}-{linha_central[1]}-{linha_central[2]}). Lucro: {lucro}", fg="red")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Simulador Didático - Máquina Estatística")
janela.geometry("520x460")
janela.resizable(False, False)

# 1. AVISO OBRIGATÓRIO DO ENUNCIADO
lbl_aviso = tk.Label(
    janela, 
    text="Simulador acadêmico somente créditos fictícios", 
    font=("Arial", 11, "bold"), 
    fg="#B71C1C", 
    pady=10
)
lbl_aviso.pack()

# 2. GRELHA 3x3 DOS ROLOS
frame_rolete = tk.Frame(janela, bd=2, relief="groove", padx=15, pady=10)
frame_rolete.pack(pady=10)

labels_grade = []
for i in range(3):
    linha_labels = []
    for j in range(3):
        # Destaque com fundo diferente na linha central avaliada
        bg_cor = "#FFF9C4" if i == 1 else "#F5F5F5"
        lbl = tk.Label(
            frame_rolete, 
            text="-", 
            font=("Arial", 26, "bold"), 
            width=3, 
            height=1, 
            relief="solid", 
            bd=1, 
            bg=bg_cor
        )
        lbl.grid(row=i, column=j, padx=5, pady=5)
        linha_labels.append(lbl)
    labels_grade.append(linha_labels)

lbl_legenda = tk.Label(janela, text="* Linha central realçada a amarelo é a única avaliada", font=("Arial", 8, "italic"), fg="gray")
lbl_legenda.pack()

# 3. PAINEL DE CONTROLO E SALDO
lbl_saldo = tk.Label(janela, text=f"Saldo atual: {saldo} créditos", font=("Arial", 13, "bold"), pady=5)
lbl_saldo.pack()

btn_girar = tk.Button(janela, text="Girar Rolos (Aposta: 1)", font=("Arial", 12, "bold"), bg="#1976D2", fg="white", padx=15, pady=5, command=girar_rodada)
btn_girar.pack(pady=10)

lbl_resultado = tk.Label(janela, text="Clique em 'Girar Rolos' para iniciar", font=("Arial", 10), pady=5)
lbl_resultado.pack()

janela.mainloop()