from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from clients.models import Client
from maintenance.models import MaintenanceRecord


@login_required
def dashboard_view(request):
    context = {
        "page_title": "Dashboard",
        "clients_count": Client.objects.count(),
        "records_count": MaintenanceRecord.objects.count(),
        "recent_records": MaintenanceRecord.objects.select_related("client", "technician")[:10],
    }
    return render(request, "users/dashboard.html", context)