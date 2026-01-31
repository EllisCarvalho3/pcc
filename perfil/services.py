from perfil.utils import calcular_meta

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