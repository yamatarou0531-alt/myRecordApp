from django import forms
from .models import SakeRecord


class SakeRecordForm(forms.ModelForm):
    class Meta:
        model = SakeRecord
        fields = ["title", "brewery", "sake_type", "rating", "memo", "image"]