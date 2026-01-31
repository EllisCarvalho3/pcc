from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    idade = models.IntegerField(null=True, blank=True)
    meta_calorica = models.FloatField(null=True, blank=True)
    atividade = models.CharField(
        max_length=20,
        choices=[
            ('sedentario', 'Sedentário'),
            ('leve', 'Leve'),
            ('moderado', 'Moderado'),
            ('intenso', 'Intenso'),
        ],
        default='sedentario'
    )

    objetivo = models.CharField(
        max_length=20,
        choices=[
            ('perder', 'Perder peso'),
            ('manter', 'Manter peso'),
            ('ganhar', 'Ganhar peso'),
        ],
        default='manter'
    )

    meta_calorica = models.FloatField(default=0)

    def __str__(self):
        return f"Perfil de {self.user.username}"
