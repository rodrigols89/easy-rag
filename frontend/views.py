from django.shortcuts import render


def index(request):
    if request.method == "GET":
        return render(request, "pages/index.html")


def create_account(request):
    if request.method == "GET":
        return render(request, "pages/create-account.html")
