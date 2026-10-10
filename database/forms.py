from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # Os campos que aparecerão para o usuário preencher
        fields = ['nome', 'tipo_estoque', 'quant_total']