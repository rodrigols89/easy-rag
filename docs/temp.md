

 - [`Criando a sessão de login/logout + página home.html`](#session-home)
 - [`Criando o login com Google e GitHub`](#login-google-github)















































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

<div id="app-documents"></div>

## `18 - Criando e configurando o App documents`

> Aqui nós vamos criar o App `documents` que vai ser responsável por armazenar os dados enviados pelos usuários no Banco de Dados.

```bash
python manage.py startapp documents
```

[core/settings.py](../core/settings.py)
```python
INSTALLED_APPS = [

  ...

    # seus apps
    "users",
    "documents",
]
```












































---

<div id="documents-models"></div>

## `19 - Implementando os models do App documents`

> **Um model é a representação, no banco de dados, de um tipo de dado do seu sistema.**

No nosso caso, queremos armazenar arquivos enviados pelos usuários, por isso o model File (ou Document) terá:

 - Uma ligação com o usuário dono (user);
 - O próprio arquivo (file);
 - A data de upload (uploaded_at).

Além disso, adicionaremos **validações automáticas** para restringir o tipo de arquivo e o tamanho máximo (50MB).

 - **📎 Upload direto aqui no chat:**
   - *Tamanho máximo:* 50 MB por arquivo;
   - O usuário vai poder enviar vários arquivos, desde que cada um tenha até 50 MB;
   - *Tipos aceitos:* textos (.txt, .pdf, .docx, .md).

Vamos começar implementando uma validação se o arquivo enviado tem um tamanho maior do que 50MB:

[documents/models.py](../documents/models.py)
```python
from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size = 50 * 1024 * 1024  # 50 megabytes
    if value.size > max_size:
        raise ValidationError(
            "O arquivo excede o tamanho máximo permitido de 50MB."
        )
```

**Explicação das principais partes do código:**

 - `max_size = 50 * 1024 * 1024`
   - Aqui definimos a constante `max_size` em bytes.
   - A expressão `50 * 1024 * 1024` converte 50 megabytes para bytes (1 MB = 1024 * 1024 bytes).
 - `if value.size > max_size:`
   - Este bloco testa se o *tamanho do arquivo (value.size)* é maior que *max_size*:
     - *value.size* normalmente retorna o tamanho do arquivo em bytes.
   - Se a condição for verdadeira, significa que o arquivo excede o limite definido.
   - `raise ValidationError("...")`
     - Se o arquivo for maior que o limite, a função lança uma exceção `ValidationError` com a mensagem em português.
     - Essa exceção interrompe o fluxo de execução e sinaliza ao chamador (por exemplo, o formulário ou o serializer) que a validação falhou — geralmente resultando em uma mensagem de erro exibida ao usuário.

Continuando, agora nós vamos validar os tipos de arquivos que o usuário pode enviar:

[documents/models.py](../documents/models.py)
```python
def validate_file_extension(value):
    valid_extensions = [".txt", ".pdf", ".docx", ".md"]
    if not any(str(value).lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError(
            "Tipo de arquivo inválido. Use apenas os formatos .txt, .pdf, .docx ou .md."
        )
```

**Explicação das principais partes do código:**

 - `valid_extensions = [".txt", ".pdf", ".docx", ".md"]`
   - Cria uma lista com as extensões válidas de arquivos permitidas:
     - `.txt` → Texto simples;
     - `.pdf` → Documento em PDF;
     - `.docx` → Documento do Word;
     - `.md` → Arquivo Markdown.
 - `if not any(str(value).lower().endswith(ext) for ext in valid_extensions):`
   - `str(value).lower()`
     - Converte o nome do arquivo para minúsculas (garantindo que .PDF e .pdf sejam tratados igualmente).
   - `.endswith(ext`
     - O método `.endswith(ext)` verifica se o nome do arquivo termina com cada uma das extensões da lista.
 - `raise ValidationError("...")`
   - Se o arquivo não tiver uma extensão válida, a função levanta uma exceção `ValidationError` com uma mensagem de erro clara.

Por fim, vamos implementar a classe `File` que vai ser responsável por representar os arquivos enviados pelos usuários:

[documents/models.py](../documents/models.py)
```python
from django.conf import settings
from django.db import models


class File(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.FileField(
        upload_to="uploads/",
        validators=[validate_file_size, validate_file_extension],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} (de {self.user.username})"
```

**Explicação das principais partes do código:**

```python
user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="files",
)
```

 - Cria uma relação de chave estrangeira (ForeignKey) entre o modelo File e o modelo de usuário do projeto (definido em `settings.AUTH_USER_MODEL`).
 - `on_delete=models.CASCADE`
   - Se o usuário for excluído, todos os seus arquivos também serão automaticamente deletados.
 - `related_name="files"`
   - Permite acessar os arquivos de um usuário facilmente, por exemplo:
     - `user.files.all()  # retorna todos os arquivos enviados por esse usuário`

```python
file = models.FileField(
    upload_to="uploads/",
    validators=[validate_file_size, validate_file_extension],
)
```

 - **Define o campo de arquivo principal do modelo:**
   - `upload_to="uploads/"`
     - Especifica o diretório (dentro de *MEDIA_ROOT*) onde os arquivos serão armazenados.
     - Exemplo: um arquivo será salvo como `media/uploads/nome_do_arquivo.pdf`.
   - `validators=[validate_file_size, validate_file_extension]`
     - Aplica os dois validadores personalizados:
       - `validate_file_size` → Impede upload de arquivos maiores que *50MB*.
       - `validate_file_extension` → Só aceita arquivos *.txt*, *.pdf*, *.docx* ou *.md*.
     - **NOTE:** Esses validadores são chamados automaticamente quando o arquivo é enviado ou salvo.

```python
uploaded_at = models.DateTimeField(auto_now_add=True)
```

 - **Adiciona um campo que armazena a data e hora em que o arquivo foi enviado:**
   - `auto_now_add=True`
     - Faz com que o Django preencha automaticamente esse campo com o horário atual na criação do registro (e nunca mais o altere depois).
   - Ideal para manter o histórico de uploads.

```python
def __str__(self):
    return f"{self.file.name} (de {self.user.username})"
```

 - Define a representação textual do objeto quando ele é exibido no painel administrativo ou no shell do Django.
 - Exemplo de saída: `uploads/relatorio.pdf (de rodrigo)`
 - **NOTE:** Isso facilita a identificação dos arquivos no admin e em consultas.

#### Aplicando as migrações

Por fim, vamos aplicar as migrações:

```bash
python manage.py makemigrations documents
```

```bash
python manage.py migrate
```













































---

<div id="fileupload-form"></div>

## `20 - Criando o formulário customizado (FileUploadForm) com ModelForm`

Agora vamos criar um formulário customizado para o upload de arquivos utilizando o ModelForm.

> **Mas o que é um "ModelForm"?**
> O `ModelForm` é uma classe especial do Django que cria automaticamente um formulário HTML com base em um modelo (no nosso caso, o File).

Ele faz a ponte entre:

 - O front-end (HTML), onde o usuário escolhe e envia o arquivo;
 - O back-end (models), onde os dados são validados e salvos no banco.

Assim, o Django cuida automaticamente de:

 - Validar os campos do formulário;
 - Garantir o tipo correto de arquivo;
 - Associar o arquivo ao usuário;
 - Salvar no banco de dados e no diretório definido.

[documents/forms.py](../documents/forms.py)
```python
from django import forms

from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]
```

**🧩 1. Importações necessárias**
```python
from django import forms
from .models import File
```

 - `from django import forms`
   - Importa o módulo *forms* do Django, que contém todas as classes e ferramentas para criar formulários HTML dinâmicos.
 - `from .models import File`
   - Importa o modelo File do mesmo app (documents).
   - Assim, o formulário pode ser conectado diretamente ao modelo e saber como os dados devem ser armazenados no banco.

**🧩 2. Criação do formulário de upload**
```python
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]
```

 - `class FileUploadForm(forms.ModelForm):`
   - Cria uma classe baseada em ModelForm, que é o tipo de formulário que já “entende” como o modelo funciona.
 - `class Meta:`
   - É uma classe interna usada para dizer ao Django qual modelo o formulário representa e quais campos devem aparecer.
 - `model = File`
   - Informa que este formulário está ligado ao modelo `File`.
 - `fields = ["file"]`
   - Define que apenas o campo file (o upload do arquivo em si) aparecerá no formulário.













































---

## `21 - Implementando a view upload_file_view() no App documents`

> Aqui nós vamos implementar a view (ação) `upload_file_view`.

Ela decide o que fazer dependendo do tipo de requisição (GET ou POST):

 - `GET` → Exibe a página com o formulário vazio (FileUploadForm),
 - `POST` → Recebe os dados enviados (arquivo + usuário), valida e salva no banco.

Além disso:

 - Vamos proteger a view (ação) com `@login_required` (somente usuários autenticados podem enviar arquivos).

[documents/views.py](../documents/views.py)
```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FileUploadForm


@login_required(login_url="/")
def upload_file_view(request):
    # Caso GET → exibe o formulário vazio
    if request.method == "GET":
        form = FileUploadForm()
        return render(request, "pages/upload.html", {"form": form})

    # Caso POST → processa o upload
    elif request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)  # ainda não salva no banco
            file.user = request.user  # vincula ao usuário logado
            file.save()  # agora salva no banco
            return redirect("upload-file")
        else:
            messages.error(
                request,
                "Erro ao enviar o arquivo. Verifique o formato ou tamanho.",
            )
            return render(request, "pages/upload.html", {"form": form})
```

**🧩 1. Caso GET → Exibe o formulário vazio**
```python
if request.method == "GET":
    form = FileUploadForm()
    return render(request, "pages/upload.html", {"form": form})
```

 - Se o usuário apenas acessar a página, criamos um formulário vazio (FileUploadForm()).
 - O template upload.html é renderizado, e o formulário é enviado ao HTML via contexto { "form": form }.




























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
