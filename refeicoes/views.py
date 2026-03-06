from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Refeicao
from .forms import RefeicaoForm
from alimentacao.services import buscar_alimento_api
from django.contrib import messages
from django.http import JsonResponse
from alimentacao.services import buscar_alimento_api
from django.http import JsonResponse
from alimentacao.services import buscar_alimento_api
from .api import buscar_alimento_api
import requests




class Refeicao(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=200)

    quantidade = models.FloatField(help_text="Quantidade consumida em gramas")

    # valores por 100g
    carboidratos = models.FloatField(help_text="Carboidratos por 100g")
    proteinas = models.FloatField(help_text="Proteínas por 100g")
    gorduras = models.FloatField(help_text="Gorduras por 100g")

    data = models.DateField(auto_now_add=True)

    def calorias(self):

        fator = self.quantidade / 100

        carbo = self.carboidratos * fator
        prot = self.proteinas * fator
        gord = self.gorduras * fator

        return (carbo * 4) + (prot * 4) + (gord * 9)

    def __str__(self):
        return f"{self.nome} ({self.quantidade}g)"
    
@login_required
def editar_refeicao(request, id):
    refeicao = get_object_or_404(
        Refeicao,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = RefeicaoForm(request.POST, instance=refeicao)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = RefeicaoForm(instance=refeicao)

    return render(request, "refeicoes/form.html", {
        "form": form,
        "editar": True
    })

@login_required
def excluir_refeicao(request, id):
    refeicao = get_object_or_404(
        Refeicao,
        id=id,
        user=request.user
    )

    refeicao.delete()
    return redirect("dashboard")


    
@login_required
def autocomplete_alimento(request):

    termo = request.GET.get("q")

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": termo,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }

    response = requests.get(url, params=params)

    data = response.json()

    sugestoes = []

    for produto in data.get("products", []):

        nome = produto.get("product_name")

        if nome:
            sugestoes.append(nome)

    return JsonResponse(sugestoes, safe=False)