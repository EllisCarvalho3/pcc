from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Refeicao
from .forms import RefeicaoForm
from .api import buscar_alimento_api

@login_required
def criar_refeicao(request):

    if request.method == "POST":

        form = RefeicaoForm(request.POST)

        if form.is_valid():

            refeicao = form.save(commit=False)
            refeicao.user = request.user

            # busca alimento na API
            dados_api = buscar_alimento_api(refeicao.nome)

            if dados_api:

                quantidade = refeicao.quantidade

                refeicao.carboidratos = (dados_api["carboidratos"] * quantidade) / 100
                refeicao.proteinas = (dados_api["proteinas"] * quantidade) / 100
                refeicao.gorduras = (dados_api["gorduras"] * quantidade) / 100

                messages.success(request, "Alimento encontrado na base nutricional.")

            else:
                messages.warning(request, "Alimento não encontrado. Preencha manualmente.")

            refeicao.save()

            return redirect("dashboard")

    else:
        form = RefeicaoForm()

    return render(request, "refeicoes/form.html", {"form": form})
    
@login_required
def editar_refeicao(request, id):

    refeicao = get_object_or_404(Refeicao, id=id, user=request.user)

    if request.method == "POST":

        form = RefeicaoForm(request.POST, instance=refeicao)

        if form.is_valid():
            form.save()
            messages.success(request, "Refeição atualizada.")
            return redirect("dashboard")

    else:
        form = RefeicaoForm(instance=refeicao)

    return render(request, "refeicoes/form.html", {"form": form})

@login_required
def excluir_refeicao(request, id):

    refeicao = get_object_or_404(Refeicao, id=id, user=request.user)

    refeicao.delete()

    messages.success(request, "Refeição removida.")

    return redirect("dashboard")


    
@login_required
def autocomplete_alimento(request):

    termo = request.GET.get("q")

    if not termo:
        return JsonResponse({"resultados": []})

    dados = buscar_alimento_api(termo)

    if not dados:
        return JsonResponse({"resultados": []})

    return JsonResponse(dados)