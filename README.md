
## Como rodar o projeto


### 1. Criar Env

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicie o servidor:

```bash
python app.py
```

4. Abra no navegador:

- Login: http://localhost:8000
- Dashboard: http://localhost:8000/app
- Editor de perfil: http://localhost:8000/profile

(Se aparecer "Página não encontrada", confirme que você está usando **http://localhost:8000** (ou **http://127.0.0.1:8000**) e **não** **http://0.0.0.0:8000**).

### Parar / reiniciar o servidor

- No terminal onde está rodando, pressione **Ctrl+C**.
- Se o processo travar, mate-o (Linux/macOS):

```bash
lsof -i :8000
kill <PID>
```

- Reinicie com:

```bash
python app.py
```

## Depurar / inspecionar o banco de dados

Inicie o servidor com uma chave de debug (isso habilita `/debug/db`):

```bash
DEBUG_DB_KEY=abc123 python app.py
```

Depois, abra no navegador:

- Visualização JSON: `http://localhost:8000/debug/db?key=abc123`
- Visualização HTML: `http://localhost:8000/debug/db?key=abc123&format=html`

## Observações

- Os dados são armazenados em `advogados.db` (SQLite). O esquema está em `schema.sql`.
- Perfis ficam em `Advogados` ou `Clientes`, ligados pela tabela `Usuarios`.
- Fotos de perfil enviadas são salvas em `static/uploads/` (ignorado pelo git).
