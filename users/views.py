import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek
from django.shortcuts import render
from django.utils import timezone

from clients.models import Client
from maintenance.models import MaintenanceRecord


@login_required
def dashboard_view(request):
    now = timezone.localdate()
    month_start = now.replace(day=1)

    total_records = MaintenanceRecord.objects.count()
    total_clients = Client.objects.count()
    month_records = MaintenanceRecord.objects.filter(date__gte=month_start).count()
    correctivos = MaintenanceRecord.objects.filter(maintenance_type="correctivo").count()
    preventivos = MaintenanceRecord.objects.filter(maintenance_type="preventivo").count()

    top_technicians = list(
        MaintenanceRecord.objects
        .filter(technician__isnull=False)
        .values("technician__first_name", "technician__last_name", "technician__username")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    top_clients = list(
        MaintenanceRecord.objects
        .values("client__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    top_equipment = list(
        MaintenanceRecord.objects
        .values("equipment")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    by_type = list(
        MaintenanceRecord.objects
        .values("maintenance_type")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    by_status = list(
        MaintenanceRecord.objects
        .values("general_status")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    monthly_trend = list(
        MaintenanceRecord.objects
        .annotate(period=TruncMonth("date"))
        .values("period")
        .annotate(total=Count("id"))
        .order_by("period")
    )

    weekly_trend = list(
        MaintenanceRecord.objects
        .annotate(period=TruncWeek("date"))
        .values("period")
        .annotate(total=Count("id"))
        .order_by("period")
    )

    recent_records = MaintenanceRecord.objects.select_related("client", "technician").order_by("-date", "-created_at")[:8]

    technician_labels = [
        (
            f"{item['technician__first_name'] or ''} {item['technician__last_name'] or ''}".strip()
            or item["technician__username"]
            or "Sin técnico"
        )
        for item in top_technicians
    ]
    technician_values = [item["total"] for item in top_technicians]

    client_labels = [item["client__name"] or "Sin cliente" for item in top_clients]
    client_values = [item["total"] for item in top_clients]

    equipment_labels = [item["equipment"] or "Sin equipo" for item in top_equipment]
    equipment_values = [item["total"] for item in top_equipment]

    type_labels = [item["maintenance_type"] or "Sin tipo" for item in by_type]
    type_values = [item["total"] for item in by_type]

    monthly_labels = [
        item["period"].strftime("%Y-%m") if item["period"] else ""
        for item in monthly_trend
    ]
    monthly_values = [item["total"] for item in monthly_trend]

    weekly_labels = [
        item["period"].strftime("%Y-%m-%d") if item["period"] else ""
        for item in weekly_trend
    ]
    weekly_values = [item["total"] for item in weekly_trend]

    most_incidence_client = top_clients[0]["client__name"] if top_clients else "-"
    most_failing_equipment = top_equipment[0]["equipment"] if top_equipment else "-"

    context = {
        "page_title": "Dashboard Ejecutivo",
        "total_records": total_records,
        "total_clients": total_clients,
        "month_records": month_records,
        "correctivos": correctivos,
        "preventivos": preventivos,
        "most_incidence_client": most_incidence_client,
        "most_failing_equipment": most_failing_equipment,
        "recent_records": recent_records,
        "technician_labels": json.dumps(technician_labels),
        "technician_values": json.dumps(technician_values),
        "client_labels": json.dumps(client_labels),
        "client_values": json.dumps(client_values),
        "equipment_labels": json.dumps(equipment_labels),
        "equipment_values": json.dumps(equipment_values),
        "type_labels": json.dumps(type_labels),
        "type_values": json.dumps(type_values),
        "monthly_labels": json.dumps(monthly_labels),
        "monthly_values": json.dumps(monthly_values),
        "weekly_labels": json.dumps(weekly_labels),
        "weekly_values": json.dumps(weekly_values),
    }
    return render(request, "maintenance/dashboard.html", context)