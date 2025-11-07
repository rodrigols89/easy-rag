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
