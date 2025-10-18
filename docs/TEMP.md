uvicorn = 'uvicorn core.asgi:application --reload --env-file .env'
killserver = 'sudo kill -9 $(sudo lsof -t -i:8000)'  # Kill service/port 8000
















---

<div id="poetry-export"></div>

## `09 - Exportando as dependências com o Poetry`

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

<div id="web-container"></div>

## `10 - Criando o container web: Dockerfile + Django + Uvicorn`

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
