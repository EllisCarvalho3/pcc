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

    headers = {
        "User-Agent": "nutricao-estudante-app/1.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        print("API STATUS:", response.status_code)

        if response.status_code != 200:
            print("Erro HTTP:", response.status_code)
            return None

        data = response.json()
        
        print("API STATUS:", response.status_code)

        if data.get("products"):
            for produto in data["products"]:
                nutr = produto.get("nutriments", {})

                carbo = nutr.get("carbohydrates_100g")
                prot = nutr.get("proteins_100g")
                gord = nutr.get("fat_100g")

                if carbo and prot and gord:
                    return {
                        "carboidratos": float(carbo),
                        "proteinas": float(prot),
                        "gorduras": float(gord),
                    }

    except Exception as e:
        print("Erro API:", e)

    return None