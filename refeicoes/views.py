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
import requests

@login_required
def buscar_alimento(request):
    nome = request.GET.get("nome")

    dados = buscar_alimento_api(nome)

    if dados:
        return JsonResponse({
            "encontrado": True,
            "carboidratos": dados["carboidratos"],
            "proteinas": dados["proteinas"],
            "gorduras": dados["gorduras"]
        })

    return JsonResponse({"encontrado": False})

@login_required
def criar_refeicao(request):
    if request.method == "POST":
        form = RefeicaoForm(request.POST)
        
        if form.is_valid():
            refeicao = form.save(commit=False)
            refeicao.user = request.user

            # 🔎 Busca alimento na API
            dados_api = buscar_alimento_api(refeicao.nome)

            print("Resultado API:", dados_api)
                
            if dados_api:
                porcao = refeicao.porcao

                refeicao.carboidratos = (dados_api["carboidratos"] * porcao) / 100
                refeicao.proteinas = (dados_api["proteinas"] * porcao) / 100
                refeicao.gorduras = (dados_api["gorduras"] * porcao) / 100

                messages.success(request, "Alimento encontrado automaticamente na base nutricional.")
            else:
                messages.warning(request, "Alimento não encontrado. Preencha os macronutrientes manualmente.")

            # 💾 salva no banco
            refeicao.save()

            return redirect("dashboard")

    else:
        form = RefeicaoForm()

    return render(request, "refeicoes/form.html", {"form": form})

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
def buscar_alimento_ajax(request):
    nome = request.GET.get("nome")

    if not nome:
        return JsonResponse({"erro": "Nome não informado"})

    dados = buscar_alimento_api(nome)

    if dados:
        return JsonResponse({
            "encontrado": True,
            "carboidratos": dados["carboidratos"],
            "proteinas": dados["proteinas"],
            "gorduras": dados["gorduras"]
        })
    else:
        return JsonResponse({"encontrado": False})
    
@login_required
def autocomplete_alimentos(request):

    termo = request.GET.get("term")

    if not termo:
        return JsonResponse([], safe=False)

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": termo,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        resultados = []

        for produto in data.get("products", []):
            nome = produto.get("product_name")

            if nome:
                resultados.append(nome)

        return JsonResponse(resultados, safe=False)

    except:
        return JsonResponse([], safe=False)    