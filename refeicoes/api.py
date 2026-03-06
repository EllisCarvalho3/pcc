import requests

def buscar_alimento_api(nome):

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": nome,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    resposta = requests.get(url, params=params)

    if resposta.status_code != 200:
        return None

    dados = resposta.json()

    if not dados["products"]:
        return None

    produto = dados["products"][0]
    nutr = produto.get("nutriments", {})

    return {
        "carboidratos": nutr.get("carbohydrates_100g", 0),
        "proteinas": nutr.get("proteins_100g", 0),
        "gorduras": nutr.get("fat_100g", 0)
    }