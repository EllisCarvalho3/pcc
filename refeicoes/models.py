from django.db import models
from django.contrib.auth.models import User


class Refeicao(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=200)

    quantidade = models.FloatField(help_text="Quantidade consumida em gramas")

    # valores por 100g
    carboidratos = models.FloatField(help_text="Carboidratos por 100g")
    proteinas = models.FloatField(help_text="Proteínas por 100g")
    gorduras = models.FloatField(help_text="Gorduras por 100g")

    data = models.DateField(auto_now_add=True)

    def calorias(self):

        fator = self.quantidade / 100

        carbo = self.carboidratos * fator
        prot = self.proteinas * fator
        gord = self.gorduras * fator

        return (carbo * 4) + (prot * 4) + (gord * 9)

    def __str__(self):
        return f"{self.nome} ({self.quantidade}g)"