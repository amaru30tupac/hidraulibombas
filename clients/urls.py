from django.urls import path
from .views import (
    client_create_view,
    client_delete_view,
    client_list_view,
    client_update_view,
)

urlpatterns = [
    path("", client_list_view, name="client_list"),
    path("nuevo/", client_create_view, name="client_create"),
    path("<int:pk>/editar/", client_update_view, name="client_update"),
    path("<int:pk>/eliminar/", client_delete_view, name="client_delete"),
]