from django.urls import path
from .views import (
    client_create_view,
    client_delete_view,
    client_list_view,
    client_update_view,
client_detail_api,
)

urlpatterns = [
    path("", client_list_view, name="client_list"),
    path("nuevo/", client_create_view, name="client_create"),
    path("<int:pk>/editar/", client_update_view, name="client_update"),
    path("<int:pk>/eliminar/", client_delete_view, name="client_delete"),
path("api/client/<int:client_id>/", client_detail_api, name="client_detail_api"),
]