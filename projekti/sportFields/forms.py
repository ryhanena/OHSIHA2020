from django import forms
from .models import sportField

class fieldForm(forms.ModelForm):
    class Meta:
        model = sportField
        fields = "__all__"