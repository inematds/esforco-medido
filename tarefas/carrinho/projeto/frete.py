FRETE = 25.0
MINIMO_GRATIS = 200.0


def frete(valor):
    if valor > MINIMO_GRATIS:
        return 0.0
    return FRETE
