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

    total = sum(r.calorias() for r in refeicoes)

    perfil = getattr(request.user, "perfil", None)

    percentual = 0
    feedback = []

    if perfil and perfil.meta_calorica:

        percentual = (total / perfil.meta_calorica) * 100

        if percentual < 80:
            feedback.append("Você consumiu menos calorias que sua meta.")
        elif percentual <= 110:
            feedback.append("Você está dentro da meta diária.")
        else:
            feedback.append("Você ultrapassou sua meta calórica.")

    contexto = {
        "refeicoes": refeicoes,
        "total": total,
        "perfil": perfil,
        "percentual": percentual,
        "feedback": feedback
    }

    return render(request, "dashboard.html", contexto)

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
