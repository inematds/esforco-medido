# CLAUDE.md — esforço medido

Kit público (inematds/esforco-medido): mede o que o nível de esforço muda no Claude Fable 5.2 e no Claude Opus 5.5
(medir.sh + relatorio.py + tarefas com checador oculto) e traz 14 dicas com fonte (dicas/DICAS.md).

- Autor dos commits: `inematds <inematds@gmail.com>`. Publicar = push (guia no GitHub Pages, `guia/`).
- Testes: `python3 -m unittest discover tests` (sem rede). Não editar `medir.sh` enquanto uma varredura roda (o bash lê o
  script aos poucos).
- Números do README, do guia e do vídeo vêm só de `exemplos/` (rodadas reais). Separar sempre "a Anthropic diz" de "eu medi"
  e dizer "uma rodada, esta tarefa".
- Tarefa nova = `tarefas/<nome>/{projeto/,pedido.txt,oculto/checar.py}`; o checador imprime `NOTA n/total` e dá nota baixa
  ao projeto original (teste em `tests/`).

## Self-learning

Quando o usuário corrigir algo, ou você notar um erro seu: antes de continuar, escreva a lição como uma regra de uma linha
no TOPO da seção Lessons abaixo.

## Lessons

- O stream-json do `claude -p` registra escrita por `python3 - <<EOF` como Bash, não Edit: classificar o comando (relatorio.bash_tipo).
- `--setting-sources` e `CLAUDE_CONFIG_DIR` não impedem o CLAUDE.md global de entrar; só um HOME temporário (fora do HOME real) isola.
