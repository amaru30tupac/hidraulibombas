from django import forms
from .models import Client


BASE_INPUT_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 "
    "text-sm text-slate-900 shadow-sm focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-100"
)

BASE_TEXTAREA_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 "
    "text-sm text-slate-900 shadow-sm focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-100 min-h-[120px]"
)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "phone",
            "address",
            "contact_name",
            "is_active",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "email": forms.EmailInput(attrs={"class": BASE_INPUT_CLASSES}),
            "phone": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "address": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "contact_name": forms.TextInput(attrs={"class": BASE_INPUT_CLASSES}),
            "is_active": forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500"}),
            "notes": forms.Textarea(attrs={"class": BASE_TEXTAREA_CLASSES, "rows": 4}),
        }