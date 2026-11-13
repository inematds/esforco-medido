#!/usr/bin/env python3
"""Checador oculto do calendário: 20 casos, comparados com uma implementação de referência. Uso: checar.py <pasta>."""
import datetime as dt, importlib, os, sys

D = dt.date
UM = dt.timedelta(days=1)


# ---------- referência ----------
def r_pascoa(a):
    g = a % 19; c = a // 100; h = (c - c // 4 - (8 * c + 13) // 25 + 19 * g + 15) % 30
    i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
    j = (a + a // 4 + i + 2 - c + c // 4) % 7
    l = i - j; m = 3 + (l + 40) // 44; d = l + 28 - 31 * (m // 4)
    return D(a, m, d)


def r_feriados(a):
    p = r_pascoa(a)
    fixos = {D(a, m, d) for m, d in [(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (11, 20), (12, 25)]}
    return fixos | {p - 48 * UM, p - 47 * UM, p - 2 * UM, p + 60 * UM}


def r_util(x):
    return x.weekday() < 5 and x not in r_feriados(x.year)


def r_somar(x, n):
    if n == 0:
        while not r_util(x):
            x += UM
        return x
    passo = UM if n > 0 else -UM
    k = abs(n)
    while k:
        x += passo
        if r_util(x):
            k -= 1
    return x


def r_entre(a, b):
    if b < a:
        return -r_entre(b, a)
    n, x = 0, a
    while x <= b:
        n += r_util(x); x += UM
    return n


# ---------- casos ----------
pasta = os.path.abspath(sys.argv[1]); sys.path.insert(0, pasta)
try:
    c = importlib.import_module("calendario")
except Exception as e:
    print(f"NOTA 0/20 (não importa: {e})"); sys.exit(1)

CASOS = [
    ("pascoa_1900_2099", lambda: all(c.pascoa(a) == r_pascoa(a) for a in range(1900, 2100))),
    ("pascoa_anomalias", lambda: [c.pascoa(a) for a in (1954, 1981, 2049, 2076)] == [r_pascoa(a) for a in (1954, 1981, 2049, 2076)]),
    ("feriados_2026", lambda: set(c.feriados(2026)) == r_feriados(2026)),
    ("feriados_2027", lambda: set(c.feriados(2027)) == r_feriados(2027)),
    ("feriados_tipo_set", lambda: isinstance(c.feriados(2030), (set, frozenset)) and len(c.feriados(2030)) == 13),
    ("feriados_2000_2050", lambda: all(set(c.feriados(a)) == r_feriados(a) for a in range(2000, 2051))),
    ("util_carnaval_2027", lambda: [c.eh_dia_util(D(2027, 2, d)) for d in (5, 8, 9, 10)] == [True, False, False, True]),
    ("util_corpus_2026", lambda: c.eh_dia_util(D(2026, 6, 4)) is False and c.eh_dia_util(D(2026, 6, 5)) is True),
    ("util_consciencia_negra", lambda: c.eh_dia_util(D(2026, 11, 20)) is False),
    ("util_sabado", lambda: c.eh_dia_util(D(2026, 11, 14)) is False),
    ("somar_sexta_mais_um", lambda: c.somar_dias_uteis(D(2026, 11, 13), 1) == D(2026, 11, 16)),
    ("somar_zero_util", lambda: c.somar_dias_uteis(D(2026, 11, 12), 0) == D(2026, 11, 12)),
    ("somar_zero_feriado", lambda: c.somar_dias_uteis(D(2026, 12, 25), 0) == D(2026, 12, 28)),
    ("somar_negativo_virada", lambda: c.somar_dias_uteis(D(2027, 1, 4), -2) == r_somar(D(2027, 1, 4), -2)),
    ("somar_pula_carnaval", lambda: c.somar_dias_uteis(D(2027, 2, 5), 1) == D(2027, 2, 10)),
    ("somar_250", lambda: c.somar_dias_uteis(D(2026, 1, 2), 250) == r_somar(D(2026, 1, 2), 250)),
    ("entre_ano_2026", lambda: c.dias_uteis_entre(D(2026, 1, 1), D(2026, 12, 31)) == r_entre(D(2026, 1, 1), D(2026, 12, 31))),
    ("entre_mesmo_feriado", lambda: c.dias_uteis_entre(D(2026, 12, 25), D(2026, 12, 25)) == 0),
    ("entre_invertido", lambda: c.dias_uteis_entre(D(2026, 3, 31), D(2026, 3, 1)) == -r_entre(D(2026, 3, 1), D(2026, 3, 31))),
    ("entre_varios_anos", lambda: c.dias_uteis_entre(D(2025, 6, 1), D(2028, 6, 1)) == r_entre(D(2025, 6, 1), D(2028, 6, 1))),
]
ok = 0
for nome, f in CASOS:
    try:
        if f():
            ok += 1
        else:
            print(f"  falhou {nome}")
    except Exception as e:
        print(f"  falhou {nome}: {type(e).__name__} {e}")
print(f"NOTA {ok}/{len(CASOS)}")
sys.exit(0 if ok == len(CASOS) else 1)
