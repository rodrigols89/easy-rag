from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/")
def workspace(request):
    return render(request, "pages/workspace.html")
