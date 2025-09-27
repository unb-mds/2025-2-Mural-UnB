# Manipulação de Dados em SQL 

## Introdução

A manipulação de dados é uma das operações mais fundamentais em bancos de dados. Este guia cobre as quatro operações básicas do CRUD (Create, Read, Update, Delete) com foco no SQLite.

## 1. Inserção de Dados (INSERT)

### 1.1. Sintaxe Básica do INSERT

A instrução `INSERT` é usada para adicionar novos registros a uma tabela.

**Sintaxe:**
```sql
INSERT INTO nome_tabela (coluna1, coluna2, coluna3, ...)
VALUES (valor1, valor2, valor3, ...);

# Manipulação de Dados em SQL - Guia Completo

## Introdução

A manipulação de dados é uma das operações mais fundamentais em bancos de dados. Este guia cobre as quatro operações básicas do CRUD (Create, Read, Update, Delete) com foco no SQLite.

## 1. Inserção de Dados (INSERT)

### 1.1. Sintaxe Básica do INSERT

A instrução `INSERT` é usada para adicionar novos registros a uma tabela.

**Sintaxe:**

INSERT INTO nome_tabela (coluna1, coluna2, coluna3, ...)
VALUES (valor1, valor2, valor3, ...);

## 1.2. Exemplos de INSERT
sql
-- Inserir um único registro
INSERT INTO clientes (nome, email, cidade)
VALUES ('João Silva', 'joao@email.com', 'São Paulo');

-- Inserir múltiplos registros de uma vez (SQLite suporta)
INSERT INTO produtos (nome, preço, categoria)
VALUES 
    ('Notebook', 2500.00, 'Eletrônicos'),
    ('Livro SQL', 89.90, 'Livros'),
    ('Mouse', 45.50, 'Acessórios');

-- Inserir sem especificar colunas (deve incluir todos os valores na ordem correta)
INSERT INTO categorias
VALUES (NULL, 'Eletrodomésticos', '2023-10-15');
1.3. INSERT com SELECT
Inserir dados a partir de uma consulta em outra tabela:

sql
INSERT INTO clientes_backup (nome, email)
SELECT nome, email FROM clientes WHERE cidade = 'Rio de Janeiro';
## 1.4. Valores Padrão e NULL
sql
-- Usar DEFAULT para valores padrão
INSERT INTO pedidos (cliente_id, data_pedido, status)
VALUES (1, '2023-10-15', DEFAULT);

-- Inserir NULL explicitamente
INSERT INTO clientes (nome, email, telefone)
VALUES ('Maria Santos', 'maria@email.com', NULL);
2. Atualização de Dados (UPDATE)
2.1. Sintaxe Básica do UPDATE
A instrução UPDATE modifica registros existentes em uma tabela.

Sintaxe:

sql
UPDATE nome_tabela
SET coluna1 = valor1, coluna2 = valor2, ...
WHERE condição;
2.2. Exemplos de UPDATE
sql
-- Atualizar um único registro
UPDATE clientes
SET cidade = 'Belo Horizonte'
WHERE id = 5;

-- Atualizar múltiplas colunas
UPDATE produtos
SET preço = preço * 0.9,  -- 10% de desconto
    estoque = estoque - 1
WHERE id = 10;

-- Atualizar com base em outra tabela
UPDATE pedidos
SET status = 'Enviado'
WHERE cliente_id IN (SELECT id FROM clientes WHERE cidade = 'São Paulo');

-- Atualizar todos os registros (CUIDADO!)
UPDATE configuracoes
SET ultima_atualizacao = CURRENT_TIMESTAMP;
2.3. UPDATE com JOIN (SQLite)
O SQLite não suporta JOIN diretamente no UPDATE, mas podemos usar subconsultas:

sql
-- Atualizar preços com base em outra tabela
UPDATE produtos
SET preço = preço * 1.1  -- Aumento de 10%
WHERE categoria_id IN (
    SELECT id FROM categorias WHERE nome = 'Eletrônicos'
);
3. Exclusão de Dados (DELETE)
3.1. Sintaxe Básica do DELETE
A instrução DELETE remove registros de uma tabela.

Sintaxe:

sql
DELETE FROM nome_tabela
WHERE condição;
3.2. Exemplos de DELETE
sql
-- Deletar um registro específico
DELETE FROM clientes
WHERE id = 15;

-- Deletar com condição complexa
DELETE FROM pedidos
WHERE data_pedido < '2023-01-01'
AND status = 'Cancelado';

-- Deletar todos os registros (CUIDADO EXTREMO!)
DELETE FROM tabela_temporaria;
3.3. DELETE com Subconsultas
sql
-- Deletar clientes sem pedidos
DELETE FROM clientes
WHERE id NOT IN (SELECT DISTINCT cliente_id FROM pedidos);

-- Deletar produtos de uma categoria específica
DELETE FROM produtos
WHERE categoria_id = (
    SELECT id FROM categorias WHERE nome = 'Obsoletos'
);
4. Transações
4.1. O que são Transações?
Transações garantem que uma série de operações seja executada completamente ou não seja executada nenhuma (princípio ACID).

4.2. Comandos de Transação
sql
-- Iniciar uma transação
BEGIN TRANSACTION;

-- Ou alternativamente (no SQLite)
BEGIN;
4.3. Exemplos de Transações
sql
-- Exemplo 1: Transferência bancária
BEGIN TRANSACTION;

UPDATE contas SET saldo = saldo - 100 WHERE id = 1;
UPDATE contas SET saldo = saldo + 100 WHERE id = 2;

-- Se tudo estiver correto
COMMIT;

-- Se ocorrer erro
ROLLBACK;
sql
-- Exemplo 2: Processamento de pedido
BEGIN;

INSERT INTO pedidos (cliente_id, total) VALUES (1, 250.00);
UPDATE produtos SET estoque = estoque - 1 WHERE id = 5;
UPDATE clientes SET ultimo_pedido = CURRENT_DATE WHERE id = 1;

COMMIT;
4.4. Savepoints (Pontos de Salvamento)
sql
BEGIN;

INSERT INTO tabela1 VALUES (...);
SAVEPOINT ponto1;

UPDATE tabela2 SET ...;
-- Se algo der errado no UPDATE
ROLLBACK TO ponto1;

-- Ou continuar
RELEASE ponto1;
COMMIT;
5. Boas Práticas de Manipulação de Dados
5.1. Prevenção de Acidentes
sql
-- SEMPRE teste com SELECT primeiro
SELECT * FROM clientes WHERE cidade = 'Rio de Janeiro';
-- Depois faça o UPDATE/DELETE
DELETE FROM clientes WHERE cidade = 'Rio de Janeiro';

-- Use transações para operações críticas
BEGIN;
DELETE FROM pedidos_antigos;
-- Verifique se está correto antes de COMMIT
ROLLBACK; -- ou COMMIT;
5.2. Performance em Múltiplas Inserções
sql
-- Inserções em lote são mais eficientes
BEGIN;
INSERT INTO tabela VALUES (...);
INSERT INTO tabela VALUES (...);
INSERT INTO tabela VALUES (...);
COMMIT;

-- Do que inserções individuais
INSERT INTO tabela VALUES (...);
INSERT INTO tabela VALUES (...);
INSERT INTO tabela VALUES (...);
5.3. Controle de Concorrência
O SQLite gerencia automaticamente a concorrência, mas transações explícitas ajudam:

sql
BEGIN EXCLUSIVE; -- Modo exclusivo para operações críticas
-- operações críticas
COMMIT;
6. Exemplos Práticos Completos
6.1. Sistema de Vendas
sql
-- Processar um novo pedido
BEGIN TRANSACTION;

-- 1. Criar o pedido
INSERT INTO pedidos (cliente_id, data_pedido, total)
VALUES (1, CURRENT_DATE, 0);

-- 2. Obter o ID do pedido recém-criado
.last_insert_rowid() -- Função do SQLite para pegar último ID

-- 3. Adicionar itens ao pedido
INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
VALUES 
    (last_insert_rowid(), 5, 2, 45.50),
    (last_insert_rowid(), 8, 1, 2500.00);

-- 4. Atualizar o total do pedido
UPDATE pedidos
SET total = (
    SELECT SUM(quantidade * preco_unitario) 
    FROM itens_pedido 
    WHERE pedido_id = last_insert_rowid()
)
WHERE id = last_insert_rowid();

-- 5. Atualizar estoque
UPDATE produtos SET estoque = estoque - 2 WHERE id = 5;
UPDATE produtos SET estoque = estoque - 1 WHERE id = 8;

COMMIT;
6.2. Manutenção de Dados
sql
-- Limpeza anual de dados antigos
BEGIN;

-- Backup dos dados antigos
INSERT INTO pedidos_arquivo
SELECT * FROM pedidos 
WHERE data_pedido < date('now', '-5 years');

-- Remover os dados antigos
DELETE FROM pedidos 
WHERE data_pedido < date('now', '-5 years');

-- Atualizar estatísticas
UPDATE estatisticas 
SET ultima_limpeza = CURRENT_TIMESTAMP;

COMMIT;
7. Exercícios Práticos
Exercício 1: Inserção de Dados
sql
-- 1. Insira 3 novos clientes
INSERT INTO clientes (nome, email, cidade) VALUES
('Ana Costa', 'ana@email.com', 'Rio de Janeiro'),
('Carlos Souza', 'carlos@email.com', 'Belo Horizonte'),
('Mariana Lima', 'mariana@email.com', 'São Paulo');

-- 2. Insira 5 produtos diferentes
INSERT INTO produtos (nome, preco, categoria) VALUES
('Tablet', 899.90, 'Eletrônicos'),
('Caderno', 15.50, 'Material'),
('Caneta', 2.50, 'Material'),
('Fone de Ouvido', 120.00, 'Acessórios'),
('Carregador', 45.00, 'Acessórios');
Exercício 2: Atualização de Dados
sql
-- 1. Aumente em 10% o preço de todos os eletrônicos
UPDATE produtos
SET preco = preco * 1.1
WHERE categoria = 'Eletrônicos';

-- 2. Mude a cidade de um cliente específico
UPDATE clientes
SET cidade = 'Porto Alegre'
WHERE email = 'ana@email.com';
Exercício 3: Exclusão com Transação
sql
-- 1. Remova todos os produtos sem estoque usando transação
BEGIN;
DELETE FROM produtos WHERE estoque <= 0;
COMMIT;

-- 2. Remova clientes inativos (sem pedidos nos últimos 2 anos)
BEGIN;
DELETE FROM clientes 
WHERE id NOT IN (
    SELECT DISTINCT cliente_id 
    FROM pedidos 
    WHERE data_pedido > date('now', '-2 years')
);
COMMIT;
8. Tratamento de Erros Comuns
8.1. Violação de Restrições
sql
-- Erro: Chave única duplicada
INSERT INTO clientes (id, nome) VALUES (1, 'João'); -- Se id=1 já existe

-- Solução: Use INSERT OR IGNORE ou INSERT OR REPLACE
INSERT OR IGNORE INTO clientes (id, nome) VALUES (1, 'João');
INSERT OR REPLACE INTO clientes (id, nome) VALUES (1, 'João');
8.2. Valores Nulos em Campos NOT NULL
sql
-- Erro: Campo obrigatório não preenchido
INSERT INTO clientes (nome) VALUES (NULL); -- Se nome é NOT NULL

-- Solução: Sempre forneça valores para campos NOT NULL
INSERT INTO clientes (nome, email) VALUES ('João', 'joao@email.com');

<sub>Documentação criada por **João Gonzaga** ([@Karmantinedev](https://github.com/Karmantinedev))</sub>