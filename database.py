
import sqlite3
import os

BANCO = os.path.join(os.path.dirname(__file__), "clinica.db")


def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_banco():
    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT,
            data_nascimento TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            status TEXT DEFAULT 'Agendada',
            FOREIGN KEY (paciente_id)
                REFERENCES pacientes(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")
