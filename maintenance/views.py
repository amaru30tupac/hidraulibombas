from typing import Dict, List, Tuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MaintenanceRecordForm
from .models import InspectionValue, MaintenancePhoto, MaintenanceRecord


STATE_OPTIONS = ["", "A", "C", "F", "P", "D", "V", "NA"]

TABLERO_CONTROL_ROWS = [
    ("variador", "Variador", "state"),
    ("muletillas", "Muletillas", "state"),
    ("piloto", "Piloto", "state"),
    ("contactores", "Contactores", "state"),
    ("presostatos", "Presostatos", "state"),
    ("alternador", "Alternador", "state"),
    ("guarda_motor", "Guarda motor", "state"),
    ("temporizador", "Temporizador", "state"),
    ("rele_termico", "Relé térmico", "state"),
    ("flotador_electrico", "Flotador eléctrico", "state"),
    ("conexiones", "Conexiones", "state"),
    ("amperaje", "Amperaje", "number"),
    ("voltaje", "Voltaje", "number"),
]

HIDROSISTEMA_ROWS = [
    ("precarga", "Precarga"),
    ("flotador_mecanico", "Flotador mecánico"),
    ("valvulas_succion", "Válvulas de succión"),
    ("tanque_hidro", "Tanque hidro"),
    ("cheques", "Cheques"),
    ("presion_linea", "Presión de línea"),
    ("registros", "Registros"),
    ("membrana", "Membrana"),
    ("manometro", "Manómetro"),
    ("cargador_aire", "Cargador de aire"),
    ("tanque_reserva", "Tanque reserva"),
    ("flauta_descarga", "Flauta de descarga"),
]

SISTEMA_EYECTOR_ROWS = [
    ("guarda_motor", "Guarda motor", "state"),
    ("breaker", "Breaker", "state"),
    ("muletilla", "Muletilla", "state"),
    ("contactores", "Contactores", "state"),
    ("flotador_electrico", "Flotador eléctrico", "state"),
    ("conexiones", "Conexiones", "state"),
    ("amperaje", "Amperaje", "number"),
    ("voltaje", "Voltaje", "number"),
    ("sirena", "Sirena", "state"),
    ("rele_termico", "Relé térmico", "state"),
    ("residuos_solidos", "Residuos sólidos", "state"),
]

MOTOR_ROWS = [
    ("rodamientos", "Rodamientos", "state"),
    ("casquillo", "Casquillo", "state"),
    ("empaque", "Empaque", "state"),
    ("ventilador", "Ventilador", "state"),
    ("bornera", "Bornera", "state"),
    ("bobinado", "Bobinado", "state"),
]

BOMBAS_ROWS = [
    ("impulsor", "Impulsor", "state"),
    ("sello_mecanico", "Sello mecánico", "state"),
    ("empaque", "Empaque", "state"),
    ("carcasa", "Carcasa", "state"),
    ("casquillo", "Casquillo", "state"),
]


def build_state_choices() -> List[Tuple[str, str]]:
    return [
        ("", "—"),
        ("A", "A – Ajustadas"),
        ("C", "C – Cambio"),
        ("F", "F – Falla"),
        ("P", "P – Pendiente"),
        ("D", "D – Diagnóstico"),
        ("V", "V – Verificado / OK / Operando"),
        ("NA", "N/A – No aplica"),
    ]


def build_table_rows_for_template(rows_config, positions, section_name, existing_map=None):
    existing_map = existing_map or {}
    built_rows = []

    for row in rows_config:
        key = row[0]
        label = row[1]
        row_type = row[2] if len(row) > 2 else "state"

        cells = []
        for position in positions:
            existing = existing_map.get((section_name, key, position))
            cell_name = f"{section_name}__{key}__{position}"

            value = ""
            numeric_value = ""

            if existing:
                value = existing.value or ""
                numeric_value = "" if existing.numeric_value is None else str(existing.numeric_value)

            cells.append({
                "name": cell_name,
                "type": row_type,
                "value": value,
                "numeric_value": numeric_value,
                "position": position,
            })

        built_rows.append({
            "key": key,
            "label": label,
            "type": row_type,
            "cells": cells,
        })

    return built_rows


def build_hidrosistema_rows_for_template(rows_config, existing_map=None):
    existing_map = existing_map or {}
    built_rows = []

    for key, label in rows_config:
        existing = existing_map.get(("hidrosistema", key, "estado"))
        built_rows.append({
            "key": key,
            "label": label,
            "name": f"hidrosistema__{key}__estado",
            "value": existing.value if existing else "",
        })

    return built_rows


def calculate_general_status_from_post(post_data: Dict[str, str]) -> str:
    values = [value for key, value in post_data.items() if "__" in key and value]

    if "F" in values:
        return "Con fallas"
    if "P" in values:
        return "Pendiente"
    if "D" in values:
        return "En diagnóstico"
    if values:
        return "Revisado"
    return "Sin clasificar"


@transaction.atomic
def save_inspection_values(record: MaintenanceRecord, post_data):
    InspectionValue.objects.filter(maintenance=record).delete()

    for key, value in post_data.items():
        if "__" not in key:
            continue

        section, parameter, position = key.split("__", 2)

        if section not in {
            "tablero_control",
            "hidrosistema",
            "sistema_eyector",
            "motor",
            "bombas",
        }:
            continue

        if value == "":
            continue

        if parameter in {"amperaje", "voltaje"}:
            try:
                numeric_value = float(value)
            except ValueError:
                numeric_value = None

            InspectionValue.objects.create(
                maintenance=record,
                section=section,
                parameter=parameter,
                position=position,
                value="",
                numeric_value=numeric_value,
            )
        else:
            InspectionValue.objects.create(
                maintenance=record,
                section=section,
                parameter=parameter,
                position=position,
                value=value,
                numeric_value=None,
            )


@transaction.atomic
def save_uploaded_photos(record: MaintenanceRecord, files):
    for file in files:
        MaintenancePhoto.objects.create(
            maintenance=record,
            image=file,
        )


@login_required
def maintenance_list_view(request):
    query = request.GET.get("q", "").strip()

    records = MaintenanceRecord.objects.select_related("client", "technician").all()

    if query:
        records = records.filter(title__icontains=query)

    return render(request, "maintenance/maintenance_list.html", {
        "page_title": "Mantenimientos",
        "records": records,
        "query": query,
    })


@login_required
def maintenance_detail_view(request, pk):
    record = get_object_or_404(
        MaintenanceRecord.objects.select_related("client", "technician"),
        pk=pk,
    )

    inspection_values = record.inspection_values.all()
    grouped = {}
    for item in inspection_values:
        grouped.setdefault(item.section, []).append(item)

    return render(request, "maintenance/maintenance_detail.html", {
        "page_title": f"Detalle #{record.id}",
        "record": record,
        "grouped_values": grouped,
    })


@login_required
@transaction.atomic
def maintenance_create_view(request):
    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST, request.FILES)

        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.general_status = calculate_general_status_from_post(request.POST)
            record.title = f"{record.client.name} - {record.date} - {record.equipment}"
            record.save()

            save_inspection_values(record, request.POST)
            save_uploaded_photos(record, request.FILES.getlist("photos"))

            messages.success(request, "Mantenimiento creado correctamente.")
            return redirect("maintenance_detail", pk=record.pk)
    else:
        form = MaintenanceRecordForm()

    context = build_maintenance_form_context(form=form, page_title="Nuevo mantenimiento")
    return render(request, "maintenance/maintenance_form.html", context)


@login_required
@transaction.atomic
def maintenance_update_view(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)

    existing_values = {
        (item.section, item.parameter, item.position): item
        for item in record.inspection_values.all()
    }

    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST, request.FILES, instance=record)

        if form.is_valid():
            record = form.save(commit=False)
            record.general_status = calculate_general_status_from_post(request.POST)
            record.title = f"{record.client.name} - {record.date} - {record.equipment}"
            record.save()

            save_inspection_values(record, request.POST)
            save_uploaded_photos(record, request.FILES.getlist("photos"))

            messages.success(request, "Mantenimiento actualizado correctamente.")
            return redirect("maintenance_detail", pk=record.pk)
    else:
        form = MaintenanceRecordForm(instance=record)

    context = build_maintenance_form_context(
        form=form,
        page_title=f"Editar mantenimiento #{record.id}",
        record=record,
        existing_values=existing_values,
    )
    return render(request, "maintenance/maintenance_form.html", context)


@login_required
def maintenance_delete_view(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)

    if request.method == "POST":
        record.delete()
        messages.success(request, "Mantenimiento eliminado correctamente.")
        return redirect("maintenance_list")

    return render(request, "maintenance/maintenance_confirm_delete.html", {
        "page_title": "Eliminar mantenimiento",
        "record": record,
    })


def build_maintenance_form_context(form, page_title, record=None, existing_values=None):
    existing_values = existing_values or {}

    context = {
        "page_title": page_title,
        "form": form,
        "record": record,
        "state_choices": build_state_choices(),
        "tablero_rows": build_table_rows_for_template(
            TABLERO_CONTROL_ROWS,
            ["b1", "b2", "b3", "b4"],
            "tablero_control",
            existing_values,
        ),
        "hidrosistema_rows": build_hidrosistema_rows_for_template(
            HIDROSISTEMA_ROWS,
            existing_values,
        ),
        "eyector_rows": build_table_rows_for_template(
            SISTEMA_EYECTOR_ROWS,
            ["b1", "b2", "b3", "b4"],
            "sistema_eyector",
            existing_values,
        ),
        "motor_rows": build_table_rows_for_template(
            MOTOR_ROWS,
            ["m1", "m2", "m3", "m4"],
            "motor",
            existing_values,
        ),
        "bombas_rows": build_table_rows_for_template(
            BOMBAS_ROWS,
            ["b1", "b2", "b3", "b4"],
            "bombas",
            existing_values,
        ),
    }
    return context