from django.contrib import admin
from django.urls import include, path

from .views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="", view=index, name="index"),
    path("", include("users.urls")),
]
