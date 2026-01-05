from django.shortcuts import render, redirect
from .models import Refeicao, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Perfil

from django.db.models import Sum

def historico(request):
    dias = (
        Refeicao.objects
        .filter(user=request.user)
        .values('data')
        .annotate(
            total=Sum('carboidratos')*4 +
                  Sum('proteinas')*4 +
                  Sum('gorduras')*9
        )
    )
    return render(request, "historico.html", {"dias": dias})


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
        mensagens.append("⚠️ Déficit calórico alto. Considere um lanche saudável.")
    elif pct <= 100:
        mensagens.append("✅ Você está dentro da meta calórica.")
    else:
        mensagens.append("⚠️ Excesso calórico. Prefira refeições leves.")

    if prot < 50:
        mensagens.append("💪 Proteína baixa para o dia.")
    if gord > 70:
        mensagens.append("🧈 Gordura elevada.")
    if carbo < 130:
        mensagens.append("🍞 Carboidratos abaixo do recomendado.")

    return mensagens


def index(request):
    perfil = Perfil.objects.first()

    if request.method == "POST":
        # Formulário de refeição
        if "nome" in request.POST:
            Refeicao.objects.create(
                nome=request.POST["nome"],
                carboidratos=float(request.POST["carbo"]),
                proteinas=float(request.POST["proteina"]),
                gorduras=float(request.POST["gordura"]),
            )
            return redirect("index")

        # Formulário de perfil
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
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def perfil(request):
    return render(request, "perfil.html")

