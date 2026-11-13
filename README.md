# esforço medido

[![esforço medido](guia/assets/banner.jpg)](https://inematds.github.io/esforco-medido/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O esforço medido é um kit gratuito que mostra, com números, o que o nível de esforço (`low`, `medium`, `high`, `xhigh`,
`max`) muda de verdade no **Claude Fable 5.2** e no **Claude Opus 5.5**. Ele roda a mesma tarefa em cada nível, pelo
Claude Code da sua assinatura, e conta o que o modelo fez: quantas ferramentas chamou, quantas vezes conferiu o próprio
trabalho, quanto pensou, quanto tempo levou e se acertou, segundo um checador oculto que o modelo não vê. Junto vêm 14
dicas de esforço, cada uma com a fonte. Precisa de Python 3 e do Claude Code; não usa API.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/esforco-medido/guia/**

## Por quê

Esforço não é cronômetro. Pela documentação da Anthropic, ele controla quanto o modelo pensa **e age** em cada passo
("the level also changes how the model thinks and how many tool calls it makes"). O tempo é consequência. E o mesmo nome
não quer dizer a mesma coisa nos dois modelos: na API o Fable 5.2 vem em `high` e o Opus 5.5 em `medium`, e o `medium` do
Opus 5.5 já passa o `high` do Opus 5. O jeito de saber qual nível serve para você é medir na sua tarefa.

## O que eu medi (12/11/2026)

3 tarefas de código, cada uma em 5 níveis nos dois modelos: 30 rodadas, cópia limpa, checador escondido, uma rodada por
combinação. **Todas as 30 tiraram nota máxima.** O que mudou foi o resto (soma das 3 tarefas):

| | Nota | Tempo | Pensamento (tokens) | Conferências | Custo equivalente* |
|---|---|---|---|---|---|
| Fable 5.2 · low | 48/48 | 1 min 05 s | 1.015 | 3 | US$ 0,72 |
| Fable 5.2 · high | 48/48 | 1 min 53 s | 3.174 | 7 | US$ 1,05 |
| Fable 5.2 · max | 48/48 | 26 min 42 s | 132.112 | 25 | US$ 9,78 |
| Opus 5.5 · low | 48/48 | 1 min 04 s | 253 | 5 | US$ 0,30 |
| Opus 5.5 · medium | 48/48 | 1 min 29 s | 760 | 4 | US$ 0,39 |
| Opus 5.5 · max | 48/48 | 18 min 06 s | 92.889 | 16 | US$ 3,77 |

O pensamento subiu em todo degrau; as conferências cresceram pouco até o `high` (Fable 3 → 7; no Opus quase não mudaram, 5 → 4) e saltaram
no `xhigh` e no `max` (Fable 25, Opus 16). São tarefas curtas: elas não mostram onde o esforço alto ajuda (trabalho longo, problema aberto). Os quadros
completos, com os 5 níveis, estão em `exemplos/`.

Repetição (ruído): Fable 5.2 no carrinho, `low` e `high` 3 vezes cada → todas 12/12; `low` 26–33 s, `high` 39–49 s, e o
`high` sempre pensou mais. Já o número de ferramentas variou de 3 a 12 entre rodadas iguais: compare pensamento e tempo,
não uma contagem solta de ferramentas (`exemplos/carrinho-repeticao/`).

\* Custo que o Claude Code calcula pela tabela da API; na assinatura você paga em limite.

## Começo rápido

```bash
git clone https://github.com/inematds/esforco-medido.git
cd esforco-medido
./medir.sh carrinho -m opus -e low,medium        # 2 rodadas rápidas para ver funcionando
./medir.sh calendario                            # fable e opus, low → max (10 rodadas; o max demora)
cat dicas/DICAS.md                               # as 14 dicas
```

## Conteúdo

| Arquivo | O que faz |
|---|---|
| `medir.sh` | Roda a tarefa em cada `modelo × esforço` (`-m fable,opus -e low,…,max -r N`), cada rodada numa cópia limpa e com um HOME temporário: o modelo não lê o seu CLAUDE.md, hooks, plugins, skills nem MCP. Só a credencial da assinatura é ligada. `--sem-isolar` roda com tudo seu. |
| `relatorio.py` | Lê o stream-json de cada rodada e conta ferramentas (por tipo), conferências (código rodado para checar, inclusive a suíte), edições, releituras depois de editar, subagentes, erros, tokens de pensamento, tempo, custo equivalente e se o fim oferece continuar em vez de terminar. `sessao <arquivo.jsonl>` faz as mesmas contagens numa sessão sua. |
| `tarefas/` | 3 tarefas com checador oculto (`oculto/checar.py`, nota `n/total`): `intervalos` (fácil, 16 casos), `carrinho` (caça a 6 erros com as regras num arquivo, 12 casos), `calendario` (5 funções com feriados móveis, 20 casos). |
| `dicas/DICAS.md` | 14 dicas de esforço para Fable 5.2 e Opus 5.5, com a fonte de cada uma. |
| `dicas/terminar-o-trabalho.pt.txt` | O bloco "terminar o trabalho" da Anthropic, para colar no CLAUDE.md quando o modelo parar antes da hora (original em `.en.txt`, versão em espanhol em `.es.txt`). |
| `exemplos/` | As rodadas reais deste kit (12/11/2026): `RESULTADO.md` e `resultado.json` de cada tarefa. |
| `tests/` | 18 testes sem rede: `python3 -m unittest discover tests`. |

## Tarefa sua

Crie `tarefas/<nome>/` com `projeto/` (o código que o modelo recebe), `pedido.txt` (o pedido, igual ao que você
digitaria) e `oculto/checar.py <pasta>` imprimindo `NOTA n/total`. Rode `./medir.sh <nome>`.

## O processo, do início ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Baixar o kit | `git clone https://github.com/inematds/esforco-medido.git` | 🧠 você |
| 2 | Escolher ou criar a tarefa | `ls tarefas/` ou `tarefas/<nome>/` | 🧠 você |
| 3 | Medir os níveis | `./medir.sh <tarefa> [-m …] [-e …] [-r 3]` | ⚙️ script + 🤖 `claude -p` |
| 4 | Ler o quadro | `resultados/<tarefa>-<data>/RESULTADO.md` | 🧠 você |
| 5 | Fixar o nível | `/effort <nível>` ou `effortLevel` / `modelSettings` no settings | 🧠 você |
| 6 | Se parar cedo | colar `dicas/terminar-o-trabalho.pt.txt` no CLAUDE.md | 🧠 você |

## Cuidados

- Cada rodada gasta o limite da sua assinatura. O `max` pode levar muito tempo; comece com `-e low,medium,high`.
- Uma rodada é a medida daquela tarefa, naquele dia. Antes de virar regra, repita (`-r 3`).
- O custo no quadro é o que o Claude Code calcula pela tabela da API; na assinatura você paga em limite.
- No macOS o login fica no Keychain: se o isolamento não achar a credencial, o script avisa e roda sem isolar.

## Kit irmão

[esforço certo](https://github.com/inematds/esforco-certo): audita em que modelo e esforço cada parte do seu projeto
roda e compara dois níveis num trabalho seu (`ab.sh`).

## Licença

MIT.
