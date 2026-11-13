#!/usr/bin/env python3
"""relatorio.py — lê o stream-json de uma rodada do Claude Code e conta o que o esforço muda.

  relatorio.py rodada <rodada.jsonl> --id ID --modelo M --esforco E [--rc N] [--parede S] [--checar arq]  → 1 linha JSON
  relatorio.py juntar <pasta>                                                                            → RESULTADO.md + resultado.json
  relatorio.py sessao <sessao.jsonl>   → as mesmas contagens para uma sessão sua do Claude Code (~/.claude/projects/…)

Sem rede, só a biblioteca padrão.
"""
import json, os, re, sys, argparse

ORDEM = {"low": 0, "medium": 1, "high": 2, "xhigh": 3, "max": 4}
# frases de fim que pedem licença ou oferecem continuar em vez de terminar (PT/EN)
OFERTA = re.compile(r"(quer que eu|posso (também|continuar|fazer)|se quiser|deseja que|would you like|want me to|shall i|"
                    r"next steps?:|próximos passos|ainda falta|falta(m)? (fazer|implementar))", re.I)
SUITE = re.compile(r"\b(unittest|pytest)\b")                                   # rodou a suíte de testes
RODA = re.compile(r"\bpython3?\b")                                             # executou código
ESCREVE = re.compile(r"(open\([^)]*['\"][wa]['\"]|\.write(_text)?\(|sed\s+-i|\btee\b|>\s*[\w./-]+\.\w+|cat\s*>)")
RASCUNHO = re.compile(r"(mktemp|/tmp/|\$TMPDIR|scratch)")                         # escreve em pasta temporária = teste
LE = re.compile(r"^\s*(cat|ls|head|tail|grep|rg|find|sed\s+-n|wc)\b")


def bash_tipo(cmd):
    """Classifica um comando Bash: escreve arquivo? roda a suíte? executa código para conferir? só lê?"""
    t = set()
    if ESCREVE.search(cmd):
        t.add("escrita")
    if SUITE.search(cmd):
        t.add("suite")
    # executou código para ver o resultado = conferência; um único python que só escreve o arquivo não conta
    n = len(RODA.findall(cmd))
    if "suite" in t or (n and "escrita" not in t) or n >= 2:
        t.add("conferencia")
    if not t and LE.search(cmd):
        t.add("leitura")
    return t


def contar(eventos):
    """Conta ferramentas, conferências e tokens a partir dos eventos do stream-json (ou das linhas de uma sessão)."""
    c = {"ferramentas": 0, "por_ferramenta": {}, "conferencias": 0, "suite_rodada": 0, "edicoes": 0, "leituras": 0,
         "releituras_pos_edicao": 0, "rascunhos": 0, "subagentes": 0, "erros_ferramenta": 0, "blocos_pensamento": 0,
         "texto_final": ""}
    editou = False
    cwd = None   # pasta do projeto (evento init); escrita fora dela = rascunho para conferir, não edição
    resultado = None
    for d in eventos:
        t = d.get("type")
        if t == "system" and d.get("subtype") == "init" and d.get("cwd"):
            cwd = d["cwd"].rstrip("/") + "/"
        if t == "assistant":
            for b in (d.get("message") or {}).get("content") or []:
                bt = b.get("type")
                if bt == "tool_use":
                    n = b.get("name", "?")
                    c["ferramentas"] += 1
                    c["por_ferramenta"][n] = c["por_ferramenta"].get(n, 0) + 1
                    inp = b.get("input") or {}
                    if n in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                        alvo = str(inp.get("file_path") or inp.get("notebook_path") or "")
                        if cwd and alvo.startswith("/") and not alvo.startswith(cwd):
                            c["rascunhos"] += 1   # script de teste escrito fora do projeto
                        else:
                            c["edicoes"] += 1; editou = True
                    elif n in ("Read", "Grep", "Glob"):
                        c["leituras"] += 1
                        if editou and n == "Read":
                            c["releituras_pos_edicao"] += 1
                    elif n == "Bash":
                        tipo = bash_tipo(str(inp.get("command", "")))
                        if "escrita" in tipo:
                            if RASCUNHO.search(str(inp.get("command", ""))):
                                c["rascunhos"] += 1; tipo.add("conferencia")
                            else:
                                c["edicoes"] += 1; editou = True
                        if "suite" in tipo:
                            c["suite_rodada"] += 1
                        if "conferencia" in tipo:
                            c["conferencias"] += 1
                        if "leitura" in tipo:
                            c["leituras"] += 1
                            if editou:
                                c["releituras_pos_edicao"] += 1
                    elif n in ("Task", "Agent"):
                        c["subagentes"] += 1
                elif bt == "thinking":
                    c["blocos_pensamento"] += 1
                elif bt == "text" and b.get("text", "").strip():
                    c["texto_final"] = b["text"].strip()
        elif t == "user":
            cont = (d.get("message") or {}).get("content")
            for b in cont if isinstance(cont, list) else []:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"):
                    c["erros_ferramenta"] += 1
        elif t == "result":
            resultado = d
    return c, resultado


def ler_jsonl(arq):
    ev = []
    with open(arq, encoding="utf-8", errors="replace") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                try:
                    ev.append(json.loads(linha))
                except json.JSONDecodeError:
                    pass
    return ev


def nota(arq):
    if not arq or not os.path.exists(arq):
        return None, None
    m = re.search(r"NOTA (\d+)/(\d+)", open(arq, encoding="utf-8", errors="replace").read())
    return (int(m[1]), int(m[2])) if m else (None, None)


def rodada(a):
    c, r = contar(ler_jsonl(a.arquivo))
    r = r or {}
    u = r.get("usage") or {}
    mu = r.get("modelUsage") or {}
    ok, tot = nota(a.checar)
    final = c.pop("texto_final")
    linha = {
        "id": a.id, "modelo_pedido": a.modelo, "esforco": a.esforco, "modelo_real": ",".join(mu.keys()) or "?",
        "rc": a.rc, "erro": bool(r.get("is_error")) or not r, "subtipo": r.get("subtype"),
        "nota": f"{ok}/{tot}" if ok is not None else "?", "nota_ok": ok, "nota_total": tot,
        "tempo_s": round((r.get("duration_ms") or 0) / 1000) or a.parede, "turnos": r.get("num_turns"),
        "tokens_saida": u.get("output_tokens", 0), "cache_criado": u.get("cache_creation_input_tokens", 0),
        "tokens_pensamento": (u.get("output_tokens_details") or {}).get("thinking_tokens", 0),
        "custo_equivalente_usd": round(r.get("total_cost_usd") or 0, 4),
        "negacoes": len(r.get("permission_denials") or []),
        "ofereceu_continuar": bool(OFERTA.search(final)), "fim": final[-400:],
        **c,
    }
    print(json.dumps(linha, ensure_ascii=False))


def linha(a):
    """Resumo de uma linha da última rodada (progresso do medir.sh)."""
    d = json.loads([l for l in open(a.arquivo, encoding="utf-8") if l.strip()][-1])
    print(f"  {d['id']}: nota {d['nota']} · {d['ferramentas']} ferramentas · {d['conferencias']} conferências · "
          f"{d['tempo_s']} s · {d['tokens_saida']} tokens")


def refazer(a):
    """Recalcula rodadas.jsonl de uma pasta a partir dos .jsonl brutos (depois de mudar a contagem)."""
    velhas = [json.loads(l) for l in open(os.path.join(a.pasta, "rodadas.jsonl"), encoding="utf-8") if l.strip()]
    import io
    from contextlib import redirect_stdout
    novas = []
    for v in velhas:
        buf = io.StringIO()
        ns = argparse.Namespace(arquivo=os.path.join(a.pasta, v["id"] + ".jsonl"), id=v["id"], modelo=v["modelo_pedido"],
                                esforco=v["esforco"], rc=v.get("rc", 0), parede=v.get("tempo_s", 0),
                                checar=os.path.join(a.pasta, v["id"] + ".checar.txt"))
        with redirect_stdout(buf):
            rodada(ns)
        novas.append(buf.getvalue().strip())
    open(os.path.join(a.pasta, "rodadas.jsonl"), "w", encoding="utf-8").write("\n".join(novas) + "\n")
    juntar(a)


def juntar(a):
    pasta = a.pasta
    rs = [json.loads(l) for l in open(os.path.join(pasta, "rodadas.jsonl"), encoding="utf-8") if l.strip()]
    rs.sort(key=lambda d: (d["modelo_pedido"], ORDEM.get(d["esforco"], 9), d["id"]))
    cfg = open(os.path.join(pasta, "config.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(pasta, "config.txt")) else ""
    linhas = ["# Esforço medido — " + os.path.basename(pasta), "", "```", cfg.strip(), "```", "",
              "| Rodada | Modelo real | Nota oculta | Ferramentas | Conferências (suíte) | Edições no projeto | Releu após editar | Tempo | Tokens de saída (pensando) | Custo equiv.* | Fecha com “se quiser…”** |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for d in rs:
        aviso = "" if d["modelo_pedido"] in d["modelo_real"] else " ⚠"
        linhas.append(f"| {d['id']} | {d['modelo_real']}{aviso} | {d['nota']} | {d['ferramentas']} | {d['conferencias']} ({d['suite_rodada']}) | "
                      f"{d['edicoes']} | {d['releituras_pos_edicao']} | {d['tempo_s']} s | {d['tokens_saida']} ({d['tokens_pensamento']}) | "
                      f"US$ {d['custo_equivalente_usd']:.2f} | {'sim' if d['ofereceu_continuar'] else 'não'} |")
    linhas += ["", "\\*\\* O fim da resposta oferece mais trabalho (\"se quiser, faço…\"). Com nota cheia é oferta de extra; com nota baixa costuma ser o modelo parando antes de terminar.",
               "\\* Custo que o Claude Code calcula pela tabela da API. Na assinatura você paga em limite, não em dólar.",
               "Uma rodada por linha: é a medida desta tarefa, nesta máquina, neste dia — repita (-r 3) antes de tirar regra.",
               "⚠ = o Claude Code rodou outro modelo que não o pedido: a linha não vale para a comparação."]
    open(os.path.join(pasta, "RESULTADO.md"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    json.dump(rs, open(os.path.join(pasta, "resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def sessao(a):
    c, _ = contar(ler_jsonl(a.arquivo))
    c.pop("texto_final")
    print(json.dumps(c, ensure_ascii=False, indent=1))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    r = s.add_parser("rodada"); r.add_argument("arquivo"); r.add_argument("--id", required=True)
    r.add_argument("--modelo", required=True); r.add_argument("--esforco", required=True)
    r.add_argument("--rc", type=int, default=0); r.add_argument("--parede", type=int, default=0); r.add_argument("--checar")
    j = s.add_parser("juntar"); j.add_argument("pasta")
    se = s.add_parser("sessao"); se.add_argument("arquivo")
    rf = s.add_parser("refazer"); rf.add_argument("pasta")
    li = s.add_parser("linha"); li.add_argument("arquivo")
    a = p.parse_args(argv)
    {"rodada": rodada, "juntar": juntar, "sessao": sessao, "refazer": refazer, "linha": linha}[a.cmd](a)


if __name__ == "__main__":
    main()
