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
    total_prot = 0
    total_gord = 0

    for r in refeicoes:

        carbo = r.carboidratos or 0
        prot = r.proteinas or 0
        gord = r.gorduras or 0
        qtd = r.quantidade or 0

        fator = qtd / 100

        carbo_total = carbo * fator
        prot_total = prot * fator
        gord_total = gord * fator

        total_carbo += carbo_total
        total_prot += prot_total
        total_gord += gord_total

        total_calorias += (carbo_total * 4) + (prot_total * 4) + (gord_total * 9)

    perfil = getattr(request.user, "perfil", None)

    percentual = 0
    feedback = []

    # FEEDBACK CALÓRICO
    if perfil and perfil.meta_calorica:

        percentual = (total_calorias / perfil.meta_calorica) * 100

        if percentual < 80:
            feedback.append(" Você está consumindo menos calorias que sua meta diária.")
        elif percentual <= 110:
            feedback.append(" Seu consumo calórico está dentro da meta.")
        else:
            feedback.append(" Você ultrapassou sua meta calórica diária.")

    # FEEDBACK DE MACRONUTRIENTES
    if total_calorias > 0:

        perc_carbo = (total_carbo * 4) / total_calorias * 100
        perc_prot = (total_prot * 4) / total_calorias * 100
        perc_gord = (total_gord * 9) / total_calorias * 100

        # referência nutricional média
        if perc_prot < 10:
            feedback.append(" Consumo de proteína baixo.")
        elif perc_prot > 35:
            feedback.append(" Consumo de proteína alto.")

        if perc_carbo < 45:
            feedback.append(" Consumo de carboidratos baixo.")
        elif perc_carbo > 65:
            feedback.append(" Consumo de carboidratos alto.")

        if perc_gord < 20:
            feedback.append(" Consumo de gorduras baixo.")
        elif perc_gord > 35:
            feedback.append(" Consumo de gorduras alto.")

        if not feedback:
            feedback.append(" Distribuição de macronutrientes equilibrada.")

    contexto = {
        "refeicoes": refeicoes,
        "total": round(total_calorias, 2),
        "perfil": perfil,
        "percentual": percentual,
        "feedback": feedback,
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
