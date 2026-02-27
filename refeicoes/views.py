from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Refeicao
from .forms import RefeicaoForm
from alimentacao.services import buscar_alimento_api

@login_required
def criar_refeicao(request):
    if request.method == "POST":
        form = RefeicaoForm(request.POST)
        if form.is_valid():
            refeicao = form.save(commit=False)
            refeicao.user = request.user
            dados_api = buscar_alimento_api(refeicao.nome)

        if dados_api:
            refeicao.carboidratos = dados_api["carboidratos"]
            refeicao.proteinas = dados_api["proteinas"]
            refeicao.gorduras = dados_api["gorduras"]
            refeicao.calorias = dados_api["calorias"]
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
