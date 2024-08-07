from django import forms
from .models import Inverter

class InverterForm(forms.ModelForm):
    class Meta:
        model = Inverter
        fields = '__all__'
