from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, asdict
from typing import List, Optional

from flask import (
    Flask,
    jsonify,
    redirect,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = "replace-with-a-secure-secret"

DB_PATH = "advogados.db"
SCHEMA_FILE = "schema.sql"
UPLOAD_DIR = os.path.join("static", "uploads")


@dataclass
class Lawyer:
    id: int
    name: str
    area: str
    city: str
    description: str
    price_per_hour: float


@dataclass
class UserSession:
    id: int
    email: str
    tipo: str
    perfil_id: int


def _ensure_column(table: str, column: str, definition: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cursor.fetchall()]
    if column not in cols:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        conn.commit()
    conn.close()


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    _ensure_column("Usuarios", "foto", "TEXT")


def find_user(email: str) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, senha_hash, tipo, perfil_id FROM Usuarios WHERE email = ?",
        (email.lower().strip(),),
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "senha_hash": row[2],
        "tipo": row[3],
        "perfil_id": row[4],
    }


def find_user_by_id(user_id: int) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, senha_hash, tipo, perfil_id FROM Usuarios WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "senha_hash": row[2],
        "tipo": row[3],
        "perfil_id": row[4],
    }


def create_user(email: str, password: str, tipo: str, perfil_id: int) -> int:
    pw_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Usuarios (email, senha_hash, tipo, perfil_id) VALUES (?, ?, ?, ?)",
        (email.lower().strip(), pw_hash, tipo, perfil_id),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_basic_info(user_id: int) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, tipo, perfil_id, foto FROM Usuarios WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "tipo": row[2],
        "perfil_id": row[3],
        "foto": row[4],
    }


def get_profile_for_user(session_user: UserSession) -> dict:
    info = get_user_basic_info(session_user.id)
    if not info:
        return {}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if session_user.tipo == "advogado":
        cursor.execute(
            "SELECT nome, Email, telefone, endereco, especializacao, cep, experiencia, casos_ganhos, biografia, preco_hora FROM Advogados WHERE id = ?",
            (session_user.perfil_id,),
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return info
        profile = {
            "nome": row[0],
            "email": row[1],
            "telefone": row[2],
            "endereco": row[3],
            "especializacao": row[4],
            "cep": row[5],
            "experiencia": row[6],
            "casos_ganhos": row[7],
            "biografia": row[8],
            "preco_hora": row[9],
        }
    else:
        cursor.execute(
            "SELECT nome, Email, telefone, endereco FROM Clientes WHERE id = ?",
            (session_user.perfil_id,),
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return info
        profile = {
            "nome": row[0],
            "email": row[1],
            "telefone": row[2],
            "endereco": row[3],
        }

    return {**info, "profile": profile}


def save_uploaded_photo(user_id: int, file) -> Optional[str]:
    if not file or not getattr(file, "filename", None):
        return None

    from werkzeug.utils import secure_filename

    filename = secure_filename(file.filename)
    if not filename:
        return None

    name = f"{user_id}_{int(__import__('time').time())}_{filename}"
    dest = os.path.join(UPLOAD_DIR, name)
    file.save(dest)
    return f"/static/uploads/{name}"


def update_profile_for_user(session_user: UserSession, data: dict, photo_url: Optional[str] = None) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if photo_url is not None:
        cursor.execute("UPDATE Usuarios SET foto = ? WHERE id = ?", (photo_url, session_user.id))

    if session_user.tipo == "advogado":
        telefone = data.get("telefone") or 0
        endereco = data.get("endereco") or ""
        especializacao = data.get("especializacao") or ""
        cep = data.get("cep") or ""
        casos_ganhos = int(data.get("casos_ganhos") or 0)
        biografia = data.get("biografia") or ""

        # preco_hora is optional: if the form doesn't send it, we keep the existing value
        preco_hora_raw = data.get("preco_hora")
        cols = [
            "nome = ?",
            "Email = ?",
            "telefone = ?",
            "endereco = ?",
            "especializacao = ?",
            "cep = ?",
            "casos_ganhos = ?",
            "biografia = ?",
        ]
        params = [
            data.get("nome", session_user.email),
            session_user.email,
            telefone,
            endereco,
            especializacao,
            cep,
            casos_ganhos,
            biografia,
        ]

        if preco_hora_raw is not None and str(preco_hora_raw).strip() != "":
            preco_hora = float(preco_hora_raw)
            cols.append("preco_hora = ?")
            params.append(preco_hora)

        params.append(session_user.perfil_id)

        cursor.execute(
            f"UPDATE Advogados SET {', '.join(cols)} WHERE id = ?",
            tuple(params),
        )
    else:
        telefone = data.get("telefone") or 0
        endereco = data.get("endereco") or ""
        cursor.execute(
            "UPDATE Clientes SET nome = ?, Email = ?, telefone = ?, endereco = ? WHERE id = ?",
            (
                data.get("nome", session_user.email),
                session_user.email,
                telefone,
                endereco,
                session_user.perfil_id,
            ),
        )

    conn.commit()
    conn.close()


def get_lawyers_from_db(query: Optional[str] = None) -> List[Lawyer]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retornamos o ID do usuário (Usuarios.id) para poder linkar ao perfil.
    base_query = (
        "SELECT Usuarios.id, Advogados.nome, Advogados.especializacao, Advogados.endereco, "
        "Advogados.biografia, Advogados.preco_hora "
        "FROM Advogados "
        "JOIN Usuarios ON Usuarios.perfil_id = Advogados.id AND Usuarios.tipo = 'advogado' "
    )

    if query:
        q = f"%{query.strip().lower()}%"
        cursor.execute(
            base_query
            + "WHERE LOWER(Advogados.nome) LIKE ? OR LOWER(Advogados.especializacao) LIKE ? "
            + "OR LOWER(Advogados.endereco) LIKE ? OR LOWER(Advogados.biografia) LIKE ?",
            (q, q, q, q),
        )
    else:
        cursor.execute(base_query)

    rows = cursor.fetchall()
    conn.close()

    return [
        Lawyer(
            id=row[0],
            name=row[1],
            area=row[2],
            city=row[3],
            description=row[4] or "",
            price_per_hour=row[5] or 0.0,
        )
        for row in rows
    ]


def _fetch_rows(table: str, limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))
    columns = [c[0] for c in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    return [dict(zip(columns, r)) for r in rows]


def is_logged_in() -> bool:
    return bool(session.get("user"))


def current_user() -> Optional[UserSession]:
    u = session.get("user")
    if not u:
        return None
    return UserSession(**u)


init_db()


@app.route("/")
def login_page() -> str:
    if is_logged_in():
        return redirect(url_for("home"))
    return send_from_directory(".", "login.html")


@app.route("/register")
def register_page() -> str:
    if is_logged_in():
        return redirect(url_for("home"))
    return send_from_directory(".", "register.html")


@app.route("/login", methods=["POST"])
def login() -> str:
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = find_user(email)
    if not user:
        return redirect(url_for("login_page", error=1))

    if not check_password_hash(user["senha_hash"], password):
        return redirect(url_for("login_page", error=1))

    session["user"] = {
        "id": user["id"],
        "email": user["email"],
        "tipo": user["tipo"],
        "perfil_id": user["perfil_id"],
    }

    return redirect(url_for("home"))


@app.route("/register", methods=["POST"])
def register() -> str:
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    tipo = request.form.get("tipo")

    if not nome or not email or not password or tipo not in ("advogado", "cliente"):
        return redirect(url_for("register_page", error="Preencha todos os campos."))

    if find_user(email):
        return redirect(url_for("register_page", error="Já existe uma conta com esse e-mail."))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if tipo == "advogado":
        especializacao = request.form.get("especializacao", "")
        cep = request.form.get("cep", "")
        casos_ganhos = int(request.form.get("casos_ganhos", "0") or 0)
        biografia = request.form.get("biografia", "")

        cursor.execute(
            "INSERT INTO Advogados (nome, Email, telefone, biografia, especializacao, cep, experiencia, casos_ganhos, endereco, preco_hora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (nome, email, 0, biografia, especializacao, cep, 0, casos_ganhos, "", 0.0),
        )
    else:
        cursor.execute(
            "INSERT INTO Clientes (nome, Email, telefone, endereco) VALUES (?, ?, ?, ?)",
            (nome, email, 0, ""),
        )

    perfil_id = cursor.lastrowid
    conn.commit()
    conn.close()

    create_user(email=email, password=password, tipo=tipo, perfil_id=perfil_id)

    return redirect(url_for("login_page"))


@app.route("/logout")
def logout() -> str:
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/app")
def home() -> str:
    if not is_logged_in():
        return redirect(url_for("login_page"))

    return send_from_directory(".", "index.html")


@app.route("/profile")
def profile_page() -> str:
    if not is_logged_in():
        return redirect(url_for("login_page"))

    return send_from_directory(".", "profile.html")


@app.route("/user/<int:user_id>")
def user_page(user_id: int) -> str:
    if not is_logged_in():
        return redirect(url_for("login_page"))

    return send_from_directory(".", "user.html")


@app.route("/api/profile", methods=["GET", "POST"])
def api_profile():
    user = current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401

    if request.method == "GET":
        return jsonify(get_profile_for_user(user))

    photo_url = None
    if "foto" in request.files:
        photo_url = save_uploaded_photo(user.id, request.files["foto"])

    update_profile_for_user(user, request.form, photo_url=photo_url)
    return jsonify({"success": True})


@app.route("/api/user/<int:user_id>")
def api_user(user_id: int):
    if not is_logged_in():
        return jsonify({"error": "unauthorized"}), 401

    user = find_user_by_id(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404

    profile = get_profile_for_user(UserSession(**user))
    return jsonify(profile)


@app.route("/api/lawyers")
def api_lawyers():
    if not is_logged_in():
        return jsonify({"error": "unauthorized"}), 401

    query = request.args.get("q", "")
    lawyers = get_lawyers_from_db(query=query)
    return jsonify([asdict(l) for l in lawyers])


@app.route("/api/session")
def api_session():
    user = current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"email": user.email, "tipo": user.tipo, "perfil_id": user.perfil_id})


DEBUG_DB_KEY = os.environ.get("DEBUG_DB_KEY")


def _to_html_table(name: str, rows: list[dict]) -> str:
    if not rows:
        return f"<h2>{name}</h2><p><em>nenhuma linha</em></p>"

    cols = rows[0].keys()
    header = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join(
        "<tr>" + "".join(f"<td>{row.get(c,'')}</td>" for c in cols) + "</tr>"
        for row in rows
    )
    return f"<h2>{name}</h2><table border=1 cellpadding=6 cellspacing=0><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>"


@app.route("/debug/db")
def debug_db():
    if not DEBUG_DB_KEY:
        return jsonify({"error": "debug endpoint not enabled"}), 404

    key = request.args.get("key")
    if key != DEBUG_DB_KEY:
        return jsonify({"error": "unauthorized"}), 401

    results = {
        "Advogados": _fetch_rows("Advogados"),
        "Clientes": _fetch_rows("Clientes"),
        "Usuarios": _fetch_rows("Usuarios"),
    }

    fmt = request.args.get("format", "json").lower()
    if fmt == "html":
        tables = "".join(_to_html_table(name, rows) for name, rows in results.items())
        return f"<html><body><h1>Debug DB</h1>{tables}</body></html>"

    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Starting AdvogadoPro on http://localhost:{port} (or http://127.0.0.1:{port})")
    print("Use DEBUG_DB_KEY=<key> to enable /debug/db")
    app.run(host="0.0.0.0", port=port, debug=True)
