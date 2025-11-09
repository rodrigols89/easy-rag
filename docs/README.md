# Easy RAG

## Conteúdo

 - [`Adicionando .editorconfig e .gitignore`](#editorconfig-gitignore)
 - [`Iniciando o projeto com "poetry init"`](#poetry-init)
 - [`Instalando e configurando o Ruff`](#ruff-settings-pyproject)
 - [`Instalando e configurando o Pytest`](#pytest-settings-pyproject)
 - [`Instalando e configurando o Taskipy`](#taskipy-settings-pyproject)
 - [`Instalando e configurando o pre-commit`](#precommit-settings)
 - [`Instalando a biblioteca psycopg2-binary`](#psycopg2-binary)
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


---

<div id="psycopg2-binary"></div>

## `Instalando a biblioteca psycopg2-binary`

> Antes de começar a trabalhar com o Django, precisamos instalar o driver nativo do nosso Banco de Dados (PostgreSQL).

 - Este é o driver oficial do PostgreSQL para Python — o Django usa ele internamente para conversar com o banco.
 - **NOTE:** Sem ele, o Django não consegue abrir a conexão porque depende de um driver nativo específico do PostgreSQL.

```bash
poetry add psycopg2-binary@latest
```

#### `O que o psycopg2-binary faz?`

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

> **Aqui vamos explicar quais os comando do Taskipy que nós estamos utilizando na nossa aplicação.**

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
