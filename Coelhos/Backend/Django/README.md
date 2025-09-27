# Estrutura de um projeto Django (MTV)

No Django, o padrão clássico **MVC (Model–View–Controller)** é interpretado de forma diferente, resultando no padrão **MTV (Model–Template–View)**.  
O “controller” do MVC, no Django, é o próprio **framework**, que recebe a requisição e a direciona para a view correta com base nas configurações de URL.

---

### Configuração inicial e boas práticas de organização

# Criar ambiente virtual
```bash
python3 -m venv .venv
```
# Ativar ambiente virtual
# Linux/Mac
```bash
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```
# Instalar Django dentro do ambiente
```bash
python3 -m pip install Django
```
# Verificar versão instalada
```bash
python3 -m django --version
```
# Criação de app 
```bash
python manage.py startapp nome_app
```
# Boas práticas
# 1. Usar .env para credenciais e configs sensíveis
# 2. Manter requirements.txt atualizado
pip freeze > requirements.txt; lista tudo que tá instalado no teu ambiente virtual (Django, libs extras, etc.) e salva dentro desse arquivo.
# 3. Criar apps para dividir responsabilidades (ex: users, events, payments)
# 4. Configurar settings separados (dev, prod) quando o projeto crescer
# 5. Usar migrations sempre que alterar modelos
São scripts automáticos que o Django gera pra manter o banco de dados sincronizado com os seus modelos (models.py).
python manage.py makemigrations, Roda-o;
python manage.py migrate, aplica no banco
# Exemplo prático
```bash
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
```
# Resumo: migrations = ponte entre o código Python (models) e o banco de dados real.
# 6. Criar superusuário para acessar o admin
```bash
python manage.py createsuperuser
```
# 7. Testar o projeto antes de subir alterações
```bash
python manage.py test
```
## Models e ORM (Banco de Dados com SQLite)

### Banco de Dados com SQLite

- Por padrão, o Django usa **SQLite**, que já vem incluído no Python.
- Isso elimina a necessidade de instalar ou configurar sistemas de banco de dados.
- Para criar as tabelas necessárias (apps do usuário e apps padrão do Django), basta rodar:

```bash
python manage.py migrate
```

Esse comando analisa todos os apps ativados em `INSTALLED_APPS` e cria as tabelas adequadas no banco.

---

### Models no Django

- Um **Model** é a representação de uma estrutura de dados (tabela) no banco.
- Ele é definido como uma **classe Python** que herda de `django.db.models.Model`.
- Cada atributo da classe corresponde a uma **coluna** no banco de dados.

**Exemplo clássico (tutorial polls):**

```python
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

- Uma **pergunta** tem texto e data de publicação.
- Cada **opção** está ligada a uma pergunta, com texto e contagem de votos.
- O Django gera automaticamente nomes de tabelas (`app_modelname`), campos, chaves primárias e tipos específicos.

---

### ORM — Object-Relational Mapper

- O **ORM do Django** permite interagir com o banco de dados usando **Python ao invés de SQL**.
- Facilita operações CRUD: **criar, ler, atualizar, deletar** registros.

**Exemplo no shell interativo:**

```python
# Criar uma pergunta
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()

# Acessar dados
q.id
q.question_text

# Listar todas as perguntas
Question.objects.all()
```

- O ORM gera **migrações** com `makemigrations` e aplica ao banco com `migrate`.
- As migrações são **versionáveis** e mantêm o histórico de alterações.

---

## Views e URLs (Rotas e Lógica do Backend)

### Views

- Uma **View** é uma função (ou classe) Python que recebe um `request` e retorna um `response`.
- O retorno pode ser: **HTML, redirecionamento, JSON, imagem, erro 404**, etc.

**Exemplo do tutorial polls:**

- `index`: lista as últimas perguntas.
- `detail`: mostra os detalhes de uma pergunta específica.
- `results`: exibe resultados das votações.
- `vote`: processa um voto.

As views geralmente:

1. Buscam dados dos Models.
2. Processam formulários.
3. Retornam o conteúdo via `HttpResponse`.

---

### URLs e Rotas (URLconf)

- O **URLconf** é um módulo `urls.py` que define uma lista `urlpatterns`.
- Cada entrada mapeia um padrão de URL para uma View.

**Exemplo (`polls/urls.py`):**

```python
urlpatterns = [
    path("", views.index, name="index"),                       # /polls/
    path("<int:question_id>/", views.detail, name="detail"),   # /polls/5/
    path("<int:question_id>/results/", views.results, name="results"), # /polls/5/results/
    path("<int:question_id>/vote/", views.vote, name="vote"),  # /polls/5/vote/
]
```

---

## Templates e Renderização

### Templates no Django

- Arquivos de texto (normalmente **HTML**) que misturam conteúdo estático com **dados dinâmicos**.
- Usam a **linguagem de templates do Django (DTL)**.

**Exemplo de recursos:**

- Variáveis: `{{ variavel }}`
- Tags de controle: `{% if ... %}`, `{% for ... %}`
- Filtros, comentários, etc.

---

### Estrutura de Pastas

```
polls/
    templates/
        polls/
            index.html
```

**Exemplo (`index.html`):**

```html
{% if latest_question_list %}
<ul>
  {% for question in latest_question_list %}
  <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
  {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}
```

---

### Renderização na View

A view prepara o contexto (dicionário de dados) e renderiza:

```python
return render(request, "polls/index.html", context)
```

Isso gera um `HttpResponse` com o HTML final.

---

### Renderização como API

- **HTML tradicional:** usa-se o sistema de templates conforme descrito acima, adequado para páginas web.
- **APIs JSON:** normalmente não se usa templates. Em aplicações Django tradicionais, você retornaria algo como `JsonResponse(...)`.
- Com **Django REST Framework (DRF)**, usam-se **Renderers** (ex: `JSONRenderer`) para gerar JSON.

---

## Django Admin

### O que é?

- Interface administrativa **automática** gerada pelo Django para permitir que administradores (como editores ou gerentes de conteúdo) criem, atualizem e apaguem dados dos seus modelos de forma rápida e sem necessidade de programar formulários ou views.
- Essa interface não é voltada para usuários públicos do site, mas sim para gente da equipe que precisa gerenciar o conteúdo.

---

### Como ativar

1. O app `django.contrib.admin` já está ativo por padrão.
2. Criar superusuário:
   ```bash
   python manage.py createsuperuser
   ```
3. Acessar no navegador:
   ```
   http://127.0.0.1:8000/admin/
   ```
4. Registrar os Models em `admin.py`:

```python
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

---

## Autenticação e Autorização

### Autenticação (Authentication)

- Processo de **verificar a identidade do usuário** (ex: login com usuário e senha).
- O Django oferece:
  - Modelos para usuários, grupos e permissões.
  - Hashing seguro de senhas.
  - Views prontas para login/logout.
  - Backends de autenticação customizáveis.

---

### Autorização (Authorization)

- Define **o que um usuário autenticado pode fazer** na aplicação.
- Baseada em **permissões** associadas a modelos (ex: adicionar, alterar, deletar).
- Permissões podem ser atribuídas a **usuários ou grupos**.

**Exemplo:**

```python
if user.has_perm("polls.add_choice"):
    # Usuário pode adicionar uma escolha
```

### Criação de APIs com Django REST Framework (DRF)

## Instalação
```bash
pip install djangorestframework
```
# No settings.py, adicione em INSTALLED_APPS:
```bash
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```
# Serializers
Transformam models em JSON (e vice-versa).
# Exemplo Prático
```bash
from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]
```
# Views para API
DRF oferece ViewSets e APIView para lidar com requisições.
# Exemplo usando ModelViewSet:
```bash
from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
```
# URLs com DRF Router
DRF tem routers que criam rotas automaticamente.
# Exemplo simples
```bash
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
```
# Testando a API
```bash
python manage.py runserver
```
# Navegador
http://127.0.0.1:8000/api/questions/


### Deploy de aplicações Django

# Preparar o ambiente
```bash
pip install -r requirements.txt
```
# Configurar banco de dados
Settings.py:
```bash
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```
O banco é só o arquivo .sqlite3 que fica junto do projeto

# Configurar variáveis do ambiente
Nunca deixar segredos (como SECRET_KEY) no código.
Usar .env ou variáveis no servidor:
```bash
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
```
# Servidor WSGI/ASGI
O Django não deve rodar com runserver em produção.
Usar:

Gunicorn (mais comum).

Uvicorn (se quiser suporte assíncrono).

gunicorn projeto.wsgi

# Servidor Web

Usar Nginx ou Apache para:

Redirecionar tráfego HTTP/HTTPS.

Servir arquivos estáticos (CSS, JS, imagens).

# Arquivo estáticos e mídia
```bash python manage.py collectstatic 
```
Isso junta todos os arquivos estáticos num só diretório, para o Nginx servir.

# Deploy em serviços gerenciados
Se não quiser configurar tudo manualmente:

Heroku, Railway, Render, PythonAnywhere → todos suportam SQLite.

Docker também pode ser usado para empacotar o projeto.

<sub>Documentação criada por **Matheus Saraiva** ([@apptrx](https://github.com/apptrx)) e **Lucas Fujimoto** ([@Lucasft16](https://github.com/Lucasft16))</sub>
