import requests

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

def buscar_alimento_api(nome):
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": nome,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("products"):
            produto = data["products"][0]
            nutr = produto.get("nutriments", {})

            return {
                "nome": produto.get("product_name", nome),
                "calorias": nutr.get("energy-kcal_100g", 0),
                "proteinas": nutr.get("proteins_100g", 0),
                "carboidratos": nutr.get("carbohydrates_100g", 0),
                "gorduras": nutr.get("fat_100g", 0),
            }

    except Exception:
        return None

    return None