from .models import Product
from django import forms


class prodform(forms.ModelForm):
    class Meta:
        model = Product
        fields ="__all__"