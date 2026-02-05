def calcular_meta(peso, altura, idade, atividade, objetivo):
    # Proteção contra dados incompletos
    if not all([peso, altura, idade, atividade, objetivo]):
        return None

    bmr = (10 * peso) + (6.25 * altura) - (5 * idade) + 5

    fatores = {
        'sedentario': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'intenso': 1.725
    }

    tdee = bmr * fatores.get(atividade, 1)

    if objetivo == 'perder':
        return tdee - 300
    elif objetivo == 'ganhar':
        return tdee + 300
    else:
        return tdee
