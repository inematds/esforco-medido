# Esforço medido — calendario-20261112-214229

```
tarefa=calendario
modelos=fable,opus
esforcos=low,medium,high,xhigh,max
repeticoes=1
isolado=1
claude=2.1.323 (Claude Code)
inicio=2026-11-12T21:42:29-03:00
fim=2026-11-12T22:05:48-03:00
```

| Rodada | Modelo real | Nota oculta | Ferramentas | Conferências (suíte) | Edições no projeto | Releu após editar | Tempo | Tokens de saída (pensando) | Custo equiv.* | Fecha com “se quiser…”** |
|---|---|---|---|---|---|---|---|---|---|---|
| fable-low-1 | claude-fable-5-2 | 20/20 | 2 | 1 (1) | 1 | 0 | 19 s | 2140 (238) | US$ 0.22 | não |
| fable-medium-1 | claude-fable-5-2 | 20/20 | 2 | 1 (1) | 0 | 0 | 21 s | 2225 (343) | US$ 0.22 | não |
| fable-high-1 | claude-fable-5-2 | 20/20 | 2 | 1 (1) | 1 | 0 | 28 s | 3060 (668) | US$ 0.28 | não |
| fable-xhigh-1 | claude-fable-5-2 | 20/20 | 5 | 2 (1) | 1 | 0 | 94 s | 10102 (5532) | US$ 0.69 | não |
| fable-max-1 | claude-fable-5-2 | 20/20 | 21 | 8 (3) | 5 | 2 | 581 s | 60039 (48199) | US$ 3.66 | não |
| opus-low-1 | claude-opus-5-5 | 20/20 | 2 | 1 (1) | 0 | 0 | 19 s | 1593 (47) | US$ 0.09 | não |
| opus-medium-1 | claude-opus-5-5 | 20/20 | 2 | 1 (1) | 0 | 0 | 23 s | 2219 (279) | US$ 0.11 | não |
| opus-high-1 | claude-opus-5-5 | 20/20 | 2 | 1 (1) | 1 | 0 | 37 s | 3797 (745) | US$ 0.15 | não |
| opus-xhigh-1 | claude-opus-5-5 | 20/20 | 10 | 6 (3) | 1 | 0 | 100 s | 10207 (3757) | US$ 0.36 | não |
| opus-max-1 | claude-opus-5-5 | 20/20 | 16 | 6 (3) | 6 | 0 | 466 s | 52843 (40079) | US$ 1.58 | sim |

\*\* O fim da resposta oferece mais trabalho ("se quiser, faço…"). Com nota cheia é oferta de extra; com nota baixa costuma ser o modelo parando antes de terminar.
\* Custo que o Claude Code calcula pela tabela da API. Na assinatura você paga em limite, não em dólar.
Uma rodada por linha: é a medida desta tarefa, nesta máquina, neste dia — repita (-r 3) antes de tirar regra.
⚠ = o Claude Code rodou outro modelo que não o pedido: a linha não vale para a comparação.
