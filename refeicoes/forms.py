from django import forms
from .models import Refeicao


class RefeicaoForm(forms.ModelForm):

    class Meta:
        model = Refeicao

        fields = [
            "nome",
            "quantidade",
            "carboidratos",
            "proteinas",
            "gorduras",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "placeholder": "Ex: Feijão cozido"
            }),

            "quantidade": forms.NumberInput(attrs={
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["carboidratos"].required = False
        self.fields["proteinas"].required = False
        self.fields["gorduras"].required = False