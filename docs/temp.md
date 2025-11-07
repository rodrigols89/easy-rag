







































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


