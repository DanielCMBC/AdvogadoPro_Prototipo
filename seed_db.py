from __future__ import annotations

import sqlite3
from typing import List, Dict

from werkzeug.security import generate_password_hash

from app import DB_PATH, init_db


SAMPLE_LAWYERS: List[Dict[str, object]] = [
    {
        "nome": "Ana Clara Santos",
        "email": "ana.santos@example.com",
        "telefone": 11987654321,
        "especializacao": "Direito de Família",
        "cep": "01001-000",
        "experiencia": 8,
        "casos_ganhos": 45,
        "endereco": "Rua das Flores, 123, São Paulo, SP",
        "biografia": "Advogada especializada em direito de família, com foco em guarda compartilhada e pensão alimentícia.",
    },
    {
        "nome": "Bruno Oliveira",
        "email": "bruno.oliveira@example.com",
        "telefone": 21999998888,
        "especializacao": "Direito Trabalhista",
        "cep": "20010-000",
        "experiencia": 12,
        "casos_ganhos": 120,
        "endereco": "Avenida Rio Branco, 1000, Rio de Janeiro, RJ",
        "biografia": "Atende trabalhadores e empresas em disputas trabalhistas, acordos e consultoria preventiva.",
    },
    {
        "nome": "Carla Mendes",
        "email": "carla.mendes@example.com",
        "telefone": 31988887777,
        "especializacao": "Direito Penal",
        "cep": "30140-000",
        "experiencia": 15,
        "casos_ganhos": 88,
        "endereco": "Praça Sete de Setembro, 200, Belo Horizonte, MG",
        "biografia": "Defensora com ampla experiência em júri e crimes complexos, sempre buscando os melhores resultados.",
    },
    {
        "nome": "Daniel Costa",
        "email": "daniel.costa@example.com",
        "telefone": 41977776666,
        "especializacao": "Direito Empresarial",
        "cep": "80010-000",
        "experiencia": 10,
        "casos_ganhos": 72,
        "endereco": "Rua XV de Novembro, 500, Curitiba, PR",
        "biografia": "Atua em contratos, fusões e aquisições, e compliance para empresas de todos os portes.",
    },
    {
        "nome": "Eduarda Lima",
        "email": "eduarda.lima@example.com",
        "telefone": 51966665555,
        "especializacao": "Direito Imobiliário",
        "cep": "90010-000",
        "experiencia": 6,
        "casos_ganhos": 55,
        "endereco": "Avenida Borges de Medeiros, 999, Porto Alegre, RS",
        "biografia": "Assessora clientes em compra e venda, locação e regularização de imóveis.",
    },
]


def lawyer_exists(conn: sqlite3.Connection, email: str) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Usuarios WHERE email = ?", (email.lower().strip(),))
    return cur.fetchone() is not None


def insert_lawyer(conn: sqlite3.Connection, lawyer: Dict[str, object]) -> None:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Advogados (nome, Email, telefone, biografia, especializacao, cep, experiencia, casos_ganhos, endereco) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            lawyer["nome"],
            lawyer["email"],
            lawyer["telefone"],
            lawyer["biografia"],
            lawyer["especializacao"],
            lawyer["cep"],
            lawyer["experiencia"],
            lawyer["casos_ganhos"],
            lawyer["endereco"],
        ),
    )
    perfil_id = cur.lastrowid
    pw_hash = generate_password_hash("password123")
    cur.execute(
        "INSERT INTO Usuarios (email, senha_hash, tipo, perfil_id) VALUES (?, ?, ?, ?)",
        (lawyer["email"].lower().strip(), pw_hash, "advogado", perfil_id),
    )


def main() -> None:
    print("Inicializando banco de dados (se necessário)...")
    init_db()

    conn = sqlite3.connect(DB_PATH)

    inserted = 0
    for lawyer in SAMPLE_LAWYERS:
        if lawyer_exists(conn, lawyer["email"]):
            continue
        insert_lawyer(conn, lawyer)
        inserted += 1

    conn.commit()
    conn.close()

    if inserted:
        print(f"Inseridos {inserted} novos advogados.\nUsuário padrão para todos: senha 'password123'.")
    else:
        print("Já existem advogados cadastrados; nada foi alterado.")


if __name__ == "__main__":
    main()
