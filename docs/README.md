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
 - [`Criando o container com o Django e criando o projeto "core"`](#install-django-core)
 - [`Configurações iniciais do Django (templates, static, media)`](#init-django-settings)
 - [`Criando a landing page index.html`](#index-landing)
 - [`Criando App users e um superusuario no Django Admin`](#app-users-more-django-admin)
 - [`Instalando a biblioteca psycopg2-binary`](#psycopg2-binary)
 - [`Configurando o Django para reconhecer o PostgreSQL como Banco de Dados`](#django-setting-db)
 - [`Criando a página de cadastro (create-account.html + DB Commands)`](#create-account)
 - [`Criando a sessão de login/logout + página home.html`](#session-home)
 - [`Criando o login com Google e GitHub`](#login-google-github)
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

Vamos ter alguns comandos no Taskipy para nos ajudar no gerenciamento:

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

## `Criando o container com o Django e criando o projeto "core"`

Nessa parte do nosso projeto vamos executar várias tarefas, como:

 - Instalar o Django;
 - Exportar as dependências do projeto:
   - `requirements.txt`
   - `requirements-dev.txt`
 - Criar um Dockerfile para o Django;

#### `Instalando o Django e Uvicorn`

Vamos iniciar instalando o `Django` e `Uvicorn`:

```bash
poetry add django@latest
```

```bash
poetry add uvicorn@latest
```

#### `Exportando as dependências do projeto`

> Antes de criar nossos containers, precisamos gerar os `requirements.txt` e `requirements-dev.txt`.

**Mas, primeiro devemos instalar o plugin "export" do Poetry:**
```bash
poetry self add poetry-plugin-export
```

Agora vamos gerar `requirements.txt` de *produção*:

```bash
poetry export --without-hashes --format=requirements.txt --output=requirements.txt
```

Continuando, agora vamos gerar `requirements-dev.txt` (esse é mais utilizado durante o desenvolvimento para quem não usa o Poetry):

```bash
poetry export --without-hashes --with dev --format=requirements.txt --output=requirements-dev.txt
```

#### `Criando o Dockerfile`

Agora, vamos criar o nosso `Dockerfile`...

> **Mas por que eu preciso de um Dockerfile para o Django + Uvicorn?**

**NOTE:**  
O `Dockerfile` é onde você diz **como** essa imagem será construída.

> **O que o Dockerfile faz nesse caso?**

 - Escolhe a imagem base (ex.: python:3.12-slim) para rodar o Python.
 - Instala as dependências do sistema (por exemplo, libpq-dev para PostgreSQL).
 - Instala as dependências Python (pip install -r requirements.txt).
 - Copia o código do projeto para dentro do container.
 - Define o diretório de trabalho (WORKDIR).
 - Configura o comando de entrada.
 - Organiza assets estáticos e outras configurações.

> **Quais as vantagens de usar o Dockerfile?**

 - **Reprodutibilidade:**
   - Qualquer pessoa consegue subir seu projeto com o mesmo ambiente que você usa.
 - **Isolamento:**
   - Evita conflitos de versão no Python e dependências.
 - **Customização:**
   - Você pode instalar pacotes de sistema ou bibliotecas específicas.
 - **Portabilidade:**
   - Mesma imagem funciona no seu PC, no servidor ou no CI/CD.

O nosso [Dockerfile](../Dockerfile) vai ficar da seguinte maneira:

[Dockerfile](../Dockerfile)
```bash
# ===============================
# 1️⃣ Imagem base
# ===============================
FROM python:3.12-slim

# ===============================
# 2️⃣ Configuração de ambiente
# ===============================
WORKDIR /code
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# ===============================
# 3️⃣ Dependências do sistema
# ===============================
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    bash \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 4️⃣ Instalar dependências Python
# ===============================
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# ===============================
# 5️⃣ Copiar código do projeto
# ===============================
COPY . /code/

# ===============================
# 6️⃣ Ajustes de produção
# ===============================
# Criar usuário não-root para segurança
RUN adduser --disabled-password --no-create-home appuser && \
    chown -R appuser /code
USER appuser

# ===============================
# 7️⃣ Porta exposta (Uvicorn usa 8000 por padrão)
# ===============================
EXPOSE 8000

# ===============================
# 8️⃣ Comando padrão
# ===============================
# Mantém o container rodando e abre um shell se usado com
# `docker run` sem sobrescrever comando.
CMD ["bash"]
```

**NOTE:**  
Se você desejar testar o `Dockerfile` antes de executar com o *docker compose*, utilize o seguinte comando:

```bash
docker build -t teste-django .
```

 - `-t teste-django`
   - Dá um nome para a imagem *(teste-django)*.
 - `.`
   - Indica que o contexto de build é a pasta atual.

Até, então nós criamos a imagem do container, agora vamos executar (run) o container:

**Executa (run) e entra no container via bash:**
```bash
docker run -it --rm -p 8000:8000 teste-django bash
```

#### `Criando o docker compose para o container web`

> Aqui vamos entender e criar um container contendo o `Django` e o `Uvicorn`.

 - **Função:**
   - Executar a aplicação Django em produção.
 - **Quando usar:**
   - Sempre para servir sua aplicação backend.
 - **Vantagens:**
   - Uvicorn é um servidor WSGI otimizado para produção.
   - Separa lógica da aplicação da entrega de arquivos estáticos.
 - **Desvantagens:**
   - Não serve arquivos estáticos eficientemente.

Antes de criar nosso container contendo o *Django* e o *Uvicorn*, vamos criar as variáveis de ambiente para esse container:

[.env](../.env)
```bash
# ==========================
# CONFIGURAÇÃO DJANGO
# ==========================
DJANGO_SECRET_KEY=change-me       # Chave secreta do Django para criptografia e segurança
DJANGO_DEBUG=True                 # True para desenvolvimento; False para produção
DJANGO_ALLOWED_HOSTS=*            # Hosts permitidos; * libera para qualquer host

# ==========================
# CONFIGURAÇÃO DO UVICORN
# ==========================
UVICORN_HOST=0.0.0.0              # Escutar em todas as interfaces
UVICORN_PORT=8000                 # Porta interna do app
```

 - `DJANGO`
   - `DJANGO_SECRET_KEY` → chave única e secreta usada para assinar cookies, tokens e outras partes sensíveis.
   - `DJANGO_DEBUG` → habilita/desabilita debug e mensagens de erro detalhadas.
   - `DJANGO_ALLOWED_HOSTS` → lista de domínios que o Django aceita; `*` significa todos (não recomendado para produção).
 - `UVICORN`
   - `UVICORN_HOST` → define o IP/host onde o servidor Uvicorn vai rodar.
   - `UVICORN_PORT` → porta interna que o container expõe para o nginx ou para acesso direto no dev.

Continuando, agora vamos configurar os arquivos *docker composes*:

[docker-compose.yml (arquivo base)](../docker-compose.yml)
```yml

```

[docker-compose.dev.yml (ambiente de desenvolvimento)](../docker-compose.dev.yml)
```yml

```

[docker-compose.prod.yml (ambiente de produção)](../docker-compose.prod.yml)
```yml

```







 - `build: context + dockerfile.`
   - `context: .`
     - Ponto `(.)` significa que o contexto de build é a raiz do projeto.
     - Isso quer dizer que todos os arquivos dessa pasta estarão disponíveis para o build.
   - `dockerfile: Dockerfile`
     - Nome do arquivo Dockerfile usado para construir a imagem.
 - `container_name: django_web`
   - Nome fixo do container (para facilitar comandos como docker logs django_web).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `command`
   - `sh -c`
     - Executa um shell POSIX dentro do container e roda tudo o que estiver entre aspas como um único comando.
     - Usar *sh -c* permite encadear vários comandos com &&.
   - `python manage.py migrate &&`
     - Aplica migrações do Django ao banco (cria/atualiza tabelas).
     - O *&&* significa: só execute o próximo comando se este retornar sucesso (exit code 0).
     - **NOTE:** Se a migração falhar, nada depois roda.
   - `python manage.py collectstatic --noinput &&`
     - Coleta os arquivos estáticos de todas as apps para a pasta do *STATIC_ROOT*.
     - *--noinput* evita prompts interativos (obrigatório em automação/containers).
     - **NOTE:** Novamente, *&&* encadeia: só continua se deu tudo certo.
   - `uvicorn core.asgi:application --reload --host ${UVICORN_HOST} --port ${UVICORN_PORT}`
     - Inicia o servidor ASGI com Uvicorn usando a aplicação em core/asgi.py (objeto application).
     - `--reload` → modo desenvolvimento; monitora arquivos e reinicia automaticamente ao salvar (não use em produção).
     - `--host ${UVICORN_HOST}` → endereço de bind dentro do container. Normalmente 0.0.0.0 para aceitar conexões externas.
     - `--port ${UVICORN_PORT}` → porta interna onde o Uvicorn escuta (ex.: 8000).
 - `env_file: .env`
   - Carrega variáveis do `.env`.
 - `volumes:`
   - `./:/code`
     - pasta atual `.` → `/code` dentro do container.
   - `./static:/code/staticfiles`
     - `./static` → `/code/staticfiles`
   - `./media:/code/media`
     - `./media` → `/code/media`
   - **NOTE:** Aqui estamos aplicando o coneito de *"Bind Mounts"*.
 - `ports: "${UVICORN_PORT}:${UVICORN_PORT}"`
   - Para acessar pelo navegador no seu computador, você precisa de `ports`.
   - **NOTE:** `expose` apenas informa a porta para outros containers, não mapeia para o host.
 - `networks: backend`
   - Rede interna para comunicação.

#### Crie as pastas `./static`, `./media` e `./staticfiles` no host

Uma observação aqui é que antes de nós executamos o container web nós precisamos criar as pastas (diretórios) `./static`, `./media` e `./staticfiles` no host.

> **Por que?**

Porque se essas pastas (diretórios) forem criadas pelo container ela não terterão as permissões do nosso usuário (do nosso sistema), elas virão com permissão root (do container).

O comando para fazer isso é o seguinte:

```bash
mkdir -p static media staticfiles
```

Continuando...  

> **Uma dúvida... tudo o que eu modifico no meu projeto principal é alterado no container?**

**SIM!**  
No nosso caso, sim — porque no serviço `web` você fez este mapeamento:

[docker-compose.yml](../docker-compose.yml)
```yaml
volumes:
  - .:/code
```

Isso significa que:

 - O diretório atual no seu `host (.)` é montado dentro do container em `/code`.
 - Qualquer alteração nos arquivos do seu projeto no host aparece instantaneamente no container.
 - E o inverso também vale: se você mudar algo dentro do container nessa pasta, muda no seu host.

Continuando, agora é só criar o container:

**Cria o(s) container(s) em background:**
```bash
docker compose up -d
```

**NOTE:**
Se você desejar conectar nesse container via bash utilize o seguinte comando (As vezes é necesario esperar o container subir):

**Entrar no container "django_web" via bash:**
```bash
docker exec -it django_web bash
```

Agora você pode listar as dependências Python instaladas do container:

```bash
pip list
```

**OUTPUT:**
```bash
Package         Version
--------------- -------
asgiref         3.9.1
click           8.2.1
Django          5.2.5
h11             0.16.0
pip             25.2
psycopg2-binary 2.9.10
python-dotenv   1.1.1
sqlparse        0.5.3
uvicorn         0.35.0
```

Por fim, você pode ir no seu `locaohost` e verificar se o container está rodando com Django e Uvicorn:

 - [http://localhost:8000/](http://localhost:8000/)















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

> Aqui nós vamos fazer as configurações iniciais do Django que serão.

Fazer o Django identificar onde estarão os arquivos `templates`, `static` e `media`:

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

Agora vamos garantir que o Django só sirva arquivos diretamente quando estiver em modo de desenvolvimento (DEBUG=True):

[core/urls.py](../core/urls.py)
```python
from django.conf import settings
from django.conf.urls.static import static

  ...


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

**Explicação das principais partes do código:**

 - `from django.conf import settings`
   - Permite acessar as variáveis definidas no `settings.py`, como `MEDIA_URL` e `MEDIA_ROOT`.
 - `from django.conf.urls.static import static`
   - Fornece uma função utilitária para servir arquivos estáticos e de mídia durante o desenvolvimento.
 - `if settings.DEBUG`
   - Garante que o Django **só sirva arquivos diretamente** quando estiver em modo de desenvolvimento (DEBUG=True).
   - Em produção, essa função não deve ser usada — o servidor web (Nginx, Apache, etc.) serve esses arquivos.
 - `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
   - Faz o Django mapear as URLs que começam com /media/ para os arquivos dentro da pasta física definida em MEDIA_ROOT.
   - Assim, se o usuário enviar um arquivo uploads/teste.pdf, o Django poderá exibi-lo no navegador.

Por fim, mas não menos importante, vamos criar o arquivo `base.html`:

[base.html](../templates/base.html)
```html
<!DOCTYPE html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}{% endblock title %}</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        {% block head %}{% endblock head %}
    </head>
    <body class="min-h-screen bg-[#343541]">
        {% block content %}{% endblock content %}
        {% block scripts %}{% endblock scripts %}
    </body>
</html>
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

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import login_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
]
```

 - Essa rota/url `/` vai ser tratada dentro do App `users` porque futuramente nós vamos criar condições para verificar se o usuário está logado ou não no sistema.
 - Desta maneira, é interessante que essa rota/url `/` seja tratada dentro do App `users`.

Continuando, agora vamos criar uma view (ação) para essa `landing page`:

[users/views.py](../users/views.py)
```python
from django.shortcuts import render


def login_view(request):
    # GET → renderiza pages/index.html (form de login)
    if request.method == "GET":
        return render(request, "pages/index.html")
```

Por fim, vamos criar o HTML para essa `landing page`; por enquanto sem nenhuma estilização:

[templates/pages/index.html](../templates/pages/index.html)
```html
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

![img](images/index-landing-01.png)  

Continuando, vamos adicionar `base.html` e algumas classes *TailwindCSS* para ficar mais estilizado:

[templates/pages/index.html](../templates/pages/index.html)
```html
{% extends "base.html" %}
{% load socialaccount %}

{% block title %}Easy RAG — Login{% endblock %}

{% block content %}
    <main class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <!-- Card -->
            <div class="bg-white py-8 px-6 shadow rounded-lg">
                <!-- Logo / Title -->
                <div class="mb-6 text-center">
                    <h2 class="mt-4 text-2xl font-semibold text-gray-900">Easy RAG</h2>
                    <p class="mt-1 text-sm text-gray-500">Faça login para acessar seu painel</p>
                </div>

                {% if messages %}
                    <div class="mb-4">
                        {% for message in messages %}
                            <div class="text-red-600 bg-red-100 border border-red-200 rounded-md px-4 py-2 text-sm">
                                {{ message }}
                            </div>
                        {% endfor %}
                    </div>
                {% endif %}

                <!-- Form -->
                <form method="post" action="" class="space-y-6">
                    {% csrf_token %}

                    <!-- Username -->
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700">Usuário</label>
                        <div class="mt-1">
                            <input id="username" name="username" type="text" autocomplete="username"
                                required
                                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        </div>
                    </div>

                    <!-- Password -->
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
                        <div class="mt-1">
                            <input id="password" name="password" type="password" autocomplete="current-password"
                                required
                                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        </div>
                    </div>

                    <!-- Submit -->
                    <div>
                        <button type="submit"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                            Entrar
                        </button>
                    </div>
                </form>

                <!-- Divider -->
                <div class="mt-6 relative">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-200"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="bg-white px-2 text-gray-500">ou continuar com</span>
                    </div>
                </div>

                <!-- Social login buttons -->
                <div class="mt-6 grid grid-cols-2 gap-3">
                    <!-- Google -->
                    <div>
                        <a href="{% provider_login_url 'google' %}"
                        class="w-full inline-flex justify-center items-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-50">
                            <!-- Google icon (svg) -->
                            <svg class="h-5 w-5 mr-2" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                <path d="M533.5 278.4c0-18.2-1.6-36-4.7-53.2H272v100.8h147.4c-6.4 34.9-26 64.5-55.5 84.3v69.9h89.6c52.5-48.3 82-119.7 82-201.8z" fill="#4285F4"/>
                                <path d="M272 544.3c73.5 0 135.3-24.5 180.4-66.7l-89.6-69.9c-24.9 16.7-56.9 26.6-90.8 26.6-69.7 0-128.7-47.1-149.8-110.4H31.6v69.5C76.3 494.7 169 544.3 272 544.3z" fill="#34A853"/>
                                <path d="M122.2 327.1c-11.7-34.6-11.7-72 0-106.6V150.9H31.6c-39.6 77-39.6 168.5 0 245.5l90.6-69.3z" fill="#FBBC05"/>
                                <path d="M272 107.7c39.9 0 75.7 13.7 104 40.6l78-78C403.3 24.7 337.2 0 272 0 169 0 76.3 49.6 31.6 150.9l90.6 69.5C143.3 154.8 202.3 107.7 272 107.7z" fill="#EA4335"/>
                            </svg>
                            <span class="text-sm font-medium text-gray-700">Google</span>
                        </a>
                    </div>

                    <!-- GitHub -->
                    <div>
                        <a href="{% provider_login_url 'github' %}"
                        class="w-full inline-flex justify-center items-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-50">
                            <!-- GitHub icon -->
                            <svg class="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                                <path fill-rule="evenodd" d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.11.82-.26.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.333-1.754-1.333-1.754-1.09-.745.083-.73.083-.73 1.205.085 1.84 1.236 1.84 1.236 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.304.762-1.603-2.665-.303-5.467-1.333-5.467-5.93 0-1.31.468-2.38 1.235-3.22-.124-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.3 1.23a11.5 11.5 0 013.003-.404c1.02.005 2.045.138 3.003.404 2.29-1.552 3.297-1.23 3.297-1.23.653 1.653.243 2.873.12 3.176.77.84 1.234 1.91 1.234 3.22 0 4.61-2.807 5.624-5.48 5.92.43.372.823 1.102.823 2.222 0 1.604-.014 2.896-.014 3.29 0 .32.217.694.825.576C20.565 21.796 24 17.297 24 12c0-6.63-5.37-12-12-12z"/>
                            </svg>
                            <span class="text-sm font-medium text-gray-700">GitHub</span>
                        </a>
                    </div>
                </div>

                <!-- Footer: cadastrar -->
                <p class="mt-6 text-center text-sm text-gray-600">
                    Não tem conta?
                    <a href="{% url 'create-account' %}" class="font-medium text-blue-600 hover:text-blue-700">Cadastrar</a>
                </p>
            </div>
        </div>
    </main>
{% endblock %}
```

> **NOTE:**  
> Não vou comentar sobre os *CSS/TailwindCSS* utilizados porque não é o foco desse tutorial.

Finalmente, se você abrir o projeto (site) na rota/url principal vai aparecer essa `landing page`.

 - [http://localhost:8000/](http://localhost:8000/)

![landing page](images/index-landing-02.png)  










































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

<div id="create-account"></div>

## `Criando a página de cadastro (create-account.html + DB Commands)`

> Aqui nós vamos criar e configurar a nossa `página de cadastro`.

De início vamos começar configurando a rota/url `create-account`:

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import create_account

urlpatterns = [
    path(route="create-account/", view=create_account, name="create-account"),
]
```

Agora, antes de criar a view (ação) que vai ser responsável por redirecionar o usuário para a página de cadastro (GET) e enviar os dados para o Banco de Dados (POST) vamos criar um formulário customizado.

Para fazer esse formulário customizado vamos criar o arquivo [users/forms.py](../users/forms.py) que nada mais é que um classe para criar um formulário genêrico para o nosso App `users` utilizando de tudo o que o Django já tem pronto:

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

> **NOTE:**  
> Ótimo, nós já temos um modelo de formulário com os campos *("username", "email", "password1", "password2")* necessários na hora de criar um novo usuário.

Agora vamos criar uma view (ação) para:

 - Quando alguém clicar em "Cadastrar" na [landing page (index.html)](../templates/pages/index.html) seja redirecionado para [página de cadastro (create-account.html)](../users/templates/pages/create-account.html).
 - E quando alguém cadastrar algum usuário (corretamente), ele seja salvo no Banco de Dados e depois redirecionado para a [landing page (index.html)](../templates/pages/index.html).

[users/views.py](../users/views.py)
```python
from django.contrib import messages
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


def create_account(request):
    # Caso 1: Requisição GET → apenas exibe o formulário vazio
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "pages/create-account.html", {"form": form})

    # Caso 2: Requisição POST → processa o envio do formulário
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        # Se o formulário for válido, salva e redireciona
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("/")

        # Se houver erros, mostra a mesma página com mensagens
        messages.error(request, "Corrija os erros abaixo.")
        return render(request, "pages/create-account.html", {"form": form})
```

**Explicação das principais partes do código:**

**🧩 1. Imports**
```python
from django.contrib import messages
from django.shortcuts import redirect, render
from users.forms import CustomUserCreationForm
```

 - **messages:**
   - Sistema do Django para mostrar mensagens temporárias (feedback ao usuário).
 - **redirect:**
   - Redireciona o usuário para outra página.
 - **render:**
   - Exibe um template HTML com dados.
 - **CustomUserCreationForm:**
   - Formulário customizado criado em `users/forms.py`

**🧩 2. GET — Exibe o formulário**
```python
if request.method == "GET":
    form = CustomUserCreationForm()
    return render(request, "pages/create-account.html", {"form": form})
```

 - `if request.method == "GET":`
   - Verifica se o método é *GET (ou seja, o usuário apenas abriu a página)*.
 - `form = CustomUserCreationForm()`
   - Aqui nós estamos criando uma *instância* do nosso formulário customizado (CustomUserCreationForm).
   - Esse objeto tem todos os metadados necessários:
     - Quais campos devem aparecer (username, email, password1, password2);
     - Como renderizar cada campo (por exemplo: input type="text", input type="password", etc.);
     - Como validar os dados depois que o usuário preencher.
     - **NOTE:** Por fim, vejam que nós não passamos nenhum valor para o objeto CustomUserCreationForm().
 - `return render(request, "pages/create-account.html", {"form": form})`
   - O `form` é enviado ao template (dentro de um dicionário).
   - `O terceiro argumento de render() é o contexto:`
     - Um dicionário com variáveis que o *template (HTML)* pode usar.
     - Nesse caso, o Django envia a variável `form` para o template.
     - Dentro do HTML, você pode acessá-la assim:
       - `{{ form.username }}`
       - `{{ form.email }}`
       - `{{ form.password1 }}`
       - `{{ form.password2 }}`
   - **NOTE:** Essas expressões podem ser utilizadas para gerar automaticamente os elementos `<input>` do formulário com o HTML correto.

**🧩 3. POST — Processa o envio**
```python
elif request.method == "POST":
    form = CustomUserCreationForm(request.POST)
```

 - `elif request.method == "POST":`
   - Verifica se o método é *POST (ou seja, o usuário enviou o formulário)*.
 - `form = CustomUserCreationForm(request.POST)`
   - Aqui nós estamos criando uma *instância* do nosso formulário customizado (CustomUserCreationForm).
   - Porém, agora nós estamos passando como argumento `request.POST`, ou seja, os dados que o usuário enviou.

**🧩 4. Verifica validade e salva**
```python
if form.is_valid():
    form.save()
    messages.success(request, "Conta criada com sucesso! Faça login.")
    return redirect("/")
```

 - `if form.is_valid():`
   - Verifica se o formulário (form) é válido:
     - Se os campos obrigatórios foram preenchidos;
     - Se as senhas coincidem;
     - Se o usuário e o e-mail não existem ainda.
 - `form.save()`
   - Cria automaticamente um novo usuário no banco de dados.
   - O Django já trata de:
     - Fazer o hash da senha (não salva senha em texto puro);
     - Popular os campos corretos da tabela `auth_user`.
 - `messages.success(request, "Conta criada com sucesso! Faça login.")`
   - Adiciona uma mensagem de sucesso à sessão.
   - Essa mensagem pode ser exibida no template com `{% if messages %}`.
 - `return redirect("/")`
   - Redireciona o usuário para a página inicial (login).

**🧩 5. Erros de validação**
```python
messages.error(request, "Corrija os erros abaixo.")
return render(request, "pages/create-account.html", {"form": form})
```

 - Se o formulário tiver erros, o código não redireciona.
 - Mostra o mesmo template novamente, mas com o `form` já contendo:
   - Os dados digitados pelo usuário.
   - As mensagens de erro (`{{ form.errors }}`).`
 - **NOTE:** Assim, o usuário vê o que digitou e pode corrigir os erros sem perder tudo.

> **E o formulário de cadastro?**

Bem, aqui nós vamos criar um formulários (HTML) dinâmicos usando os dados enviados pelo usuário:

```python
form = CustomUserCreationForm(request.POST)
return render(request, "pages/create-account.html", {"form": form})
```

O código completo para fazer isso é o seguinte:

[users/templates/pages/create-account.html](../users/templates/pages/create-account.html)
```html
{% extends "base.html" %}

{% block title %}Criar Conta — Easy RAG{% endblock %}

{% block content %}

    <h1>Criar Conta</h1>

    {% if messages %}
        <ul>
            {% for msg in messages %}
                <li>{{ msg }}</li>
            {% endfor %}
        </ul>
    {% endif %}

    <form method="post" action="">
        {% csrf_token %}

        {{ form.non_field_errors }}

        <div>
            {{ form.username.label_tag }}
            {{ form.username }}
            {{ form.username.errors }}
        </div>

        <div>
            {{ form.email.label_tag }}
            {{ form.email }}
            {{ form.email.errors }}
        </div>

        <div>
            {{ form.password1.label_tag }}
            {{ form.password1 }}
            {{ form.password1.errors }}
        </div>

        <div>
            {{ form.password2.label_tag }}
            {{ form.password2 }}
            {{ form.password2.errors }}
        </div>

        <div>
            <button type="submit">Cadastrar</button>
        </div>
    </form>

    <br>

    <div>
        <a href="/">Já tem uma conta? Fazer login</a>
    </div>

{% endblock %}
```

**Explicação das principais partes do código:**

**🧩 1. Exibe as mensagens criadas na view**
```html
{% if messages %}
    <ul>
        {% for msg in messages %}
            <li>{{ msg }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

 - Esse bloco exibe mensagens do Django (vindas do `messages` framework).
 - Essas mensagens são criadas na view, por exemplo:
   - `messages.success(request, "Conta criada com sucesso!")`

**🧩 2. Inicia o formulário**
```html
<form method="post" action="">
    {% csrf_token %}
```

 - Inicia o formulário HTML.
 - `method="post"` → os dados do formulário serão enviados via POST (para o mesmo endpoint).
 - `action=""` → Significa “enviar para a mesma página”.
 - `{% csrf_token %}` → Gera um token oculto de segurança (CSRF = Cross-Site Request Forgery):
   - Esse token impede que sites externos façam requisições maliciosas no seu sistema.
   - É obrigatório em formulários POST no Django.

**🧩 3. Exibe erros gerais do formulário**
```html
{{ form.non_field_errors }}
```

 - Exibe erros gerais do formulário, que não pertencem a um campo específico.
 - Exemplo: “As senhas não coincidem.”
 - Esses erros são definidos internamente pelo `UserCreationForm` do Django.

**🧩 4. Renderiza o campo username dinamicamente**
```html
<div>
    {{ form.username.label_tag }}
    {{ form.username }}
    {{ form.username.errors }}
</div>
```

 - Renderiza (dinamicamente) o campo username do formulário, gerado automaticamente pelo Django:
   - label_tag → cria a tag `<label>` (ex: “Username:”).
   - form.username → gera o `<input>` correspondente (ex: `<input type="text" name="username">`).
   - form.username.errors → exibe erros específicos desse campo (ex: “Este nome de usuário já existe.”).
 - 💡 O Django gera todo o HTML desses elementos com base na definição da classe `CustomUserCreationForm` em [users/forms.py](../users/forms.py).

**🧩 5. Renderiza o campo email dinamicamente**
```html
<div>
    {{ form.email.label_tag }}
    {{ form.email }}
    {{ form.email.errors }}
</div>
```

 - Mesmo padrão do campo anterior, mas para o campo email.
 - Esse campo foi adicionado manualmente no formulário personalizado *(CustomUserCreationForm)*.

**🧩 6. Renderiza os campos de senha dinamicamente**
```html
<div>
    {{ form.password1.label_tag }}
    {{ form.password1 }}
    {{ form.password1.errors }}
</div>

<div>
    {{ form.password2.label_tag }}
    {{ form.password2 }}
    {{ form.password2.errors }}
</div>
```

 - Esses dois campos vêm do `UserCreationForm` padrão do Django.
 - password1 é a senha principal.
 - password2 é a confirmação da senha.
 - **NOTE:** O próprio Django valida se as duas são iguais e mostra erros automaticamente caso não coincidam.

> **Por fim, como eu sei que os usuários estão sendo gravados no Banco de Dados?**

Primeiro, vamos abrir o container que tem PostgreSQL:

```bash
task opendb
```

Agora vamos listar as tabelas:

```bash
\dt+
```

**OUTPUT:**
```bash
                                               List of relations
 Schema |            Name            | Type  |  Owner  | Persistence | Access method |    Size    | Description
--------+----------------------------+-------+---------+-------------+---------------+------------+-------------
 public | auth_group                 | table | easyrag | permanent   | heap          | 0 bytes    |
 public | auth_group_permissions     | table | easyrag | permanent   | heap          | 0 bytes    |
 public | auth_permission            | table | easyrag | permanent   | heap          | 8192 bytes |
 public | auth_user                  | table | easyrag | permanent   | heap          | 16 kB      |
 public | auth_user_groups           | table | easyrag | permanent   | heap          | 0 bytes    |
 public | auth_user_user_permissions | table | easyrag | permanent   | heap          | 0 bytes    |
 public | django_admin_log           | table | easyrag | permanent   | heap          | 8192 bytes |
 public | django_content_type        | table | easyrag | permanent   | heap          | 8192 bytes |
 public | django_migrations          | table | easyrag | permanent   | heap          | 16 kB      |
 public | django_session             | table | easyrag | permanent   | heap          | 16 kB      |
```

Agora, vamos listas as colunas da tabela `auth_user`:

```bash
\d auth_user
```

**OUTPUT:**
```bash
                                     Table "public.auth_user"
    Column    |           Type           | Collation | Nullable |             Default
--------------+--------------------------+-----------+----------+----------------------------------
 id           | integer                  |           | not null | generated by default as identity
 password     | character varying(128)   |           | not null |
 last_login   | timestamp with time zone |           |          |
 is_superuser | boolean                  |           | not null |
 username     | character varying(150)   |           | not null |
 first_name   | character varying(150)   |           | not null |
 last_name    | character varying(150)   |           | not null |
 email        | character varying(254)   |           | not null |
 is_staff     | boolean                  |           | not null |
 is_active    | boolean                  |           | not null |
 date_joined  | timestamp with time zone |           | not null |
Indexes:
    "auth_user_pkey" PRIMARY KEY, btree (id)
    "auth_user_username_6821ab7c_like" btree (username varchar_pattern_ops)
    "auth_user_username_key" UNIQUE CONSTRAINT, btree (username)
Referenced by:
    TABLE "auth_user_groups" CONSTRAINT "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
    TABLE "auth_user_user_permissions" CONSTRAINT "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
    TABLE "django_admin_log" CONSTRAINT "django_admin_log_user_id_c564eba6_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
```

Por fim, vamos listar todos os usuários (com suas colunas) já cadastrados no Banco de Dados:

```bash
select * from auth_user;
```

**OUTPUT:**
```bash
 id |                                         password                                          |          last_login           | is_superuser | username | first_name | last_name |           email            | is_staff | is_active |          date_joined
----+-------------------------------------------------------------------------------------------+-------------------------------+--------------+----------+------------+-----------+----------------------------+----------+-----------+-------------------------------
  2 | pbkdf2_sha256$1000000$Q77ZUEe8nNZFT3DLvOBMRf$pLgNiCmXRUEaX0XGmC+JX8jTrNqS5I6QMVuutC3ypTw= |                               | f            | rodrigo  |            |           | rodrigo.praxedes@gmail.com | f        | t         | 2025-10-21 10:30:23.466991+00
  3 | pbkdf2_sha256$1000000$93BBiOAKodPLbmgJJtbfBY$HLYRqEN5oCfmZKsA0iGkbbG+KbITmlz26BDl2xRMGbs= | 2025-11-02 09:19:36.900889+00 | f            | romario  |            |           | romario@gmail.com          | f        | t         | 2025-10-28 00:52:23.111699+00
  4 | pbkdf2_sha256$1000000$AW4kQwpGOjvxBWaCg5EMkC$+YnHIhK29DhI8PMJQyx3SIuOnCHGUJgvuuc0XNDrEKs= | 2025-11-02 09:36:10.701396+00 | f            | brenda   |            |           | brenda@gmail.com           | f        | t         | 2025-11-02 09:36:05.24123+00
  1 | pbkdf2_sha256$1000000$TwwCgqC0kp0GRli3xEyzhO$5r01g9G+sbI99a9a6cvgky5XudMjI/ADg+t5wO+1tHw= | 2025-11-02 10:07:32.909962+00 | t            | drigols  |            |           | drigols.creative@gmail.com | t        | t         | 2025-10-21 09:01:46.482399+00
(4 rows)
```










































---

<div id="session-home"></div>

## `Criando a sessão de login/logout + página home.html`

> Aqui nós vamos criar todo mecanismo de `login` e `logout` de usuários.

De início vamos começar configurando as rotas/urls em `users/urls.py`:

[users/urls.py](../users/urls.py)
```python
from django.urls import path

from .views import create_account, home_view, login_view, logout_view

urlpatterns = [
    path(route="", view=login_view, name="index"),
    path(route="home/", view=home_view, name="home"),
    path(route="logout/", view=logout_view, name="logout"),
    path(route="create-account/", view=create_account, name="create-account"),
]
```

> **NOTE:**  
> Antes de criarmos as views (ações) para essas rotas/urls, vamos revisar as views (ações) que nós já tínhamos implementado.

[users/views.py](../users/views.py)
```python
from django.contrib import messages
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


def create_account(request):
    # Caso 1: Requisição GET → apenas exibe o formulário vazio
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "pages/create-account.html", {"form": form})

    # Caso 2: Requisição POST → processa o envio do formulário
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        # Se o formulário for válido, salva e redireciona
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("/")

        # Se houver erros, mostra a mesma página com mensagens
        messages.error(request, "Corrija os erros abaixo.")
        return render(request, "pages/create-account.html", {"form": form})
```

Continuando na implementação das views (ações), vamos começar implementando a view (ação) `home_view`:

[users/views.py](../users/views.py)
```python
# Redireciona para o login se não estiver autenticado
@login_required(login_url="/")
def home_view(request):
    return render(request, "pages/home.html")
```

**Explicação das principais partes do código:**

**🧩 1. Importações necessárias**
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
```

 - `login_required`
   - É um decorator que protege a view, garantindo que somente usuários autenticados possam acessá-la.
   - Se o usuário não estiver logado, ele é automaticamente redirecionado para a página de login (definida no parâmetro login_url).
 - `render`
   - Função do Django que combina um template HTML (`home.html`) com dados do contexto (caso existam) e retorna uma resposta HTTP para o navegador.
   - É a forma mais comum de retornar páginas renderizadas em views Django.

**🧩 2. Aplicação do decorator @login_required**
```python
# Redireciona para o login se não estiver autenticado
@login_required(login_url="/")
```

 - **O que faz?**
   - Essa linha é um decorator, ou seja, um "envoltório" que executa código antes da função `home_view`.
   - Quando alguém tenta acessar `/home/`, o Django verifica:
     - Se o usuário está autenticado, executa `home_view(request)` normalmente.
     - Se não estiver autenticado, o Django interrompe a execução e redireciona automaticamente para `login_url="/"`.
 - **Por que precisamos?**
   - Garante segurança — impede acesso não autorizado a páginas internas do sistema.
   - Evita que um usuário acesse `/home/` apenas digitando a URL no navegador.
 - **Observação:**
   - O `login_url="/"` indica que a página de login é a raiz do site (`index.html`).

Continuando na implementação das views (ações), vamos agora implementar a view (ação) `login_view`:

[users/views.py](../users/views.py)
```python
def login_view(request):
    # Se o usuário já estiver logado, envia direto pra home
    if request.user.is_authenticated:
        return redirect("home")

    # GET → renderiza pages/index.html (form de login)
    if request.method == "GET":
        return render(request, "pages/index.html")

    # POST → processa credenciais
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.error(request, "Usuário ou senha inválidos.")
        return render(request, "pages/index.html")
```

**Explicação das principais partes do código:**

**🧩 1. Checagem se já está autenticado**
```python
if request.user.is_authenticated:
    return redirect("home")
```

 - **O que faz?**  
   - Verifica se a requisição já tem um usuário autenticado (Django fornece request.user).
 - **Por que existe:**  
   - Evita que usuários logados vejam a tela de login novamente — redireciona imediatamente para a página privada (`home`).
 - **Observação:**
   - `is_authenticated` é `True` quando a sessão contém um usuário válido (cookie de sessão presente e válido).

**🧩 2. Tratamento do GET — mostrar o formulário de login**
```python
if request.method == "GET":
    return render(request, "pages/index.html")
```

 - **O que faz?**
   - Quando a página é acessada via `GET`, renderiza o template com o formulário de login.
 - **Por que existe:**
   - Separa o `fluxo de exibição do formulário (GET)` do `fluxo de processamento (POST)`.
 - **Resultado:**
   - O navegador recebe o HTML do `index.html` contendo os campos *"username"* e *"password"*.

**🧩 3. Leitura dos dados do POST e autenticação**
```python
username = request.POST.get("username")
password = request.POST.get("password")
user = authenticate(request, username=username, password=password)
```

 - **O que faz?**
   - Pega os valores enviados pelo formulário `(request.POST)` e chama `authenticate(...)`.
   - **authenticate faz:**
     - Verifica as credenciais contra o backend de autenticação (normalmente a tabela auth_user).
     - Retorna um objeto User se as credenciais baterem, caso contrário None.
 - **Por que:**
   - Permite verificar identidade sem ainda criar sessão — apenas valida.

**🧩 4. Login bem-sucedido → criar sessão e redirecionar**
```python
if user is not None:
    login(request, user)
    return redirect("home")
```

 - **O que faz?**
   - `login(request, user)`
     - Cria a sessão do usuário (Django grava na sessão o ID do usuário e configura o cookie de sessão).
   - `redirect("home")`
     - Envia o usuário à página protegida.
     - **Por que?** Estabelecimento da sessão é o passo que efetivamente **“loga”** o usuário no site; após isso, `request.user` será o usuário autenticado em requisições seguintes.

**🧩 5. Falha na autenticação → feedback e reexibir o formulário**`
```python
else:
    messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "pages/index.html")
```

 - **O que faz?**
   - Adiciona uma mensagem de erro (usando o framework `messages`) e renderiza novamente a página de login (`index.html`).
 - **Por que:**
   - Informar o usuário que as credenciais estavam incorretas e permitir uma nova tentativa, preservando a UX.
 - **Observação de segurança:**
   - Não dá detalhe sobre qual campo falhou **(boa prática para evitar user-enumeration)**.

Por fim, o nosso usuário precisa também deslogar do sistema e para isso vamos criar a view (ação) `logout_view`:

[users/views.py](../users/views.py)
```pydef logout_view(request):
    logout(request)
    return redirect("/")
```

**Explicação das principais partes do código:**

**🧩 1. Encerramento da sessão do usuário**
```python
logout(request)
```

 - **O que faz?**
   - Chama a função `logout()` do Django, que remove o usuário autenticado da sessão.
   - Isso significa que:
     - O cookie de autenticação é apagado.
     - `request.user` deixa de ser o usuário logado e passa a ser `AnonymousUser`.
   - A sessão no banco de dados (ou no cache, dependendo da configuração) é destruída.
 - **Por que existe?**
   - Garante que o usuário saia com segurança do sistema, protegendo o acesso à conta em dispositivos compartilhados.
 - **Importante:**
   - Essa função não precisa de parâmetros extras — o Django automaticamente identifica e limpa a sessão ativa a partir do request.

**🧩 2. Redirecionamento após logout**
```python
return redirect("/")
```

 - **O que faz?**
   - Redireciona o usuário de volta para a página de login (raiz `/`).
 - **Por que existe?**
   - Depois que o usuário sai, não faz sentido mantê-lo em uma página protegida (`home`, por exemplo);
   - Enviar de volta para `/ (login)` é o comportamento padrão e esperado após logout.
 - **Resultado final:**
   - Sessão encerrada;
   - Usuário anônimo;
   - Redirecionamento automático para a tela de login.

> **Ótimo, o que falta agora?**  
> Implementar o template `users/templates/pages/home.html` (página de boas-vindas);

[users/templates/pages/home.html](../users/templates/pages/home.html)
```html
{% extends "base.html" %}

{% block title %}Home — Easy RAG{% endblock %}

{% block content %}
    <h1>Bem-vindo, {{ request.user.username }}!</h1>
    <p>Você está logado com sucesso.</p>

    <a href="{% url 'logout' %}">Sair</a>
{% endblock %}
```










































---

<div id="login-google-github"></div>

## `Criando o login com Google e GitHub`

#### 17.1 Instalando e Configurando a biblioteca django-allauth

> Aqui nós vamos instalar e configurar o `django-allauth`, que é uma biblioteca pronta para adicionar *autenticação social (OAuth)* e *funcionalidades de conta (login, logout, registro, verificação de e-mail)* ao seu projeto Django.

Vamos começar instalando as dependências e a biblioteca `django-allauth`:

**Dependências para o "django-allauth" funcionar corretamente:**
```bash
poetry add PyJWT@latest
```

```bash
poetry add cryptography@latest
```

**Instalando o "django-allauth":**
```bash
poetry add django-allauth@latest
```

Agora vamos adicionar o `django-allauth` aos apps do projeto:

[core/settings.py](../core/settings.py)
```python
INSTALLED_APPS = [
    # Apps padrão do Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Obrigatório pro allauth
    "django.contrib.sites",

    # Apps principais do allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Provedores de login social
    "allauth.socialaccount.providers.google",  # 👈 habilita login com Google
    "allauth.socialaccount.providers.github",  # 👈 habilita login com GitHub

    # Seus apps
    "users",
]
```

 - `django.contrib.sites`
   - App do Django que permite associar configurações a um Site (domínio) — o allauth usa isso para saber qual domínio/URL usar para callbacks OAuth.
   - Você precisará criar/ajustar um Site no admin (ou via fixtures) com SITE_ID = 1 (ver mais abaixo).
 - `allauth, allauth.account, allauth.socialaccount`
   - `allauth` é o pacote principal;
   - `account` fornece funcionalidade de conta (registro, login local, confirmação de e-mail);
   - `socialaccount` é a camada que integra provedores OAuth (Google, GitHub, etc.).
 - `allauth.socialaccount.providers.google, allauth.socialaccount.providers.github`
   - Provedores prontos do allauth — carregam os adaptadores e rotas específicas para cada provedor.
   - Adicione apenas os provedores que você pretende suportar (pode ativar mais tarde).

Agora nós vamos adicionar `context_processors.request` e configurar `AUTHENTICATION_BACKENDS` (`settings.py`):

[core/settings.py](../core/settings.py)
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # <- Necessário para allauth
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# AUTHENTICATION_BACKENDS — combine o backend padrão com o do allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",            # Seu login normal
    "allauth.account.auth_backends.AuthenticationBackend",  # Login social
]
```

Outras configurações importantes no `settings.py` são as seguintes:

[core/settings.py](../core/settings.py)
```python
SITE_ID = 1

LOGIN_REDIRECT_URL = "/home/"  # ou o nome da rota que preferir
LOGOUT_REDIRECT_URL = "/"      # para onde o usuário vai depois do logout

# Permitir login apenas com username (pode ser {'username', 'email'} se quiser os dois)
ACCOUNT_LOGIN_METHODS = {"username"}

# Campos obrigatórios no cadastro (asterisco * indica que o campo é requerido)
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"     # "mandatory" em produção
```

 - `SITE_ID = 1`
   - Diz ao Django qual registro na tabela django_site representa este site. Allauth usa essa associação para Social Applications (cada SocialApplication é vinculado a um Site).
   - No admin, você provavelmente terá que criar/editar o Site com id=1 para corresponder a localhost:8000 (em dev) ou o domínio real em produção.
 - `LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL`
   - Define para onde o usuário é enviado após login/logout. Ajuste conforme sua rota home.
 - `ACCOUNT_LOGIN_METHODS`
   - Define quais métodos de login o allauth deve aceitar.
   - Ele usa um set `{}` porque você pode permitir mais de um método:
     - `ACCOUNT_LOGIN_METHODS = {"username"}           # só com username`
     - `ACCOUNT_LOGIN_METHODS = {"email"}              # só com email`
     - `ACCOUNT_LOGIN_METHODS = {"username", "email"}  # permite ambos`
 - `ACCOUNT_SIGNUP_FIELDS`
   - Lista os campos exibidos e obrigatórios no cadastro.
   - O asterisco `*` significa “campo obrigatório”:
     - `["email*", "username*", "password1*", "password2*"]`
     - **NOTE:** Assim, se o usuário tentar se cadastrar sem um desses campos, o allauth exibirá automaticamente os erros de validação.

Agora depois de tudo configurado, nós devemos:

 - `python manage.py migrate`
   - Aplica tabelas necessárias (inclui *django_site*, *socialaccount models*, etc.).
 - `Rode o servidor:`
   - `python manage.py runserver`
   - Acesse o admin → http://localhost:8000/admin/
   - Vá em Sites → clique em Sites → edite o existente (id=1):
     - Domain name: localhost:8000
     - Display name: Easy RAG

Agora que o `django-allauth` está instalado e registrado no `settings.py`, precisamos conectar suas rotas (URLs) ao projeto principal.

Essas rotas incluem:

 - /accounts/login/ (Não é o nosso caso, pois já implementamos)
 - /accounts/logout/ (Não é o nosso caso, pois já implementamos)
 - /accounts/signup/ (Não é o nosso caso, pois já implementamos - cadastro)
 - /accounts/google/login/
 - /accounts/github/login/,... etc.

E também vamos garantir que o **SITE_ID** e o **modelo Site** estejam corretamente configurados para o domínio do projeto (como localhost:8000 no ambiente de desenvolvimento).

No seu arquivo `core/urls.py`, adicione a seguinte linha:

[core/urls.py](../core/urls.py)
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    # Rotas do django-allauth
    path("accounts/", include("allauth.urls")),
]
```

 - `path("accounts/", include("allauth.urls"))`
   - Importa e registra automaticamente todas as rotas padrão do `django-allauth`.
   - Isso adiciona páginas como:
     - `/accounts/login/` → página de login.
     - `/accounts/signup/` → página de cadastro.
     - `/accounts/logout/` → logout.
     - `/accounts/google/login/` → login social com Google.
     - `/accounts/github/login/` → login social com GitHub.

Com o servidor Django rodando acesse (só para testes):

 - http://localhost:8000/accounts/login/
 - http://localhost:8000/accounts/signup/
 - http://localhost:8000/accounts/google/login/
 - http://localhost:8000/accounts/github/login/

 - **🧩 1.**
   - Essas rotas são criadas automaticamente pelo allauth.
   - Você ainda não configurou as credenciais (client ID e secret) dos provedores, então clicar nelas ainda não vai funcionar — isso é normal neste ponto.
 - **🧩 2.**
   - Esse teste serve apenas para confirmar que as rotas foram registradas corretamente e o `django-allauth` está funcionando.

**NOTE:**  
O `django-allauth` usa seus próprios templates internos, mas você pode sobrescrevê-los criando uma pasta como:

```
templates/account/login.html
templates/account/signup.html
```

#### 17.2 Configuração do Google OAuth (login social)

 - Agora que o django-allauth já está instalado e com as rotas funcionando, nós vamos integrar o login social usando o Google e o GitHub.
 - Essas integrações permitirão que o usuário acesse seu sistema sem criar uma conta manualmente, apenas autenticando-se com uma dessas plataformas.

 - **Etapas no Console do Google:**
   - Acesse https://console.cloud.google.com/
   - Faça login e crie um novo projeto (ex: Easy RAG Auth).
   - No menu lateral, vá em:
     - APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth 2.0
   - Clique no botão “Configure consent screen”
     - Clique em `Get started`
     - **Em App Information:**
       - `App name:`
         - Easy RAG
         - Esse nome aparecerá para o usuário quando ele for fazer login pelo Google.
       - `User support email:`
         - Selecione seu e-mail pessoal (ele aparece automaticamente no menu).
         - É usado pelo Google caso o usuário queira contato sobre privacidade.
       - Cli quem `next`
     - **Em Audience:**
       - Aqui o Google vai perguntar quem pode usar o aplicativo.
       - ✅ External (Externo):
         - Isso significa que qualquer usuário com uma conta Google poderá fazer login (ótimo para ambiente de testes e produção pública).
     - **Contact Information:**
       - O campo será algo como:
         - Developer contact email:
           - Digite novamente o mesmo e-mail (ex: seuemail@gmail.com)
         - Esse é o contato para eventuais notificações do Google sobre a aplicação.
     - **Finish:**
       - Revise as informações e clique em Create (botão azul no canto inferior esquerdo).
       - Isso cria oficialmente a tela de consentimento OAuth.

**✅ Depois que criar**

Você será redirecionado automaticamente para o painel de `OAuth consent screen`. De lá, basta voltar:

 - Ao menu lateral → APIs & Services → Credentials;
 - e aí sim o botão `+ Create credentials` → `OAuth client ID` ficará habilitado.

Agora escolha:

 - **Tipo de aplicativo:**
   - Aplicativo da Web
 - **Nome:**
   - Easy RAG - Django
 - **Em URIs autorizados de redirecionamento, adicione:**
   - http://localhost:8000/accounts/google/login/callback/
 - **Clique em Criar**
 - Copie o `Client ID` e o `Client Secret`

> **NOTE:**  
> Essas *informações (Client ID e Secret)* serão configuradas no admin do Django, não diretamente no código.

#### 17.3 Configuração do GitHub OAuth (login social)

 - Vá em https://github.com/settings/developers
 - Clique em OAuth Apps → New OAuth App
 - Preencha:
   - *Application name:* Easy RAG
   - *Homepage URL:* http://localhost:8000
   - *Authorization callback URL:* http://localhost:8000/accounts/github/login/callback/
 - Clique em `Register Application`
 - Copie o `Client ID`
 - Clique em `Generate new client secret` e copie o `Client Secret`

#### 17.4 Registrando os provedores no Django Admin

 - 1️⃣ Acesse: http://localhost:8000/admin/
 - 2️⃣ Vá em: Social Accounts → Social Applications → Add Social Application
 - 3️⃣ Crie o do Google:
   - Provider: Google
   - Name: Google Login
   - Client ID: (cole o do Google)
   - Secret Key: (cole o secret)
   - Por fim, vá em `Sites`:
     - *"Available sites"*
     - *"Choose sites by selecting them and then select the "Choose" arrow button"*
       - Adicione (Se não tiver): localhost:8000
       - Selecione localhost:8000 e aperta na seta `->`
 - 4️⃣ Repita o processo para o GitHub:
   - Provider: GitHub
   - Name: GitHub Login
   - Client ID: (cole o do GitHub)
   - Secret Key: (cole o secret)
   - Por fim, vá em `Sites`:
     - *"Available sites"*
     - *"Choose sites by selecting them and then select the "Choose" arrow button"*
       - Adicione (Se não tiver): localhost:8000
       - Selecione localhost:8000 e aperta na seta `->`

#### 17.5 Testando os logins sociais (Google e GitHub)

Uma maneira de testar os logins sociais é abrindo a rota/url:

 - http://localhost:8000/accounts/login/

> **NOTE:**  
> Se aparecer os botões de `Google` e `GitHub` para login é porque tudo está configurado corretamente.

#### 17.6 Customizando os botões do Google e GitHub no template `index.html`

 - Até aqui, você configurou o `django-allauth` e registrou os provedores (Google e GitHub) no painel administrativo.
 - Agora, vamos fazer com que os botões **“Entrar com Google”** e **“Entrar com GitHub”** funcionem de verdade, conectando o *front-end* com o *allauth*.

[templates/pages/index.html](../templates/pages/index.html)
```html
{% extends "base.html" %}
{% load socialaccount %}

{% block title %}Easy RAG{% endblock %}

{% block content %}
    <h1>Easy RAG</h1>

    <!-- Formulário de login básico -->
    <form method="post" action="">
        {% csrf_token %}
        <div>
            <label for="username">Username</label><br>
            <input type="text" id="username" name="username" autocomplete="username" required>
        </div>

        <div>
            <label for="password">Password</label><br>
            <input type="password" id="password" name="password" autocomplete="current-password" required>
        </div>

        <div>
            <button type="submit">Entrar</button>
        </div>
    </form>

    <br>

    <!-- Botões de login social reais -->
    <div>
        <a href="{% provider_login_url 'google' %}">
            <button type="button">Entrar com Google</button>
        </a>
        <a href="{% provider_login_url 'github' %}">
            <button type="button">Entrar com GitHub</button>
        </a>
    </div>

    <br>

    <div>
        <a href="{% url 'create-account' %}">Cadastrar</a>
    </div>
{% endblock %}
```

**Explicação das principais partes do código:**

**🧩 1. Herança do template e carregamento de tags**
```html
{% extends "base.html" %}
{% load socialaccount %}
```

 - `{% extends "base.html" %}`
   - Indica que este template herda a estrutura geral de `base.html (cabeçalho, <html>, <body>, etc.)`.
 - `{% load socialaccount %}`
   - Importa as template tags fornecidas pelo `django-allauth (ex.: {% provider_login_url %})`.
   - Sem esse `load`, as tags sociais nao seriam reconhecidas pelo template engine.

**🧩 2. Botões de login social (links gerados pelo allauth)**
```html
<div>
    <a href="{% provider_login_url 'google' %}">
        <button type="button">Entrar com Google</button>
    </a>
    <a href="{% provider_login_url 'github' %}">
        <button type="button">Entrar com GitHub</button>
    </a>
</div>
```

 - **O que faz?**
   - `{% provider_login_url 'google' %}` e `{% provider_login_url 'github' %}`
     - Geram as URLs corretas para iniciar o fluxo `OAuth` com *Google* e *GitHub* (fornecidas pelo django-allauth).
     - Os `<a>` envolvem botões visuais que, ao clicar, redirecionam o usuário para o provedor externo.
 - **Por que é importante?**
   - Conecta o front-end ao sistema de login social do allauth.
   - O allauth cuida de gerar a URL correta, adicionar parâmetros e tratar callbacks.
 - **Observações práticas:**
   - Antes de usar essas tags, você precisa ter:
     - Registrado os provedores em `INSTALLED_APPS` (ex.: allauth.socialaccount.providers.google e ...github).
     - Criado os SocialApplication no Admin com Client ID/Secret e associado ao Site correto.
   - Se algum desses estiver faltando, o template pode lançar erros (DoesNotExist) ao renderizar a tag.

#### 17.6 Criando `adapter.py`

O arquivo `adapter.py` serve para *personalizar o comportamento interno do Django Allauth*, que é o sistema responsável pelos *logins*, *logouts* e *cadastros* — tanto locais quanto via provedores sociais (como Google e GitHub).

Por padrão, o Allauth envia automaticamente mensagens para o sistema de mensagens do Django (django.contrib.messages), exibindo textos como:

 - “Successfully signed in as rodrigols89.”
 - “You have signed out.”
 - “Your email has been confirmed.”

Essas mensagens são geradas dentro dos adapters do `Allauth` — classes que controlam como ele interage com o Django.

Agora, vamos criar nossas versões personalizadas dos adapters (`NoMessageAccountAdapter` e `NoMessageSocialAccountAdapter`) para impedir que essas mensagens automáticas sejam exibidas.

> **NOTE:**  
> Assim, temos controle total sobre quais mensagens aparecem para o usuário — mantendo o front mais limpo e sem textos gerados automaticamente.

[users/adapter.py](../users/adapter.py)
```python
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoMessageAccountAdapter(DefaultAccountAdapter):
    """
    Adapter para suprimir mensagens que o allauth adicionaria ao sistema
    de messages.

    Aqui fazemos nada no add_message — assim o allauth não adiciona
    mensagens.
    """
    def add_message(self, request, level, message_template,
                    message_context=None):
        # Return sem chamar super()
        # Evita que o allauth chame messages.add_message(...)
        return


class NoMessageSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Mesmo para socialaccount, caso mensagens venham de lá."""
    def add_message(self, request, level, message_template,
                    message_context=None):
        # Return sem chamar super()
        # Evita que o allauth chame messages.add_message(...)
        return
```

Por fim, vamos adicionar algumas configurações gerais em `settings.py`:

[settings.py](../core/settings.py)
```python
ACCOUNT_ADAPTER = "users.adapter.NoMessageAccountAdapter"
SOCIALACCOUNT_ADAPTER = "users.adapter.NoMessageSocialAccountAdapter"
```

**Observações:**

 - Use o caminho Python completo para a classe. No exemplo acima assumimos que o app chama `users` e que `users` está no `INSTALLED_APPS`.
 - Reinicie o servidor (python manage.py runserver) depois de editar `settings.py` para que as mudanças tenham efeito.

























































































---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
