# Easy RAG

## Conteúdo

 - [`Criando o projeto (django) core`](#create-core)
 - [`Exportando as dependências com o Poetry`](#poetry-export)
 - [`Criando as variáveis de ambiente`](#env-vars)
 - [`Instalando o Docker`](#docker-install)
 - [`Criando o container PostgreSQL (db)`](#container-db)
 - [`Criando o container Redis (redis_cache)`](#container-redis)
 - [`Criando o Dockerfile para o container Django + Uvicorn (web)`](#dockerfile-django)
 - [`Criando o container Django + Uvicorn (web)`](#container-django)
 - [`Criando o container Nginx (nginx)`](#container-nginx)
 - [Comandos Taskipy](#taskipy-commands)
<!---
[WHITESPACE RULES]
- "40" Whitespace character.
--->








































---

<div id="create-core"></div>

## `Criando o projeto (django) core`

De início vamos criar o `core` do nosso projeto:

```bash
django-admin startproject core .
```

Agora é só executar:

```bash
python manage.py runserver
```









































---

<div id="poetry-export"></div>

## `Exportando as dependências com o Poetry`

Antes de criar nossos containers, precisamos gerar os `requirements.txt` e `requirements-dev.txt`:

**Primeiro devemos instalar o plugin "export" do Poetry:**
```bash
poetry self add poetry-plugin-export
```

Agora vamos gerar `requirements.txt` de produção.

**Produção:**
```bash
poetry export --without-hashes --format=requirements.txt --output=requirements.txt
```

Agora vamos gerar `requirements-dev.txt` (esse é mais utilizado durante o desenvolvimento para quem não usa o Poetry):

**Desenvolvimento:**
```bash
poetry export --without-hashes --with dev --format=requirements.txt --output=requirements-dev.txt
```









































---

<div id="env-vars"></div>

## `Criando as variáveis de ambiente`

Outra coisa importante que nós precisamos fazer antes de criar nossos containers é criar as variáveis de ambiente:

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

# ==========================
# CONFIGURAÇÃO DO REDIS
# ==========================
REDIS_HOST=redis                  # Nome do serviço (container) do Redis no docker-compose
REDIS_PORT=6379                   # Porta padrão do Redis

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

# ==========================
# CONFIGURAÇÃO DE ARMAZENAMENTO DE ARQUIVOS
# ==========================
MEDIA_ROOT=/code/media            # Caminho onde arquivos enviados (uploads) serão salvos no container
STATIC_ROOT=/code/staticfiles     # Caminho onde arquivos estáticos coletados do Django serão salvos no container
```

Onde:

 - `1️⃣ PostgreSQL (db)`
   - `POSTGRES_DB` → nome do banco criado automaticamente ao subir o container.
   - `POSTGRES_USER` → usuário administrador do banco.
   - `POSTGRES_PASSWORD` → senha do usuário do banco.
   - `POSTGRES_HOST` → para o Django se conectar, usamos o nome do serviço (db), não localhost, pois ambos estão na mesma rede docker.
   - `POSTGRES_PORT` → porta padrão 5432.
 - `2️⃣ Redis (redis)`
   - `REDIS_HOST` → nome do serviço no docker-compose.
   - `REDIS_PORT` → porta padrão 6379.
   - **NOTE:** O Redis será usado como cache e possivelmente fila de tarefas (com Celery, RQ ou outro).
 - `3️⃣ Django (web)`
   - `DJANGO_SECRET_KEY` → chave única e secreta usada para assinar cookies, tokens e outras partes sensíveis.
   - `DJANGO_DEBUG` → habilita/desabilita debug e mensagens de erro detalhadas.
   - `DJANGO_ALLOWED_HOSTS` → lista de domínios que o Django aceita; `*` significa todos (não recomendado para produção).
 - `4️⃣ UVICORN (web)`
   - `UVICORN_HOST` → define o IP/host onde o servidor Uvicorn vai rodar.
   - `UVICORN_PORT` → porta interna que o container expõe para o nginx ou para acesso direto no dev.
 - `5️⃣ Arquivos (Armazenamento: media e staticfiles)`
   - `MEDIA_ROOT` → onde os uploads de usuários são salvos dentro do container.
   - `STATIC_ROOT` → onde os arquivos estáticos (collectstatic) são guardados.









































---

<div id="docker-install"></div>

## `Instalando o Docker`

Aqui nós vamos instalar o Docker na nossa maquina virtual (WSL2) que será utilizado na construção e manutenção dos nossos containers.

**Atualizar pacotes:**
```bash
sudo apt update && sudo apt upgrade -y
```

**Remover versões antigas (se existirem):**
```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

**Instalar dependências:**
```bash
sudo apt install ca-certificates curl gnupg lsb-release -y
```

**Cria a pasta /etc/apt/keyrings com permissões seguras para guardar chaves GPG de repositórios:**
```bash
sudo mkdir -m 0755 -p /etc/apt/keyrings
```

**baixa a chave GPG oficial do Docker e a converte para o formato binário aceito pelo APT, salvando no diretório de chaves do sistema:**
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

**Adicionar repositório do Docker:**
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Atualizar pacotes (novamente):**
```bash
sudo apt update && sudo apt upgrade -y
```

**Instalar Docker e Compose:**
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

**O Docker, por padrão, só permite que o root (ou membros do grupo `docker`) executem comandos. Criar o grupo `docker` permite conceder permissão a usuários comuns sem precisar usar sudo o tempo todo:**
```bash
sudo groupadd docker
```

> **NOTE:**
> - Em muitas distros, esse grupo já existe — nesse caso, o comando só vai dar erro dizendo que o grupo já existe, o que é normal.
> - groupadd: group 'docker' already exists

**Isso coloca o usuário atual no grupo docker, permitindo executar comandos como `docker ps`:**
```bash
sudo usermod -aG docker $USER
```









































---

<div id="container-db"></div>

## `Criando o container PostgreSQL (db)`

> Aqui nós vamos entender e criar um container contendo um `Banco de Dados PostgreSQ`L.

 - **Função:**
   - Armazenar dados persistentes da aplicação (usuários, arquivos, prompts, etc.).
 - **Quando usar:**
   - Sempre que precisar de um banco de dados relacional robusto.
 - **Vantagens:**
   - ACID (consistência e confiabilidade).
   - Suporte avançado a consultas complexas.
 - **Desvantagens:**
   - Mais pesado que bancos NoSQL para dados muito simples.

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  db:
    image: postgres:15
    container_name: postgres_db
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    networks:
      - backend
```

 - `image: postgres:15`
   - Pega a versão 15 oficial do PostgreSQL no Docker Hub.
 - `container_name: postgres_db`
   - Nome fixo do container (para facilitar comandos como docker logs postgres_db).
 - `restart: unless-stopped`
   - Faz o container reiniciar automaticamente caso falhe, a não ser que seja parado manualmente.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo .env (ex.: POSTGRES_USER, POSTGRES_PASSWORD).
 - `environment`
   - Define as variáveis de ambiente consumidas pela imagem oficial do Postgres:
     - `POSTGRES_DB` → cria um banco inicial com esse nome (somente no primeiro start, quando o diretório de dados está vazio).
     - `POSTGRES_USER` → cria/define o usuário administrativo inicial.
     - `POSTGRES_PASSWORD` → senha do usuário acima (obrigatória, a menos que use POSTGRES_HOST_AUTH_METHOD=trust, não recomendado).
 - `volumes:`
   - Persistência de dados:
     - `./data/postgres:` → pasta local (no host, raiz do projeto)
     - `/var/lib/postgresql/data` → pasta interna do container onde o Postgres armazena os dados.
 - `ports: 5432:5432`
   - `Primeiro 5432:` → porta no host (sua máquina).
   - `Segundo 5432:` → porta dentro do container onde o Postgres está rodando.
   - **NOTE:** Isso permite que você use o psql ou qualquer ferramenta de banco de dados (DBeaver, TablePlus, etc.) diretamente do seu PC.
 - `networks: backend`
   - Coloca o container na rede backend para comunicação interna segura.

**NOTE:**
Se você desejar conectar nesse Banco de Dados via bash utilize o seguinte comando (As vezes é necessário esperar o container/banco de dados subir):

**Entrar no container "postgres_db" via bash:**
```bash
docker exec -it postgres_db bash
```

**Entra no banco de sados a partir das variáveis de ambiente:**
```bash
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```










































---

<div id="container-redis"></div>

## `Criando o container Redis (redis_cache)`

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

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  redis:
    image: redis:7
    container_name: redis_cache
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - REDIS_HOST=${REDIS_HOST}
      - REDIS_PORT=${REDIS_PORT}
    networks:
      - backend
```

 - `image: redis:7`
   - Pega a versão 7 oficial do Redis no Docker Hub.
 - `container_name: redis_cache`
   - Nome fixo do container (para facilitar comandos como docker logs redis_cache).
 - `restart: unless-stopped`
   - Faz o container reiniciar automaticamente caso falhe, a não ser que seja parado manualmente.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo `.env (ex.: REDIS_HOST, REDIS_PORT)`.
 - `environment`
   - Define as variáveis de ambiente consumidas pela imagem oficial do Redis:
     - `REDIS_HOST` → host do Redis (default: localhost, porém estamos utilizando "redis").
     - `REDIS_PORT` → porta do Redis (default: 6379).
 - `networks: backend`
   - Só está acessível dentro da rede interna backend (não expõe porta para fora).











































---

<div id="dockerfile-django"></div>

## `Criando o Dockerfile para o container Django + Uvicorn (web)`

> **Por que eu preciso de um Dockerfile para o Django + Uvicorn?**

**SIM!**
O Dockerfile é onde você diz **como** essa imagem será construída.

> **O que o Dockerfile faz nesse caso?**

 - Escolhe a imagem base (ex.: python:3.12-slim) para rodar o Python.
 - Instala as dependências do sistema (por exemplo, libpq-dev para PostgreSQL).
 - Instala as dependências Python (pip install -r requirements.txt).
 - Copia o código do projeto para dentro do container.
 - Define o diretório de trabalho (WORKDIR).
 - Configura o comando de entrada (no seu caso, o uvicorn já está no docker-compose).
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

O nosso Dockerfile vai ficar a da seguinte maneira:

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

Agora vamos criar o arquivo `.dockerignore`:

[.dockerignore](../.dockerignore)
```bash
data/postgres
```

> **NOTE:**
> - Isso vai impedir que o Docker envie essa pasta para o build, evitando o erro.
> - 💡 Essa é a solução mais recomendada, porque *"data/postgres"* é gerada pelo container do PostgreSQL e não deve estar no contexto da imagem.

**Se quiser manter a pasta no contexto (não recomendado nesse caso):**
```bash
sudo chmod -R 755 data/postgres
```

**NOTE:**
Se você desejar testar o Dockerfile antes de executar com o docker-compose, utilize o seguinte comando:

```bash
docker build -t teste-django .
```

 - `-t teste-django`
   - Dá um nome para a imagem *(teste-django)*.
 - `.`
   - Indica que o contexto de build é a pasta atual.

Até, então nós criamos a imagems do container, agora executar (run) o container:

**Executa (run) e entra no container via bash:**
```bash
docker run -it --rm -p 8000:8000 teste-django bash
```







































---

<div id="container-django"></div>

## `Criando o container Django + Uvicorn (web)`

> Aqui vamos entender e criar um container contendo o `Django` e o `Uvicorn`.

 - **Função:**
   - Executar a aplicação Django em produção.
 - **Quando usar:** Sempre para servir sua aplicação backend.
 - **Vantagens:**
   - Uvicorn é um servidor WSGI otimizado para produção
   - Separa lógica da aplicação da entrega de arquivos estáticos
 - **Desvantagens:**
   - Não serve arquivos estáticos eficientemente (por isso usamos o Nginx)

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django_web
    restart: unless-stopped
    command: >
      sh -c "
      python manage.py migrate &&
      python manage.py collectstatic --noinput &&
      uvicorn core.asgi:application --reload --host ${UVICORN_HOST} --port ${UVICORN_PORT}
      "
    env_file:
      - .env
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DJANGO_DEBUG=${DJANGO_DEBUG}
      - DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_HOST=${POSTGRES_HOST}
      - POSTGRES_PORT=${POSTGRES_PORT}
      - REDIS_HOST=${REDIS_HOST}
      - REDIS_PORT=${REDIS_PORT}
      - MEDIA_ROOT=${MEDIA_ROOT}
      - STATIC_ROOT=${STATIC_ROOT}
    volumes:
      - .:/code
      - static:/code/staticfiles
      - media:/code/media
    depends_on:
      - db
      - redis
    ports:
      - "${UVICORN_PORT}:${UVICORN_PORT}"
    networks:
      - backend
```

 - `build: context + dockerfile.`
   - `context: .`
     - Ponto `(.)` significa que o contexto de build é a raiz do projeto.
     - Isso quer dizer que todos os arquivos dessa pasta estarão disponíveis para o build.
   - `dockerfile: Dockerfile`
     - Nome do arquivo Dockerfile usado para construir a imagem.
 - `container_name: django_web`
   - Nome fixo do container (para facilitar comandos como docker logs django_web).
 - `restart: unless-stopped`
   - Faz o container reiniciar automaticamente caso falhe, a não ser que seja parado manualmente.
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
   - Carrega variáveis do .env (como DEBUG, DATABASE_URL, SECRET_KEY).
 - `environment`
   - Define as variáveis de ambiente consumidas pela imagem oficial do Django:
     - `DJANGO_SECRET_KEY` → chave secreta do Django.
     - `DJANGO_DEBUG` → modo de desenvolvimento do Django.
     - `DJANGO_ALLOWED_HOSTS` → hosts permitidos pelo Django.
     - `POSTGRES_DB` → nome do banco de dados.
     - `POSTGRES_USER` → usuário do banco de dados.
     - `POSTGRES_PASSWORD` → senha do banco de dados.
     - `POSTGRES_HOST` → host do banco de dados.
     - `POSTGRES_PORT` → porta do banco de dados.
     - `REDIS_HOST` → host do Redis.
     - `REDIS_PORT` → porta do Redis.
     - `MEDIA_ROOT` → pasta de uploads de usuários.
     - `STATIC_ROOT` → pasta de arquivos estáticos.
 - `volumes:`
   - Código fonte: pasta atual `.` → `/code` dentro do container.
   - Arquivos estáticos: volume nomeado `static`.
   - Uploads de usuários: volume nomeado `media`.
 - `depends_on:`
   - Garante que `db` e `redis` sejam inicializados antes do Django.
 - `ports: "${UVICORN_PORT}:${UVICORN_PORT}"`
   - Para acessar pelo navegador no seu computador, você precisa de `ports`.
   - **NOTE:** `expose` apenas informa a porta para outros containers, não mapeia para o host.
 - `networks: backend`
   - Rede interna para comunicação.

> **Uma dúvida... tudo o que minha eu modifico no meu projeto principal é alterado no container?**

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
```
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








































---

<div id="container-nginx"></div>

## `Criando o container Nginx (nginx)`

> Aqui vamos entender e criar um container contendo o `Nginx (nginx)`.

 - **Função:**
   - Servir arquivos estáticos e atuar como *proxy reverso* para o Django.
 - **Quando usar:**
   - Sempre em produção para segurança e desempenho.
 - **Vantagens:**
   - Muito rápido para servir arquivos estáticos.
   - HTTPS e balanceamento de carga.
 - **Desvantagens:**
   - Exige configuração inicial extra.

[docker-compose.yml](../docker-compose.yml)
```yml
services:
  nginx:
    image: nginx:1.27
    container_name: nginx_reverse_proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf:/etc/nginx/conf.d
      - static:/code/staticfiles
      - media:/code/media
    depends_on:
      - web
    networks:
      - backend
```

 - `image: nginx:1.27`
   - Pega a versão 1.27 oficial do Nginx no Docker Hub.
 - `container_name: nginx_reverse_proxy`
   - Nome fixo do container (para facilitar comandos como docker logs nginx_server).
 - `restart: unless-stopped`
   - Faz o container reiniciar automaticamente caso falhe, a não ser que seja parado manualmente.
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
































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































---

<div id="taskipy-commands"></div>

## Comandos Taskipy

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

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
