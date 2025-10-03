# SQLite Específico - Guia Completo

## Introdução

O SQLite é um banco de dados embutido com características únicas que o diferenciam de outros sistemas de gerenciamento de banco de dados. Este guia cobre aspectos específicos do SQLite, incluindo funções built-in, limitações, extensões e operações de manutenção.

## 1. Funções Built-in do SQLite

### 1.1. Funções de Data e Hora

**Funções principais:**
```sql
-- Data e hora atual
SELECT datetime('now');        -- 2023-12-07 15:30:45
SELECT date('now');            -- 2023-12-07
SELECT time('now');            -- 15:30:45

-- Com timezone (UTC)
SELECT datetime('now', 'utc'); -- 2023-12-07 18:30:45

-- Manipulação de datas
SELECT date('now', '+1 day');     -- Amanhã
SELECT date('now', '-1 month');   -- Mês passado
SELECT datetime('now', '+3 hours', '-30 minutes');

-- Formatação personalizada
SELECT strftime('%Y-%m-%d %H:%M:%S', 'now');
SELECT strftime('%d/%m/%Y', 'now');  -- 07/12/2023
Exemplos práticos:

sql
-- Idade a partir da data de nascimento
SELECT nome, 
       date('now') - data_nascimento AS idade_aproximada,
       (julianday('now') - julianday(data_nascimento)) / 365.25 AS idade_exata
FROM clientes;

-- Pedidos dos últimos 30 dias
SELECT * FROM pedidos 
WHERE data_pedido >= date('now', '-30 days');

-- Agrupar por semana
SELECT strftime('%Y-%W', data_pedido) AS semana,
       COUNT(*) AS total_pedidos
FROM pedidos
GROUP BY semana;
1.2. Funções Matemáticas
sql
-- Funções básicas
SELECT ABS(-15);              -- 15
SELECT ROUND(3.14159, 2);     -- 3.14
SELECT RANDOM();              -- Número aleatório
SELECT RANDOM() % 100;        -- Número entre 0-99

-- Funções avançadas
SELECT MAX(10, 20, 5);        -- 20
SELECT MIN(10, 20, 5);        -- 5
SELECT COALESCE(NULL, NULL, 'valor', NULL); -- 'valor'

-- Exemplos com dados
SELECT produto, 
       preco,
       ROUND(preco * 0.9, 2) AS preco_com_desconto,
       CEIL(preco) AS preco_arredondado
FROM produtos;
1.3. Funções de Agregação
Além das funções SQL padrão, SQLite tem algumas particularidades:

sql
-- GROUP_CONCAT - Concatena valores do grupo
SELECT departamento, 
       GROUP_CONCAT(nome, ', ') AS funcionarios
FROM empregados
GROUP BY departamento;

-- Total aggregates
SELECT TOTAL(preco) AS soma_total FROM vendas;  -- Sempre retorna REAL
SELECT SUM(preco) AS soma FROM vendas;          -- Retorna INTEGER se possível

-- Statistical functions (com extensão math)
SELECT AVG(salario) AS media_salarial,
       COUNT(*) AS total_funcionarios,
       MAX(salario) AS maior_salario,
       MIN(salario) AS menor_salario
FROM funcionarios;
1.4. Funções de Texto
sql
-- Manipulação de strings
SELECT LENGTH('SQLite');           -- 6
SELECT LOWER('SQLite');            -- 'sqlite'
SELECT UPPER('sqlite');            -- 'SQLITE'
SELECT SUBSTR('SQLite', 1, 3);     -- 'SQL'
SELECT REPLACE('Hello World', 'World', 'SQLite'); -- 'Hello SQLite'

-- Busca e posição
SELECT INSTR('SQLite', 'Lite');    -- 3
SELECT TRIM('   SQLite   ');       -- 'SQLite'
SELECT LTRIM('   SQLite');         -- 'SQLite'
SELECT RTRIM('SQLite   ');         -- 'SQLite'

-- Exemplo prático: extrair domínio de email
SELECT email,
       SUBSTR(email, INSTR(email, '@') + 1) AS dominio
FROM usuarios;
2. Tipos de Armazenamento e Limitações
2.1. Sistema de Tipagem Dinâmica
SQLite usa tipagem dinâmica (manifest typing):

sql
CREATE TABLE exemplo_tipagem (
    id INTEGER,
    qualquer_dado
);

INSERT INTO exemplo_tipagem VALUES (1, 100);       -- INTEGER
INSERT INTO exemplo_tipagem VALUES (2, 3.14);      -- REAL
INSERT INTO exemplo_tipagem VALUES (3, 'Texto');   -- TEXT
INSERT INTO exemplo_tipagem VALUES (4, NULL);      -- NULL
INSERT INTO exemplo_tipagem VALUES (5, x'0001');   -- BLOB
2.2. Limitações do SQLite
Limites conhecidos:

sql
-- Tamanho máximo do banco: ~140 TB
-- Tamanho máximo de texto: 1 bilhão de caracteres
-- Tamanho máximo de BLOB: 2.1 GB
-- Colunas por tabela: 2000
-- Tamanho máximo de SQL: 1 milhão de bytes

-- Verificar limites
PRAGMA page_size;          -- Tamanho da página (1024-65536)
PRAGMA max_page_count;     -- Número máximo de páginas
PRAGMA encoding;           -- UTF-8 ou UTF-16
2.3. Gerenciamento de Memória
sql
-- Configurações de cache
PRAGMA cache_size = -2000;   -- 2000 páginas em cache (cerca de 2MB)
PRAGMA temp_store = MEMORY;  -- Armazenar temporários em memória

-- Otimização de desempenho
PRAGMA journal_mode = WAL;   -- Write-Ahead Logging (recomendado)
PRAGMA synchronous = NORMAL; -- Balance entre segurança e performance

-- Ver estatísticas de memória
PRAGMA memory_map_size = 0;      -- Desativar memory mapping
PRAGMA mmap_size = 268435456;    -- 256MB para memory mapping
3. Backup e Recuperação
3.1. Métodos de Backup
Backup usando SQLite Online Backup API:

sql
-- Backup programático (exemplo em Python)
import sqlite3

def backup_database(src_db, dst_db):
    src = sqlite3.connect(src_db)
    dst = sqlite3.connect(dst_db)
    
    with dst:
        src.backup(dst)
    
    src.close()
    dst.close()

# Uso
backup_database('prod.db', 'backup.db')
Backup via Command Line:

bash
# Backup completo
sqlite3 database.db .dump > backup.sql

# Backup apenas esquema
sqlite3 database.db .schema > schema_backup.sql

# Backup apenas dados
sqlite3 database.db .dump --data-only > data_backup.sql

# Backup incremental usando .dump com WHERE
sqlite3 database.db "SELECT * FROM pedidos WHERE data > '2023-01-01'" > pedidos_recentes.sql
3.2. Recuperação de Dados
sql
-- Restaurar de arquivo SQL
sqlite3 restored.db < backup.sql

-- Restaurar apenas dados específicos
sqlite3 database.db
.read data_backup.sql

-- Recuperação de dados excluídos acidentalmente
-- (Requer ferramentas externas como sqlite3_undrop)
3.3. Estratégias de Backup
Backup Automatizado:

sql
-- Script de backup com timestamp
.backup /var/backups/db_backup_$(date +%Y%m%d_%H%M%S).db

-- Backup com retenção (exemplo em shell)
#!/bin/bash
BACKUP_DIR="/var/backups"
DB_FILE="/app/data/database.db"
RETENTION_DAYS=7

# Criar backup
sqlite3 $DB_FILE ".backup '$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).db'"

# Limpar backups antigos
find $BACKUP_DIR -name "backup_*.db" -mtime +$RETENTION_DAYS -delete
4. Extensões do SQLite
4.1. Extensão JSON (JSON1)
Funções JSON disponíveis:

sql
-- Extrair dados JSON
SELECT json_extract('{"nome": "João", "idade": 30}', '$.nome'); -- 'João'

-- Consultar dados JSON em colunas
SELECT id, 
       json_extract(dados_json, '$.email') AS email,
       json_extract(dados_json, '$.endereco.cidade') AS cidade
FROM usuarios;

-- Funções JSON completas
SELECT json('{"id": 1, "nome": "Teste"}');
SELECT json_object('id', 1, 'nome', 'João');
SELECT json_array(1, 2, 3);
SELECT json_group_array(nome) FROM clientes;
Exemplo prático com JSON:

sql
-- Armazenar dados flexíveis
CREATE TABLE configuracoes (
    id INTEGER PRIMARY KEY,
    chave TEXT UNIQUE,
    valor_json TEXT
);

INSERT INTO configuracoes VALUES 
(1, 'usuario', '{"nome": "admin", "permissoes": ["read", "write"]}');

-- Consultar dados JSON
SELECT json_extract(valor_json, '$.permissoes[0]') AS permissao
FROM configuracoes
WHERE chave = 'usuario';
4.2. Full-Text Search (FTS5)
Criando tabelas de busca textual:

sql
-- Tabela FTS5
CREATE VIRTUAL TABLE documentos USING fts5(
    titulo,
    conteudo,
    autor
);

-- Inserir dados
INSERT INTO documentos VALUES 
('Introdução ao SQLite', 'SQLite é um banco de dados...', 'Autor1'),
('Busca Full-Text', 'FTS5 permite buscas avançadas...', 'Autor2');

-- Buscar texto
SELECT * FROM documentos WHERE documentos MATCH 'SQLite';
SELECT * FROM documentos WHERE titulo MATCH 'introdução';

-- Buscas avançadas
SELECT * FROM documentos WHERE documentos MATCH 'SQLite OR FTS5';
SELECT * FROM documentos WHERE documentos MATCH 'titulo:SQLite';
SELECT * FROM documentos WHERE documentos MATCH 'conteudo:banco NEAR dados';
4.3. Outras Extensões Úteis
Math Extension:

sql
-- Habilitar extensão matemática
.load /usr/lib/sqlite3/libmath.so

-- Funções matemáticas avançadas
SELECT sin(radians(30));     -- Seno de 30 graus
SELECT log10(100);           -- Logaritmo base 10
SELECT power(2, 8);          -- 2^8 = 256
Regex Extension:

sql
-- Habilitar regex
.load /usr/lib/sqlite3/libregexp.so

-- Usar regex em consultas
SELECT * FROM usuarios WHERE email REGEXP '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$';
SELECT * FROM produtos WHERE nome REGEXP '^[A-Z]';
5. Recursos Avançados
5.1. Common Table Expressions (CTEs)
sql
-- CTE recursiva (hierarquia)
WITH RECURSIVE hierarquia AS (
    -- Caso base
    SELECT id, nome, supervisor_id, 1 as nivel
    FROM funcionarios
    WHERE supervisor_id IS NULL
    
    UNION ALL
    
    -- Caso recursivo
    SELECT f.id, f.nome, f.supervisor_id, h.nivel + 1
    FROM funcionarios f
    JOIN hierarquia h ON f.supervisor_id = h.id
)
SELECT * FROM hierarquia ORDER BY nivel, nome;

-- CTE para queries complexas
WITH vendas_por_mes AS (
    SELECT strftime('%Y-%m', data) as mes,
           SUM(total) as total_vendas
    FROM pedidos
    GROUP BY mes
),
media_movel AS (
    SELECT mes,
           total_vendas,
           AVG(total_vendas) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as media_3meses
    FROM vendas_por_mes
)
SELECT * FROM media_movel;
5.2. Window Functions
sql
-- Funções de janela
SELECT nome, 
       departamento,
       salario,
       RANK() OVER (PARTITION BY departamento ORDER BY salario DESC) as ranking,
       AVG(salario) OVER (PARTITION BY departamento) as media_departamento,
       SUM(salario) OVER (ORDER BY data_contratacao) as soma_acumulativa
FROM funcionarios;

-- Paginação eficiente
SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY data_criacao DESC) as row_num
    FROM artigos
) WHERE row_num BETWEEN 11 AND 20;
5.3. Triggers Avançados
sql
-- Trigger para histórico de alterações
CREATE TABLE historico_precos (
    id INTEGER PRIMARY KEY,
    produto_id INTEGER,
    preco_antigo REAL,
    preco_novo REAL,
    data_alteracao DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario TEXT
);

CREATE TRIGGER trg_historico_preco
AFTER UPDATE OF preco ON produtos
FOR EACH ROW
WHEN OLD.preco <> NEW.preco
BEGIN
    INSERT INTO historico_precos (produto_id, preco_antigo, preco_novo, usuario)
    VALUES (OLD.id, OLD.preco, NEW.preco, 'sistema');
END;
6. Performance e Otimização
6.1. Análise de Desempenho
sql
-- Habilitar profiling
.timer on
.echo on

-- Analisar query plan
EXPLAIN QUERY PLAN
SELECT * FROM pedidos 
WHERE cliente_id = 100 
ORDER BY data_pedido DESC;

-- Statistics
ANALYZE;
SELECT * FROM sqlite_stat1;
6.2. Otimizações Específicas
sql
-- Configurações para performance
PRAGMA optimize;                  -- Otimização automática
PRAGMA automatic_index = ON;      -- Índices automáticos
PRAGMA busy_timeout = 3000;       -- Timeout de 3 segundos

-- Para operações em lote
BEGIN TRANSACTION;
-- Múltiplas operações
COMMIT;

-- Usar índices covering
CREATE INDEX idx_pedidos_covering ON pedidos(cliente_id, data_pedido, status);
7. Exercícios Práticos
Exercício 1: Funções de Data
sql
-- Calcular idade exata dos clientes
SELECT nome, 
       data_nascimento,
       FLOOR((julianday('now') - julianday(data_nascimento)) / 365.25) AS idade
FROM clientes;

-- Pedidos do mês atual
SELECT * FROM pedidos 
WHERE strftime('%Y-%m', data_pedido) = strftime('%Y-%m', 'now');
Exercício 2: Full-Text Search
sql
-- Criar índice de busca para artigos
CREATE VIRTUAL TABLE artigos_fts USING fts5(titulo, conteudo);

-- Popular com dados
INSERT INTO artigos_fts 
SELECT id, titulo, conteudo FROM artigos;

-- Buscar artigos sobre "banco de dados"
SELECT * FROM artigos_fts 
WHERE artigos_fts MATCH 'banco NEAR dados';
Exercício 3: Backup e Recovery
bash
# Script de backup automatizado
#!/bin/bash
DB="app.db"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Criar backup
sqlite3 $DB ".backup '$BACKUP_DIR/${DB}_${TIMESTAMP}.bak'"

# Manter apenas últimos 7 backups
ls -t $BACKUP_DIR/*.bak | tail -n +8 | xargs rm -f */

<sub>Documentação criada por **João Gonzaga** ([@Karmantinedev](https://github.com/Karmantinedev))</sub>