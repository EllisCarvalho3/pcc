from collections import defaultdict

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from alimentacao.services import gerar_feedback
from perfil.models import Perfil
from refeicoes.models import Refeicao

from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):

    hoje = timezone.localdate()

    inicio = timezone.make_aware(
    timezone.datetime.combine(
        hoje,
        timezone.datetime.min.time()
    )
)

    fim = inicio + timedelta(days=1)

    refeicoes = Refeicao.objects.filter(
    user=request.user,
    data__gte=inicio,
    data__lt=fim
)

    total_calorias = 0
    total_carbo = 0
    total_prot = 0
    total_gord = 0

    for r in refeicoes:

        fator = r.quantidade / 100

        carbo = (r.carboidratos or 0) * fator
        prot = (r.proteinas or 0) * fator
        gord = (r.gorduras or 0) * fator

        total_carbo += carbo
        total_prot += prot
        total_gord += gord

        total_calorias += (
            (carbo * 4) +
            (prot * 4) +
            (gord * 9)
        )

    perfil = getattr(request.user, "perfil", None)

    percentual = 0
    feedback = []

    # FEEDBACK CALÓRICO
    if perfil and perfil.meta_calorica:

        percentual = (total_calorias / perfil.meta_calorica) * 100

        if percentual < 80:
            feedback.append(
                "Você está consumindo menos calorias que sua meta diária."
            )

        elif percentual <= 110:
            feedback.append(
                "Seu consumo calórico está dentro da meta."
            )

        else:
            feedback.append(
                "Você ultrapassou sua meta calórica diária."
            )

    # FEEDBACK DE MACRONUTRIENTES
    if total_calorias > 0:

        perc_carbo = (total_carbo * 4) / total_calorias * 100
        perc_prot = (total_prot * 4) / total_calorias * 100
        perc_gord = (total_gord * 9) / total_calorias * 100

        if perc_prot < 10:
            feedback.append("Consumo de proteína baixo.")
        elif perc_prot > 35:
            feedback.append("Consumo de proteína alto.")

        if perc_carbo < 45:
            feedback.append("Consumo de carboidratos baixo.")
        elif perc_carbo > 65:
            feedback.append("Consumo de carboidratos alto.")

        if perc_gord < 20:
            feedback.append("Consumo de gorduras baixo.")
        elif perc_gord > 35:
            feedback.append("Consumo de gorduras alto.")

        if (
            10 <= perc_prot <= 35 and
            45 <= perc_carbo <= 65 and
            20 <= perc_gord <= 35
        ):
            feedback.append(
                "Distribuição de macronutrientes equilibrada."
            )

    meta_restante = 0

    if perfil and perfil.meta_calorica:
        meta_restante = round(
            max(perfil.meta_calorica - total_calorias, 0),
            2
        )

    contexto = {
        "refeicoes": refeicoes,
        "total": round(total_calorias, 2),
        "total_carboidratos": round(total_carbo, 2),
        "total_proteinas": round(total_prot, 2),
        "total_gorduras": round(total_gord, 2),
        "meta_restante": meta_restante,
        "perfil": perfil,
        "percentual": percentual,
        "feedback": feedback,
    }

    return render(
        request,
        "dashboard.html",
        contexto
    )

@login_required
def historico(request):
    refeicoes = Refeicao.objects.filter(user=request.user).order_by("-data")

    dias = defaultdict(list)

    for r in refeicoes:
        dias[r.data.date()].append(r)

    historico_formatado = []

    for data in sorted(dias.keys(), reverse=True):

        itens = dias[data]
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
    
    total_refeicoes = Refeicao.objects.count()

    total_usuarios = User.objects.count()

    usuarios_com_perfil = Perfil.objects.exclude(
        meta_calorica__isnull=True
    ).count()

    refeicoes_com_macros = Refeicao.objects.exclude(
        carboidratos=0,
        proteinas=0,
        gorduras=0
    ).count()

    if total_refeicoes > 0:
        precisao = round(
            (refeicoes_com_macros / total_refeicoes) * 100
        )
    else:
        precisao = 0

    contexto = {
        "total_refeicoes": total_refeicoes,
        "precisao": precisao,
        "calculos": refeicoes_com_macros,
        "usuarios_meta": usuarios_com_perfil,
    }

    return render(
        request,
        "home.html",
        contexto
    )
