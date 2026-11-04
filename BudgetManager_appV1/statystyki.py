def policz_sume_wydatkow_kategori(wydatki, kategoria=None):
    suma_wydatkow = 0

    for wydatek in wydatki:
        if kategoria is None:
            suma_wydatkow += wydatek["kwota"]
        elif wydatek["kategoria"] == kategoria:
            suma_wydatkow += wydatek["kwota"]

    return suma_wydatkow