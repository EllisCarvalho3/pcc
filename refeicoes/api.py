# refeicoes/api.py

import requests
from django.conf import settings
TRADUCOES = {
    "arroz": "rice",
    "arroz branco": "white rice",
    "arroz branco cozido": "cooked white rice",

    "feijao": "beans",
    "feijão": "beans",
    "feijao cozido": "cooked beans",
    "feijão cozido": "cooked beans",

    "banana": "banana",
    "maca": "apple",
    "maçã": "apple",

    "frango": "chicken",
    "ovo": "egg",
    "leite": "milk",
    "pao": "bread",
    "pão": "bread"
}


def buscar_alimento_api(nome):
    
    nome_busca = TRADUCOES.get(
    nome.lower().strip(),
    nome
)

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    print(f"Busca: {nome} -> {nome_busca}")

    params = {
        "query": nome_busca,
        "api_key": settings.USDA_API_KEY,
        "pageSize": 20
    }

    try:

        resposta = requests.get(
            url,
            params=params,
            timeout=15
        )

        if resposta.status_code != 200:
            print("Erro USDA:", resposta.status_code)
            return None

        dados = resposta.json()

        alimentos = dados.get("foods", [])

        if not alimentos:
            return None

        alimentos_ordenados = sorted(
            alimentos,
            key=lambda a: (
                a.get("dataType") != "Foundation",
                a.get("dataType") != "SR Legacy",
                a.get("dataType") != "Survey (FNDDS)"
            )
        )

        for alimento in alimentos_ordenados:

            descricao = alimento.get(
                "description",
                ""
            ).lower()

            busca = nome.lower()

            if busca not in descricao:
                continue

            nutrientes = alimento.get(
                "foodNutrients",
                []
            )

            carbo = None
            prot = None
            gord = None

            for nutriente in nutrientes:

                nome_nutriente = nutriente.get(
                    "nutrientName",
                    ""
                )

                if nome_nutriente == "Carbohydrate, by difference":
                    carbo = nutriente.get("value")

                elif nome_nutriente == "Protein":
                    prot = nutriente.get("value")

                elif nome_nutriente == "Total lipid (fat)":
                    gord = nutriente.get("value")

            if (
                carbo is not None and
                prot is not None and
                gord is not None
            ):
                return {
                    "carboidratos": float(carbo),
                    "proteinas": float(prot),
                    "gorduras": float(gord)
                }

    except Exception as erro:
        print("Erro USDA:", erro)

    return None