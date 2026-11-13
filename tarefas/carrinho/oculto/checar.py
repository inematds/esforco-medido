#!/usr/bin/env python3
"""Checador oculto do carrinho: 6 regras de REGRAS.md, 2 casos cada (12). Uso: checar.py <pasta>. Imprime 'NOTA n/12'."""
import importlib, sys, os

pasta = os.path.abspath(sys.argv[1])
sys.path.insert(0, pasta)
try:
    total = importlib.import_module("carrinho").total
except Exception as e:
    print(f"NOTA 0/12 (não importa: {e})"); sys.exit(1)

CASOS = [
    # regra 2: cupom não desconta o frete
    ("cupom_sem_frete", [(100.0, 1)], "DEZ", 115.0),
    ("cupom_sem_frete2", [(40.0, 2)], "VINTE", 89.0),
    # regra 3: frete grátis olha o subtotal JÁ com cupom
    ("gratis_pos_cupom", [(210.0, 1)], "DEZ", 214.0),          # 189 + 25
    ("gratis_pos_cupom2", [(400.0, 1)], "METADE", 200.0),      # 200 → grátis (>=)
    # regra 3: 200 ou mais
    ("gratis_igual", [(100.0, 2)], None, 200.0),
    ("gratis_maior", [(150.0, 2)], None, 300.0),
    # regra 1: quantidade 0 ou negativa não conta
    ("qtd_zero", [(50.0, 2), (999.0, 0)], None, 125.0),
    ("qtd_negativa", [(300.0, -1), (10.0, 1)], None, 35.0),
    # regra 5: arredonda só no fim, meio centavo para cima
    ("arred_fim", [(0.335, 3)], None, 26.01),                  # 1,005 + 25 = 26,005 → 26,01
    ("arred_meio", [(10.005, 1)], None, 35.01),
    # regra 6: cupom desconhecido é ignorado
    ("cupom_desconhecido", [(50.0, 1)], "NATAL", 75.0),
    ("cupom_minusculo", [(100.0, 1)], "dez", 115.0),
]
ok = 0
for nome, itens, cupom, esp in CASOS:
    try:
        r = total(list(itens), cupom) if cupom is not None else total(list(itens))
        if abs(float(r) - esp) < 1e-9:
            ok += 1
        else:
            print(f"  falhou {nome}: {r!r} != {esp!r}")
    except Exception as e:
        print(f"  falhou {nome}: {type(e).__name__} {e}")
print(f"NOTA {ok}/{len(CASOS)}")
sys.exit(0 if ok == len(CASOS) else 1)
