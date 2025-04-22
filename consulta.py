import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from database import buscar_tarefas, excluir_tarefa

def abrir_tela_consulta(root):
    consulta = tk.Toplevel(root)
    consulta.title("Consultar Tarefas")

    tk.Label(consulta, text="Data Inicial:").grid(row=0, column=0)
    data_ini = DateEntry(consulta)
    data_ini.grid(row=0, column=1)

    tk.Label(consulta, text="Data Final:").grid(row=0, column=2)
    data_fim = DateEntry(consulta)
    data_fim.grid(row=0, column=3)

    tree = ttk.Treeview(consulta, columns=("data", "titulo", "desc", "horas"), show="headings")
    for col in ("data", "titulo", "desc", "horas"):
        tree.heading(col, text=col.capitalize())
    tree.grid(row=2, column=0, columnspan=4, pady=10)

    def carregar():
        for row in tree.get_children():
            tree.delete(row)
        tarefas = buscar_tarefas(data_ini.get(), data_fim.get())
        for tarefa in tarefas:
            tree.insert('', tk.END, values=tarefa, iid=tarefa[0])

    def excluir():
        selecionado = tree.selection()
        if selecionado:
            id_tarefa = selecionado[0]
            excluir_tarefa(id_tarefa)
            tree.delete(id_tarefa)
            messagebox.showinfo("Removido", "Tarefa excluída com sucesso")

    tk.Button(consulta, text="Buscar", command=carregar).grid(row=1, column=0, columnspan=2)
    tk.Button(consulta, text="Excluir", command=excluir).grid(row=1, column=2, columnspan=2)

