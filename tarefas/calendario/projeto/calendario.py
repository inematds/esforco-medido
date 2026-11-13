"""Calendário de dias úteis do Brasil (escritório da Loja Exemplo).

Implemente as 5 funções. Datas são `datetime.date`.

Feriados nacionais:
- fixos: 01/01, 21/04, 01/05, 07/09, 12/10, 02/11, 15/11, 20/11, 25/12;
- móveis (contados a partir do domingo de Páscoa do ano): Carnaval (segunda e terça, 48 e 47 dias antes),
  Sexta-feira Santa (2 dias antes) e Corpus Christi (60 dias depois).
Dia útil = segunda a sexta que não é feriado.
"""
import datetime as dt


def pascoa(ano):
    """Domingo de Páscoa do ano (calendário gregoriano), para 1900 ≤ ano ≤ 2099."""
    raise NotImplementedError


def feriados(ano):
    """Conjunto (set) com todas as datas de feriado do ano."""
    raise NotImplementedError


def eh_dia_util(data):
    raise NotImplementedError


def somar_dias_uteis(data, n):
    """Data que fica n dias úteis depois de `data` (n negativo = antes; n = 0 devolve `data` se for útil, senão o
    próximo dia útil). A própria `data` não conta: sexta + 1 = segunda."""
    raise NotImplementedError


def dias_uteis_entre(inicio, fim):
    """Quantos dias úteis há de `inicio` até `fim`, contando os dois. Se fim < inicio, devolve o número negativo
    (dias_uteis_entre(b, a) == -dias_uteis_entre(a, b))."""
    raise NotImplementedError
