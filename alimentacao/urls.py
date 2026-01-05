from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('historico/', views.historico, name='historico'),
      path('cadastro/', views.cadastrar, name='cadastro'),
      

]
