import sqlite3

from datetime import datetime

def conectar():
    conn = sqlite3.connect("tarefas.db")
    criar_tabela(conn)
    return conn

def criar_tabela(conn):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                titulo TEXT,
                descricao TEXT,
                horas INTEGER
            )
        """)

def inserir_tarefa(data, titulo, descricao, horas):
    with conectar() as conn:
        conn.execute("INSERT INTO tarefas (data, titulo, descricao, horas) VALUES (?, ?, ?, ?)",
                     (data, titulo, descricao, horas))

def buscar_tarefas(data_ini, data_fim):
    with conectar() as conn:
        return conn.execute("""
            SELECT id, data, titulo, descricao, horas
            FROM tarefas
            WHERE data BETWEEN ? AND ?
        """, (data_ini, data_fim)).fetchall()

def excluir_tarefa(id):
    with conectar() as conn:
        conn.execute("DELETE FROM tarefas WHERE id = ?", (id,))
