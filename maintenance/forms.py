from django import forms
from clients.models import Client
from users.models import User
from .models import MaintenancePhoto, MaintenanceRecord


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
            "technician",
            "site",
            "parts_for_change",
            "observations",
        ]
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "tower": forms.TextInput(attrs={"class": "form-input"}),
            "number": forms.TextInput(attrs={"class": "form-input"}),
            "maintenance_type": forms.Select(attrs={"class": "form-select"}),
            "equipment": forms.TextInput(attrs={"class": "form-input"}),
            "date": forms.DateInput(attrs={"class": "form-input", "type": "date"}),
            "entry_time": forms.TimeInput(attrs={"class": "form-input", "type": "time"}),
            "exit_time": forms.TimeInput(attrs={"class": "form-input", "type": "time"}),
            "technician": forms.Select(attrs={"class": "form-select"}),
            "site": forms.TextInput(attrs={"class": "form-input"}),
            "parts_for_change": forms.Textarea(attrs={"class": "form-textarea", "rows": 4}),
            "observations": forms.Textarea(attrs={"class": "form-textarea", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["client"].queryset = Client.objects.filter(is_active=True).order_by("name")
        self.fields["technician"].queryset = User.objects.filter(is_active=True).order_by(
            "first_name", "last_name", "username"
        )
        self.fields["technician"].required = False
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