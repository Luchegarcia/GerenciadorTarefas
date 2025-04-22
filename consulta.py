import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from database import buscar_tarefas, excluir_tarefa,atualizar_tarefa,buscar_tarefas_por_id
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
            data_formatada = datetime.strptime(tarefa[1], "%Y%m%d").strftime("%d/%m/%Y")
            tree.insert('', tk.END, values=(data_formatada, tarefa[2], tarefa[3], tarefa[4]), iid=tarefa[0])

    def excluir():
        selecionado = tree.selection()
        if selecionado:
            id_tarefa = selecionado[0]
            excluir_tarefa(id_tarefa)
            tree.delete(id_tarefa)
            messagebox.showinfo("Removido", "Tarefa excluída com sucesso")

    def copiar():
        colunas = [tree.heading(col)["text"] for col in tree["columns"]]
        dados = [colunas]
    
        for item in tree.get_children():
            dados.append(tree.item(item, 'values'))
    
        texto = '\n'.join(['\t'.join(map(str, linha)) for linha in dados])
        consulta.clipboard_clear()
        consulta.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Dados copiados")

    def abrir_tela_edicao(tarefa_id):
        edicao = tk.Toplevel(consulta)
        edicao.title("Editar Tarefa")

        tarefa = buscar_tarefas_por_id(tarefa_id)  

        tk.Label(edicao, text="Data:").grid(row=0, column=0, sticky='w', padx=10, pady=(10, 0))
        data_entry = DateEntry(edicao, width=20)
        data_entry.set_date(datetime.strptime(tarefa[1], "%Y%m%d").strftime("%d/%m/%Y"))
        data_entry.grid(row=1, column=0, padx=10, sticky='we')

        tk.Label(edicao, text="Título:").grid(row=2, column=0, sticky='w', padx=10, pady=(10, 0))
        titulo_entry = tk.Entry(edicao, width=70)
        titulo_entry.insert(0, tarefa[2])
        titulo_entry.grid(row=3, column=0, padx=10, sticky='we')

        tk.Label(edicao, text="Descrição:").grid(row=4, column=0, sticky='w', padx=10, pady=(10, 0))
        desc_entry = tk.Text(edicao, width=70, height=5)
        desc_entry.insert("1.0", tarefa[3])
        desc_entry.grid(row=5, column=0, padx=10, sticky='we')

        tk.Label(edicao, text="Horas:").grid(row=6, column=0, sticky='w', padx=10, pady=(10, 0))
        horas_entry = tk.Entry(edicao, width=20)
        horas_entry.insert(0, tarefa[4])
        horas_entry.grid(row=7, column=0, padx=10, sticky='w')

        edicao.grid_columnconfigure(0, weight=1)

        def salvar_edicao():
            try:
                horas = int(horas_entry.get())
                titulo = titulo_entry.get()
                data = datetime.strptime(data_entry.get(), "%d/%m/%Y").strftime("%Y%m%d")
                descricao = desc_entry.get("1.0", "end-1c")
                atualizar_tarefa(tarefa_id, data, titulo, descricao, horas)  
                messagebox.showinfo("Sucesso", "Tarefa atualizada!")
                edicao.destroy()
                carregar()  
            except ValueError:
                messagebox.showerror("Erro", "Horas deve ser um número inteiro")

        tk.Button(edicao, text="Salvar", command=salvar_edicao, width=20).grid(row=10, columnspan=2, pady=10)

    def on_tree_select(event):
        selecionado = tree.selection()
        if selecionado:
            tarefa_id = selecionado[0]
            abrir_tela_edicao(tarefa_id)

    tree.bind("<Double-1>", on_tree_select)

    tk.Button(consulta, text="Buscar", command=carregar).grid(row=1, column=0, columnspan=2)
    tk.Button(consulta, text="Excluir", command=excluir).grid(row=1, column=1, columnspan=2)
    tk.Button(consulta, text="Copiar", command=copiar).grid(row=1, column=3, columnspan=2)
