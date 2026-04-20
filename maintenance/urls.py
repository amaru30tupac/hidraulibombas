from django.urls import path
from .views import (
    maintenance_create_view,
    maintenance_delete_view,
    maintenance_detail_view,
    maintenance_delete_photo_view,
    maintenance_export_detail_pdf_view,
    maintenance_export_excel_view,
    maintenance_export_list_pdf_view,
    maintenance_list_view,
    maintenance_sign_client_view,
    maintenance_sign_technician_view,
    maintenance_update_view,
)

urlpatterns = [
    path("", maintenance_list_view, name="maintenance_list"),
    path("nuevo/", maintenance_create_view, name="maintenance_create"),
    path("exportar-pdf/", maintenance_export_list_pdf_view, name="maintenance_export_list_pdf"),
    path("exportar-excel/", maintenance_export_excel_view, name="maintenance_export_excel"),
    path("<int:pk>/", maintenance_detail_view, name="maintenance_detail"),
    path("<int:pk>/editar/", maintenance_update_view, name="maintenance_update"),
    path("<int:pk>/eliminar/", maintenance_delete_view, name="maintenance_delete"),
    path("<int:pk>/pdf/", maintenance_export_detail_pdf_view, name="maintenance_export_detail_pdf"),
    path("<int:pk>/firmar-tecnico/", maintenance_sign_technician_view, name="maintenance_sign_technician"),
    path("<int:pk>/firmar-cliente/", maintenance_sign_client_view, name="maintenance_sign_client"),
    path("foto/<int:photo_id>/eliminar/", maintenance_delete_photo_view, name="maintenance_delete_photo"),
]