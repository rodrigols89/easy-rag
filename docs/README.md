# Easy RAG

## Conteúdo

 - [`Adicionando .editorconfig e .gitignore`](#editorconfig-gitignore)
 - [`Iniciando o projeto com "poetry init"`](#poetry-init)
 - [`Instalando e configurando o Ruff`](#ruff-settings-pyproject)
 - [`Instalando e configurando o Pytest`](#pytest-settings-pyproject)
 - [`Instalando e configurando o Taskipy`](#taskipy-settings-pyproject)
 - [`Instalando e configurando o pre-commit`](#precommit-settings)
 - [`Criando o container com PostgreSQL (db)`](#db-container)
 - [`Criando o container com Redis (redis_cache)`](#redis-container)
 - [`Instalando/Configurando/Exportando o Django + Uvicorn + PostgresSQL`](#django-settings)
 - [`Criando o container web: Dockerfile + Django + Uvicorn`](#web-container)
 - [`Criando o container Nginx (nginx)`](#nginx-container)
 - [`Configurando o Django para reconhecer o PostgreSQL (+ .env) como Banco de Dados`](#django-postgresql-settings)
 - [`Variáveis de Ambiente`](#env-vars)
 - [`Comandos Taskipy`](#taskipy-commands)
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

```bash
poetry add --group dev pytest-cov@latest
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

<div id="db-container"></div>

## `Criando o container com PostgreSQL (db)`

> Aqui nós vamos entender e criar um container contendo o `Banco de Dados PostgreSQL`.

 - **Função:**
   - Armazenar dados persistentes da aplicação (usuários, arquivos, prompts, etc.).
 - **Quando usar:**
   - Sempre que precisar de um banco de dados relacional robusto.
 - **Vantagens:**
   - ACID (consistência e confiabilidade).
   - Suporte avançado a consultas complexas.
 - **Desvantagens:**
   - Mais pesado que bancos NoSQL para dados muito simples.

Antes de criar nosso container contendo o *PostgreSQL* vamos criar as variáveis de ambiente para esse container:

[.env](../.env)
```bash
# ==========================
# CONFIGURAÇÃO DO POSTGRES
# ==========================
POSTGRES_DB=easy_rag_db           # Nome do banco de dados a ser criado
POSTGRES_USER=easyrag             # Usuário do banco
POSTGRES_PASSWORD=easyragpass     # Senha do banco
POSTGRES_HOST=db                  # Nome do serviço (container) do banco no docker-compose
POSTGRES_PORT=5432                # Porta padrão do PostgreSQL
```

 - `PostgreSQL (db)`
   - `POSTGRES_DB` → nome do banco criado automaticamente ao subir o container.
   - `POSTGRES_USER` → usuário administrador do banco.
   - `POSTGRES_PASSWORD` → senha do usuário do banco.
   - `POSTGRES_HOST` → para o Django se conectar, usamos o nome do serviço (db), não localhost, pois ambos estão na mesma rede docker.
   - `POSTGRES_PORT` → porta padrão 5432.

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *PostgreSQL* ficará assim:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  db:
    image: postgres:15
    container_name: postgresql
    restart: always
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
```

 - `db`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: postgres:15`
   - Pega a versão 15 oficial do PostgreSQL no Docker Hub.
 - `container_name: postgresql`
   - Nome fixo do container (para facilitar comandos como docker logs postgresql).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.
 - `volumes:`
     - `postgres_data:` → Volume docker (Named Volume).
     - `/var/lib/postgresql/data` → pasta interna do container onde o Postgres armazena os dados.
 - `ports: 5432:5432`
   - `Primeiro 5432:` → porta no host (sua máquina).
   - `Segundo 5432:` → porta dentro do container onde o Postgres está rodando.
   - **NOTE:** Isso permite que você use o psql ou qualquer ferramenta de banco de dados (DBeaver, TablePlus, etc.) diretamente do seu PC.
 - `volumes:`
   - `postgres_data:` → Volume docker (Named Volume).
 - `networks: backend`
   - Coloca o container na rede backend para comunicação interna segura.

Agora é só subir o container:

```bash
docker compose up -d
```

Agora, se você desejar se conectar nesse Banco de Dados via *bash* utilize o seguinte comando (As vezes é necessário esperar o container/banco de dados subir):

**Entrar no container "postgres_db" via bash:**
```bash
docker exec -it postgresql bash
```

**Entra no banco de sados a partir das variáveis de ambiente:**
```bash
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

> **E os volumes como eu vejo?**

```bash
docker volume ls
```

**OUTPUT:**
```bash
DRIVER    VOLUME NAME
local     ragproject_postgres_data
```

Nós também podemos inspecionar esse volume:

```bash
docker volume inspect ragproject_postgres_data
```

**OUTPUT:**
```bash
[
    {
        "CreatedAt": "2025-08-18T10:11:49-03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "a700fdfee7f177c7f6362471e765e6d38489efcbffced2de9741a321d0b88646",
            "com.docker.compose.project": "easy-rag",
            "com.docker.compose.version": "2.39.1",
            "com.docker.compose.volume": "postgres_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/easy-rag_postgres_data/_data",
        "Name": "easy-rag_postgres_data",
        "Options": null,
        "Scope": "local"
    }
]
```

 - `Mountpoint`
   - O *Mountpoint* é onde os arquivos realmente ficam, mas não é recomendado mexer manualmente lá.
   - Para interagir com os dados, use o *container* ou ferramentas do próprio serviço (por exemplo, psql no Postgres).










































---

<div id="redis-container"></div>

## `Criando o container com Redis (redis_cache)`

> Aqui nós vamos entender e criar um container contendo um `cache Redis`.

 - **Função:**
   - Armazenar dados temporários (cache, sessões, filas de tarefas).
 - **Quando usar:**
   - Quando for necessário aumentar velocidade de acesso a dados temporários ou usar filas.
 - **Vantagens:**
   - Muito rápido (em memória).
   - Perfeito para cache e tarefas assíncronas.
 - **Desvantagens:**
   - Não indicado para dados críticos (pode perder dados em caso de reinício)

Antes de criar nosso container contendo o *Redis* vamos criar as variáveis de ambiente para esse container:

[.env](../.env)
```bash
# ==========================
# CONFIGURAÇÃO DO REDIS
# ==========================
REDIS_HOST=redis                  # Nome do serviço (container) do Redis no docker-compose
REDIS_PORT=6379                   # Porta padrão do Redis
```

 - `Redis (redis)`
   - `REDIS_HOST` → nome do serviço no docker-compose.
   - `REDIS_PORT` → porta padrão 6379.
   - **NOTE:** O Redis será usado como cache e possivelmente fila de tarefas (com Celery, RQ ou outro).

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *Redis* ficará assim:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  redis:
    image: redis:7
    container_name: redis_cache
    restart: always
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  redis_data:

networks:
  backend:
```

 - `redis:`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: redis:7`
   - Pega a versão 7 oficial do Redis no Docker Hub.
 - `container_name: redis_cache`
   - Nome fixo do container (para facilitar comandos como docker logs redis_cache).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.
 - `volumes:`
     - `redis_data:` → Volume docker (Named Volume).
     - `/data` → pasta interna do container onde o Redis armazena os dados.
 - `networks: backend`
   - Só está acessível dentro da rede interna backend (não expõe porta para fora).

Agora é só subir o container:

```bash
docker compose up -d
```

> **E os volumes como eu vejo?**

```bash
docker volume ls
```

**OUTPUT:**
```bash
DRIVER    VOLUME NAME
local     ragproject_redis_data
```

Nós também podemos inspecionar esse volume:

```bash
docker volume inspect ragproject_redis_data
```

**OUTPUT:**
```bash
[
    {
        "CreatedAt": "2025-11-10T07:35:18-03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "75e82217f9045c1c51074e1c927a0ba2be71af9e784263a59e10d6bfb25e12e6",
            "com.docker.compose.project": "ragproject",
            "com.docker.compose.version": "2.39.1",
            "com.docker.compose.volume": "redis_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/ragproject_redis_data/_data",
        "Name": "ragproject_redis_data",
        "Options": null,
        "Scope": "local"
    }
]
```

 - `Mountpoint`
   - O *Mountpoint* é onde os arquivos realmente ficam, mas não é recomendado mexer manualmente lá.
   - Para interagir com os dados, use o *container* ou ferramentas do próprio serviço (por exemplo, psql no Postgres).










































---

<div id="django-settings"></div>

## `Instalando/Configurando/Exportando o Django + Uvicorn + PostgresSQL`

 - Antes de criar um container contendo o Django, vamos instalar e configurar o Django + Uvicorn na nossa máquina local (host).
 - **NOTE:** Vai ser como um modelo que nós vamos utilizar dentro do container.

#### `Instalações iniciais`

De início, vamos instalar as bibliotecas necessárias:

```bash
poetry add django@latest
```

```bash
poetry add uvicorn@latest
```

#### `Criando o projeto Django (core)`

Agora vamos criar o projeto (core) que vai ter as configurações iniciais do Django:

```bash
django-admin startproject core .
```

#### `Configurando os arquivos: templates, static e media`

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

Até aqui está quase tudo ok para criarmos um Container com `Django` e `Uvicorn`...

> Mas, antes de criar nossos containers, precisamos gerar os `requirements.txt` e `requirements-dev.txt`.

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

Outra coisa importante agora é excluir o arquivo `core/settings.py` do ruff:

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











































---

<div id="web-container"></div>

## `Criando o container web: Dockerfile + Django + Uvicorn`

Antes de criar o container contendo o *Django* e o *Uvicorn*, vamos criar o nosso Dockerfile...

> **Mas por que eu preciso de um Dockerfile para o Django + Uvicorn?**

**NOTE:**  
O Dockerfile é onde você diz **como** essa imagem será construída.

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

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *web* ficará assim:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django_web
    restart: always
    env_file: .env
    command: >
      sh -c "
      python manage.py migrate &&
      python manage.py collectstatic --noinput &&
      uvicorn core.asgi:application --host 0.0.0.0 --port 8000
      "
    volumes:
      - .:/code
      - ./static:/code/staticfiles
      - ./media:/code/media
    depends_on:
      - db
      - redis
    ports:
      - "${UVICORN_PORT}:${UVICORN_PORT}"
    networks:
      - backend

networks:
  backend:
```

 - `web`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `build: context + dockerfile.`
   - `context: .`
     - Ponto `(.)` significa que o contexto de build é a raiz do projeto.
     - Isso quer dizer que todos os arquivos dessa pasta estarão disponíveis para o build.
   - `dockerfile: Dockerfile`
     - Nome do arquivo Dockerfile usado para construir a imagem.
 - `container_name: django`
   - Nome fixo do container (para facilitar comandos como docker logs django).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env`.
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
 - `volumes:`
   - `./:/code`
     - pasta atual `.` → `/code` dentro do container.
   - `./static:/code/staticfiles`
     - `./static` → `/code/staticfiles`
   - `./media:/code/media`
     - `./media` → `/code/media`
   - **NOTE:** Aqui estamos aplicando o coneito de *"Bind Mounts"*.
 - `depends_on:`
   - Dependendo que os containers `db` e `redis` estejam rodando.
 - `ports: "${UVICORN_PORT}:${UVICORN_PORT}"`
   - `expose` - Para apenas informa a porta para outros containers, não mapeia para o host.
   - `port` - Para acessar pelo navegador no seu computador, você precisa de `ports`.
 - `networks: backend`
   - Rede interna para comunicação.

#### `Crie as pastas ./static, ./media e ./staticfiles no host (máquina local)`

Uma observação aqui é que antes de nós executamos o container web nós precisamos criar as pastas (diretórios) `./static`, `./media` e `./staticfiles` no host (máquina local).

> **Por que?**

Porque se essas pastas (diretórios) forem criadas pelo container ela não terterão as permissões do nosso usuário (do nosso sistema), elas virão com permissão root (do container).

O comando para fazer isso é o seguinte:

```bash
mkdir -p static media staticfiles
```

Outra coisa interessante é você dar permissões para esses diretórios:

```bash
sudo chown -R 1000:1000 ./static ./media ./staticfiles || true &&
sudo chmod -R 755 ./static ./media ./staticfiles
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

Por fim, vamos subir o container web:

```bash
docker compose up -d
```

Se tudo ocorrer bem você pode abrir no navegador:

 - [http://localhost:8000/](http://localhost:8000/)












































---

<div id="nginx-container"></div>

## `Criando o container Nginx (nginx)`

Para entender a necessidade do Nginx, vamos começar imaginando que nós criamos uma conta de **super usuário** no Django (pode ser na sua máquina local mesmo):

**Roda/Executa o comando "migrate" a partir do serviçor "web":**
```bash
docker compose exec web python manage.py migrate
```

**Roda/Executa o comando "createsuperuser" a partir do serviçor "web":**
```bash
docker compose exec web python manage.py createsuperuser
```

Agora é só abrir o **Django Admin** e verificar se temos a tabela `users`:

 - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

![img](images/nginx-01.png)  

Vejam que:

 - Está tudo mal formado;
 - Sem estilização (CSS)...

> **Por que isso?**

 - **Executando/Rodando na máquina local**:
   - Quando você roda o Django na sua máquina local (fora do container), ele serve os arquivos estáticos automaticamente porque:
     - `DEBUG=True`
     - O servidor de desenvolvimento (runserver) serve /static/ diretamente.
 - **Executando/Rodando no container**:
   - Mas dentro do Docker, o **servidor Uvicorn não serve arquivos estáticos por padrão**.
   - Uvicorn é um ASGI server puro, *não um servidor web completo (como o runserver do Django)*.
   - **NOTE:** Por isso, o Django Admin aparece sem CSS.

#### `Como resolver isso? Usando Nginx`

Para ambientes de produção profissional, você deve:

 - Deixar o Uvicorn apenas para as requisições dinâmicas (ASGI);
 - Deixar o Nginx servir /static/ e /media/ diretamente.

 - **Função:**
   - Servir arquivos estáticos e atuar como *proxy reverso* para o Django.
 - **Quando usar:**
   - Sempre em produção para segurança e desempenho.
 - **Reverse proxy:**
   - Receber as requisições HTTP/HTTPS dos clientes.
   - Redirecionar (proxy_pass) para seu container Django (web).
   - Isso permite que seu backend fique “escondido” atrás do Nginx, ganhando segurança e performance.
 - **Servir arquivos estáticos e de mídia diretamente:**
   - Em Django, arquivos estáticos (/static/) e de upload (/media/) não devem ser servidos pelo Uvicorn (ineficiente).
   - O Nginx é muito melhor para isso, então ele entrega esses arquivos direto do volume.
 - **HTTPS (SSL/TLS):**
   - Configurar certificados (ex.: Let’s Encrypt) para rodar sua aplicação com HTTPS.
   - O Django não lida com certificados nativamente, então o Nginx faz esse papel.
 - **Balanceamento e cache (futuro):**
   - Se você crescer, pode colocar vários containers de Django e usar o Nginx como load balancer.
   - Também pode configurar cache de páginas ou de assets.
 - **Vantagens:**
   - Muito rápido para servir arquivos estáticos.
   - HTTPS e balanceamento de carga.
 - **Desvantagens:**
   - Exige configuração inicial extra.
 - **👉 Resumindo:**
   - O Nginx é a porta de entrada da sua aplicação, cuidando de performance, segurança e organização.

**NOTE:**  
Mas antes de criar e iniciar o nosso container com Nginx, vamos alterar uma configuração no nosso container `web`:

[docker-compose.yml](../docker-compose.yml)
```yaml
  web:

    ...

    expose:
      - "8000"

    ...
```

> **O que mudou?**

 - **Antes nós tinhamos:**
   - `ports: "${UVICORN_PORT}:${UVICORN_PORT}"`
   - ✅ Antes (ports) — Tornava a porta 8000 acessível externamente no host (ex.: http://localhost:8000).
 - **Agora nós temos:**
   - `expose: ["8000"]`
   - ✅ Agora (expose) — Deixa a porta 8000 visível apenas entre containers na rede Docker, invisível fora.

Com essa alteração feita, agora vamos criar/configurar o [docker-compose.yml](../docker-compose.yml) para o nosso container `nginx`:

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  nginx:
    image: nginx:1.27
    container_name: nginx_reverse_proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/code/staticfiles
      - ./media:/code/media
    depends_on:
      - web
    networks:
      - backend

networks:
  backend:
```

 - `nginx:`
   - Nome do *serviço (container)* criado pelo docker-compose.
 - `image: nginx:1.27`
   - Pega a versão 1.27 oficial do Nginx no Docker Hub.
 - `container_name: nginx_reverse_proxy`
   - Nome fixo do container (para facilitar comandos como docker logs nginx_server).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `ports:`
   - Mapeia portas do host para o container:
     - `80:80` → HTTP
     - `443:443` → HTTPS
 - `volumes:`
   - Pasta local `./nginx/conf` → onde ficam configs do Nginx.
   - Volumes `static` e `media` para servir arquivos.
 - `depends_on:`
   - Só inicia depois que o `Django (web)` estiver rodando.
 - `networks: backend`
   - Rede interna para conversar com Django sem expor a aplicação diretamente.

Agora nós precisamos criar o arquivo de configuração do `Nginx`:

[nginx.conf](../nginx/nginx.conf)
```bash
server {
    listen 80;
    server_name _;

    # Servir arquivos estáticos diretamente
    location /static/ {
        alias /code/staticfiles/;
        expires 30d;
        access_log off;
    }

    # Servir arquivos de mídia
    location /media/ {
        alias /code/media/;
        expires 30d;
        access_log off;
    }

    # Repassar o resto das requisições para o Django (Uvicorn)
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Por fim, vamos subir o container `nginx`:

```bash
docker compose up -d
```

 - **🧩 Fluxo de funcionamento**
   - `Uvicorn (web)` executa o Django e responde às rotas dinâmicas.
   - `Nginx` recebe todas as requisições HTTP externas:
     - `/static/` → servido diretamente da pasta staticfiles;
     - `/media/` → servido diretamente da pasta media;
     - outras rotas → redirecionadas para o container web (Uvicorn).
   - `PostgreSQL` e Redis são usados internamente via rede backend.

Agora tente abrir:

 - [http://localhost:8000/](http://localhost:8000/)
 - [http://localhost:8000/admin/](http://localhost:8000/admin/)

> **What? Não funcionou!**  
> 👉 Porque o Nginx está na porta 80 e o Uvicorn está atrás dele, **exposto (expose)** apenas internamente no Docker.

Agora para acessar nossa aplicação `web` primeiro nós devemos passar pelo container `nginx`:

 - [http://localhost/](http://localhost/)
 - [http://localhost/admin/](http://localhost/admin/)

> **Explicando brevemente:**  
> O container *nginx* atua como `reverse proxy`; ele recebe todas as requisições HTTP (nas portas 80/443) e as encaminha internamente para o container web (Uvicorn/Django).

Agora você pode abrir o seu Django Admin que estará tudo disponível pelo Nginx:

![img](images/nginx-02.png)  

> **Mas como eu testo se meu nginx está funcionando corretamente?**

Primeiro, vamos ver se há mensagem de erro dentor do container `nginx`:

```bash
docker logs nginx_reverse_proxy
```

**OUTPUT:**
```bash
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf differs from the packaged version
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/11/10 13:10:11 [notice] 1#1: using the "epoll" event method
2025/11/10 13:10:11 [notice] 1#1: nginx/1.27.5
2025/11/10 13:10:11 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2025/11/10 13:10:11 [notice] 1#1: OS: Linux 6.6.87.2-microsoft-standard-WSL2
2025/11/10 13:10:11 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2025/11/10 13:10:11 [notice] 1#1: start worker processes
2025/11/10 13:10:11 [notice] 1#1: start worker process 28
2025/11/10 13:10:11 [notice] 1#1: start worker process 29
2025/11/10 13:10:11 [notice] 1#1: start worker process 30
2025/11/10 13:10:11 [notice] 1#1: start worker process 31
2025/11/10 13:10:11 [notice] 1#1: start worker process 32
2025/11/10 13:10:11 [notice] 1#1: start worker process 33
2025/11/10 13:10:11 [notice] 1#1: start worker process 34
2025/11/10 13:10:11 [notice] 1#1: start worker process 35
172.18.0.1 - - [10/Nov/2025:13:10:28 +0000] "GET / HTTP/1.1" 200 12068 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:10:28 +0000] "GET /favicon.ico HTTP/1.1" 404 2201 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:10:39 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:10:39 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 4173 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:15:32 +0000] "GET / HTTP/1.1" 200 12068 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:29 +0000] "GET / HTTP/1.1" 200 12068 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:29 +0000] "GET /favicon.ico HTTP/1.1" 404 2201 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:30 +0000] "GET /admin/ HTTP/1.1" 302 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
172.18.0.1 - - [10/Nov/2025:13:18:30 +0000] "GET /admin/login/?next=/admin/ HTTP/1.1" 200 4173 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" "-"
```

Ótimo, agora vamos fazer alguns testes no navegador:

 - http://localhost/static/ → deve(ria) exibir arquivos estáticos.
 - http://localhost/media/ → deve(ria) exibir uploads.

**OUTPUT:**
```bash
403 Forbidden
nginx/1.27.5
```

> **What? Não funcionou!**

Agora vamos tentar acessar um arquivo específico:

 - http://localhost/static/admin/css/base.css
 - http://localhost/static/admin/img/inline-delete.svg

> **What? Agora funcionou!**

 - Esse comportamento indica que o *Nginx* está conseguindo servir arquivos existentes, mas não consegue listar diretórios.
 - **NOTE:** Por padrão, o Nginx não habilita autoindex (listagem de diretórios).

Então:

 - http://localhost/static/admin/css/base.css → Funciona porque você está acessando um arquivo específico.
 - http://localhost/static/ → Dá *403 Forbidden* porque você está acessando o diretório, e o Nginx não lista o conteúdo (diretório) por padrão.

> **Como resolver isso?**

#### Habilitar autoindex (não recomendado para produção, só para teste):

[nginx.conf](../nginx/conf/nginx.conf)
```bash
location /static/ {
    alias /code/staticfiles/;
    autoindex on;
}

location /media/ {
    alias /code/media/;
    autoindex on;
}
```

**Força recriar o container `nginx`**:
```
docker compose up -d --force-recreate nginx
```

> **NOTE:**  
> Isso permite ver os arquivos listados no navegador, mas não é seguro em produção, porque expõe todos os arquivos publicamente.

Agora, abra diretamente algum arquivo, como:

 - [http://localhost/static/admin/css/base.css](http://localhost/static/admin/css/base.css)
 - [http://localhost/media/example.txt](http://localhost/media/example.txt)
   - Crie esse arquivo em `/media (host)` antes de tentar acessar (testar).

Se esses arquivos carregarem, significa que tudo está correto para servir conteúdo estático e uploads, mesmo que a listagem do diretório não funcione.

> **💡 Resumo:**  
> O erro `403` ao acessar `/static/` ou `/media/` é normal no Nginx quando você não habilita `autoindex`. Para produção, você normalmente não quer listar diretórios, apenas servir arquivos diretamente.

Outra maneira de testar se o Nginx está funcionando corretamente seria usar o `curl`:

```bash
curl http://localhost/static/admin/css/base.css -I
```

**OUTPUT:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Tue, 19 Aug 2025 02:29:18 GMT
Content-Type: text/css
Content-Length: 22120
Last-Modified: Tue, 19 Aug 2025 01:58:34 GMT
Connection: keep-alive
ETag: "68a3da4a-5668"
Accept-Ranges: bytes
```

```bash
curl http://localhost/media/example.txt -I
```

**OUTPUT:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Tue, 19 Aug 2025 02:30:17 GMT
Content-Type: text/plain
Content-Length: 15
Last-Modified: Tue, 19 Aug 2025 02:26:29 GMT
Connection: keep-alive
ETag: "68a3e0d5-f"
Accept-Ranges: bytes
```

```bash
curl http://localhost/static/admin/img/inline-delete.svg -I
```

**OUTPUT:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.27.5
Date: Tue, 19 Aug 2025 02:33:07 GMT
Content-Type: image/svg+xml
Content-Length: 537
Last-Modified: Tue, 19 Aug 2025 01:58:34 GMT
Connection: keep-alive
ETag: "68a3da4a-219"
Accept-Ranges: bytes
```

 - Vejam que quem está servindo os dados é o servidor Nginx e não o Django (container web).
 - Além, disso nós também estamos vendo algumas informações interessantes sobre os arquivos:
   - tipo: `text/css`, `text/plain`, `image/svg+xml`, etc.












































---

<div id="django-postgresql-settings"></div>

## `Configurando o Django para reconhecer o PostgreSQL (+ .env) como Banco de Dados`

Antes de começar a configurar o Django para reconhecer o PostgreSQL como Banco de Dados, vamos fazer ele reconhecer as variáveis de ambiente dentro de [core/settings.py](../core/settings.py).

Primeiro, vamos instalar o `python-dotenv`:

```bash
poetry add python-dotenv@latest
```

Agora, vamos iniciar uma instância de `python-dotenv`:

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
# ==========================
# CONFIGURAÇÃO DO POSTGRES
# ==========================
POSTGRES_DB=easy_rag_db                     # Nome do banco de dados a ser criado
POSTGRES_USER=easyrag                       # Usuário do banco
POSTGRES_PASSWORD=easyragpass               # Senha do banco
POSTGRES_HOST=db                            # Nome do serviço (container) do banco no docker-compose
POSTGRES_PORT=5432                          # Porta padrão do PostgreSQL
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
db

>>> print(os.getenv("POSTGRES_PASSWORD"))
easyragpass
```

> **NOTE:**  
> Vejam que realmente nós estamos conseguindo acessar as variáveis de ambiente.

Continuando, agora vamos dizer ao Django qual Banco de Dados vamos utilizar.

Por exemplo:

[core/settings.py](../core/settings.py)
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
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
> - *"NUNCA"* colocar credenciais reais em `settings.py`.
> - Use `.env` (não comitado) ou um *"secret manager"*.

Por fim, vamos testar a conexão ao banco de dados:

**Roda/Executa o comando "migrate" a partir do serviçor "web":**
```bash
docker compose exec web python manage.py migrate
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

<div id="env-vars"></div>

## `Variáveis de Ambiente`

Aqui só para fins de estudos (entendimento) vamos mostrar as variáveis de ambiente do nosso projeto:

[.env](../.env)
```bash
# ==========================
# CONFIGURAÇÃO DO POSTGRES
# ==========================
POSTGRES_DB=easy_rag_db                     # Nome do banco de dados a ser criado
POSTGRES_USER=easyrag                       # Usuário do banco
POSTGRES_PASSWORD=easyragpass               # Senha do banco
POSTGRES_HOST=db                            # Nome do serviço (container) do banco no docker-compose
POSTGRES_PORT=5432                          # Porta padrão do PostgreSQL

# ==========================
# CONFIGURAÇÃO DO REDIS
# ==========================
REDIS_HOST=redis                            # Nome do serviço (container) do Redis no docker-compose
REDIS_PORT=6379                             # Porta padrão do Redis

# ==========================
# CONFIGURAÇÃO DJANGO
# ==========================
DJANGO_SECRET_KEY=djangopass                # Chave secreta do Django para criptografia e segurança
DJANGO_DEBUG=True                           # True para desenvolvimento; False para produção
DJANGO_ALLOWED_HOSTS=*                      # Hosts permitidos; * libera para qualquer host

# ==========================
# CONFIGURAÇÃO DO UVICORN
# ==========================
UVICORN_HOST=0.0.0.0                        # Escutar em todas as interfaces
UVICORN_PORT=8000                           # Porta interna do app

# ==========================
# CONFIGURAÇÃO DO CELERY
# ==========================

# Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0      # Onde as tasks vão ser enfileiradas (Redis service redis no compose)
CELERY_RESULT_BACKEND=redis://redis:6379/1  # Onde o resultado das tasks será guardado (usar Redis DB 1 separado é comum)

# Optional - For unit tests
CELERY_TASK_ALWAYS_EAGER=False
CELERY_TASK_EAGER_PROPAGATES=True
```










---

<div id="taskipy-commands"></div>

## `Comandos Taskipy`

> **Aqui vamos explicar quais os comando nós estamos utilizando na nossa aplicação.**

### Lint, Format, Pre-Commit

```toml
lint = 'ruff check'
```

 - Executa o Ruff (um linter rápido para Python) para verificar problemas no código, como:
   - Erros de sintaxe;
   - Problemas de estilo (PEP8);
   - Imports não utilizados;
   - Variáveis não usadas.
   - **📌 Importante:** Este comando só verifica, não corrige nada.

```toml
pre_format = 'ruff check --fix'
```

 - Faz a mesma verificação do comando acima, mas corrige automaticamente os problemas que puder (como remover imports não usados, ajustar espaçamentos, etc.).

```toml
format = 'ruff format'
```

 - Formata o código de acordo com as regras de estilo configuradas no Ruff, similar ao Black.
 - Foca mais na formatação visual do código do que nas regras de qualidade.

```toml
precommit = 'pre-commit run --all-files'
```

 - Executa todos os hooks do pre-commit em todos os arquivos do projeto.
 - Pode incluir: lint, formatação, verificação de imports, checagem de segurança, etc.

### Testes

```toml
pre_test = 'task lint'
```

 - Executa o comando `lint` antes de rodar os testes.
 - Isso garante que o código está limpo antes de testar.

```toml
test = 'pytest -s -x --cov=. -vv'
```

 - Executa os testes com pytest com algumas opções:
   - `-s` → Mostra os prints do código durante os testes;
   - `-x` → Para na primeira falha.
   - `--cov=.` → Mede a cobertura de testes no diretório atual.
   - `-vv` → Modo muito verboso, mostrando mais detalhes de cada teste.

```toml
post_test = 'coverage html'
```

 - Depois que os testes rodam, gera um relatório HTML da cobertura de código.
 - Normalmente, cria uma pasta `htmlcov/` com o relatório.

### Docker (Containers)

```toml
prodcompose = 'docker compose -f docker-compose.yml up --build -d'
```

 - Sobe os containers do projeto em modo produção, usando `docker-compose.yml`.
 - `-d` significa detached mode (em background).

```toml
devcompose = 'docker compose up -d'
```

 - Mesma ideia do anterior, mas usando o comando mais recente (docker compose sem hífen).
 - `-d` Também sobe os containers em modo detached.
 - Provavelmente pensado (usado) para ambiente de desenvolvimento.

```toml
rcontainers = 'docker compose up -d --force-recreate'
```

 - Recria todos os containers do projeto, mesmo que nada tenha mudado no código ou no `docker-compose.yml`.
 - Útil quando o container está corrompido ou com cache problemático.

```toml
cleandocker = """
docker stop $(docker ps -aq) 2>/dev/null || true &&
docker rm $(docker ps -aq) 2>/dev/null || true &&
docker rmi -f $(docker images -aq) 2>/dev/null || true &&
docker volume rm $(docker volume ls -q) 2>/dev/null || true &&
docker system prune -a --volumes -f
"""
```

 - Limpa todos os *containers*, *imagens*, *volumes* e *cache* do Docker.

### Comandos do Sistema (OS)

```toml
addpermissions = """
sudo chown -R 1000:1000 ./static ./media ./staticfiles || true &&
sudo chmod -R 755 ./static ./media ./staticfiles
"""
```

 - `sudo chown -R 1000:1000 ./static ./media ./staticfiles || true`
   - `sudo` → Executa o comando com privilégios de administrador.
   - `chown -R 1000:1000` → Altera o dono e grupo de todos os arquivos e pastas *recursivamente (-R)* para *UID=1000* e *GID=1000*.
   - `./static ./media ./staticfiles` → Pastas (ou poderiam ser arquivos) alvo do comando.
   - `|| true` → Significa “se o comando falhar, não interrompa a execução”:
     - Útil se você estiver rodando sem sudo ou se o usuário já for dono.
   - **Resumo:** garante que todas as pastas e arquivos pertencem ao usuário 1000:1000, evitando problemas de permissões.
 - `&& sudo chmod -R 755 ./static ./media ./staticfiles`
   - `&&` → Só executa o próximo comando se o anterior tiver sucesso.
   - `chmod -R 755` → Altera permissões recursivamente:
     - `7 (rwx)` para o dono → leitura, escrita e execução.
     - `5 (r-x)` para grupo e outros → leitura e execução, mas não escrita.
   - `./static ./media ./staticfiles` → pastas alvo.
   - **Resumo:** garante que:
     - O dono pode ler, escrever e executar arquivos/pastas.
     - Grupo e outros podem apenas ler e executar (necessário para o Nginx servir os arquivos).

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
