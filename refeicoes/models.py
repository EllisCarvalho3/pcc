from django.db import models
from django.contrib.auth.models import User

class Refeicao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    porcao = models.FloatField(help_text="Quantidade consumida em gramas")

    carboidratos = models.FloatField(help_text="Carboidratos por 100g")
    proteinas = models.FloatField(help_text="Proteínas por 100g")
    gorduras = models.FloatField(help_text="Gorduras por 100g")

    data = models.DateField(auto_now_add=True)

    def calorias(self):
        fator = self.porcao / 100
        return (
            (self.carboidratos * 4 +
             self.proteinas * 4 +
             self.gorduras * 9)
            * fator
        )



