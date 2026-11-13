# 14 dicas de esforço — Claude Fable 5.2 e Claude Opus 5.5

Fonte de cada dica entre colchetes: **[guia]** = guia de migração da API da Anthropic (seções "Migrating to Claude Fable 5.2"
e "Migrating to Claude Opus 5.5"); **[Claude Code]** = code.claude.com/docs/en/model-config; **[medido]** = o que este kit
mediu (ver `exemplos/`). Lido em 12/11/2026.

## O que o esforço é

1. **Esforço não é cronômetro.** Ele controla quanto o modelo pensa *e age* em cada passo: o raciocínio e quantas
   chamadas de ferramenta ele faz. O tempo que a tarefa leva é consequência disso, não o botão. [guia: "the level also
   changes how the model thinks and how many tool calls it makes"]
2. **Mesmo nome, quantidade diferente.** Os cinco níveis (`low`, `medium`, `high`, `xhigh`, `max`) seguem a mesma ordem
   nos dois modelos, mas o raciocínio por trás de cada um muda de modelo para modelo. No Opus 5.5, o `medium` passou o
   `high` do Opus 5 em código e trabalho de escritório; no Fable 5.2, o `low` ficou perto do Fable 5.1 em níveis mais
   altos. Não compare "Fable high" com "Opus high" como se fossem a mesma coisa: meça. [guia]
3. **Esforço quase não muda o tamanho da resposta.** Para resposta curta ou longa, use o pedido, não o esforço. [guia]

## Por onde começar

4. **Os padrões são diferentes.** Na API, o Fable 5.2 vem em `high` e o Opus 5.5 vem em `medium`. Uma chamada que não diz
   o esforço roda um nível acima no Fable. No Claude Code, veja o nível da sessão com `/effort status` e escolha com
   `/effort <nível>`. [guia] [Claude Code]
5. **Fable 5.2: comece no `high`.** É onde chega a maior parte do ganho. Desça para `medium` onde a qualidade se mantiver
   (código interativo, chat, dia a dia) e use `low` para tarefa rápida e bem descrita e para subagentes. [guia]
6. **Opus 5.5: comece no `medium`** e teste os vizinhos. Em vários testes de código, o `low` chegou perto dele, custando
   bem menos. [guia]
7. **`xhigh` só onde você mediu ganho.** No Fable, ele subiu um pouco as notas de código e gastou muito mais tokens. O
   `max` serve para medir o teto do modelo ou para a tarefa rara em que tempo e tokens não importam. [guia]

## Armadilhas

8. **Esforço baixo para mais cedo.** Em tarefa longa, o modelo às vezes encerra o turno com uma lista do que falta ou
   oferecendo continuar, e isso acontece mais no `low` e no `medium`. Se acontecer, cole o bloco
   `dicas/terminar-o-trabalho.pt.txt` no CLAUDE.md, sob `# Terminar o trabalho` (o original em inglês está ao lado).
   Nos testes da Anthropic, ele cortou pela metade as sessões que terminavam com trabalho por fazer, e a saída cresceu
   cerca de 30%. [guia]
9. **"Pense menos" não funciona no Fable 5.2** a partir do `medium`: ele pensa do mesmo jeito. Apague essas frases e
   baixe o nível. [guia]
10. **No `high` ou acima, o Fable pensa até para dizer "oi".** Para turno fácil, use um nível mais baixo. [guia]
11. **No `xhigh` e no `max`, o Fable pode chamar subagentes** (outra cópia da IA aberta para uma parte do trabalho)
    para revisar o próprio trabalho, e cada subagente gasta. Nas rodadas curtas deste kit, nenhum foi chamado.
    Se o seu CLAUDE.md ou as suas skills mandam delegar, revise essas linhas primeiro. [guia]
12. **Ultracode não é um nível de esforço.** É uma configuração do Claude Code que monta um time de agentes no esforço
    em que a sessão já está (`--effort ultracode` liga e põe em `xhigh`). [Claude Code]

## Como usar no dia a dia

13. **Misture os níveis no mesmo trabalho:** planeje no `medium` e suba o esforço para a parte longa que roda sozinha.
    No Claude Code, o `/effort` no meio da sessão vale a partir da próxima mensagem. [guia] [Claude Code]
14. **Meça na sua tarefa, não na de outra pessoa.** Rode `./medir.sh <tarefa>` (cópia limpa, checador oculto, 5 níveis) e
    escolha o nível mais baixo que acerta. Para comparar só dois níveis num projeto seu, use o `ab.sh` do kit irmão
    [esforço certo](https://inematds.github.io/esforco-certo/guia/). [medido]
