from django.db import models
from django.contrib.auth.models import User

class Refeicao(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=200)

    quantidade = models.FloatField()

    carboidratos = models.FloatField(default=0)
    proteinas = models.FloatField(default=0)
    gorduras = models.FloatField(default=0)

    data = models.DateTimeField(auto_now_add=True)

    def calorias(self):

        fator = self.quantidade / 100

        carbo = (self.carboidratos or 0) * fator
        prot = (self.proteinas or 0) * fator
        gord = (self.gorduras or 0) * fator

        calorias = (carbo * 4) + (prot * 4) + (gord * 9)

        return round(calorias, 2)