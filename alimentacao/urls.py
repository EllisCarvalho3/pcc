from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historico/', views.historico, name='historico'),
      path('cadastro/', views.cadastrar, name='cadastro'),
      path("refeicoes/", include("refeicoes.urls")),
      

]
