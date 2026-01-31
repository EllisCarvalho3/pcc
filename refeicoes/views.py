from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Refeicao
from .forms import RefeicaoForm

@login_required
def criar_refeicao(request):
    if request.method == "POST":
        form = RefeicaoForm(request.POST)
        if form.is_valid():
            refeicao = form.save(commit=False)
            refeicao.user = request.user
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
            return redirect("dashboard")
    else:
        form = RefeicaoForm(instance=refeicao)

    return render(request, "refeicoes/form.html", {"form": form})

@login_required
def excluir_refeicao(request, id):
    refeicao = get_object_or_404(Refeicao, id=id, user=request.user)
    refeicao.delete()
    return redirect("dashboard")
