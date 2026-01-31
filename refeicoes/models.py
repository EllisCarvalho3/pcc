from django.db import models
from django.contrib.auth.models import User

class Refeicao(models.Model):
   user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="refeicoes")
   nome = models.CharField(max_length=100)
   carboidratos = models.FloatField()
   proteinas = models.FloatField()
   gorduras = models.FloatField()
   data = models.DateField(auto_now_add=True)
   
   def calorias(self):
        return (self.carboidratos * 4) + (self.proteinas * 4) + (self.gorduras * 9) 
   def __str__(self):
        return self.nome

