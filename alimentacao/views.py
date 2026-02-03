from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.db.models import Sum
from perfil.models import Perfil
from refeicoes.models import Refeicao
from refeicoes.forms import RefeicaoForm 

@login_required
def dashboard(request):
    perfil = Perfil.objects.filter(user=request.user).first()
    refeicoes = Refeicao.objects.filter(user=request.user)

    if request.method == "POST":
        form = RefeicaoForm(request.POST)
        if form.is_valid():
            refeicao = form.save(commit=False)
            refeicao.user = request.user
            refeicao.save()
            return redirect("dashboard")
    else:
        form = RefeicaoForm()

    total_calorias = sum(r.calorias() for r in refeicoes)

    percentual = 0
    if perfil and perfil.meta_calorica > 0:
        percentual = min((total_calorias / perfil.meta_calorica) * 100, 100)

    feedback = gerar_feedback(
        total_calorias,
        perfil.meta_calorica if perfil else 0,
        sum(r.carboidratos for r in refeicoes),
        sum(r.proteinas for r in refeicoes),
        sum(r.gorduras for r in refeicoes),
    )

    return render(request, "dashboard.html", {
        "perfil": perfil,
        "refeicoes": refeicoes,
        "total": total_calorias,
        "percentual": percentual,
        "feedback": feedback,
        "form": form
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

