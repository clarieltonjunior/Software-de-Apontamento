import tkinter as tk
from tkinter import messagebox, simpledialog

# =====================================================
# 1️⃣ DADOS INICIAIS (LISTAS EM MEMÓRIA)
# =====================================================

MAQUINAS = [
    "Centro Usinagem 01",
    "Centro Usinagem 02",
    "Torno CNC 01",
    "Fresa Convencional"
]

OPERADORES = [
    "Joao",
    "Maria",
    "Carlos",
    "Ana"
]

# =====================================================
# 2️⃣ FUNÇÕES AUXILIARES
# =====================================================

def beep():
    root.bell()

def selecionar_da_lista(event, entry_destino, listbox):
    try:
        selecionado = listbox.get(listbox.curselection())
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, selecionado)
        beep()
    except:
        pass

def filtrar_lista(entry, lista_original, listbox):
    termo = entry.get().lower()
    listbox.delete(0, tk.END)
    for item in lista_original:
        if termo in item.lower():
            listbox.insert(tk.END, item)

# =====================================================
# 3️⃣ FUNÇÕES DE CADASTRO (MENU)
# =====================================================

def cadastrar_maquina():
    nome = simpledialog.askstring("Cadastrar Máquina", "Nome da máquina:")
    if nome:
        MAQUINAS.append(nome)
        lista_maquinas.insert(tk.END, nome)

def cadastrar_operador():
    nome = simpledialog.askstring("Cadastrar Operador", "Nome do operador:")
    if nome:
        OPERADORES.append(nome)
        lista_operadores.insert(tk.END, nome)

# =====================================================
# 4️⃣ FUNÇÕES PRINCIPAIS
# =====================================================

def iniciar_apontamento():
    maquina = entry_maquina.get()
    operador = entry_operador.get()

    if not maquina or not operador:
        messagebox.showwarning("Atenção", "Selecione uma máquina e um operador.")
        return

    messagebox.showinfo(
        "Apontamento Iniciado",
        f"Máquina: {maquina}\nOperador: {operador}"
    )

def fechar_apontamento():
    resposta = messagebox.askyesno(
        "Confirmar",
        "Deseja realmente fechar o apontamento?"
    )
    if resposta:
        entry_maquina.delete(0, tk.END)
        entry_operador.delete(0, tk.END)

# =====================================================
# 5️⃣ JANELA PRINCIPAL
# =====================================================

root = tk.Tk()
root.title("Sistema de Apontamento - Beta")
root.state("zoomed")

# =====================================================
# 6️⃣ MENU SUPERIOR
# =====================================================

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_cadastro = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Cadastro", menu=menu_cadastro)

menu_cadastro.add_command(label="Cadastrar Máquina", command=cadastrar_maquina)
menu_cadastro.add_command(label="Cadastrar Operador", command=cadastrar_operador)

# =====================================================
# 7️⃣ LAYOUT PRINCIPAL
# =====================================================

frame_principal = tk.Frame(root, padx=20, pady=20)
frame_principal.pack(fill="both", expand=True)

frame_listas = tk.Frame(frame_principal)
frame_listas.pack(side="left", fill="y", padx=20)

frame_selecao = tk.Frame(frame_principal)
frame_selecao.pack(side="right", fill="both", expand=True)

# =====================================================
# 8️⃣ LISTA DE MÁQUINAS
# =====================================================

tk.Label(frame_listas, text="Máquinas").pack()

pesquisa_maquina = tk.Entry(frame_listas)
pesquisa_maquina.pack(fill="x")

lista_maquinas = tk.Listbox(frame_listas, height=15)
scroll_maquinas = tk.Scrollbar(frame_listas)

lista_maquinas.pack(side="left", fill="y")
scroll_maquinas.pack(side="right", fill="y")

lista_maquinas.config(yscrollcommand=scroll_maquinas.set)
scroll_maquinas.config(command=lista_maquinas.yview)

for m in MAQUINAS:
    lista_maquinas.insert(tk.END, m)

pesquisa_maquina.bind(
    "<KeyRelease>",
    lambda e: filtrar_lista(pesquisa_maquina, MAQUINAS, lista_maquinas)
)

# =====================================================
# 9️⃣ LISTA DE OPERADORES
# =====================================================

tk.Label(frame_listas, text="Operadores").pack(pady=(20, 0))

pesquisa_operador = tk.Entry(frame_listas)
pesquisa_operador.pack(fill="x")

lista_operadores = tk.Listbox(frame_listas, height=15)
scroll_operadores = tk.Scrollbar(frame_listas)

lista_operadores.pack(side="left", fill="y")
scroll_operadores.pack(side="right", fill="y")

lista_operadores.config(yscrollcommand=scroll_operadores.set)
scroll_operadores.config(command=lista_operadores.yview)

for o in OPERADORES:
    lista_operadores.insert(tk.END, o)

pesquisa_operador.bind(
    "<KeyRelease>",
    lambda e: filtrar_lista(pesquisa_operador, OPERADORES, lista_operadores)
)

# =====================================================
# 🔟 CAMPOS DE SELEÇÃO
# =====================================================

tk.Label(frame_selecao, text="Máquina Selecionada").pack()
entry_maquina = tk.Entry(frame_selecao, font=("Arial", 14))
entry_maquina.pack(fill="x", pady=10)

tk.Label(frame_selecao, text="Operador Selecionado").pack()
entry_operador = tk.Entry(frame_selecao, font=("Arial", 14))
entry_operador.pack(fill="x", pady=10)

lista_maquinas.bind(
    "<<ListboxSelect>>",
    lambda e: selecionar_da_lista(e, entry_maquina, lista_maquinas)
)

lista_operadores.bind(
    "<<ListboxSelect>>",
    lambda e: selecionar_da_lista(e, entry_operador, lista_operadores)
)

# =====================================================
# 1️⃣1️⃣ BOTÕES
# =====================================================

tk.Button(
    frame_selecao,
    text="Iniciar Apontamento",
    height=2,
    command=iniciar_apontamento
).pack(fill="x", pady=20)

tk.Button(
    frame_selecao,
    text="Fechar Apontamento",
    height=2,
    command=fechar_apontamento
).pack(fill="x")

# =====================================================
# 1️⃣2️⃣ LOOP PRINCIPAL
# =====================================================

root.mainloop()
