import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from database import inserir_tarefa

def abrir_tela_cadastro(root):
    cadastro = tk.Toplevel(root)
    cadastro.title("Cadastro de Tarefas")
    cadastro.geometry("600x400") 

    tk.Label(cadastro, text="Data:").grid(row=0, column=0, sticky='w', padx=10, pady=(10, 0))
    data_entry = DateEntry(cadastro, width=20)
    data_entry.grid(row=1, column=0, padx=10, sticky='we')


    tk.Label(cadastro, text="Título:").grid(row=2, column=0, sticky='w', padx=10, pady=(10, 0))
    titulo_entry = tk.Entry(cadastro, width=70)
    titulo_entry.grid(row=3, column=0, padx=10, sticky='we')


    tk.Label(cadastro, text="Descrição:").grid(row=4, column=0, sticky='w', padx=10, pady=(10, 0))
    desc_entry = tk.Text(cadastro, width=70, height=5)
    desc_entry.grid(row=5, column=0, padx=10, sticky='we')


    tk.Label(cadastro, text="Horas:").grid(row=6, column=0, sticky='w', padx=10, pady=(10, 0))
    horas_entry = tk.Entry(cadastro, width=20)
    horas_entry.grid(row=7, column=0, padx=10, sticky='w')


    cadastro.grid_columnconfigure(0, weight=1)

    def salvar():
        try:
            horas = int(horas_entry.get())
            titulo = titulo_entry.get()
            data = data_entry.get()
            descricao = desc_entry.get("1.0", "end-1c")
            inserir_tarefa(data, titulo, descricao, horas)
            messagebox.showinfo("Sucesso", "Tarefa cadastrada!")
            cadastro.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Horas deve ser um número inteiro")

    tk.Button(cadastro, text="Salvar", command=salvar, width=20).grid(row=10, columnspan=2, pady=10)
