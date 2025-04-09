# 📡 netDiag API

## 🧩 Visão Geral

A **netDiag API** é a camada de backend de um sistema de diagnósticos de rede. O projeto simula um ambiente corporativo onde analistas e administradores podem consultar, filtrar e agregar dados de diagnósticos coletados de dispositivos espalhados em diferentes localidades.

Este repositório contém a implementação da API RESTful desenvolvida em **Flask**, com banco de dados **PostgreSQL**, utilizando SQL puro para atender aos requisitos técnicos do desafio proposto.

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
git clone https://github.com/seu-usuario/netDiag-api.git
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

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/netdiag
SECRET_KEY=sua_chave_secreta
```

> **Dica:** Você pode usar `python-dotenv` para carregar esse `.env` automaticamente.

### 5. Suba o banco com Docker

```bash
docker-compose up -d
```

> Isso criará o container do PostgreSQL e executará o script `init_db.sql`.

---

## ▶️ Executando a API

```bash
flask run
```

A API estará disponível em: [http://localhost:5000](http://localhost:5000)

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
| `analyst`| Leitura de dados de diagnóstico (lista e agregados)          |
