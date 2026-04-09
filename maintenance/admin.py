from django.contrib import admin
from .models import MaintenanceRecord, MaintenancePhoto, InspectionValue


class MaintenancePhotoInline(admin.TabularInline):
    model = MaintenancePhoto
    extra = 1


class InspectionValueInline(admin.TabularInline):
    model = InspectionValue
    extra = 0


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "client",
        "maintenance_type",
        "equipment",
        "date",
        "technician",
        "general_status",
    )
    list_filter = ("maintenance_type", "date", "general_status")
    search_fields = ("title", "client__name", "equipment", "site")
    inlines = [MaintenancePhotoInline, InspectionValueInline]


@admin.register(MaintenancePhoto)
class MaintenancePhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "maintenance", "created_at")


@admin.register(InspectionValue)
class InspectionValueAdmin(admin.ModelAdmin):
    list_display = ("id", "maintenance", "section", "parameter", "position", "value", "numeric_value")
    list_filter = ("section", "position")
    search_fields = ("parameter", "maintenance__title")