from dataclasses import fields
from django import forms
from .models import File


class FileForm(forms.ModelForm):
    body = forms.CharField(required=True)

    class Meta:
        model = File
        fields = "__all__"
        # exclude = ("user", )