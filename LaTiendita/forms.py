from django import forms
from .models import Suscripcion

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ['email']