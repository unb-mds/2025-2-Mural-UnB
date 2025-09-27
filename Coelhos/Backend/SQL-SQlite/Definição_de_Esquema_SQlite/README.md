# Definição de Esquema em SQLite - Guia Completo

## Introdução

A definição do esquema do banco de dados é a base de qualquer aplicação. Este guia cobre a criação e modificação de tabelas, tipos de dados, restrições e índices no SQLite.

## 1. Criação de Tabelas (CREATE TABLE)

### 1.1. Sintaxe Básica do CREATE TABLE

```sql
CREATE TABLE [IF NOT EXISTS] nome_tabela (
    coluna1 tipo_dado [restrições],
    coluna2 tipo_dado [restrições],
    ...
    [restrições_de_tabela]
);
1.2. Exemplos de Criação de Tabelas
Tabela simples:

sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);
Tabela com múltiplas restrições:

sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK(LENGTH(nome) > 0),
    categoria TEXT NOT NULL,
    preco REAL CHECK(preco >= 0),
    estoque INTEGER DEFAULT 0 CHECK(estoque >= 0),
    data_cadastro DATE DEFAULT (date('now'))
);
Tabela com chave estrangeira:

sql
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Pendente' CHECK(status IN ('Pendente', 'Processando', 'Concluído', 'Cancelado')),
    total REAL DEFAULT 0,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
2. Tipos de Dados no SQLite
O SQLite usa tipagem dinâmica, mas reconhece os seguintes tipos:

2.1. Principais Tipos de Dados
Tipo	Descrição	Exemplo
INTEGER	Números inteiros	1, -5, 1000
REAL	Números de ponto flutuante	3.14, -2.5
TEXT	Texto (UTF-8, UTF-16)	'João', 'Hello'
BLOB	Dados binários	x'53514C697465'
NULL	Valor nulo	NULL
2.2. Afinidade de Tipos
O SQLite tem "afinidade de tipos" que converte valores automaticamente:

sql
CREATE TABLE exemplo_tipos (
    col_int INTEGER,    -- Afinidade INTEGER
    col_real REAL,      -- Afinidade REAL
    col_text TEXT,      -- Afinidade TEXT
    col_blob BLOB,      -- Afinidade BLOB
    col_num NUMERIC     -- Afinidade NUMERIC (INTEGER ou REAL)
);
2.3. Exemplos de Conversão Automática
sql
INSERT INTO exemplo_tipos VALUES (
    '123',      -- Convertido para INTEGER 123
    '45.67',    -- Convertido para REAL 45.67
    100,        -- Convertido para TEXT '100'
    NULL,       -- Permanece NULL
    '42'        -- Convertido para INTEGER 42
);
3. Restrições (Constraints)
3.1. PRIMARY KEY
Identifica unicamente cada registro na tabela.

sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,          -- Chave primária simples
    username TEXT NOT NULL UNIQUE
);

-- Chave primária composta
CREATE TABLE pedidos_itens (
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
3.2. FOREIGN KEY
Mantém a integridade referencial entre tabelas.

sql
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    -- Restrição de chave estrangeira com ações
    FOREIGN KEY (cliente_id) 
        REFERENCES clientes(id)
        ON DELETE CASCADE
        ON UPDATE SET NULL
);
Ações de FOREIGN KEY:

ON DELETE CASCADE - Exclui registros relacionados

ON DELETE SET NULL - Define como NULL

ON DELETE RESTRICT - Impede exclusão

ON DELETE SET DEFAULT - Define valor padrão

ON UPDATE - Mesmas opções para atualizações

3.3. UNIQUE
Garante que todos os valores em uma coluna sejam diferentes.

sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,               -- Email único
    cpf TEXT UNIQUE NOT NULL,        -- CPF único e obrigatório
    username TEXT UNIQUE
);
3.4. NOT NULL
Impede valores nulos na coluna.

sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,              -- Nome obrigatório
    descricao TEXT,                  -- Descrição opcional
    preco REAL NOT NULL CHECK(preco >= 0)
);
3.5. CHECK
Define condições personalizadas para os valores.

sql
CREATE TABLE funcionarios (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    idade INTEGER CHECK(idade >= 18 AND idade <= 65),
    salario REAL CHECK(salario >= 1212.00),
    email TEXT CHECK(email LIKE '%@%.%'),
    -- Check com múltiplas colunas
    CHECK (NOT (salario > 10000 AND idade < 25))
);
3.6. DEFAULT
Define valor padrão quando nenhum valor é especificado.

sql
CREATE TABLE registros (
    id INTEGER PRIMARY KEY,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Ativo',
    contador INTEGER DEFAULT 0,
    preco REAL DEFAULT 0.0
);
4. Modificação de Tabelas (ALTER TABLE)
4.1. Adicionar Colunas
sql
-- Adicionar uma nova coluna
ALTER TABLE clientes ADD COLUMN telefone TEXT;

-- Adicionar coluna com restrições
ALTER TABLE produtos 
ADD COLUMN peso REAL 
CHECK(peso > 0) 
DEFAULT 1.0;
4.2. Renomear Tabela
sql
ALTER TABLE clientes_antigos RENAME TO clientes;
4.3. Limitações do ALTER TABLE no SQLite
O SQLite não suporta:

Remover colunas

Alterar tipo de coluna

Adicionar/remover restrições diretamente

Solução para remover colunas:

sql
-- 1. Criar nova tabela
CREATE TABLE clientes_nova (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT
);

-- 2. Copiar dados (excluindo a coluna indesejada)
INSERT INTO clientes_nova (id, nome, email)
SELECT id, nome, email FROM clientes;

-- 3. Excluir tabela antiga
DROP TABLE clientes;

-- 4. Renomear nova tabela
ALTER TABLE clientes_nova RENAME TO clientes;
5. Índices e Otimização (CREATE INDEX)
5.1. Criando Índices
sql
-- Índice simples
CREATE INDEX idx_clientes_nome ON clientes(nome);

-- Índice único
CREATE UNIQUE INDEX idx_clientes_email ON clientes(email);

-- Índice composto
CREATE INDEX idx_pedidos_data_cliente ON pedidos(data_pedido, cliente_id);

-- Índice com ordenação específica
CREATE INDEX idx_produtos_preco_desc ON produtos(preco DESC);
5.2. Quando Usar Índices
Use índices para:

Colunas frequentemente usadas em WHERE

Colunas usadas em JOINs

Colunas usadas em ORDER BY

Colunas com alta seletividade

Exemplo prático:

sql
-- Sem índice (lento para grandes tabelas)
SELECT * FROM pedidos WHERE cliente_id = 100;

-- Com índice (rápido)
CREATE INDEX idx_pedidos_cliente_id ON pedidos(cliente_id);
5.3. Gerenciando Índices
sql
-- Ver índices existentes
SELECT * FROM sqlite_master WHERE type = 'index';

-- Ver informações de índice
PRAGMA index_list('nome_tabela');
PRAGMA index_info('nome_indice');

-- Reconstruir índice
REINDEX nome_indice;

-- Excluir índice
DROP INDEX IF EXISTS nome_indice;
6. Exemplos Completos de Esquemas
6.1. Sistema E-commerce Completo
sql
-- Tabela de clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK(LENGTH(nome) > 2),
    email TEXT UNIQUE CHECK(email LIKE '%@%.%'),
    telefone TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
);

-- Tabela de categorias
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Tabela de produtos
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL CHECK(preco >= 0),
    estoque INTEGER DEFAULT 0 CHECK(estoque >= 0),
    categoria_id INTEGER,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Tabela de pedidos
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Pendente' 
        CHECK(status IN ('Pendente', 'Processando', 'Enviado', 'Entregue', 'Cancelado')),
    total REAL DEFAULT 0,
    
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Tabela de itens do pedido
CREATE TABLE pedidos_itens (
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER CHECK(quantidade > 0),
    preco_unitario REAL CHECK(preco_unitario >= 0),
    subtotal REAL GENERATED ALWAYS AS (quantidade * preco_unitario) VIRTUAL,
    
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
);

-- Índices para otimização
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX idx_pedidos_cliente_data ON pedidos(cliente_id, data_pedido DESC);
CREATE UNIQUE INDEX idx_produtos_nome_unique ON produtos(nome, categoria_id);
6.2. Sistema de Blog
sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL CHECK(LENGTH(username) >= 3),
    email TEXT UNIQUE NOT NULL CHECK(email LIKE '%@%.%'),
    senha_hash TEXT NOT NULL,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT 1
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL CHECK(LENGTH(titulo) BETWEEN 5 AND 200),
    conteudo TEXT NOT NULL,
    autor_id INTEGER NOT NULL,
    data_publicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    visivel BOOLEAN DEFAULT 1,
    
    FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    conteudo TEXT NOT NULL CHECK(LENGTH(conteudo) > 0),
    data_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    aprovado BOOLEAN DEFAULT 0,
    
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
);

CREATE TABLE posts_tags (
    post_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
7. Boas Práticas de Design
7.1. Normalização
Primeira Forma Normal (1NF):

Cada coluna contém valores atômicos

Sem grupos repetitivos

Segunda Forma Normal (2NF):

Está na 1NF

Todas as colunas não-chave dependem de toda a chave primária

Terceira Forma Normal (3NF):

Está na 2NF

Não há dependências transitivas (colunas dependem apenas da chave primária)

7.2. Nomenclatura
sql
-- Use nomes descritivos
CREATE TABLE usuario_pedidos (...-);  -- ❌ Ruim
CREATE TABLE pedidos_usuarios (...);  -- ✅ Bom

-- Use snake_case
CREATE TABLE UsuarioPedidos (...);    -- ❌ Ruim
CREATE TABLE usuario_pedidos (...);   -- ✅ Bom

-- Seja consistente
CREATE TABLE produtos (...);
CREATE TABLE categorias (...);
CREATE TABLE produtos_categorias (...);
7.3. Documentação do Esquema
sql
-- Use comentários SQL
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,          -- ID único do cliente
    nome TEXT NOT NULL,              -- Nome completo
    email TEXT UNIQUE,               -- Email único para login
    -- ... outras colunas
);

-- Mantenha um arquivo de documentação
/*
TABELA: clientes
DESCRIÇÃO: Armazena informações dos clientes do sistema
COLUNAS:
  - id: Identificador único (PK)
  - nome: Nome completo do cliente
  - email: Email único para comunicação
*/
8. Ferramentas e Utilitários
8.1. Visualizar Esquema
sql
-- Ver todas as tabelas
SELECT name FROM sqlite_master WHERE type = 'table';

-- Ver estrutura de uma tabela
PRAGMA table_info('nome_tabela');

-- Ver SQL de criação
SELECT sql FROM sqlite_master WHERE name = 'nome_tabela';

-- Ver chaves estrangeiras
PRAGMA foreign_key_list('nome_tabela');
8.2. Manutenção do Banco de Dados
sql
-- Otimizar espaço (VACUUM)
VACUUM;

-- Verificar integridade
PRAGMA integrity_check;

-- Verificar chaves estrangeiras (ativar)
PRAGMA foreign_keys = ON;

-- Backup do esquema
.sqlite3 database.db .schema > schema_backup.sql
9. Exercícios Práticos
Exercício 1: Criar Esquema de Biblioteca
sql
CREATE TABLE livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT UNIQUE,
    ano_publicacao INTEGER CHECK(ano_publicacao > 1450),
    disponivel BOOLEAN DEFAULT 1
);

CREATE TABLE membros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE CHECK(email LIKE '%@%.%'),
    data_inscricao DATE DEFAULT (date('now'))
);

CREATE TABLE emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    membro_id INTEGER NOT NULL,
    data_emprestimo DATE DEFAULT (date('now')),
    data_devolucao DATE,
    multa REAL DEFAULT 0,
    
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (membro_id) REFERENCES membros(id),
    CHECK(data_devolucao IS NULL OR data_devolucao >= data_emprestimo)
);
Exercício 2: Modificar Esquema Existente
sql
-- Adicionar nova coluna
ALTER TABLE livros ADD COLUMN editora TEXT;

-- Criar índice para buscas por autor
CREATE INDEX idx_livros_autor ON livros(autor);

-- Adicionar restrição de e-mail único em membros
CREATE UNIQUE INDEX idx_membros_email_unique ON membros(email);
Exercício 3: Normalização
sql
-- Refatorar para 3NF
CREATE TABLE autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE editoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

ALTER TABLE livros 
ADD COLUMN autor_id INTEGER,
ADD COLUMN editora_id INTEGER;

-- Atualizar constraints
CREATE TABLE livros_autores (
    livro_id INTEGER,
    autor_id INTEGER,
    PRIMARY KEY (livro_id, autor_id),
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (autor_id) REFERENCES autores(id)
);

<sub>Documentação criada por **João Gonzaga** ([@Karmantinedev](https://github.com/Karmantinedev))</sub>
