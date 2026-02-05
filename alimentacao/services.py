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