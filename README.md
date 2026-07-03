# API de Doação de Livros

Uma API desenvolvida em Python com Flask para gerenciamento de doações de livros. A aplicação permite o cadastro de usuários, cadastro de livros disponíveis para doação, e controle do processo de doação, incluindo histórico de doações realizadas.

## Funcionalidades

- **Cadastro de Usuários**: Registro de novos usuários com geração automática de ID (auto-incremento)
- **Busca de Usuários**: Consulta de informações de usuários através do ID
- **Lista de Usuários**: Visualização de todos os usuários cadastrados
- **Cadastro de Livros**: Registro de livros disponíveis para doação com autor e título
- **Lista de Livros Disponíveis**: Visualização de todos os livros disponíveis para doação
- **Deletar Livro**: Remoção de livros (apenas se disponíveis)
- **Realização de Doações**: Processo de doação de livros entre usuários
- **Documentação Swagger**: Interface interativa para testar e documentar a API

## Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação
- **Flask**: Framework web para criação da API
- **Flask-SQLAlchemy**: ORM para interação com banco de dados
- **SQLite**: Banco de dados relacional leve
- **Flask-Swagger-UI**: Documentação interativa da API (OpenAPI/Swagger)

## Estrutura do Banco de Dados

### Tabela `usuarios`
- `id`: Chave primária (auto-incremento)
- `nome`: Nome completo do usuário
- `email`: Email do usuário (único)
- `data_cadastro`: Data de cadastro (formato DD/MM/AAAA)

### Tabela `livros`
- `id`: Chave primária (auto-incremento)
- `titulo`: Título do livro
- `autor`: Nome do autor do livro
- `usuario_doador_id`: ID do usuário que doou o livro (chave estrangeira para usuarios.id)
- `usuario_receptor_id`: ID do usuário que recebeu o livro (chave estrangeira para usuarios.id, null se disponível)
- `data_doacao`: Data da doação (formato DD/MM/AAAA, null se disponível)
- `status`: Status do livro ('disponivel' ou 'doado')
- `data_cadastro`: Data de cadastro do livro (formato DD/MM/AAAA)

## Instalação

### Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes do Python)

### Passo 1: Navegar para o Diretório do Projeto, por exemplo

```bash
cd "C:\Users\evely\MVP\Back-End"
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

### Passo 3: Ativar o Ambiente Virtual

**No Windows:**

Ative o ambiente virtual:
```bash
venv\Scripts\activate
```

Se encontrar um erro de política de execução do PowerShell, execute primeiro:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

**No Linux/Mac:**
```bash
source venv/bin/activate
```

### Passo 4: Instalar as Dependências

Instale todas as dependências necessárias listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

As dependências incluem:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- flask-swagger-ui==4.11.1

## Execução da Aplicação

### Iniciar o Servidor

Após instalar as dependências, execute o seguinte comando para iniciar a aplicação:

```bash
python app.py
```

O servidor será iniciado em `http://localhost:5000`

### Acessar a Documentação Swagger

A documentação interativa da API está disponível em:
```
http://localhost:5000/api/docs
```

Esta interface permite visualizar todas as rotas, métodos HTTP, estruturas de requisição/resposta, e testar os endpoints diretamente.

## Rotas da API

### Rotas Principais

#### 1. POST `/cadastrar_usuario`
Cadastra um novo usuário no sistema.

**Corpo da Requisição:**
```json
{
  "nome": "João Silva",
  "email": "joao.silva@email.com"
}
```

**Resposta (201):**
```json
{
  "mensagem": "Usuário cadastrado com sucesso",
  "id": 1,
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "data_cadastro": "28/06/2026"
}
```

#### 2. GET `/buscar_usuario/{usuario_id}`
Busca informações de um usuário específico.

**Parâmetros:**
- `usuario_id` (path): ID do usuário (inteiro)

**Resposta (200):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "data_cadastro": "28/06/2026"
}
```

#### 3. POST `/cadastrar_livro`
Cadastra um novo livro para doação.

**Corpo da Requisição:**
```json
{
  "titulo": "O Pequeno Príncipe",
  "autor": "Antoine de Saint-Exupéry",
  "usuario_doador_id": 1
}
```

**Resposta (201):**
```json
{
  "mensagem": "Livro cadastrado com sucesso",
  "id": 1,
  "titulo": "O Pequeno Príncipe",
  "autor": "Antoine de Saint-Exupéry",
  "usuario_doador_id": 1,
  "data_cadastro": "28/06/2026",
  "status": "disponivel"
}
```

#### 4. GET `/livros_disponiveis`
Lista todos os livros disponíveis para doação.

**Resposta (200):**
```json
{
  "total": 5,
  "livros": [
    {
      "id": 1,
      "titulo": "O Pequeno Príncipe",
      "autor": "Antoine de Saint-Exupéry",
      "usuario_doador_id": 1,
      "data_cadastro": "28/06/2026"
    }
  ]
}
```

#### 5. POST `/doar_livro`
Realiza a doação de um livro disponível.

**Corpo da Requisição:**
```json
{
  "livro_id": 1,
  "usuario_receptor_id": 2
}
```

**Resposta (200):**
```json
{
  "mensagem": "Doação realizada com sucesso",
  "livro_id": 1,
  "titulo": "O Pequeno Príncipe",
  "usuario_doador_id": 1,
  "usuario_receptor_id": 2,
  "data_doacao": "28/06/2026"
}
```

#### 5. DELETE `/deletar_livro/{livro_id}`
Deleta um livro do sistema (apenas se estiver disponível).

**Parâmetros:**
- `livro_id` (path): ID do livro a ser deletado

**Resposta (200):**
```json
{
  "mensagem": "Livro deletado com sucesso",
  "id": 1
}
```

**Resposta (400):**
```json
{
  "erro": "Não é possível deletar livro que já foi doado"
}
```

#### 6. GET `/usuarios`
Lista todos os usuários cadastrados.

**Resposta (200):**
```json
{
  "total": 10,
  "usuarios": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao.silva@email.com",
      "data_cadastro": "28/06/2026"
    }
  ]
}
```

## Códigos de Status HTTP

- **200 OK**: Requisição realizada com sucesso
- **201 Created**: Recurso criado com sucesso
- **400 Bad Request**: Erro na requisição (campos obrigatórios faltando, dados inválidos)
- **404 Not Found**: Recurso não encontrado
- **500 Internal Server Error**: Erro interno do servidor

## Formatação de Datas

Todas as datas no sistema seguem o formato **DD/MM/AAAA** (dia/mês/ano), conforme especificado nos requisitos.

## Validações

- **Email**: Deve ser único no sistema
- **Livro**: Só pode ser doado se estiver com status 'disponivel'
- **Usuário Receptor**: Deve existir no sistema para realizar uma doação
- **ID de Usuário**: Deve ser um número inteiro válido existente no banco de dados

## Estrutura do Projeto

```
livro-doacao-api/
├── app.py                  # Arquivo principal da aplicação Flask
├── requirements.txt        # Dependências do projeto
├── README.md              # Documentação do projeto
├── instance/              # Diretório para banco de dados (criado automaticamente)
│   └── livro_doacao.db    # Banco de dados SQLite
└── static/                # Arquivos estáticos
    └── swagger.json       # Documentação OpenAPI/Swagger
```

## Exemplo de Fluxo de Uso

1. **Cadastrar dois usuários:**
   - Usuário 1: João Silva (ID gerado: 1)
   - Usuário 2: Maria Santos (ID gerado: 2)

2. **Cadastrar um livro para doação:**
   - Livro: "O Pequeno Príncipe" de Antoine de Saint-Exupéry
   - Doador: João Silva (ID: 1)

3. **Listar livros disponíveis:**
   - Verificar que o livro está disponível

4. **Realizar a doação:**
   - Doar o livro para Maria Santos (ID: 2)

## Troubleshooting

### Erro: ModuleNotFoundError

Se encontrar erros de módulos não encontrados, certifique-se de:
- Ter ativado o ambiente virtual
- Ter instalado todas as dependências com `pip install -r requirements.txt`

### Erro: Banco de Dados

O banco de dados SQLite é criado automaticamente na primeira execução. Se precisar reiniciar o banco de dados:
- Delete o arquivo `instance/livro_doacao.db`
- Reinicie a aplicação

### Porta já em uso

Se a porta 5000 já estiver em uso, modifique a linha final do `app.py`:
```python
app.run(debug=True, port=5001)  # Use outra porta
```

## Autor

Este projeto foi desenvolvido para fins acadêmicos por Evelyn Oliveira de Souza, estudante de pós graduação em Desenvolvimento Full Stack pela Puc Rio.
