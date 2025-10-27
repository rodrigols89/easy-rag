from django.contrib import messages
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


def create_account(request):
    if request.method == "GET":
        return render(request, "pages/create-account.html")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # cria o usuário no banco
            return redirect("/")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        # Se apenas abriu a página (GET), mostra o formulário vazio
        form = CustomUserCreationForm()

    # Envia o form (com ou sem erros) para o template
    return render(request, "pages/create-account.html", {"form": form})
