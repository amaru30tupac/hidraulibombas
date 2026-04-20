from django import forms
from clients.models import Client
from .models import MaintenancePhoto, MaintenanceRecord


BASE_INPUT_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 "
    "text-sm text-slate-900 shadow-sm focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-100"
)

BASE_SELECT_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 "
    "text-sm text-slate-900 shadow-sm focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-100"
)

BASE_TEXTAREA_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 "
    "text-sm text-slate-900 shadow-sm focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-100 min-h-[120px]"
)


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            "client",
            "email",
            "tower",
            "number",
            "maintenance_type",
            "equipment",
            "date",
            "entry_time",
            "exit_time",
            "site",
            "parts_for_change",
            "observations",
            "process_status",
        ]
        widgets = {
            "client": forms.Select(attrs={"class": BASE_SELECT_CLASSES}),
            "email": forms.EmailInput(attrs={"class": BASE_INPUT_CLASSES}),
            "tower": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "number": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "maintenance_type": forms.Select(attrs={"class": BASE_SELECT_CLASSES}),
            "equipment": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "date": forms.DateInput(attrs={"class": BASE_INPUT_CLASSES, "type": "date"}),
            "entry_time": forms.TimeInput(attrs={"class": BASE_INPUT_CLASSES, "type": "time"}),
            "exit_time": forms.TimeInput(attrs={"class": BASE_INPUT_CLASSES, "type": "time"}),
            "site": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "parts_for_change": forms.Textarea(attrs={"class": BASE_TEXTAREA_CLASSES, "rows": 4}),
            "observations": forms.Textarea(attrs={"class": BASE_TEXTAREA_CLASSES, "rows": 4}),
            "process_status": forms.Select(attrs={"class": BASE_SELECT_CLASSES}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["client"].queryset = Client.objects.filter(is_active=True).order_by("name")

        self.fields["email"].required = False
        self.fields["tower"].required = False
        self.fields["number"].required = False
        self.fields["entry_time"].required = False
        self.fields["exit_time"].required = False
        self.fields["site"].required = False
        self.fields["parts_for_change"].required = False
        self.fields["observations"].required = False


class MaintenancePhotoForm(forms.ModelForm):
    class Meta:
        model = MaintenancePhoto
        fields = ["image", "caption"]
        widgets = {
            "caption": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
        }