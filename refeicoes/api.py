import requests
from django.conf import settings


def buscar_alimento_api(nome):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "query": nome,
        "api_key": settings.USDA_API_KEY,
        "pageSize": 10
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

        for alimento in alimentos:

            nutrientes = alimento.get("foodNutrients", [])

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