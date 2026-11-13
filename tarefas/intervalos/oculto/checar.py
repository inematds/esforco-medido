#!/usr/bin/env python3
"""Checador oculto (o modelo não vê): 16 casos. Uso: checar.py <pasta-do-projeto>. Imprime 'NOTA n/16' e sai 0 se 16/16."""
import importlib.util, sys, os

pasta = sys.argv[1]
spec = importlib.util.spec_from_file_location("intervalos", os.path.join(pasta, "intervalos.py"))
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
except Exception as e:
    print(f"NOTA 0/16 (não importa: {e})"); sys.exit(1)
j = mod.juntar

CASOS = [
    ("sobrepoe", ["09:00-10:30", "10:00-11:00"], ["09:00-11:00"]),
    ("encosta", ["09:00-10:00", "10:00-11:00"], ["09:00-11:00"]),
    ("ordem", ["14:00-15:00", "09:00-10:00"], ["09:00-10:00", "14:00-15:00"]),
    ("vazio", [], []),
    ("contido", ["08:00-12:00", "09:00-10:00"], ["08:00-12:00"]),
    ("tres", ["13:00-14:00", "08:00-09:30", "09:15-10:00", "13:30-15:00"], ["08:00-10:00", "13:00-15:00"]),
    ("espacos", [" 9:05 - 9:30 "], ["09:05-09:30"]),
    ("um_digito", ["7:00-8:00", "8:00-9:15"], ["07:00-09:15"]),
    ("meia_noite", ["23:00-01:00"], ["23:00-01:00"]),
    ("meia_noite_junta", ["22:00-23:30", "23:00-01:00"], ["22:00-01:00"]),
    ("duplicado", ["10:00-11:00", "10:00-11:00"], ["10:00-11:00"]),
]
ERROS = [
    ("igual", ["10:00-10:00"]),
    ("hora24", ["24:00-25:00"]),
    ("minuto60", ["10:60-11:00"]),
    ("formato", ["10h-11h"]),
]
ok = 0
for nome, ent, esp in CASOS:
    try:
        r = j(list(ent))
        if r == esp:
            ok += 1
        else:
            print(f"  falhou {nome}: {r!r} != {esp!r}")
    except Exception as e:
        print(f"  falhou {nome}: {type(e).__name__} {e}")
for nome, ent in ERROS:
    try:
        j(list(ent)); print(f"  falhou {nome}: não deu ValueError")
    except ValueError as e:
        if ent[0].strip() in str(e):
            ok += 1
        else:
            print(f"  falhou {nome}: ValueError sem o texto ruim ({e})")
    except Exception as e:
        print(f"  falhou {nome}: {type(e).__name__}")
# misto: um texto ruim no meio de bons também é erro
try:
    j(["09:00-10:00", "xx"]); print("  falhou misto: não deu ValueError")
except ValueError:
    ok += 1
except Exception:
    print("  falhou misto")
TOTAL = len(CASOS) + len(ERROS) + 1
print(f"NOTA {ok}/{TOTAL}")
sys.exit(0 if ok == TOTAL else 1)
