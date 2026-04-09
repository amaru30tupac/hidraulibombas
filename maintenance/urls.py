from django.urls import path
from .views import (
    maintenance_create_view,
    maintenance_delete_view,
    maintenance_detail_view,
    maintenance_list_view,
    maintenance_update_view,
)

urlpatterns = [
    path("", maintenance_list_view, name="maintenance_list"),
    path("nuevo/", maintenance_create_view, name="maintenance_create"),
    path("<int:pk>/", maintenance_detail_view, name="maintenance_detail"),
    path("<int:pk>/editar/", maintenance_update_view, name="maintenance_update"),
    path("<int:pk>/eliminar/", maintenance_delete_view, name="maintenance_delete"),
]