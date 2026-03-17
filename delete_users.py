import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "advogados.db")

EMAILS_TO_DELETE = [
    "ana.santos@example.com",
    "bruno.oliveira@example.com",
    "carla.mendes@example.com",
    "daniel.costa@example.com",
    "eduarda.lima@example.com",
]

def delete_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for email in EMAILS_TO_DELETE:
        cursor.execute("SELECT perfil_id FROM Usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            perfil_id = row[0]
            cursor.execute("DELETE FROM Advogados WHERE id = ?", (perfil_id,))
            cursor.execute("DELETE FROM Usuarios WHERE email = ?", (email,))
            print(f"Deletado: {email}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    delete_users()