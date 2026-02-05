from django import forms
from .models import Refeicao

class RefeicaoForm(forms.ModelForm):
    class Meta:
        model = Refeicao
        fields = [
            'nome',
            'carboidratos',
            'proteinas',
            'gorduras',
            'porcao'
        ]
