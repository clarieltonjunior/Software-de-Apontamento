import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# =========================
# DADOS DO SISTEMA
# =========================

MAQUINAS = [
    "Fresa Okada",
    "Fresa AWEA",
    "Torno Fanuc",
    "Torno Fagor",
    "Torno Conv1",
    "Torno Conv2",
    "Fresa Conv",
    "Bancada"
]

OPERADORES = [
    "Joao",
    "Maria",
    "Carlos",
    "Pedro",
    "Ana",
    "Marcos"
]

# =========================
# FUNÇÕES
# =========================

#FUNÇÃO PARA OPERADORES
def operador_selecionado(event):
    if not lista_operadores.curselection():
        return

    operador = lista_operadores.get(lista_operadores.curselection())
    entry_pesq_operador.delete(0, tk.END)
    entry_pesq_operador.insert(0, operador)

    lista_operadores.bind("<<ListboxSelect>>", operador_selecionado)


#FUNÇÃO PARA MAQUINA
def maquina_selecionada(event):
    if not lista_maquinas.curselection():
        return

    maquina = lista_maquinas.get(lista_maquinas.curselection())
    entry_pesq_maquina.delete(0, tk.END)
    entry_pesq_maquina.insert(0, maquina)

    lista_maquinas.bind("<<ListboxSelect>>", maquina_selecionada)


def iniciar_apontamento():
    if not lista_maquinas.curselection():
        messagebox.showwarning("Aviso", "Selecione uma máquina")
        return

    if not lista_operadores.curselection():
        messagebox.showwarning("Aviso", "Selecione um operador")
        return

    codigo = entry_bipe.get().strip()
    if not codigo:
        messagebox.showwarning("Aviso", "Bipe o código do desenho")
        return

    maquina = lista_maquinas.get(lista_maquinas.curselection())
    operador = lista_operadores.get(lista_operadores.curselection())

    inicio = datetime.now().strftime("%H:%M:%S")

    messagebox.showinfo(
        "Apontamento Iniciado",
        f"Máquina: {maquina}\n"
        f"Operador: {operador}\n"
        f"Código: {codigo}\n"
        f"Início: {inicio}"
    )

    entry_bipe.delete(0, tk.END)

# =========================
# INTERFACE
# =========================

root = tk.Tk()
root.title("Sistema de Apontamento - Usinagem")
root.geometry("700x500")

# --------- FRAME PRINC20IPAL ----------
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

# --------- MÁQUINAS ----------
tk.Label(frame_top, text="Máquinas", font=("Arial", 11, "bold")).grid(row=0, column=0)

entry_pesq_maquina = tk.Entry(frame_top, width=25)
entry_pesq_maquina.grid(row=1, column=0, pady=5)

frame_lista_maquina = tk.Frame(frame_top)
frame_lista_maquina.grid(row=2, column=0)

scroll_maquina = tk.Scrollbar(frame_lista_maquina)
scroll_maquina.pack(side="right", fill="y")

lista_maquinas = tk.Listbox(frame_top, height=8, exportselection=False)
lista_maquinas.pack()

scroll_maquina.config(command=lista_maquinas.yview)

for m in MAQUINAS:
    lista_maquinas.insert(tk.END, m)

    lista_maquinas.bind("<<ListboxSelect>>", maquina_selecionada)


# --------- OPERADORES ----------
tk.Label(frame_top, text="Operadores", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=30)

entry_pesq_operador = tk.Entry(frame_top, width=25)
entry_pesq_operador.grid(row=1, column=1, pady=5, padx=30)

frame_lista_operador = tk.Frame(frame_top)
frame_lista_operador.grid(row=2, column=1, padx=30)

scroll_operador = tk.Scrollbar(frame_lista_operador)
scroll_operador.pack(side="right", fill="y")

lista_operadores = tk.Listbox(frame_lista_operador,width=25,height=8,yscrollcommand=scroll_operador.set)
lista_operadores.pack()

scroll_operador.config(command=lista_operadores.yview)

for o in OPERADORES:
    lista_operadores.insert(tk.END, o)

    lista_operadores.bind("<<ListboxSelect>>", operador_selecionado)

# --------- BIPE ----------
tk.Label(root, text="Bipe o código do desenho", font=("Arial", 11)).pack(pady=10)

entry_bipe = tk.Entry(root, font=("Arial", 14), width=30)
entry_bipe.pack()
entry_bipe.focus()

# --------- BOTÃO ----------
tk.Button(
    root,
    text="Iniciar Apontamento",
    font=("Arial", 12),
    width=25,
    command=iniciar_apontamento
).pack(pady=20)

root.mainloop()
