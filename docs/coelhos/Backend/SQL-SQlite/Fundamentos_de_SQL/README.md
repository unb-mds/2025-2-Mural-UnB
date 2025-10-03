## Introdução

SQL (Structured Query Language) é a linguagem padrão para comunicação com bancos de dados relacionais. Este guia cobre os conceitos fundamentais necessários para trabalhar eficientemente com SQL, com foco especial no SQLite.

1. Sintaxe Básica do SQL

## 1.1. SELECT - Recuperando Dados
A instrução [SELECT] é usada para consultar dados de uma tabela.

# Sintaxe básica:

SELECT coluna1, coluna2, ...
FROM nome_tabela;

# Exemplos:

-- Selecionar todas as colunas
SELECT * FROM clientes;

-- Selecionar colunas específicas
SELECT nome, email FROM clientes;

-- Usar aliases para renomear colunas
SELECT nome AS cliente_nome, email AS cliente_email FROM clientes;

## 1.2. FROM - Especificando a Tabela
A cláusula [FROM] indica de qual tabela os dados serão recuperados.

SELECT * FROM produtos;
SELECT nome, preço FROM pedidos;

## 1.3. WHERE - Filtrando Resultados
A cláusula [WHERE] filtra registros com base em condições específicas.

Operadores de comparação:

[=] Igual

[<>] ou != Diferente

[>] Maior que

[<] Menor que

[>=] Maior ou igual

[<=] Menor ou igual

[BETWEEN] Entre um intervalo

[LIKE] Padrão de texto

[IN] Especifica múltiplos valores possíveis

# Exemplos:

-- Igualdade
SELECT * FROM clientes WHERE cidade = 'São Paulo';

-- Maior que
SELECT * FROM produtos WHERE preço > 100.00;

-- BETWEEN
SELECT * FROM pedidos WHERE data BETWEEN '2023-01-01' AND '2023-01-31';

-- LIKE (correspondência de padrão)
SELECT * FROM clientes WHERE nome LIKE 'João%'; -- Começa com "João"
SELECT * FROM clientes WHERE email LIKE '%@gmail.com'; -- Termina com "@gmail.com"

-- IN (múltiplos valores)
SELECT * FROM produtos WHERE categoria IN ('Eletrônicos', 'Livros');

2. Cláusulas de Agregação

## 2.1. GROUP BY - Agrupando Dados
Agrupa linhas que têm os mesmos valores em colunas especificadas.

[SELECT] categoria, COUNT(*) as quantidade
[FROM] produtos
[GROUP BY] categoria;

## 2.2. HAVING - Filtrando Grupos
Filtra grupos baseados em condições (semelhante ao [WHERE], mas para grupos).

[SELECT] categoria, COUNT(*) as quantidade
[FROM] produtos
[GROUP BY] categoria
[HAVING] COUNT(*) > 5;

# Diferença entre WHERE e HAVING:

[WHERE] filtra linhas antes do agrupamento

[HAVING] filtra grupos depois do agrupamento

## 2.3. Funções de Agregação

COUNT()	Retorna o número de linhas
SUM()	Retorna a soma dos valores
AVG()	Retorna a média dos valores
MAX()	Retorna o valor máximo
MIN()	Retorna o valor mínimo

# Exemplos:

-- Contar total de clientes
SELECT COUNT(*) FROM clientes;

-- Média de preços por categoria
SELECT categoria, AVG(preço) as preço_médio
FROM produtos
GROUP BY categoria;

-- Maior e menor preço
SELECT MAX(preço) as preço_max, MIN(preço) as preço_min
FROM produtos;

3. Junções (JOINs)

## 3.1. INNER JOIN
Retorna registros que têm correspondência em ambas as tabelas.


[SELECT] pedidos.id, clientes.nome, pedidos.data
[FROM] pedidos
[INNER] JOIN clientes ON pedidos.cliente_id = clientes.id;

## 3.2. LEFT JOIN
Retorna todos os registros da tabela à esquerda e os correspondentes da tabela à direita.


[SELECT] clientes.nome, pedidos.id
[FROM] clientes
[LEFT] JOIN pedidos ON clientes.id = pedidos.cliente_id;

## 3.3. RIGHT JOIN e FULL OUTER JOIN
Nota: SQLite não suporta RIGHT JOIN ou FULL OUTER JOIN nativamente, mas podem ser simulados.

## 3.4. Múltiplos JOINs

[SELECT] pedidos.id, clientes.nome, produtos.nome as produto
[FROM] pedidos
[INNER JOIN] clientes ON pedidos.cliente_id = clientes.id
[INNER JOIN] itens_pedido ON pedidos.id = itens_pedido.pedido_id
[INNER JOIN] produtos ON itens_pedido.produto_id = produtos.id;

4. Subconsultas

## 4.1. Subconsultas na Cláusula WHERE

[SELECT] nome, preço
[FROM] produtos
[WHERE] preço > (SELECT AVG(preço) FROM produtos);

## 4.2. Subconsultas na Cláusula FROM

[SELECT] categoria, AVG(preço) as média_preço
[FROM] (SELECT * FROM produtos WHERE estoque > 0) as produtos_em_estoque
[GROUP BY] categoria;

## 4.3. Subconsultas Correlacionadas
Subconsultas que referenciam colunas da consulta externa.


[SELECT] nome, preço, 
       (SELECT AVG(preço) FROM produtos p2 WHERE p2.categoria = p1.categoria) as média_categoria
[FROM] produtos p1;

5. Ordenação e Limitação

## 5.1. ORDER BY - Ordenando Resultados

[SELECT] nome, preço
[FROM] produtos
[ORDER BY] preço DESC; -- Do maior para o menor preço

[SELECT] nome, data_nascimento
[FROM] clientes
[ORDER BY] data_nascimento ASC; -- Ordem cronológica
Ordenação por múltiplas colunas:


[SELECT] categoria, nome, preço
[FROM] produtos
[ORDER BY] categoria ASC, preço DESC;

## 5.2. LIMIT - Limitando Resultados

-- Os 10 produtos mais caros
[SELECT] nome, preço
[FROM] produtos
[ORDER BY] preço DESC
[LIMIT] 10;

-- Paginação (limite com offset)
[SELECT] nome, preço
[FROM] produtos
[ORDER BY] nome
[LIMIT] 10 OFFSET 20; -- Pula 20 registros, pega os próximos 10

6. Combinando Consultas

## 6.1. UNION e UNION ALL
Combinam resultados de duas ou mais consultas.


-- UNION (remove duplicatas)
[SELECT] nome FROM clientes
[UNION]
[SELECT] nome FROM fornecedores;

-- UNION ALL (mantém duplicatas)
[SELECT] nome FROM clientes
[UNION ALL]
[SELECT] nome FROM fornecedores;

## Exercícios Práticos

# Exercício 1: Consultas Básicas

-- 1. Selecione todos os clientes de São Paulo
SELECT * FROM clientes WHERE cidade = 'São Paulo';

-- 2. Encontre produtos com preço entre R$ 50 e R$ 100
SELECT * FROM produtos WHERE preço BETWEEN 50 AND 100;

-- 3. Liste os 5 produtos mais caros
SELECT nome, preço FROM produtos ORDER BY preço DESC LIMIT 5;
Exercício 2: Agregações

-- 1. Conte quantos pedidos cada cliente fez
SELECT cliente_id, COUNT(*) as total_pedidos
FROM pedidos
GROUP BY cliente_id;

-- 2. Encontre a média de preço por categoria
SELECT categoria, AVG(preço) as preço_médio
FROM produtos
GROUP BY categoria;

-- 3. Categorias com mais de 10 produtos
SELECT categoria, COUNT(*) as quantidade
FROM produtos
GROUP BY categoria
HAVING COUNT(*) > 10;
Exercício 3: JOINs

-- 1. Liste todos os pedidos com nome do cliente
SELECT pedidos.*, clientes.nome as cliente_nome
FROM pedidos
INNER JOIN clientes ON pedidos.cliente_id = clientes.id;

-- 2. Produtos que nunca foram vendidos
SELECT produtos.*
FROM produtos
LEFT JOIN itens_pedido ON produtos.id = itens_pedido.produto_id
WHERE itens_pedido.produto_id IS NULL;

<sub>Documentação criada por **João Gonzaga** ([@Karmantinedev](https://github.com/Karmantinedev))</sub>