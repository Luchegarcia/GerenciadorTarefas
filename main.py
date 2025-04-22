import tkinter as tk
from cadastro import abrir_tela_cadastro
from consulta import abrir_tela_consulta


def main():
    root = tk.Tk()
    root.title("Cadastro de Tarefas")
    root.geometry("300x100")

    tk.Button(root, text="Cadastrar", width=20, command=lambda: abrir_tela_cadastro(root)).pack(pady=10)
    tk.Button(root, text="Consultar", width=20, command=lambda: abrir_tela_consulta(root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
