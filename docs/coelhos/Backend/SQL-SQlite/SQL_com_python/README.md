# SQL com Python - Guia Completo de Integração

## Introdução

A integração entre SQLite e Python é uma das mais simples e poderosas combinações para desenvolvimento de aplicações com banco de dados. Este guia cobre o uso do módulo `sqlite3` da biblioteca padrão Python, boas práticas de segurança e padrões avançados de integração.

## 1. Módulo sqlite3 da Biblioteca Padrão

### 1.1. Conexão Básica com o Banco de Dados

**Estabelecendo conexão:**
```python
import sqlite3
import os

# Conexão básica
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Conexão em memória (ótima para testes)
conn_memory = sqlite3.connect(':memory:')

# Conexão com configurações específicas
conn = sqlite3.connect(
    'app.db',
    timeout=30,  # Timeout de 30 segundos
    detect_types=sqlite3.PARSE_DECLTYPES  # Detectar tipos Python
)
Gerenciamento de contexto (recomendado):

python
# Usando context manager para conexão
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

# Conexão é automaticamente fechada ao sair do bloco
1.2. Executando Consultas Básicas
Operações CRUD:

python
# CREATE - Inserindo dados
def create_user(name, email):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        return cursor.lastrowid

# READ - Consultando dados
def get_users():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        return cursor.fetchall()

# UPDATE - Atualizando dados
def update_user_email(user_id, new_email):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET email = ? WHERE id = ?",
            (new_email, user_id)
        )
        conn.commit()
        return cursor.rowcount

# DELETE - Removendo dados
def delete_user(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount
2. Prevenção de SQL Injection
2.1. O Problema do SQL Injection
❌ NUNCA faça isso:

python
# Código vulnerável a SQL injection
def get_user_unsafe(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # ⚠️ PERIGO: Concatenção direta de strings
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # Vulnerável a injection
    
    return cursor.fetchall()

# Exemplo de ataque:
# username = "admin' OR '1'='1"
# Query resultante: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
2.2. Usando Parâmetros com Placeholders
✅ SEMPRE use placeholders:

python
# Método seguro usando placeholders
def get_user_safe(username):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        
        # Usando ? como placeholder
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)  # Tuple com parâmetros
        )
        
        return cursor.fetchall()

# Método seguro com named placeholders
def update_user_safe(user_id, **fields):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        query = f"UPDATE users SET {set_clause} WHERE id = :id"
        
        # Usando dicionário de parâmetros
        params = fields.copy()
        params['id'] = user_id
        
        cursor.execute(query, params)
        conn.commit()
2.3. Validação de Entrada
python
import re

def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_input(data):
    """Valida dados de entrada"""
    if not isinstance(data, str):
        return False
    
    # Remove caracteres potencialmente perigosos
    data = data.strip()
    if not data:
        return False
    
    return True

def safe_query(query, params):
    """Executa query com validação"""
    if not all(validate_input(str(p)) for p in params if p is not None):
        raise ValueError("Parâmetros inválidos")
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
3. Context Managers para Gerenciamento de Conexões
3.1. Classe de Gerenciamento de Database
python
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, database_path):
        self.database_path = database_path
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões"""
        conn = None
        try:
            conn = sqlite3.connect(
                self.database_path,
                timeout=30,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            conn.execute("PRAGMA foreign_keys = ON")  # Habilitar FK
            yield conn
        except sqlite3.Error as e:
            print(f"Erro de database: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self):
        """Context manager para cursor"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise

# Uso da classe
db = DatabaseManager('app.db')

with db.get_cursor() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
3.2. Decorator para Transações
python
def with_transaction(func):
    """Decorator para gerenciar transações automaticamente"""
    def wrapper(self, *args, **kwargs):
        with self.get_connection() as conn:
            try:
                result = func(self, conn, *args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e
    return wrapper

class UserRepository:
    def __init__(self, db_manager):
        self.db = db_manager
    
    @with_transaction
    def create_user(self, conn, name, email):
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        return cursor.lastrowid
    
    @with_transaction
    def get_users(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
4. Conversão de Resultados para Estruturas Python
4.1. Row Factory para Objetos Python
python
# Converter rows para dicionários
def dict_factory(cursor, row):
    """Converte resultados para dicionários"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

# Converter rows para namedtuples
from collections import namedtuple

def namedtuple_factory(cursor, row):
    """Converte resultados para namedtuples"""
    fields = [column[0] for column in cursor.description]
    Row = namedtuple('Row', fields)
    return Row(*row)

# Usando row factories
conn = sqlite3.connect('database.db')
conn.row_factory = dict_factory  # ou namedtuple_factory

cursor = conn.cursor()
cursor.execute("SELECT id, name, email FROM users")
users = cursor.fetchall()  # Lista de dicionários ou namedtuples
4.2. Mapeamento para Classes Python
python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data):
        """Cria User a partir de dicionário"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
    
    def to_dict(self):
        """Converte User para dicionário"""
        return {
            'name': self.name,
            'email': self.email
        }

class UserRepository:
    def __init__(self, db_manager):
        self.db = db_manager
        self.db.conn.row_factory = dict_factory
    
    def get_user(self, user_id):
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            data = cursor.fetchone()
            return User.from_dict(data) if data else None
    
    def save_user(self, user):
        with self.db.get_cursor() as cursor:
            if user.id:
                # Update
                cursor.execute(
                    "UPDATE users SET name = ?, email = ? WHERE id = ?",
                    (user.name, user.email, user.id)
                )
            else:
                # Insert
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (user.name, user.email)
                )
                user.id = cursor.lastrowid
        return user
4.3. Conversão de Tipos de Dados
python
import json
from datetime import datetime

# Registrar adaptadores e conversores
def adapt_datetime(dt):
    """Adapta datetime para string ISO"""
    return dt.isoformat()

def convert_datetime(text):
    """Converte string para datetime"""
    return datetime.fromisoformat(text.decode() if isinstance(text, bytes) else text)

# Registrar conversores
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)

# Para dados JSON
def adapt_json(data):
    return json.dumps(data)

def convert_json(text):
    return json.loads(text)

sqlite3.register_adapter(dict, adapt_json)
sqlite3.register_adapter(list, adapt_json)
sqlite3.register_converter("JSON", convert_json)
5. Padrões Avançados e Boas Práticas
5.1. Repository Pattern
python
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseRepository(ABC):
    @abstractmethod
    def get(self, id):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def create(self, entity):
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass

class UserRepository(BaseRepository):
    def __init__(self, db_manager):
        self.db = db_manager
        self.table = "users"
    
    def get(self, user_id: int) -> Optional[User]:
        with self.db.get_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (user_id,))
            data = cursor.fetchone()
            return User.from_dict(data) if data else None
    
    def get_all(self) -> List[User]:
        with self.db.get_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table}")
            return [User.from_dict(row) for row in cursor.fetchall()]
    
    def create(self, user: User) -> User:
        with self.db.get_cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self.table} (name, email) VALUES (?, ?)",
                (user.name, user.email)
            )
            user.id = cursor.lastrowid
            return user
    
    def update(self, user: User) -> User:
        with self.db.get_cursor() as cursor:
            cursor.execute(
                f"UPDATE {self.table} SET name = ?, email = ? WHERE id = ?",
                (user.name, user.email, user.id)
            )
            return user
    
    def delete(self, user_id: int) -> bool:
        with self.db.get_cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.table} WHERE id = ?", (user_id,))
            return cursor.rowcount > 0
5.2. Migrações de Esquema
python
import os
from pathlib import Path

class MigrationManager:
    def __init__(self, db_manager, migrations_dir="migrations"):
        self.db = db_manager
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
    
    def create_migration(self, name):
        """Cria novo arquivo de migração"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.migrations_dir / f"{timestamp}_{name}.sql"
        
        with open(filename, 'w') as f:
            f.write("-- Migration: {name}\n")
            f.write("BEGIN TRANSACTION;\n\n")
            f.write("-- Suas alterações de schema aqui\n\n")
            f.write("COMMIT;\n")
        
        return filename
    
    def run_migrations(self):
        """Executa migrações pendentes"""
        with self.db.get_connection() as conn:
            self._ensure_migrations_table(conn)
            
            applied_migrations = self._get_applied_migrations(conn)
            migration_files = sorted(self.migrations_dir.glob("*.sql"))
            
            for migration_file in migration_files:
                if migration_file.name not in applied_migrations:
                    self._apply_migration(conn, migration_file)
    
    def _ensure_migrations_table(self, conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY,
                filename TEXT UNIQUE,
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def _get_applied_migrations(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM migrations")
        return {row[0] for row in cursor.fetchall()}
    
    def _apply_migration(self, conn, migration_file):
        with open(migration_file, 'r') as f:
            sql_script = f.read()
        
        try:
            conn.executescript(sql_script)
            conn.execute(
                "INSERT INTO migrations (filename) VALUES (?)",
                (migration_file.name,)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Migration failed: {migration_file.name}") from e
5.3. Logging e Monitoramento
python
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingCursor:
    """Cursor com logging de queries"""
    def __init__(self, cursor):
        self.cursor = cursor
    
    def execute(self, query, params=None):
        start_time = time.time()
        
        try:
            if params:
                result = self.cursor.execute(query, params)
            else:
                result = self.cursor.execute(query)
            
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # ms
            
            logger.info(f"Query executed: {query[:100]}... [Duration: {duration:.2f}ms]")
            return result
        except Exception as e:
            logger.error(f"Query failed: {query} - Error: {e}")
            raise
    
    def __getattr__(self, name):
        return getattr(self.cursor, name)

class LoggingConnection:
    """Conexão com logging"""
    def __init__(self, connection):
        self.connection = connection
    
    def cursor(self):
        return LoggingCursor(self.connection.cursor())
    
    def __getattr__(self, name):
        return getattr(self.connection, name)

# Uso
conn = sqlite3.connect('database.db')
logging_conn = LoggingConnection(conn)
6. Exemplos Completos
6.1. Aplicação Completa de Blog
python
import sqlite3
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Post:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    author_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BlogDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializa o banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def create_post(self, post: Post) -> Post:
        """Cria um novo post"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
                (post.title, post.content, post.author_id)
            )
            post.id = cursor.lastrowid
            return post
    
    def get_posts(self, limit: int = 10) -> List[Post]:
        """Obtém posts recentes"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM posts ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
            return [Post(**dict(row)) for row in cursor.fetchall()]

# Uso
blog_db = BlogDatabase('blog.db')
new_post = Post(title="Hello SQLite", content="Content here", author_id=1)
created_post = blog_db.create_post(new_post)
posts = blog_db.get_posts()
6.2. Sistema de Autenticação
python
import hashlib
import secrets
from typing import Optional

class AuthSystem:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """Cria usuário com senha hasheada"""
        salt = secrets.token_hex(16)
        hashed_password = self._hash_password(password, salt)
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (username, password_hash, salt, email)
                       VALUES (?, ?, ?, ?)""",
                    (username, hashed_password, salt, email)
                )
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verifica credenciais do usuário"""
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "SELECT password_hash, salt FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            
            if not result:
                return False
            
            stored_hash, salt = result
            input_hash = self._hash_password(password, salt)
            
            return secrets.compare_digest(stored_hash, input_hash)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Gera hash da senha"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # Número de iterações
        ).hex()
7. Exercícios Práticos
Exercício 1: CRUD Completo
python
# Implementar CRUD para produtos
class ProductRepository:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_product(self, name: str, price: float, category: str):
        # Implementar criação
        pass
    
    def get_products_by_category(self, category: str):
        # Implementar busca por categoria
        pass
    
    def update_product_price(self, product_id: int, new_price: float):
        # Implementar atualização
        pass
    
    def delete_product(self, product_id: int):
        # Implementar exclusão
        pass

<sub>Documentação criada por **João Gonzaga** ([@Karmantinedev](https://github.com/Karmantinedev))</sub>