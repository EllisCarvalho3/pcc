from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from perfil.models import Perfil
from refeicoes.models import Refeicao


class DashboardContextTests(TestCase):
    def test_dashboard_uses_user_meals_for_macros(self):
        user = User.objects.create_user(username='ana', password='123456')
        Perfil.objects.create(user=user, meta_calorica=2000)

        Refeicao.objects.create(
            user=user,
            nome='Café',
            quantidade=200,
            carboidratos=40,
            proteinas=20,
            gorduras=10,
        )
        Refeicao.objects.create(
            user=user,
            nome='Almoço',
            quantidade=300,
            carboidratos=60,
            proteinas=25,
            gorduras=15,
        )

        other_user = User.objects.create_user(username='joao', password='123456')
        Refeicao.objects.create(
            user=other_user,
            nome='Outro',
            quantidade=100,
            carboidratos=10,
            proteinas=10,
            gorduras=10,
        )

        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['total'], 805)
        self.assertEqual(response.context['total_carboidratos'], 100)
        self.assertEqual(response.context['total_proteinas'], 45)
        self.assertEqual(response.context['total_gorduras'], 25)
        self.assertEqual(response.context['meta_restante'], 1195)
