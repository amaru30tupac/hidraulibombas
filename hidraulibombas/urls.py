from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


def root_redirect(request):
    return redirect("dashboard")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("usuarios/", include("users.urls")),
    path("clientes/", include("clients.urls")),
    path("mantenimientos/", include("maintenance.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)