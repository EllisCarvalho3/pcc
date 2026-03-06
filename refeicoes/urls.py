from django.urls import path
from . import views

urlpatterns = [
    path("nova/", views.criar_refeicao, name="criar_refeicao"),
    path("editar/<int:id>/", views.editar_refeicao, name="editar_refeicao"),
    path("excluir/<int:id>/", views.excluir_refeicao, name="excluir_refeicao"),
    path("buscar-alimento/", views.buscar_alimento_ajax, name="buscar_alimento_ajax"),
    path("autocomplete/", views.autocomplete_alimento, name="autocomplete"),
]
