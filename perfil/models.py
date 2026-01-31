from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peso = models.FloatField()
    altura = models.FloatField()
    idade = models.IntegerField()
    meta_calorica = models.FloatField()

    def __str__(self):
        return self.user.username


