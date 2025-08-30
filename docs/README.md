# Easy RAG

## Conteúdo

 - [`01 - Criando o projeto (django) core`](#create-core)
 - [`02 - Exportando as dependências com o Poetry`](#poetry-export)
 - [`03 - Instalando o Docker`](#docker-install)
 - [`04 - Criando o container PostgreSQL (db)`](#db-container)
 - [`05 - Criando o container Redis (redis_cache)`](#redis-container)
 - [`06 - Criando o container web: Dockerfile + Django + Uvicorn`](#web-container)
 - [`07 - Criando o container Nginx (nginx)`](#nginx-container)
 - [`08 - Configurando o PostgreSQL como Banco de Dados do nosos projeto`](#db-setting)
 - [`09 - Entendendo: Tasks Assíncronas e Celery no Django`](#understanding-async-celery)
 - [`10 - Fazendo o Celery reconhecer o Django e vice-versa`](#create-core-celery)
 - [`Variáveis de Ambiente`](#env-vars)
 - [`Comandos Taskipy`](#taskipy-commands)
<!---
[WHITESPACE RULES]
- "40" Whitespace character.
--->








































---

<div id="create-core"></div>

## `01 - Criando o projeto (django) core`

De início vamos criar o projeto `core` com o comando:

```bash
django-admin startproject core .
```

Agora é só executar o comando:

```bash
python manage.py runserver
```









































---

<div id="poetry-export"></div>

## `02 - Exportando as dependências com o Poetry`

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









































---

<div id="docker-install"></div>

## `03 - Instalando o Docker`

> Aqui nós vamos instalar o Docker na nossa maquina virtual (WSL2 no meu caso) que será utilizado na construção e manutenção dos nossos containers.

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

**O Docker, por padrão, só permite que o root (ou membros do grupo `docker`) executem comandos. Criar o grupo `docker` permite conceder permissão a usuários comuns sem precisar usar *sudo* o tempo todo:**
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

<div id="db-container"></div>

## `04 - Criando o container PostgreSQL (db)`

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

Mas antes de criar nosso container contendo o *PostgreSQL* vamos criar as variáveis de ambiente para esse container:

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
    container_name: postgres_db
    restart: always
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
```

 - `image: postgres:15`
   - Pega a versão 15 oficial do PostgreSQL no Docker Hub.
 - `container_name: postgres_db`
   - Nome fixo do container (para facilitar comandos como docker logs postgres_db).
 - `restart: always`
   - 🔹 O container vai voltar sempre que o Docker daemon subir, independente do motivo da parada.
   - 🔹 Mesmo se você der *docker stop*, quando o host reiniciar o container volta sozinho.
   - 👉 Bom para produção quando você quer *99% de disponibilidade*.
 - `env_file: .env`
   - Carrega variáveis de ambiente do arquivo *.env*.
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

Agora, se você desejar se conectar nesse Banco de Dados via *bash* utilize o seguinte comando (As vezes é necessário esperar o container/banco de dados subir):

**Entrar no container "postgres_db" via bash:**
```bash
docker exec -it postgres_db bash
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
local     easy-rag_postgres_data
```

Nós também podemos inspecionar esse volume:

```bash
docker volume inspect easy-rag_postgres_data
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

## `05 - Criando o container Redis (redis_cache)`

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

Mas antes de criar nosso container contendo o *PostgreSQL* vamos criar as variáveis de ambiente para esse container:

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
    env_file:
      - .env
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  redis_data:

networks:
  backend:
```

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
 - `networks: backend`
   - Só está acessível dentro da rede interna backend (não expõe porta para fora).

> **E os volumes como eu vejo?**

```bash
docker volume ls
```

**OUTPUT:**
```bash
DRIVER    VOLUME NAME
local     easy-rag_redis_data
```

Nós também podemos inspecionar esse volume:

```bash
docker volume inspect easy-rag_redis_data
```

**OUTPUT:**
```bash
[
    {
        "CreatedAt": "2025-08-18T10:59:18-03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "4b7c7c51ea40d8462666b2a06701fd53f46d66cb4418c612ddffb0cdca301835",
            "com.docker.compose.project": "easy-rag",
            "com.docker.compose.version": "2.39.1",
            "com.docker.compose.volume": "redis_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/easy-rag_redis_data/_data",
        "Name": "easy-rag_redis_data",
        "Options": null,
        "Scope": "local"
    }
]
```

 - `Mountpoint`
   - O *Mountpoint* é onde os arquivos realmente ficam, mas não é recomendado mexer manualmente lá.
   - Para interagir com os dados, use o *container* ou ferramentas do próprio serviço (por exemplo, psql no Postgres).











































---

<div id="web-container"></div>

## `06 - Criando o container web: Dockerfile + Django + Uvicorn`

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
Se você desejar testar o Dockerfile antes de executar com o *docker compose*, utilize o seguinte comando:

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
 - **Quando usar:** Sempre para servir sua aplicação backend.
 - **Vantagens:**
   - Uvicorn é um servidor WSGI otimizado para produção
   - Separa lógica da aplicação da entrega de arquivos estáticos
 - **Desvantagens:**
   - Não serve arquivos estáticos eficientemente (por isso usamos o Nginx)

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
    command: >
      sh -c "
      python manage.py migrate &&
      python manage.py collectstatic --noinput &&
      uvicorn core.asgi:application --reload --host ${UVICORN_HOST} --port ${UVICORN_PORT}
      "
    env_file:
      - .env
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
 - `depends_on:`
   - Garante que os containers `db` e `redis` sejam inicializados antes do `web`.
 - `ports: "${UVICORN_PORT}:${UVICORN_PORT}"`
   - Para acessar pelo navegador no seu computador, você precisa de `ports`.
   - **NOTE:** `expose` apenas informa a porta para outros containers, não mapeia para o host.
 - `networks: backend`
   - Rede interna para comunicação.

#### Crie as pastas `./static`, `./media` e `./staticfiles` no host

Uma observação aqui é que antes de nós executamos o container web nós precisamos criar as pastas (diretórios) `./static`, `./media` e `./staticfiles` no host.

> **Por que?**

Porque se essas pastas (diretórios) forem criadas pelo container ela não terá as permissões do nosso usuário (do nosso sistema), elas virão com permissão root (do container).

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

<div id="nginx-container"></div>

## `07 - Criando o container Nginx (nginx)`

> Aqui vamos entender e criar um container contendo o `Nginx (nginx)`.

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

Continuando, o arquivo [docker-compose.yml](../docker-compose.yml) para o nosso container *nginx* ficará assim:

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
      - ./nginx/conf:/etc/nginx/conf.d
      - ./static:/code/staticfiles
      - ./media:/code/media
    depends_on:
      - web
    networks:
      - backend

networks:
  backend:
```

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

A configuração inicial do nosso Nginx ficará assim:

[nginx.conf](../nginx/conf/nginx.conf)
```bash
server {
    listen 80;

    server_name _;  # or your domain, e.g., api.myproject.com

    # Serve static files
    location /static/ {
        alias /code/staticfiles/;
    }

    # Serve media files
    location /media/ {
        alias /code/media/;
    }

    # Forward requests to Django (via Uvicorn)
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

O código acima faz o seguinte:

 - `listen 80`
   - Significa que o *Nginx* vai escutar requisições HTTP na porta 80 (porta padrão para tráfego HTTP).
 - `server_name _;  # ou seu domínio, ex: api.meuprojeto.com`
   - Define o nome do servidor.
   - O `_ (underscore)` é um wildcard (coringa), ou seja, aceita qualquer domínio.
   - Em produção, você substituiria por algo como *api.meuprojeto.com* ou *meusite.com*.
 - `location /static/ {}`
   - Esse bloco diz ao *Nginx* para servir diretamente os arquivos estáticos (CSS, JS, imagens de frontend, etc).
   - Quando alguém acessa http://dominio.com/static/arquivo.css, o Nginx busca esse arquivo na pasta /code/staticfiles/ dentro do container.
   - **NOTE:** alias é usado para apontar o caminho real dentro do container.
 - `location /media/ {}`
   - Semelhante ao anterior, mas para os arquivos de mídia (uploads de usuários, fotos de perfil, documentos, etc).
   - Quando alguém acessa http://dominio.com/media/foto.png, o Nginx entrega diretamente o arquivo da pasta /code/media/.
 - `location / {}`
   - Esse bloco é o *proxy reverso* que encaminha todas as requisições que não são arquivos estáticos/mídia para o Django rodando no Uvicorn.
   - `proxy_pass http://web:8000;` → Envia a requisição para o container *web* (Django) na porta *8000*.
   - `proxy_set_header Host $host;` → Mantém o host original da requisição (importante para o Django saber qual domínio foi acessado).
   - `proxy_set_header X-Real-IP $remote_addr;` → Passa o IP real do cliente.
   - `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` → Mantém a cadeia de IPs (se passar por vários proxies).
   - `proxy_set_header X-Forwarded-Proto $scheme;` → Informa se a requisição original veio por *http* ou *https*.

> **Mas como eu testo seu meu nginx está funcionando corretamente?**

Primeiro, vamos ver se há mensagem de erro dentor do container `nginx`:

```bash
docker logs nginx_reverse_proxy
```

**OUTPUT:**
```bash
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf is not a file or does not exist
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/08/19 00:52:35 [notice] 1#1: using the "epoll" event method
2025/08/19 00:52:35 [notice] 1#1: nginx/1.27.5
2025/08/19 00:52:35 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2025/08/19 00:52:35 [notice] 1#1: OS: Linux 6.6.87.2-microsoft-standard-WSL2
2025/08/19 00:52:35 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2025/08/19 00:52:35 [notice] 1#1: start worker processes
2025/08/19 00:52:35 [notice] 1#1: start worker process 20
2025/08/19 00:52:35 [notice] 1#1: start worker process 21
2025/08/19 00:52:35 [notice] 1#1: start worker process 22
2025/08/19 00:52:35 [notice] 1#1: start worker process 23
2025/08/19 00:52:35 [notice] 1#1: start worker process 24
2025/08/19 00:52:35 [notice] 1#1: start worker process 25
2025/08/19 00:52:35 [notice] 1#1: start worker process 26
2025/08/19 00:52:35 [notice] 1#1: start worker process 27
```

Ótimo, agora vamos fazer alguns testes no navegador:

 - http://localhost/static/ → deve exibir arquivos estáticos.
 - http://localhost/media/ → deve exibir uploads.

**OUTPUT:**
```bash
403 Forbidden
nginx/1.27.5
```

> **What?** Não funcionou!

Agora vamos tentar acessar um arquivo específico:

 - http://localhost/static/admin/css/base.css
 - http://localhost/static/admin/img/inline-delete.svg

> **What?** Agora funcionou!

Esse comportamento indica que o *Nginx* está conseguindo servir arquivos existentes, mas não consegue listar diretórios. Por padrão, o Nginx não habilita autoindex (listagem de diretórios).

Então:

 - http://localhost/static/admin/css/base.css → Funciona porque você está acessando um arquivo específico.
 - http://localhost/static/ → Dá *403 Forbidden* porque você está acessando o diretório, e o Nginx não lista o conteúdo (diretório) por padrão.

> **Como resolver isso?**

#### 1️⃣ Habilitar autoindex (não recomendado para produção, só para teste):

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

> **NOTE:**  
> Isso permite ver os arquivos listados no navegador, mas não é seguro em produção, porque expõe todos os arquivos publicamente.

#### 2️⃣ Testar apenas arquivos específicos (recomendado):

Abra diretamente algum arquivo, como:

 - http://localhost/static/admin/css/base.css
 - http://localhost/media/example.txt
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

<div id="db-setting"></div>

## `08 - Configurando o PostgreSQL como Banco de Dados do nosso projeto`

> Aqui nós vamos configurar o PostgreSQL como Banco de Dados do nosso projeto.

De início vamos definir no nosso [core/settings.py](../core/settings.py) o Banco de Dados:

[core/settings.py](../core/settings.py)
```python
import os

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

> **NOTE:**
> Isso faz o Django pegar as configurações de Banco de Dados das nossas variáveis de ambiente: [.env](../.env)

Agora nós precisamos instalar o driver do PostgreSQL:

```bash
poetry add psycopg2-binary@latest
```

Se você não tiver o `psycopg2-binary` instalado dentro do container ainda pode executar o seguinte comando:

```bash
docker compose exec web pip install psycopg2-binary
```

Com tudo configurado, crie as tabelas padrão do Django no Postgres:

```bash
docker compose exec web python manage.py migrate
```

> **NOTE:**
> Isso vai criar as tabelas de *auth*, *admin*, *sessions*, etc.

Agora vamos criar um *usuário admin* para acessar o painel do Django:

```bash
docker compose exec web python manage.py createsuperuser
```

Para testar se tudo está funcionando corretamente, E acesse no navegador:

 - [http://localhost/admin/](http://localhost/admin/)

> Ok, mas como eu sei que isso está funcionando corretamente? Ou seja, minha aplicação está utilizando esse banco de dados (Postgres)?

Uma maneira é testar diretamente no container e ver se ele tem as tabelas comuns do Django, como `auth_user`, `django_migrations`, `django_session`, etc.:

**Entrar no container "postgres_db" via bash:**
```bash
docker exec -it postgres_db bash
```

**Entra no banco de sados a partir das variáveis de ambiente:**
```bash
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

**Listar as tabelas no banco de dados (que você está conectado - easy_rag_db):**
```bash
\dt
```

**OUTPUT:**
```bash
                   List of relations
 Schema |            Name            | Type  |  Owner
--------+----------------------------+-------+---------
 public | auth_group                 | table | easyrag
 public | auth_group_permissions     | table | easyrag
 public | auth_permission            | table | easyrag
 public | auth_user                  | table | easyrag
 public | auth_user_groups           | table | easyrag
 public | auth_user_user_permissions | table | easyrag
 public | django_admin_log           | table | easyrag
 public | django_content_type        | table | easyrag
 public | django_migrations          | table | easyrag
 public | django_session             | table | easyrag
(10 rows)
```

Para finalizar vamos fazer só mais um teste verificando de o usuário admin foi criado:

```bash
SELECT id, username, email, password FROM auth_user;
```

**OUTPUT:**
```bash
 id | username |           email            |                                         password
----+----------+----------------------------+-------------------------------------------------------------------------------------------
  1 | drigols  | drigols.creative@gmail.com | pbkdf2_sha256$1000000$l54dNAB9qZCB3WXotk4Y9J$XgYHNWGZuIx0bZWba9PKRfeCazSAg2h3hGJeGz0fkeE=
(1 row)
```














































---

<div id="understanding-async-celery"></div>

## `09 - Entendendo: Tasks Assíncronas e Celery no Django`

> Aqui nós vamos entender o que são **"Tasks Assíncronas"** e **"Celery"** no contexto do nosso projeto (Django).

#### 🔹 O que são Tasks Assíncronas no contexto do nosso projeto?

**👉 Para que servem:**

 - Tasks assíncronas são operações que **não precisam ser executadas imediatamente dentro do fluxo da requisição** (request/response).  
 - Em vez de bloquear o usuário esperando a conclusão, a aplicação delega a execução da tarefa para um sistema de filas (queue), que roda em segundo plano.

**👉 Quando utilizar:**

 - Sempre que a tarefa não precisar de resposta imediata para o usuário.
 - Quando a operação for demorada (segundos/minutos).
 - Quando você quiser distribuir carga em vários workers (paralelismo).

**👉 Desvantagens:**

 - Aumento da complexidade da arquitetura.
 - Necessidade de monitorar fila e workers.
 - Pode haver atraso no processamento dependendo da carga.

#### 🔹 O que é o Celery?

**👉 Para que serve:**

> O *Celery* é um framework que permite rodar tasks assíncronas em projetos Python/Django.
Ele usa um message broker (Redis, RabbitMQ, etc.) para gerenciar a fila de tarefas.

Fluxo simplificado:

 1. Django dispara a task.
 2. A task é colocada no broker (ex: Redis).
 3. Um ou mais workers Celery processam as tasks em paralelo.
 4. A resposta é opcional (pode salvar logs, status ou resultados).

**👉 Quando utilizar:**

 - Projetos que precisam de tarefas em segundo plano (ex: e-mails, relatórios, notificações).
 - Situações em que escalabilidade e paralelismo são necessários.
 - Quando quiser agendar jobs (ex: executar algo todo dia às 6h).

**👉 Vantagens:**

 - Madura e consolidada (muito usada na comunidade Django).
 - Integração nativa com Redis e RabbitMQ.
 - Suporte a retries automáticos, agendamento e monitoramento.
 - Permite criar workflows complexos (chaining, groups de tasks).

**👉 Desvantagens:**

 - Pode ser "overkill" para projetos pequenos.
 - Configuração inicial mais trabalhosa (precisa de Redis/RabbitMQ + workers).
 - Requer atenção extra para manter workers rodando em produção.

#### ⚡ Resumo prático

 - **Tasks assíncronas** → Conceito (qualquer job rodando em background).
 - **Celery** → Ferramenta que implementa isso no nosso projeto.















































---

<div id="create-core-celery"></div>

## `10 - Fazendo o Celery reconhecer o Django e vice-versa`

> Sabendo que **"Celery é um task queue manager (gerenciador de filas de tarefas assíncronas)"**.

Ou seja:

> Ele tira tarefas pesadas ou demoradas do fluxo principal do Django e executa em segundo plano, usando workers.

Vamos criar o arquivo [core/celery.py](../core/celery.py) que vai ser responsável por fazer o Celery reconhece as nossas configurações do Django.

#### `Por que precisamos do core/celery.py?`

Esse arquivo é o **ponto central de configuração do Celery dentro do Django**:

 - Ele inicializa o app Celery.
 - Faz o Django e Celery conversarem (carrega configurações do `settings.py`).
 - Define onde o Celery vai procurar tasks no projeto (app.autodiscover_tasks).

> **NOTE:**  
> Sem ele, o Celery não sabe “quem é o Django” nem onde procurar as funções assíncronas.

[core/celery.py](../core/celery.py)
```python
from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
    return "ok"
```

No código acima as partes mais importantes (não que as outras não sejam) são:

 - `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")`
   - Diz ao Celery qual `settings.py` usar (o mesmo do Django).
   - Sem isso, o Celery não consegue acessar configs do Django, como banco de dados, Redis, etc.
 - `app = Celery("core")`
   - Cria a instância principal do Celery, chamada `app`.
   - O "core" é só o nome (costuma ser igual ao nome do projeto).
 - `app.config_from_object("django.conf:settings", namespace="CELERY")`
   - Faz o Celery ler configs do Django.
   - No `core/settings.py`, usamos variáveis como:
     - CELERY_BROKER_URL = redis://redis:6379/0"
     - CELERY_RESULT_BACKEND = "redis://redis:6379/0"
 - `app.autodiscover_tasks()`
   - Faz o Celery procurar automaticamente por `tasks.py` *"em cada app Django"*.
   - Assim, basta criar um arquivo `tasks.py` em qualquer app e o Celery já reconhece.
 - `Função debug_task()`
   - Uma task de exemplo para você rodar celery -A core worker -l info e verificar se está funcionando.

#### `Como o Django reconhece esse core/celery.py?`

Para isso nós precisamos configurar isso em `core/__init__.py`:

[core/__init__.py](../core/__init__.py)
```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

> **NOTE:**  
> - Isso faz o Django expor a instância do Celery sempre que o projeto for carregado.
> - Sem esse import, o Celery não "linka" direito com o Django.

#### `Configurações do Celery no settings.py`

Continuando... O arquivo `core/settings.py` centraliza todas as configurações do Django. Quando adicionamos o Celery, precisamos definir:

 - Onde ele vai buscar as tarefas (fila);
 - Onde vai armazenar os resultados;
 - Como serializar os dados;
 - Como lidar com timezone e testes.

**📝 Passo 1 – Configuração do Broker e Backend:**
[core/settings.py](../core/settings.py)
```python
# --- Celery broker/result backend from env ---
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
```

**🔎 Explicação:**

 - **Broker (CELERY_BROKER_URL): é o "mensageiro".**
   - Ele recebe as tasks criadas pelo Django e distribui para os workers.
   - Aqui usamos o Redis como broker (redis://redis:6379/0).
   - O `0` significa que ele vai usar a database `0` do Redis.
 - **Result Backend (CELERY_RESULT_BACKEND): guarda os resultados das tasks.**
   - Exemplo: se você dispara uma task que gera um PDF, o backend pode armazenar o status e o resultado.
   - Aqui usamos também o Redis, mas na database `1 (:1)` → assim separamos tráfego de tasks (fila) e resultados.
 - **os.getenv()**
   - Usamos `os.getenv()` → para permitir configurar via `.env`. Se não encontrar, usa os valores padrão (Redis rodando no container redis).

**📝 Passo 2 – Segurança na serialização:**
[core/settings.py](../core/settings.py)
```python
# Segurança de serialization (evitar pickle)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
```

**🔎 Explicação:**

 - **Por padrão, o Celery poderia usar Pickle para serializar mensagens:**
   - O que é inseguro, pode permitir execução de código malicioso.
 - **Aqui definimos para usar apenas JSON:**
   - `CELERY_ACCEPT_CONTENT` → Só aceita mensagens em JSON.
   - `CELERY_TASK_SERIALIZER` → Tasks enviadas são serializadas em JSON.

> **Quais vantagens e desvantagens?**

 - **✅ Vantagem:**
   - Segurança e compatibilidade.
 - **⚠️ Desvantagem:**
   - JSON é limitado, não suporta objetos Python complexos (precisa converter).

**📝 Passo 3 – Configuração de Timezone:**
[core/settings.py](../core/settings.py)
```python
# Timezone
CELERY_TIMEZONE = TIME_ZONE = "UTC"
CELERY_ENABLE_UTC = True
```

**🔎 Explicação:**

 - `TIME_ZONE` = "UTC" → Django roda internamente em UTC (boa prática para sistemas globais).
 - `CELERY_TIMEZONE` → Mantém Celery sincronizado com Django.
 - `CELERY_ENABLE_UTC` = True → garante que as tasks sejam executadas em UTC.

> **Quais vantagens e desvantagens?**

 - **✅ Vantagem:**
   - Evita problemas com fuso horário (ex.: horários errados em tasks agendadas).
 - **⚠️ Desvantagem:**
   - Se você quiser logs em horário local, precisa ajustar depois.

**📝 Passo 4 – Configuração de Testes:**
[core/settings.py](../core/settings.py)
```python
# Testes
CELERY_TASK_ALWAYS_EAGER = True
```

**🔎 Explicação:**

 - `CELERY_TASK_ALWAYS_EAGER` → Se True, as tasks não vão para Redis, são executadas imediatamente e no mesmo processo do Django.
 - Isso é útil em ambiente local de desenvolvimento para testar tasks sem precisar subir Celery + Redis.

> **Quais vantagens e desvantagens?**

 - **✅ Vantagem:**
   - Facilita debug e desenvolvimento.
 - **⚠️ Desvantagem:**
   - Não simula o ambiente real → em produção sempre deixe como False.































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































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
