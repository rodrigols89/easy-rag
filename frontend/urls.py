from django.urls import path

from .views import create_account, index

urlpatterns = [
    path(route="", view=index, name="index"),
    path(route="create-account/", view=create_account, name="create-account"),
]
