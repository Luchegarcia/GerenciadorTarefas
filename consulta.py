import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from database import buscar_tarefas, excluir_tarefa
from datetime import datetime

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
        data_ini_formatada = datetime.strptime(data_ini.get(), "%m/%d/%y").strftime("%Y%m%d")
        data_fim_formatada = datetime.strptime(data_fim.get(), "%m/%d/%y").strftime("%Y%m%d")
        print(data_ini_formatada, data_fim_formatada)  
        for row in tree.get_children():
            tree.delete(row)
        tarefas = buscar_tarefas(data_ini_formatada, data_fim_formatada)
        for tarefa in tarefas:
            tree.insert('', tk.END, values=(tarefa[1], tarefa[2], tarefa[3], tarefa[4]), iid=tarefa[0])

    def excluir():
        selecionado = tree.selection()
        if selecionado:
            id_tarefa = selecionado[0]
            excluir_tarefa(id_tarefa)
            tree.delete(id_tarefa)
            messagebox.showinfo("Removido", "Tarefa excluída com sucesso")

    def copiar():
        selecionado = tree.selection()
        if selecionado:
            # Adicione os cabeçalhos das colunas
            colunas = [tree.heading(col)["text"] for col in tree["columns"]]
            dados = [colunas]
            for item in selecionado:
                dados.append(tree.item(item, 'values'))
            texto = '\n'.join(['\t'.join(map(str, linha)) for linha in dados])
            consulta.clipboard_clear()
            consulta.clipboard_append(texto)
            messagebox.showinfo("Copiado", "Dados copiados")

    tk.Button(consulta, text="Buscar", command=carregar).grid(row=1, column=0, columnspan=2)
    tk.Button(consulta, text="Excluir", command=excluir).grid(row=1, column=1, columnspan=2)
    tk.Button(consulta, text="Copiar", command=copiar).grid(row=1, column=3, columnspan=2)
