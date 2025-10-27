from django.urls import path

from .views import create_account

urlpatterns = [
    path(route="create-account/", view=create_account, name="create-account"),
]
