import requests

def buscar_alimento_api(nome):

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": nome,
        "search_simple": 1,
        "action": "process",
        "json": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        produtos = data.get("products")

        if not produtos:
            return None

        nutr = produtos[0].get("nutriments", {})

        return {
            "carboidratos": nutr.get("carbohydrates_100g", 0),
            "proteinas": nutr.get("proteins_100g", 0),
            "gorduras": nutr.get("fat_100g", 0),
        }

    except Exception as e:
        print("Erro API:", e)
        return None