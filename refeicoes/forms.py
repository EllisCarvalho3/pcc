from django import forms
from .models import Refeicao

class RefeicaoForm(forms.ModelForm):
    class Meta:
        model = Refeicao
        fields = [
            "nome",
            "porcao",
            "carboidratos",
            "proteinas",
            "gorduras",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "placeholder": "Ex: Feijão cozido"
            }),
            "porcao": forms.NumberInput(attrs={
                "placeholder": "Quantidade consumida (g)"
            }),
            "carboidratos": forms.NumberInput(attrs={
                "placeholder": "Carboidratos por 100g"
            }),
            "proteinas": forms.NumberInput(attrs={
                "placeholder": "Proteínas por 100g"
            }),
            "gorduras": forms.NumberInput(attrs={
                "placeholder": "Gorduras por 100g"
            }),
        }
