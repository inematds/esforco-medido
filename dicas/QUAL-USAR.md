# Fable 5.2 ou Opus 5.5: quando usar cada

Para código pequeno como calendario, carrinho e intervalos, você pode começar com Opus `low`: o kit mediu nota máxima e menor custo equivalente.
Para uso geral, a Anthropic diz: comece com Opus `medium` ou Fable `high`.
Suba o esforço se você medir melhora na sua tarefa. Aqui, `max` custou muito mais sem melhorar a nota.

| Situação | Modelo e nível para começar | De onde vem |
|---|---|---|
| Código pequeno parecido com as tarefas do kit | Opus `low`; confira o resultado | Medido: calendario, carrinho e intervalos |
| Uso geral com Opus | Opus `medium`; teste os níveis vizinhos | Guia da Anthropic |
| Uso geral com Fable | Fable `high` | Guia da Anthropic |
| Código interativo, chat e dia a dia com Fable | Teste Fable `medium`; mantenha se preservar a qualidade | Guia da Anthropic |
| Tarefa rápida e bem descrita com Fable | Fable `low` | Guia da Anthropic |
| Você quer testar o teto do modelo | Fable ou Opus `max`, se tempo e tokens não importarem | Guia da Anthropic |

## O que medimos

São **3 tarefas pequenas de código** (calendario, carrinho, intervalos), cada uma nos 5 níveis dos 2 modelos:
**30 rodadas**, uma por combinação. Depois, o carrinho foi repetido 3 vezes no Fable `low` e `high`
(`exemplos/carrinho-repeticao`): mais 6 rodadas, 36 no total.

Todas tiveram nota máxima: calendario **20/20**, carrinho e carrinho-repeticao **12/12**, intervalos **16/16**.
Comparando linha a linha, o Opus saiu mais barato no mesmo nível em todas as tarefas com ambos os modelos.
O carrinho-repeticao não permite essa comparação: só tem Fable.

**Custo equivalente médio por rodada, em US$:** média das 3 tarefas calendario, carrinho e intervalos.
Valores calculados a partir dos custos exibidos nos respectivos `RESULTADO.md`, com arredondamento.

| Modelo | low | medium | high | xhigh | max |
|---|---:|---:|---:|---:|---:|
| Fable | 0,24 | 0,27 | 0,35 | 0,74 | 3,26 |
| Opus | 0,10 | 0,13 | 0,16 | 0,26 | 1,26 |

Na assinatura, você paga em **limite, não em dólar**. O custo equivalente é calculado pelo Claude Code com a tabela da API.

Dividindo o custo de `max` pelo de `low`, nos valores dos `RESULTADO.md`:
- Calendario: Fable **16,64 vezes**; Opus **17,56 vezes**, a maior razão (**US$ 1,58 ÷ US$ 0,09**).
- Carrinho: Fable **12 vezes**; Opus **10 vezes**.
- Intervalos: Fable **13,20 vezes**; Opus **11,13 vezes**.

O tempo cresceu com o esforço nas tarefas comparadas, com um empate: Fable no carrinho levou **43 s** tanto em `medium` quanto em `high`.
São medições pequenas. Elas não mostram qual modelo vence em trabalho longo ou aberto.

## Como decidir na sua tarefa

Você pode usar [./medir.sh](./medir.sh) para comparar níveis com o mesmo pedido e conferir se o resultado atende ao que precisa.
Repita a medição antes de escolher. Fique com o menor esforço que mantenha a qualidade.
Para comparar níveis no seu projeto, use também o kit irmão [esforco-certo](https://inematds.github.io/esforco-certo/guia/).
As orientações atribuídas à Anthropic acima vêm do guia conforme registrado em [dicas/DICAS.md](./dicas/DICAS.md).

Medido em 12/11/2026, Claude Code 2.1.323