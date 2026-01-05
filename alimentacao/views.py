from django.shortcuts import render, redirect
from .models import Refeicao

def index(request):
    meta = None
    feedback = None

    if request.method == "POST":
        tipo = request.POST.get("tipo")

        # FORMULÁRIO DE REFEIÇÃO
        if tipo == "refeicao":
            Refeicao.objects.create(
                nome=request.POST["nome"],
                carboidratos=float(request.POST["carbo"]),
                proteinas=float(request.POST["proteina"]),
                gorduras=float(request.POST["gordura"]),
            )
            return redirect("index")

        # FORMULÁRIO DE META
        elif tipo == "meta":
            peso = float(request.POST["peso"])
            altura = float(request.POST["altura"])
            idade = int(request.POST["idade"])
            atividade = request.POST["atividade"]
            objetivo = request.POST["objetivo"]

            meta = calcular_meta(peso, altura, idade, atividade, objetivo)

    refeicoes = Refeicao.objects.all()
    total_calorias = sum(r.calorias() for r in refeicoes)

    if meta:
        feedback = gerar_feedback(total_calorias, meta)

    return render(request, "index.html", {
        "refeicoes": refeicoes,
        "total": total_calorias,
        "meta": meta,
        "feedback": feedback
    })


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
    return tdee


def gerar_feedback(consumido, meta):
    porcentagem = (consumido / meta) * 100

    if porcentagem < 70:
        return "Risco de déficit calórico alto. Adicione um lanche saudável."
    elif porcentagem <= 100:
        return "Você está dentro da meta. Bom equilíbrio!"
    else:
        return "Excesso de calorias. Tente refeições mais leves no jantar."
