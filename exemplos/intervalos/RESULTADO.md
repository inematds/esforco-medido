# Esforço medido — intervalos-20261112-212437

```
tarefa=intervalos
modelos=fable,opus
esforcos=low,medium,high,xhigh,max
repeticoes=1
isolado=1
claude=2.1.323 (Claude Code)
inicio=2026-11-12T21:24:37-03:00
fim=2026-11-12T21:42:03-03:00
```

| Rodada | Modelo real | Nota oculta | Ferramentas | Conferências (suíte) | Edições no projeto | Releu após editar | Tempo | Tokens de saída (pensando) | Custo equiv.* | Fecha com “se quiser…”** |
|---|---|---|---|---|---|---|---|---|---|---|
| fable-low-1 | claude-fable-5-2 | 16/16 | 2 | 1 (1) | 1 | 0 | 19 s | 1877 (446) | US$ 0.20 | não |
| fable-medium-1 | claude-fable-5-2 | 16/16 | 2 | 1 (1) | 1 | 0 | 22 s | 2126 (662) | US$ 0.21 | não |
| fable-high-1 | claude-fable-5-2 | 16/16 | 8 | 4 (2) | 1 | 0 | 42 s | 4139 (1524) | US$ 0.37 | não |
| fable-xhigh-1 | claude-fable-5-2 | 16/16 | 5 | 1 (1) | 1 | 0 | 100 s | 9836 (7012) | US$ 0.67 | não |
| fable-max-1 | claude-fable-5-2 | 16/16 | 13 | 7 (4) | 2 | 0 | 469 s | 44507 (37383) | US$ 2.64 | não |
| opus-low-1 | claude-opus-5-5 | 16/16 | 2 | 1 (1) | 0 | 0 | 17 s | 1449 (149) | US$ 0.08 | não |
| opus-medium-1 | claude-opus-5-5 | 16/16 | 2 | 1 (1) | 0 | 0 | 20 s | 1860 (316) | US$ 0.09 | não |
| opus-high-1 | claude-opus-5-5 | 16/16 | 2 | 1 (1) | 1 | 0 | 30 s | 2766 (907) | US$ 0.12 | sim |
| opus-xhigh-1 | claude-opus-5-5 | 16/16 | 3 | 1 (1) | 1 | 0 | 51 s | 4971 (2331) | US$ 0.19 | sim |
| opus-max-1 | claude-opus-5-5 | 16/16 | 7 | 2 (2) | 1 | 1 | 266 s | 28483 (24580) | US$ 0.89 | sim |

\*\* O fim da resposta oferece mais trabalho ("se quiser, faço…"). Com nota cheia é oferta de extra; com nota baixa costuma ser o modelo parando antes de terminar.
\* Custo que o Claude Code calcula pela tabela da API. Na assinatura você paga em limite, não em dólar.
Uma rodada por linha: é a medida desta tarefa, nesta máquina, neste dia — repita (-r 3) antes de tirar regra.
⚠ = o Claude Code rodou outro modelo que não o pedido: a linha não vale para a comparação.
