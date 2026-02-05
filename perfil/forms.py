from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'peso',
            'altura',
            'idade',
            'atividade',
            'objetivo'
        ]

    def clean(self):
        cleaned_data = super().clean()

        atividade = cleaned_data.get("atividade")
        objetivo = cleaned_data.get("objetivo")

        if not atividade:
            self.add_error("atividade", "Selecione o nível de atividade.")

        if not objetivo:
            self.add_error("objetivo", "Selecione um objetivo.")

        return cleaned_data
