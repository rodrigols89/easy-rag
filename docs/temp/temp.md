




































---

<div id="folder-file"></div>

## `Modelando o workspace: pastas (Folder) e arquivos (File)`

Nesta etapa vamos modelar o **núcleo do Workspace**:

 - pastas (Folder);
 - arquivos (File).

As models permitem representar hierarquia de pastas (pastas-filhas), associar pastas e arquivos a um usuário (owner), e armazenar metadados importantes como data de criação e localização física do arquivo no MEDIA_ROOT. Também incluiremos uma função `upload_to()` para organizar os arquivos no disco por usuário e pasta.

De início vamos começar modelando `workspace_upload_to()`:

[models.py](../workspace/models.py)
```python
import os


def workspace_upload_to(instance, filename):
    """
    Constrói o path onde o arquivo será salvo dentro de MEDIA_ROOT:
    workspace/<user_id>/<folder_id_or_root>/<filename>
    """
    user_part = (
        f"user_{instance.folder.owner.id}"
        if instance.folder and instance.folder.owner
        else f"user_{instance.uploader.id}"
    )

    folder_part = f"folder_{instance.folder.id}" if instance.folder else "root"

    # limpa nome do arquivo por segurança básica
    safe_name = os.path.basename(filename)

    return os.path.join("workspace", user_part, folder_part, safe_name)
```

 - `def workspace_upload_to(instance, filename)`:
   - Função usada pelo `FileField.upload_to` para gerar o caminho de armazenamento do arquivo.
   - Recebe a instância do modelo e o nome original do arquivo.
 - `user_part`
   - Tenta extrair `folder.owner.id`; se não houver folder tenta `instance.uploader.id (fallback)`, formatando como `user_<id>`.
   - Assim os arquivos ficam segregados (separados) por usuário.
 - `folder_part`
   - Se houver pasta associa `folder_<id>`, caso contrário usa "root" (arquivos na raiz do workspace do usuário).
 - `safe_name = os.path.basename(filename)`
   - Pega apenas o nome limpo do arquivo (proteção contra nomes com path).
 - `return os.path.join("workspace", user_part, folder_part, safe_name)`
   - Monta e retorna o caminho relativo dentro de `MEDIA_ROOT`.

Agora vamos implementar (modelar) a classe `Folder` que vai ser responsável por representar um pasta de um usuário no workspace:

[models.py](../workspace/models.py)
```python
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Folder(models.Model):
    """
    Representa uma pasta do usuário. Suporta hierarquia via parent (self-FK).
    """

    name = models.CharField(_("name"), max_length=255)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="folders",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.name
```

 - `from django.conf import settings`
   - Traz a configuração do projeto (para referência ao modelo de usuário se necessário).
 - `from django.db import models`
   - importa os tipos de campo e base Model do Django.
 - `from django.utils.translation import gettext_lazy as _`
   -  Utilitário para poder marcar strings traduzíveis (bom para labels futuros).
 - `name = models.CharField(_("name"), max_length=255)`
   - Campo para nome da pasta;
   - `_("name")` marca a label para tradução;
   - Limite de 255 caracteres.
 - `owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")`
   - Referência ao usuário dono da pasta;
   - `on_delete=models.CASCADE` remove pastas se o usuário for excluído;
   - `related_name="folders"` permite `user.folders.all()`.
 - `parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")`
   - Permite subpastas (estrutura em árvore).
   - `null/blank` permitem pastas de topo;
   - `related_name="children"` para acessar subpastas via `folder.children.all()`.
   - `created_at = models.DateTimeField(auto_now_add=True)` Armazena quando a pasta foi criada automaticamente.
 - `class Meta:`
   - Metadados do modelo:
     - `ordering = ["-created_at"]` — Ordena por data de criação descendente por padrão.
     - `verbose_name` e `verbose_name_plural` para labels traduzíveis no admin.

Por fim, vamos implementar (modelar) a classe `File` que vai ser responsável por representar um arquivo armazenado em uma pasta (Folder):

[models.py](../workspace/models.py)
```python
class File(models.Model):
    """
    Representa um arquivo armazenado em uma pasta (Folder).
    """

    name = models.CharField(_("name"), max_length=255)

    file = models.FileField(_("file"), upload_to=workspace_upload_to)

    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files"
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        return self.name
```

 - `file = models.FileField(_("file"), upload_to=workspace_upload_to)`
   - Campo que armazena o arquivo e usa a função `workspace_upload_to()` para decidir onde salvar fisicamente em `MEDIA_ROOT`.
 - `folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")`
   - Referência para a pasta que contém o arquivo;
   - Ao deletar a pasta os arquivos também são deletados (CASCADE);
   - `related_name="files"` permite `folder.files.all()`.
 - `uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_files")`
   - Usuário que fez o upload (útil para permissões e auditoria).
 - `uploaded_at = models.DateTimeField(auto_now_add=True)`
   - Timestamp do upload.

Por fim, vamos criar as migrações do App `workspace` e do Banco de Dados geral:

```bash
docker compose exec web python manage.py makemigrations workspace
```

```bash
docker compose exec web python manage.py migrate
```













































---

<div id="workspace-forms"></div>

## `Customizando os formulários FolderForm e FileForm`

Aqui vamos implementar os formulários `FolderForm` e `FileForm` do app workspace, responsáveis por coletar dados do usuário de maneira segura e validada.

[forms.py](../workspace/forms.py)
```python
from django import forms

from .models import File, Folder


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name"]  # campo que o usuário vai preencher


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]
```










































---

<div id="views-workspace-home"></div>

## `Implementando a view workspace_home()`

Aqui implementaremos a view (ação) `workspace_home()`, que será a página principal do workspace — onde o usuário logado verá suas pastas e arquivos da raiz (ou seja, que não estão dentro de nenhuma pasta).

[views.py](../workspace/views.py)
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import File, Folder


@login_required(login_url="/")
def workspace_home(request):
    folders = Folder.objects.filter(owner=request.user, parent__isnull=True)
    files = File.objects.filter(uploader=request.user, folder__isnull=True)

    context = {
        "folders": folders,
        "files": files,
    }
    return render(request, "workspace/home.html", context)
```

 - `@login_required(login_url="/")`
   - Aplica uma camada de proteção à função.
   - Se o usuário **não estiver logado**, ele é redirecionado para a página `“/”` (geralmente a tela de login).
   - Se estiver logado, pode continuar normalmente.
 - `folders = Folder.objects.filter(owner=request.user, parent__isnull=True)`
   - Busca todas as pastas pertencentes ao usuário logado *(owner=request.user)*;
   - E que não têm *pasta-pai (parent__isnull=True)*:
     - Ou seja, estão na raiz do workspace.
 - `files = File.objects.filter(uploader=request.user, folder__isnull=True)`
   - Busca todos os arquivos enviados pelo usuário logado *(uploader=request.user)*;
   - Que também não estão dentro de nenhuma pasta *(folder__isnull=True)*.
 - `context = {"folders": folders, "files": files}`
   - Cria um dicionário de contexto que será passado para o template HTML.
   - Esse dicionário permite acessar as variáveis folders e files dentro do HTML.
 - `return render(request, "workspace/home.html", context)`
   - Retorna a resposta HTTP renderizando o template `workspace/home.html`, já com as pastas e arquivos do usuário logado disponíveis para exibição.








































































