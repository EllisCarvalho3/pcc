from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.db.models import Sum
from perfil.models import Perfil
from refeicoes.models import Refeicao

@login_required
def dashboard(request):
    perfil = Perfil.objects.filter(user=request.user).first()
    refeicoes = Refeicao.objects.filter(user=request.user)

    total_calorias = sum(r.calorias() for r in refeicoes)

    percentual = 0
    if perfil and perfil.meta_calorica > 0:
        percentual = min((total_calorias / perfil.meta_calorica) * 100, 100)

    return render(request, "dashboard.html", {
        "perfil": perfil,
        "refeicoes": refeicoes,
        "total": total_calorias,
        "percentual": percentual
    })



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

