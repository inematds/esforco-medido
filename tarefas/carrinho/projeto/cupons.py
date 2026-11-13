CUPONS = {"DEZ": 10, "VINTE": 20, "METADE": 50}


def desconto(cupom):
    """Porcentagem do cupom (0 se não existe)."""
    return CUPONS[cupom.upper()]
