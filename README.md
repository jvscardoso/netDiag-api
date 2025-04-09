# 📡 netDiag API

## 🧩 Visão Geral

A **netDiag API** é a camada de backend de um sistema de diagnósticos de rede. O projeto simula um ambiente corporativo onde analistas e administradores podem consultar, filtrar e agregar dados de diagnósticos coletados de dispositivos espalhados em diferentes localidades.

Este repositório contém a implementação da API RESTful desenvolvida em **Flask**, com banco de dados **PostgreSQL**, utilizando SQL puro.

---

## 🚀 Tecnologias

- Python 3.11+
- Flask
- PostgreSQL
- SQLAlchemy (apenas modelagem)
- JWT (autenticação)
- Docker (ambiente de banco de dados)
- pytest (testes automatizados)

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/jvscardoso/netDiag-api.git
cd netDiag-api
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Faça uma copia do arquivo `.env.example` com o nome de `.env`

### 5. Suba o banco com Docker

```bash
docker-compose up -d
```

> Isso criará o container do PostgreSQL e executará o script `init_db.sql`.

### 6. Crie os usuário no banco
```bash
python users_seed.py
```

---

## ▶️ Executando a API

A API estará disponível em: [http://localhost:5000](http://localhost:5000)
Você pode visualizar as rotas pelo Postman=[https://innovatech-labs.postman.co/workspace/Net-Diag~49f707c8-17b5-4ca7-b2db-0ac1f34ae640/collection/42960732-5fe8f649-35bf-41c9-90cb-ac76e1ee0fbd?action=share&creator=42960732&active-environment=42960732-235d0d38-497c-4147-b2a4-306b66ea8973]

---

## 🧪 Rodando os testes

```bash
pytest
```

> Os testes cobrem autenticação, permissionamento e operações CRUD com cobertura mínima de status HTTP esperados (200, 401, 403).

---

## 📌 Funcionalidades

- Login com JWT
- CRUD de usuários com controle de acesso por role
- Diagnósticos com:
  - Listagem paginada e com filtros
  - Agregação diária com métricas
- Filtros por cidade e estado
- Middleware de autenticação e autorização
- Suporte a usuários bloqueados (`deleted_at`)

---

## 🔒 Perfis de acesso

| Role     | Permissões                                                    |
|----------|---------------------------------------------------------------|
| `admin`  | Acesso total a todos os recursos                              |
| `analyst`| Leitura de dados de diagnóstico (lista e agregados)           |
| `user`   | Acesso limitado a somente o perfil                            |
|--------------------------------------------------------------------------|

## 🔑 Credenciais

admin@netdiag.com / admin123

analyst@netdiag.com / analyst123

user@netdiag.com / user123
