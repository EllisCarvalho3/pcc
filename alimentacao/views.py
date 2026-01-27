from django.shortcuts import render, redirect
from .models import Refeicao, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil
from django.contrib.auth.decorators import login_required
from collections import defaultdict


from django.db.models import Sum

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

def calcular_meta(peso, altura, idade, atividade, objetivo):
    bmr = (10 * peso) + (6.25 * altura) - (5 * idade) + 5

    fatores = {
        'sedentario': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'intenso': 1.725
    }

    tdee = bmr * fatores[atividade]

    if objetivo == 'perder':
        return tdee - 300
    elif objetivo == 'ganhar':
        return tdee + 300
    else:
        return tdee


def gerar_feedback(total, meta, carbo, prot, gord):
    pct = (total / meta) * 100 if meta else 0

    mensagens = []

    if pct < 70:
        mensagens.append("Déficit calórico alto. Considere um lanche saudável.")
    elif pct <= 100:
        mensagens.append("Você está dentro da meta calórica.")
    else:
        mensagens.append("Excesso calórico. Prefira refeições leves.")

    if prot < 50:
        mensagens.append("Proteína baixa para o dia.")
    if gord > 70:
        mensagens.append("Gordura elevada.")
    if carbo < 130:
        mensagens.append("Carboidratos abaixo do recomendado.")

    return mensagens


def index(request):
    perfil = Perfil.objects.first()

    if request.method == "POST":
        # formulário de refeição
        if "nome" in request.POST:
            Refeicao.objects.create(
                nome=request.POST["nome"],
                carboidratos=float(request.POST["carbo"]),
                proteinas=float(request.POST["proteina"]),
                gorduras=float(request.POST["gordura"]),
            )
            return redirect("home")

        # formulário de perfil
        else:
            meta = calcular_meta(
                float(request.POST["peso"]),
                float(request.POST["altura"]),
                int(request.POST["idade"]),
                request.POST["atividade"],
                request.POST["objetivo"]
            )

            Perfil.objects.all().delete()
            Perfil.objects.create(
                peso=request.POST["peso"],
                altura=request.POST["altura"],
                idade=request.POST["idade"],
                atividade=request.POST["atividade"],
                objetivo=request.POST["objetivo"],
                meta_calorica=meta
            )

            return redirect("index")

    refeicoes = Refeicao.objects.all()

    total_calorias = sum(r.calorias() for r in refeicoes)
    total_carbo = sum(r.carboidratos for r in refeicoes)
    total_prot = sum(r.proteinas for r in refeicoes)
    total_gord = sum(r.gorduras for r in refeicoes)

    feedback = gerar_feedback(
        total_calorias,
        perfil.meta_calorica if perfil else 0,
        total_carbo,
        total_prot,
        total_gord
    )

    return render(request, "index.html", {
        "refeicoes": refeicoes,
        "total": total_calorias,
        "perfil": perfil,
        "feedback": feedback,
        "carbo": total_carbo,
        "proteina": total_prot,
        "gordura": total_gord
    })



def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    perfil = Perfil.objects.filter(user=request.user).first()

    if request.method == "POST":
        Refeicao.objects.create(
            user=request.user,
            nome=request.POST["nome"],
            carboidratos=float(request.POST["carbo"]),
            proteinas=float(request.POST["proteina"]),
            gorduras=float(request.POST["gordura"]),
        )

    refeicoes = Refeicao.objects.filter(user=request.user)

    total_calorias = sum(r.calorias() for r in refeicoes)
    total_carbo = sum(r.carboidratos for r in refeicoes)
    total_prot = sum(r.proteinas for r in refeicoes)
    total_gord = sum(r.gorduras for r in refeicoes)

    feedback = gerar_feedback(
        total_calorias,
        perfil.meta_calorica if perfil else 0,
        total_carbo,
        total_prot,
        total_gord
    )
   
    percentual = 0
    if perfil and perfil.meta_calorica > 0:
        percentual = min((total_calorias / perfil.meta_calorica) * 100, 100)

    return render(request, "dashboard.html", {
        "total": total_calorias,
        "perfil": perfil,
        "feedback": feedback,
        "percentual": percentual,
        "total_carbo": total_carbo,
        "total_prot": total_prot,
        "total_gord": total_gord,
        "refeicoes": refeicoes,
    })

@login_required
def perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        perfil.peso = request.POST.get("peso")
        perfil.altura = request.POST.get("altura")
        perfil.idade = request.POST.get("idade")
        perfil.atividade = request.POST.get("atividade")
        perfil.objetivo = request.POST.get("objetivo")

        perfil.meta_calorica = calcular_meta(
            float(perfil.peso),
            float(perfil.altura),
            int(perfil.idade),
            perfil.atividade,
            perfil.objetivo
        )

        perfil.save()
        return redirect("perfil")

    return render(request, "perfil.html", {"perfil": perfil})

