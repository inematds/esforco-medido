from cupons import desconto
from frete import frete


def total(itens, cupom=None):
    """itens: lista de (preco, quantidade). Devolve o total em reais (float com 2 casas). Ver REGRAS.md."""
    subtotal = 0.0
    for preco, qtd in itens:
        subtotal += round(preco * qtd, 2)
    f = frete(subtotal)
    valor = subtotal + f
    if cupom:
        valor = valor * (100 - desconto(cupom)) / 100
    return round(valor, 2)
