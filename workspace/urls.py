from django.urls import path

from .views import workspace

urlpatterns = [
    path(route="workspace", view=workspace, name="workspace"),
]
