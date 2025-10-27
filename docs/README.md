# Easy RAG

## Conteúdo

 - [`Adicionando .editorconfig e .gitignore`](#editorconfig-gitignore)
 - [`Iniciando o projeto com "poetry init"`](#poetry-init)
 - [`Instalando e configurando o Ruff`](#ruff-settings-pyproject)
 - [`Instalando e configurando o Pytest`](#pytest-settings-pyproject)
 - [`Instalando e configurando o Taskipy`](#taskipy-settings-pyproject)
 - [`Instalando e configurando o pre-commit`](#precommit-settings)
 - [`Criando os docker-compose (iniciais) da nossa aplicação`](#init-docker-compose)
 - [`Criando o container com PostgreSQL`](#postgresql-container)
 - [`Instalando o Django e criando o projeto "core"`](#install-django-core)
 - [`Configurções iniciais do Django (templates, static, media)`](#init-django-settings)
 - [`Criando a landing page index.html`](#index-landing)
 - [`Criando App users e um superusuario no Django Admin`](#app-users-more-django-admin)
 - [`Criando a página de cadastro (create-account.html)`](#create-account)
 - [`Instalando a biblioteca psycopg2-binary`](#psycopg2-binary)
 - [`Configurando o Django para reconhecer o PostgreSQL como Banco de Dados`](#django-setting-db)
<!---
[WHITESPACE RULES]
- "40" Whitespace character.
--->








































---

<div id="editorconfig-gitignore"></div>

## `Adicionando .editorconfig e .gitignore`

De início vamos adicionar os arquivos `.editorconfig` e `.gitignore` na raiz do projeto:

[.editorconfig](../.editorconfig)
```conf
# top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8

# 4 space indentation
[*.{py,html, js}]
indent_style = space
indent_size = 4

# 2 space indentation
[*.{json,y{a,}ml,cwl}]
indent_style = space
indent_size = 2
```

[.gitignore](../.gitignore)
```conf

É muito grande não vou exibir...
```








































---

<div id="poetry-init"></div>

## `Iniciando o projeto com "poetry init"`

Agora vamos iniciar nosso projeto com `poetry init`:

```bash
poetry init
```









































---

<div id="ruff-settings-pyproject"></div>

## `Instalando e configurando o Ruff`

Aqui vamos instalar e configurar o **Ruff** no nosso `pyproject.toml`:

```bash
poetry add --group dev ruff@latest
```

> Esse bloco define às *Regras Gerais de funcionamento do (Ruff)*.

#### `[tool.ruff]`

```toml
[tool.ruff]
line-length = 79
exclude = [
    "core/settings.py",
]
```

 - `line-length = 79`
   - Define que nenhuma linha de código deve ultrapassar 79 caracteres *(seguindo o padrão tradicional do PEP 8)*.
   - É especialmente útil para manter legibilidade em terminais com largura limitada.
   - Ruff irá avisar (e, se possível, corrigir) quando encontrar linhas mais longas.
 - `exclude = ["core/settings.py"]`
   - Define quais arquivos o Ruff deve ignorar:
     - Nesse caso, ele vai ignorar o arquivo `core/settings.py`.

#### `[tool.ruff.lint]`

Esse é o sub-bloco principal de configuração de linting do Ruff, ou seja, onde você define como o Ruff deve analisar o código quanto a erros, estilo, boas práticas etc.

```toml
[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
```

 - `preview = true`
   - Ativa regras experimentais (em fase de teste, mas estáveis o suficiente).
   - Pode incluir novas verificações que ainda não fazem parte do conjunto padrão.
   - Útil se você quer estar sempre com o Ruff mais “rigoroso” e atualizado.
 - `select = ['I', 'F', 'E', 'W', 'PL', 'PT']`
   - Define quais conjuntos de regras (lints) o Ruff deve aplicar ao seu código. Cada uma dessas letras corresponde a um grupo de regras:
     - `I` ([Isort](https://pycqa.github.io/isort/)): Ordenação de imports em ordem alfabética.
     - `F` ([Pyflakes](https://github.com/PyCQA/pyflakes)): Procura por alguns erros em relação a boas práticas de código.
     - `E` ([pycodestyle](https://pycodestyle.pycqa.org/en/latest/)): Erros de estilo de código.
     - `W` ([pycodestyle](https://pycodestyle.pycqa.org/en/latest/)): Avisos sobre estilo de código.
     - `PL` ([Pylint](https://pylint.pycqa.org/en/latest/index.html)): "erros" em relação a boas práticas de código.
     - `PT` ([flake8-pytest](https://pypi.org/project/flake8-pytest-style/)): Boas práticas do Pytest.

#### `[tool.ruff.format]`

O bloco [tool.ruff.format] é usado para configurar o formatador interno do Ruff, que foi introduzido recentemente como uma alternativa ao Black — mas com a vantagem de ser muito mais rápido.

```toml
[tool.ruff.format]
preview = true
quote-style = "double"
```

 - `preview = true`
   - Ativa regras experimentais (em fase de teste, mas estáveis o suficiente).
 - `quote-style = "double"`
   - Define o estilo de aspas (duplas no nosso caso) usadas pelo formatador.









































---

<div id="pytest-settings-pyproject"></div>

## `Instalando e configurando o Pytest`

Agora nós vamos instalar e configurar o **Pytest** no nosso `pyproject.toml`.

```bash
poetry add --group dev pytest@latest
```

#### `[tool.pytest.ini_options]`

O bloco `[tool.pytest.ini_options]` no `pyproject.toml` é usado para configurar o comportamento do Pytest, da mesma forma que você faria com `pytest.ini`, `setup.cfg` ou `tox.ini`:

```toml
[tool.pytest.ini_options]
pythonpath = "."
addopts = '-p no:warnings'
```

 - `pythonpath = "."`
   - Onde o Pytest procurar arquivos Python para executar.
   - Ou seja, a partir da `raiz (.)` do nosso projeto.
 - `addopts = '-p no:warnings'`
   - Para ter uma visualização mais limpa dos testes, caso alguma biblioteca exiba uma mensagem de warning, isso será suprimido pelo pytest.









































---

<div id="taskipy-settings-pyproject"></div>

## `Instalando e configurando o Taskipy`

Agora nós vamos instalar e configurar o **Taskipy** no nosso `pyproject.toml`.

```bash
poetry add --group dev taskipy@latest
```

#### `[tool.taskipy.tasks]`

O bloco `[tool.taskipy.tasks]` é usado para definir *tarefas (tasks)* automáticas personalizadas no seu `pyproject.toml`, usando o pacote taskipy.

```toml
[tool.taskipy.tasks]
lint = 'ruff check'
pre_format = 'ruff check --fix'
format = 'ruff format'
pre_test = 'task lint'
test = 'pytest -s -x --cov=. -vv'
post_test = 'coverage html'
```

 - `lint = 'ruff check'`
   - Executa o Ruff para verificar erros de estilo e código (linting), sem alterar nada.
 - `pre_format = 'ruff check --fix'`
   - Executa antes da *tarefa (task)* `format`. Aqui, você corrige automaticamente os erros encontrados por Ruff.
 - `format = 'ruff format'`
   - Usa o formatador nativo do Ruff (em vez de Black) para aplicar formatação ao código. 
 - `pre_test = 'task lint'`
   - Antes de rodar os testes, executa a tarefa lint (garantindo que o código está limpo).
 - `test = 'pytest -s -x --cov=. -vv'`
   - Roda os testes com Pytest, com as seguintes opções:
     - `-s`: Mostra print() e input() no terminal.
     - `-x`: Interrompe no primeiro erro.
     - `--cov=.`: Mede cobertura de testes com o plugin pytest-cov
     - `-vv`: Verbosidade extra (mostra todos os testes)
 - `post_test = 'coverage html'`
   - Depois dos testes, gera um relatório HTML de cobertura que você pode abrir no navegador (geralmente em htmlcov/index.html).










































---

<div id="precommit-settings"></div>

## `Instalando e configurando o pre-commit`

Para garantir que antes de cada commit seu projeto passe por:

 - ✅ lint (usando Ruff)
 - ✅ test (com pytest)
 - ✅ coverage

Você deve usar o pre-commit — uma ferramenta leve e ideal para isso. Vamos configurar passo a passo:

```bash
poetry add --group dev pre-commit
```

[.pre-commit-config.yaml](../.pre-commit-config.yaml)
```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-lint
        name: ruff check
        entry: task lint
        language: system
        types: [python]

      - id: pytest-test
        name: pytest test
        entry: task test
        language: system
        types: [python]

      - id: pytest-coverage
        name: pytest coverage
        entry: task post_test
        language: system
        types: [python]
```

Agora nós precisamos instalar o pre-commit:

```bash
pre-commit install
```

#### Dica extra: Se quiser rodar manualmente

```bash
pre-commit run --all-files
```

> **NOTE:**  
> É interessante ter uma checagem rápida no Taskipy.

[pyproject.toml](../pyproject.toml)
```toml
[tool.taskipy.tasks]
precommit = 'pre-commit run --all-files'
```










































---

<div id="init-docker-compose"></div>

## `Criando os docker-compose (iniciais) da nossa aplicação`

É comum em uma aplicação ter os seguintes *docker-composes*:

 - [⚙️ 1. docker-compose.yml (base comum)](../docker-compose.yml)
   - Esse é o arquivo principal, usado em todos os ambientes.
   - Define apenas o serviço de banco, os volumes e a rede.
   - 👉 Esse arquivo nunca muda, nem em dev nem em prod — é a base do projeto.
 - [⚙️ 2. Docker-compose.dev.yml](../docker-compose.dev.yml)
   - Para desenvolvimento, o que muda normalmente é:
     - Expor a porta do banco localmente (5432:5432);
     - Permitir acesso de ferramentas como DBeaver, PgAdmin ou psql;
     - Log mais detalhado.
   - 💡 Aqui não precisamos repetir image, volumes, etc. — o Docker herda tudo do base e apenas aplica o override.
 - [⚙️ 3. Docker-compose.prod.yml](../docker-compose.prod.yml)
   - Na produção, normalmente:
     - Não expomos a porta 5432 (para segurança);
     - Mantemos o banco acessível apenas pela rede interna do Docker;
     - Ativamos backup automatizado (opcional mais pra frente).
   - ⚠️ expose deixa a porta visível apenas dentro da rede Docker, sem expor para o host ou internet.

De início vamos criar apenas o compose base:

[docker-compose.yml](../docker-compose.yml)
```yaml
volumes:
  postgres_data:

networks:
  backend:
```

Agora vamos criar comandos no Taskipy para executar cada um dos docker-compose:

[pyproject.toml](../pyproject.toml)
```toml
[tool.taskipy.tasks]
prodcompose = 'docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d'
devcompose = 'docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d'
```










































---

<div id="postgresql-container"></div>

## `Criando o container com PostgreSQL`

Antes de iniciarmos as tarefas envolvendo Banco de Dados é claro que precisamos de um Banco de Dados para trabalhar. Sabendo disso vamos criar/configar um container com PostgreSQL.

De início vamos configurar o que é comum tanto em **produção** quanto em **desenvolvimento** no *docker-compose base*:

[docker-compose.yml](../docker-compose.yml)
```yaml
services:
  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
```

Agora vamos aplicar as configurações de produção e desenvolvimento separadamente:

[docker-compose.dev.yml](../docker-compose.dev.yml)
```yaml
services:
  db:
    ports:
      - "5432:5432"
```

[docker-compose.prod.yml](../docker-compose.prod.yml)
```yaml
services:
  db:
    expose:
      - "5432"
```

Ótimo, agora é só executar os comandos criado com Taskipy para criar o container em modo **dev** ou **produção**.

Também vamos ter esses comandos no Taskipy para nos ajudar no gerenciamento:

[pyproject.toml](../pyproject.toml)
```toml
[tool.taskipy.tasks]
opendb = "docker exec -it postgres_db psql -U easyrag -d easy_rag_db"
devcompose = 'docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d'
prodcompose = 'docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d'
cleancontainers = """
docker stop $(docker ps -aq) 2>/dev/null || true &&
docker rm $(docker ps -aq) 2>/dev/null || true &&
docker rmi -f $(docker images -aq) 2>/dev/null || true &&
docker volume rm $(docker volume ls -q) 2>/dev/null || true &&
docker system prune -a --volumes -f
"""
```










































---

<div id="install-django-core"></div>

## `Instalando o Django e criando o projeto "core"`

Agora nós vamos instalar o Django e criar o projeto `core`:

```bash
poetry add django@latest
```

```bash
django-admin startproject core .
```

> **NOTE:**  
> Uma coisa importante agora é excluir o arquivo `core/settings.py` do ruff:

[pyproject.toml](../pyproject.toml)
```bash
[tool.ruff]
line-length = 79
exclude = [
    "core/settings.py",
]
```

> **NOTE:**  
> Agora esse arquivo não vai mais passar pelo `lint`.

Agora para testar se tudo está funcionando, vamos rodar o servidor:

```bash
python manage.py runserver
```

 - [http://localhost:8000/](http://localhost:8000/)

Aqui também é interessanter ter um comando só para rodar o servidor:

[pyproject.toml](../pyproject.toml)
```toml
[tool.taskipy.tasks]
runserver = 'python manage.py runserver'
```










































---

<div id="init-django-settings"></div>

## `Configurações iniciais do Django (templates, static, media)`

Aqui nós vamos fazer as configurações iniciais do Django que serão:

> Fazer o Django identificar onde estarão os arquivos `templates`, `static` e `media`:

[core/settings.py](../core/settings.py)
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```










































---

<div id="index-landing"></div>

## `Criando a landing page index.html`

> Aqui nós vamos criar e configurar a `landing page` da nossa aplicação.

Uma `landing page` pública geralmente contem:

 - Apresentação do produto/serviço.
 - Botões de “Entrar” e “Cadastrar”.
 - Sessões com informações sobre a empresa.
 - Depoimentos, preços, etc.

Vamos começar configurando a rota/url que vai ser nosso `/`:

[core/urls.py](../core/urls.py)
```python
from django.contrib import admin
from django.urls import include, path

from .views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="", view=index, name="index"),
]
```

Agora dentro do [core](../core) vamos criar uma view (ação) para essa `landing page`:

[core/views.py](../core/views.py)
```python
from django.shortcuts import render


def index(request):
    if request.method == "GET":
        return render(request, "pages/index.html")
```

Por fim, vamos criar o HTML para essa `landing page`, por enquanto sem nenhuma estilização:

[templates/pages/index.html](../templates/pages/index.html)
```html
{% extends "base.html" %}

{% block title %}Easy RAG{% endblock %}

{% block content %}
    <h1>Easy RAG</h1>

    <!-- Formulário de login básico -->
    <form method="post" action="">
        {% csrf_token %}
        <!-- Username -->
        <div>
            <label for="username">Username</label><br>
            <input type="text"
                id="username"
                name="username"
                autocomplete="username"
                required>
        </div>
        <!-- Password -->
        <div>
            <label for="password">Password</label><br>
            <input type="password"
                id="password"
                name="password"
                autocomplete="current-password"
                required>
        </div>
        <!-- Botão de submit -->
        <div>
            <button type="submit">Entrar</button>
        </div>
    </form>

    <br/>

    <!-- Botões para login social (placeholders) -->
    <div>
        <a href="">
            <button type="button">Entrar com Google</button>
        </a>
        <a href="">
            <button type="button">Entrar com GitHub</button>
        </a>
    </div>

    <br/>

    <!-- Link para cadastro -->
    <div>
        <a href="{% url 'create-account' %}">Cadastrar</a>
    </div>
{% endblock %}
```

Finalmente, se você abrir o projeto (site) na rota/url principal vai aparecer essa `landing page`.

 - [http://localhost:8000/](http://localhost:8000/)










































---

<div id="app-users-more-django-admin"></div>

## `Criando App users e um superusuario no Django Admin`

Aqui de início vamos criar o App `users` que vai ser responsável por armazenar os dados dos nossos usuários no Banco de Dados.

```bash
python manage.py startapp users
```

[core/settings.py](../core/settings.py)
```python
INSTALLED_APPS = [
    ...
    'users',
]
```

Para não esquecer vamos já relacionar as rotas do App `users` no nosso projeto `core/urls.py`:

[core/urls.py](../core/urls.py)
```python
from django.contrib import admin
from django.urls import include, path

from .views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="", view=index, name="index"),
    path("", include("users.urls")),
]
```

Ótimo, agora vamos criar um super usuário para ver se esse usuário aparece no nosso Django Admin, mas antes nós precisamos aplicar as migrações iniciais de nossa base de dados:

```bash
python manage.py migrate
```

Pronto, agora que o nosso Banco de Dados foi iniciado vamos criar um superusuário:

```bash
python manage.py createsuperuser
```

Agora é só criar o Django Admin e verificar se temos a tabela `users`:

 - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

> **NOTE:**  
> Se você clicar nela verá que nós só temos 1 usuário, que foi o `super usuário` que nós acabamos de cadastrar.











































---

<div id="create-account"></div>

## `Criando a página de cadastro (create-account.html)`

> Aqui nós vamos criar e configurar a rota/url para a nossa `página de cadastro` dentro dos templates do nosso App `users`.

De início vamos começar configurando a rota/url `create-account`:

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import create_account

urlpatterns = [
    path(route="create-account/", view=create_account, name="create-account"),
]
```

Agora vamos criar uma view (ação) para quando alguém clicar em "Cadastrar", ele seja redirecionado para essa `página de cadastro`:

[users/views.py](../users/views.py)
```python
from django.shortcuts import redirect, render


def create_account(request):
    if request.method == "GET":
        return render(request, "pages/create-account.html")
```

> **E o formulário de cadastro?**

Bem, primeiro vamos criar um [forms.py](../users/forms.py) para criar um formulário genêrico para o nosso App `users` utilizando de tudo o que o Django já tem pronto:

[users/forms.py](../users/forms.py)
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
```

No código assim:

 - `from django import forms`
   - Importa o módulo `forms` do Django.
   - Ele contém classes e tipos de campos (CharField, EmailField, IntegerField, etc.) que permitem criar formulários Python que se transformam em HTML.
 - `from django.contrib.auth.forms import UserCreationForm`
   - Importa o formulário de criação de usuário padrão do Django.
   - Esse formulário já tem validações prontas:
     - Verifica se o nome de usuário já existe;
     - Verifica se a senha atende aos requisitos de segurança;
     - Verifica se as duas senhas digitadas são iguais.
     - 💡 Assim, você não precisa reescrever toda essa lógica manualmente — basta herdar dele.
 - `from django.contrib.auth.models import User`
   - Importa o modelo de usuário padrão do Django (a tabela *auth_user* do banco).
   - É o modelo que o *UserCreationForm* usa para criar e salvar novos usuários.
 - `class CustomUserCreationForm(UserCreationForm):`
   - Cria uma nova classe chamada *"CustomUserCreationForm"* que herda de *"UserCreationForm"*.
   - Isso significa que você está pegando toda a funcionalidade do formulário original e adicionando ou modificando o que quiser (nesse caso, o campo email).
 - `email = forms.EmailField(required=True)`
   - Adiciona um novo campo email ao formulário.
   - O *"UserCreationForm"* original não pede email — ele só tem username, password1 e password2.
   - Então, aqui você está dizendo:
     - *“Quero que meu formulário também peça o email do usuário, e que esse campo seja obrigatório.”*
     - O forms.EmailField valida automaticamente se o valor digitado parece um email válido (ex: tem @, etc.). 

> **E essa classe interna *Meta*?**

```python
class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
```

Essa classe interna `Meta` é uma configuração especial do Django Forms:

| Atributo         | Função                                                                                                                                                                                                |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model = User`   | Diz ao Django qual modelo esse formulário vai manipular (no caso, o modelo `User`). Isso significa que, ao chamar `form.save()`, o Django sabe que deve criar um novo registro na tabela `auth_user`. |
| `fields = [...]` | Lista **quais campos** do modelo (ou campos personalizados) aparecerão no formulário e na validação. A ordem dessa lista define a ordem dos campos no HTML.                                           |

[refaça] - Nós poderíamos partir agora para o nossa view, mas o nosso HTML vai ser dinâmico, então vamos logo planejar (escrever ele em código) para depois fazer a view que vai criar o HTML dinamicamente.














Ótimo, nós já temos um modelo de formulário com os campos *("username", "email", "password1", "password2")* necessários na hora de criar um novo usuário.

> **E agora o que fazer?**  
> Agora nós vamos implementar uma view (ação) para capturar esses dados e salvar no banco de dados.

De início vamos verificar se o método é `POST`, ou seja, o usuário está enviando os dados do formulário:

[users/views.py](../users/views.py)
```python
def create_account(request):
    if request.method == "GET":
        return render(request, "pages/create-account.html")
    if request.method == "POST":
        ...
```

Agora nós vamos importar o formulário customizado (CustomUserCreationForm) e passar para ele como argumento `request.POST`, ou seja, ele vai receber os dados que o usuário enviou:

[users/views.py](../users/views.py)
```python
from users.forms import CustomUserCreationForm


def create_account(request):
    if request.method == "GET":
        return render(request, "pages/create-account.html")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
```

> **O que tem dentro desse *form*?**













































> **Mas como acessar essa página?**

Bem, nós precisamos modificar o `index.html` para sempre que algum usuário clicar em "Cadastrar", ele seja redirecionado para essa `página de cadastro`:

[frontend/templates/pages/index.html](../frontend/templates/pages/index.html)
```html
<!-- Link para cadastro -->
<div>
    <a href="{% url 'create-account' %}">Cadastrar</a>
</div>
```

> **NOTE:**  
> Lembrando que nós temos que fazer o mesmo na página de cadastro para voltar ao login.

[frontend/templates/pages/create-account.html](../frontend/templates/pages/create-account.html)
```html
<!-- Link para voltar ao login -->
<div>
    <a href="/">Já tem uma conta? Fazer login</a>
</div>
```











































---

<div id="psycopg2-binary"></div>

## `Instalando a biblioteca psycopg2-binary`

 - Este é o driver oficial do PostgreSQL para Python — o Django usa ele internamente para conversar com o banco.
 - **NOTE:** Sem ele, o Django não consegue abrir a conexão porque depende de um driver nativo específico do PostgreSQL.

```bash
poetry add psycopg2-binary@latest
```

#### `⚙️ 2. O que o psycopg2-binary faz?`

> Ele é a ponte entre o Django (Python) e o PostgreSQL (servidor).

Quando o Django executa algo como:

```bash
User.objects.create(username="drigols")
```

internamente ele faz uma chamada SQL tipo:

```sql
INSERT INTO auth_user (username) VALUES ('drigols');
```

Mas pra enviar isso ao PostgreSQL, ele precisa de uma biblioteca cliente — e é aí que entra o psycopg2.












































---

<div id="django-setting-db"></div>

## `Configurando o Django para reconhecer o PostgreSQL (+ .env) como Banco de Dados`

Antes de começar a configurar o Django para reconhecer o PostgreSQL como Banco de Dados, vamos fazer ele reconhecer as variáveis de ambiente dentro de [core/settings.py](../core/settings.py).

Primeiro, vamos instalar o `python-dotenv`:

```bash
poetry add python-dotenv@latest
```

Agora iniciar uma instância do `python-dotenv`:

[core/settings.py](../core/settings.py)
```python
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
```

> **Como testar que está funcionando?**

Primeiro, imagine que nós temos as seguinte variáveis de ambiente:

[.env](../.env)
```bash
POSTGRES_DB=easy_rag_db           # Nome do banco de dados a ser criado
POSTGRES_USER=easyrag             # Usuário do banco
POSTGRES_PASSWORD=easyragpass     # Senha do banco
POSTGRES_HOST=localhost           # Nome do serviço (container) do banco no docker-compose
POSTGRES_PORT=5432                # Porta padrão do PostgreSQL
```

Agora vamos abrir um **shell interativo do Django**, ou seja, um terminal Python (REPL) com o Django já carregado, permitindo testar código com acesso total ao projeto.

É parecido com abrir um python normal, mas com estas diferenças:

| Recurso                           | Python normal | `manage.py shell` |
| --------------------------------- | ------------- | ----------------- |
| Carrega o Django automaticamente  | ❌ Não       | ✅ Sim            |
| Consegue acessar `settings.py`    | ❌           | ✅                |
| Consegue acessar models           | ❌           | ✅                |
| Consegue consultar banco de dados | ❌           | ✅                |
| Lê o `.env` (se Django carregar)  | ❌           | ✅                |
| Útil para debugar                 | Razoável      | Excelente         |

```bash
python manage.py shell

6 objects imported automatically (use -v 2 for details).
Python 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> import os

>>> print(os.getenv("POSTGRES_HOST"))
localhost

>>> print(os.getenv("POSTGRES_PASSWORD"))
easyragpass
```

> **NOTE:**  
> Vejam que realmente nós estamos conseguindo acessar as variáveis de ambiente.

#### Continuando...

> Uma coisa importante é dizer ao Django qual Banco de Dados vamos utilizar.

Por exemplo:

[core/settings.py](../core/settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'easy_rag'),
        'USER': os.getenv('POSTGRES_USER', 'easyrag'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'supersecret'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
```

No exemplo acima nós temos um dicionário que informa ao Django como conectar ao banco de dados:

 - `ENGINE`
   - Qual backend/driver o Django usa — aqui, PostgreSQL.
 - `NAME`
   - Nome do banco.
 - `USER`
   - Usuário do banco.
 - `PASSWORD`
   - Senha do usuário.
 - `HOST`
   - Host/hostname do servidor de banco.
 - `PORT`
   - Porta TCP onde o Postgres escuta.

#### `O que os.getenv('VAR', 'default') faz, exatamente?`

`os.getenv` vem do módulo padrão `os` e faz o seguinte:

 - Tenta ler a variável de ambiente chamada 'VAR' (por exemplo POSTGRES_DB);
 - Se existir, retorna o valor da variável de ambiente;
 - Se não existir, retorna o valor padrão passado como segundo argumento ('default').

#### `Por que às vezes PASSAMOS um valor padrão (default) no código?`

 - *Conforto no desenvolvimento local:* evita quebrar o projeto se você esquecer de definir `.env`.
 - *Documentação inline:* dá uma ideia do nome esperado (easy_rag, 5432, etc.).
 - *Teste rápido:* você pode rodar `manage.py` localmente sem carregar variáveis.

> **NOTE:**  
> Mas atenção: os valores padrões não devem conter segredos reais (ex.: supersecret) no repositório público — isso é um risco de segurança.

#### `Por que não você não deveria colocar senhas no código?`

 - Repositórios (Git) podem vazar ou ser lidos por terceiros.
 - Código pode acabar em backups, imagens Docker, etc.
 - Difícil rotacionar/chavear senhas se espalhadas pelo repositório.

> **Regra prática:**  
> - Nunca colocar credenciais reais em `settings.py`.
> - Use `.env` (não comitado) ou um *"secret manager"*.

Então, por enquanto vamos omitir alguns valores padrão (default):

[core/settings.py](../core/settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'easy_rag'),
        'USER': os.getenv('POSTGRES_USER', 'easyrag'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
```

Por fim, vamos testar a conexão ao banco de dados:

```bash
python manage.py migrate
```

**OUTPUT:**
```bash
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  No migrations to apply.
```


















































































---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
