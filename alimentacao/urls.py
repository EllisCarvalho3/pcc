from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("historico/", views.historico, name="historico"),
    path("cadastro/", views.cadastrar, name="cadastro"),

    # rotas do app refeições
    path("refeicoes/", include("refeicoes.urls")),
]
