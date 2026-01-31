from django.urls import path
from . import views

urlpatterns = [
    path("nova/", views.criar_refeicao, name="criar_refeicao"),
    path("editar/<int:id>/", views.editar_refeicao, name="editar_refeicao"),
    path("excluir/<int:id>/", views.excluir_refeicao, name="excluir_refeicao"),
]
