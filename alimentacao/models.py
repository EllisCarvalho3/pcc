from django.db import models

class Perfil(models.Model):
    peso = models.FloatField()
    altura = models.FloatField()
    idade = models.IntegerField()
    atividade = models.CharField(max_length=20)
    objetivo = models.CharField(max_length=20)
    meta_calorica = models.FloatField()

class Refeicao(models.Model):
    nome = models.CharField(max_length=100)
    carboidratos = models.FloatField()
    proteinas = models.FloatField()
    gorduras = models.FloatField()
    data = models.DateField(auto_now_add=True)

    def calorias(self):
        return (
            self.carboidratos * 4 +
            self.proteinas * 4 +
            self.gorduras * 9
        )

    def __str__(self):
        return self.nome


        

# Create your models here.
