import tkinter as tk
from tkinter import Listbox, messagebox, simpledialog
from datetime import datetime
from openpyxl import Workbook
import os

# =====================================================
# DADOS
# =====================================================

maquinas = ["Centro Usinagem 01", "Centro Usinagem 02", "Torno CNC 01"]
operadores = ["Joao", "Maria", "Carlos"]

maquina_selecionada = None
operador_selecionado = None

apontamentos_ativos = []

# =====================================================
# FUNÇÕES DE APOIO
# =====================================================

def atualizar_listas():
    list_maquinas.delete(0, tk.END)
    list_operadores.delete(0, tk.END)

    for m in maquinas:
        list_maquinas.insert(tk.END, m)

    for o in operadores:
        list_operadores.insert(tk.END, o)


def atualizar_apontamentos():
    list_apontamentos.delete(0, tk.END)
    agora = datetime.now()#RELOGIO AO VIVO

    for ap in apontamentos_ativos:
        duracao = agora - ap["inicio"]
        texto = f"{ap['operador']} | {ap['maquina']} | {str(duracao).split('.')[0]}"
        list_apontamentos.insert(tk.END, texto)


# =====================================================
# SELEÇÕES
# =====================================================

def selecionar_maquina():
    global maquina_selecionada
    try:
        maquina_selecionada = list_maquinas.get(list_maquinas.curselection())
        lbl_maquina.config(text=maquina_selecionada)

#DESMARCA A LISTA
        Listbox.selection_clear(0, tk.END)

    except:
        pass


def selecionar_operador():
    global operador_selecionado
    try:
        operador_selecionado = list_operadores.get(list_operadores.curselection())
        lbl_operador.config(text=operador_selecionado)

        list_operadores.selection_clear(0, tk.END)

    except:
        pass


# =====================================================
# CRUD SIMPLES
# =====================================================

def adicionar_maquina():
    nome = simpledialog.askstring("Nova Máquina", "Nome da máquina:")
    if nome:
        maquinas.append(nome)
        atualizar_listas()


def excluir_maquina():
    try:
        maquinas.remove(list_maquinas.get(list_maquinas.curselection()))
        atualizar_listas()
    except:
        messagebox.showwarning("Aviso", "Selecione uma máquina")


def adicionar_operador():
    nome = simpledialog.askstring("Novo Operador", "Nome do operador:")
    if nome:
        operadores.append(nome)
        atualizar_listas()


def excluir_operador():
    try:
        operadores.remove(list_operadores.get(list_operadores.curselection()))
        atualizar_listas()
    except:
        messagebox.showwarning("Aviso", "Selecione um operador")


# =====================================================
# APONTAMENTO
# =====================================================

def iniciar_apontamento():
    if not maquina_selecionada or not operador_selecionado:
        messagebox.showwarning("Atenção", "Selecione máquina e operador")
        return

    projeto = simpledialog.askstring("Projeto", "Código do projeto:")
    if not projeto:
        return

    apontamentos_ativos.append({
        "operador": operador_selecionado,
        "maquina": maquina_selecionada,
        "projeto": projeto,
        "inicio": datetime.now()
    })

    atualizar_apontamentos()


def finalizar_apontamento():
    if not list_apontamentos.curselection():
        messagebox.showwarning("Aviso", "Selecione um apontamento")
        return

    ap = apontamentos_ativos.pop(list_apontamentos.curselection()[0])
    salvar_excel(ap)
    atualizar_apontamentos()


def salvar_excel(ap):
    pasta = "exportacoes"
    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, "apontamentos.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["Operador", "Máquina", "Projeto", "Início", "Fim", "Duração"])

    fim = datetime.now()
    duracao = fim - ap["inicio"]

    ws.append([
        ap["operador"],
        ap["maquina"],
        ap["projeto"],
        ap["inicio"].strftime("%Y-%m-%d %H:%M:%S"),
        fim.strftime("%Y-%m-%d %H:%M:%S"),
        str(duracao).split(".")[0]
    ])

    wb.save(caminho)

# =====================================================
# INTERFACE
# =====================================================

root = tk.Tk()
root.title("Sistema de Apontamento")
root.geometry("500x500")

frame_esq = tk.Frame(root)
frame_esq.pack(side="left", padx=50)

frame_dir = tk.Frame(root)
frame_dir.pack(side="right", expand=True, fill="both")

# ---- MAQUINAS ----
tk.Label(frame_esq, text="Lista de Máquinas").pack()
list_maquinas = tk.Listbox(frame_esq, height=3, exportselection=False)
list_maquinas.pack()
list_maquinas.bind("<<ListboxSelect>>", lambda e: selecionar_maquina())

tk.Button(frame_esq, text="Adicionar Máquina", command=adicionar_maquina).pack(fill="x")
tk.Button(frame_esq, text="Excluir Máquina", command=excluir_maquina).pack(fill="x")

# ---- OPERADORES ----
tk.Label(frame_esq, text="Lista de Operadores").pack(pady=(10,0))
list_operadores = tk.Listbox(frame_esq, height=6, exportselection=False)
list_operadores.pack()
list_operadores.bind("<<ListboxSelect>>", lambda e: selecionar_operador())

tk.Button(frame_esq, text="Adicionar Operador", command=adicionar_operador).pack(fill="x")
tk.Button(frame_esq, text="Excluir Operador", command=excluir_operador).pack(fill="x")

# ---- SELEÇÃO ----
tk.Label(frame_dir, text="Máquina Selecionada").pack()
lbl_maquina = tk.Label(frame_dir, relief="sunken", width=50)
lbl_maquina.pack()

tk.Label(frame_dir, text="Operador Selecionado").pack(pady=(10,0))
lbl_operador = tk.Label(frame_dir, relief="sunken", width=50)
lbl_operador.pack()

tk.Button(frame_dir, text="Iniciar Apontamento", command=iniciar_apontamento).pack(pady=10)
tk.Button(frame_dir, text="Finalizar Apontamento", command=finalizar_apontamento).pack()

tk.Label(frame_dir, text="Apontamentos Ativos").pack(pady=(20,0))
list_apontamentos = tk.Listbox(frame_dir, width=70, height=8)
list_apontamentos.pack()

# ---- START ----
atualizar_listas()

def loop():
    atualizar_apontamentos()
    root.after(1000, loop)

loop()
root.mainloop()
