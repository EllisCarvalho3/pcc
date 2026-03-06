from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from collections import defaultdict

from perfil.models import Perfil
from refeicoes.models import Refeicao
from alimentacao.services import gerar_feedback

@login_required
def dashboard(request):

    refeicoes = Refeicao.objects.filter(user=request.user)

    total_calorias = 0
    total_carbo = 0
    total_proteina = 0
    total_gordura = 0

    for r in refeicoes:

        total_calorias += r.calorias()

        total_carbo += r.carboidratos or 0
        total_proteina += r.proteinas or 0
        total_gordura += r.gorduras or 0

    context = {
        "refeicoes": refeicoes,
        "total_calorias": round(total_calorias, 2),
        "total_carbo": round(total_carbo, 2),
        "total_proteina": round(total_proteina, 2),
        "total_gordura": round(total_gordura, 2),
    }

    return render(request, "alimentacao/dashboard.html", context)

@login_required
def historico(request):
    refeicoes = Refeicao.objects.filter(user=request.user).order_by("-data")

    dias = defaultdict(list)

    for r in refeicoes:
        dias[r.data].append(r)

    historico_formatado = []

    for data, itens in dias.items():
        total = sum(r.calorias() for r in itens)
        historico_formatado.append({
            "data": data,
            "total": total,
            "itens": itens
        })

    return render(request, "historico.html", {
        "dias": historico_formatado
    })


def cadastrar(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "cadastro.html", {"form": form})


def home(request):
    return render(request, "home.html")
