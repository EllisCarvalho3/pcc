from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peso = models.FloatField()
    altura = models.FloatField()
    idade = models.IntegerField()
    atividade = models.CharField(max_length=20)
    objetivo = models.CharField(max_length=20)
    meta_calorica = models.FloatField()

    def __str__(self):
        return self.user.username


class Refeicao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()
    data = models.DateField(auto_now_add=True)

    def calorias(self):
        return self.carboidratos * 4 + self.proteinas * 4 + self.gorduras * 9

    def __str__(self):
        return self.nome
