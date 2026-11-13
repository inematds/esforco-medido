#!/usr/bin/env bash
# medir.sh — roda a MESMA tarefa em vários esforços (e modelos) pelo Claude Code da sua assinatura e mede o que o esforço
# muda de verdade: chamadas de ferramenta, conferências (testes rodados), edições, raciocínio, tempo, tokens, se terminou e a
# nota de um checador oculto que o modelo não vê.
#
# Uso:
#   ./medir.sh <tarefa> [-m modelos] [-e esforços] [-r repetições] [--sem-isolar] [--teto SEG]
#   <tarefa> = nome em tarefas/ (intervalos, carrinho, calendario) ou uma pasta com projeto/, pedido.txt e oculto/checar.py
# Exemplos:
#   ./medir.sh carrinho                              # fable e opus, low → max (10 rodadas)
#   ./medir.sh carrinho -m fable -e low,high -r 3    # 6 rodadas
# Padrão: -m fable,opus -e low,medium,high,xhigh,max -r 1 · teto de 30 min por rodada.
#
# Como roda:
#   - cada rodada ganha uma cópia limpa de projeto/ numa pasta temporária, com um HOME temporário: o modelo NÃO lê o seu
#     CLAUDE.md global, seus hooks, plugins, skills nem MCP (isso mudaria o comportamento que você quer medir). Só a credencial
#     da assinatura é ligada (link). --sem-isolar roda com tudo seu (use no macOS se o login falhar: lá ele fica no Keychain).
#   - ANTHROPIC_API_KEY sai do ambiente: mede na ASSINATURA. Para medir na API de propósito: MEDIR_USAR_API=1.
#   - ferramentas liberadas: Read, Edit, Write, Glob, Grep e Bash para python3 (o modelo pode rodar os testes); comandos só de
#     leitura (cat, ls) e arquivos de rascunho fora do projeto o Claude Code também aceita no modo acceptEdits.
#   - ordem: esforço de baixo para cima, os mais caros por último. Max pode levar muito tempo e gastar bastante do limite.
#   - saída: resultados/<tarefa>-<data>/ (bruto .jsonl de cada rodada + RESULTADO.md + resultado.json).
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
TAREFA=""; MODELOS=fable,opus; ESFORCOS=low,medium,high,xhigh,max; REP=1; ISOLAR=1; TETO=${MEDIR_TETO:-1800}
while [ $# -gt 0 ]; do
  case "$1" in
    -m) MODELOS=$2; shift 2 ;;
    -e) ESFORCOS=$2; shift 2 ;;
    -r) REP=$2; shift 2 ;;
    --sem-isolar) ISOLAR=0; shift ;;
    --teto) TETO=$2; shift 2 ;;
    -h|--help) sed -n '2,/^set -uo/p' "$0" | grep '^#'; exit 0 ;;
    *) [ -z "$TAREFA" ] && TAREFA=$1 || { echo "argumento a mais: $1" >&2; exit 2; }; shift ;;
  esac
done
[ -n "$TAREFA" ] || { echo "uso: ./medir.sh <tarefa> (ver --help)" >&2; exit 2; }
T=$TAREFA; [ -d "$T" ] || T="$AQUI/tarefas/$TAREFA"
T=$(cd "$T" 2>/dev/null && pwd) || { echo "tarefa não encontrada: $TAREFA" >&2; exit 2; }
for f in projeto pedido.txt oculto/checar.py; do [ -e "$T/$f" ] || { echo "falta $T/$f" >&2; exit 2; }; done
for e in ${ESFORCOS//,/ }; do case $e in low|medium|high|xhigh|max) ;; *) echo "esforço inválido: $e" >&2; exit 2 ;; esac; done
command -v claude >/dev/null || { echo "claude (Claude Code) não está no PATH" >&2; exit 2; }
TO=$(command -v timeout || command -v gtimeout || true)
[ "${MEDIR_USAR_API:-0}" = 1 ] || unset ANTHROPIC_API_KEY
CRED="$HOME/.claude/.credentials.json"
if [ $ISOLAR = 1 ] && [ ! -f "$CRED" ]; then
  echo "aviso: não achei $CRED (no macOS o login fica no Keychain) → rodando sem isolar" >&2; ISOLAR=0
fi
NOME=$(basename "$T"); SAI="$AQUI/resultados/$NOME-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$SAI"
PEDIDO=$(cat "$T/pedido.txt")
{ echo "tarefa=$NOME"; echo "modelos=$MODELOS"; echo "esforcos=$ESFORCOS"; echo "repeticoes=$REP"; echo "isolado=$ISOLAR";
  echo "claude=$(claude --version 2>/dev/null | head -1)"; echo "inicio=$(date -Iseconds)"; } > "$SAI/config.txt"
echo "tarefa: $NOME · modelos: $MODELOS · esforços: $ESFORCOS · ×$REP · saída: $SAI"

for e in ${ESFORCOS//,/ }; do
 for m in ${MODELOS//,/ }; do
  for r in $(seq 1 "$REP"); do
    id="$m-$e-$r"; X=$(mktemp -d "${TMPDIR:-/tmp}/esforco-medido-XXXXXX"); mkdir -p "$X/run"
    cp -r "$T/projeto" "$X/run/p"
    ENVX=()
    if [ $ISOLAR = 1 ]; then
      mkdir -p "$X/.claude"; ln -s "$CRED" "$X/.claude/.credentials.json"; ENVX=(HOME="$X")
    fi
    echo "→ $id rodando… ($(date +%H:%M))"
    ini=$(date +%s)
    ( cd "$X/run/p" && env "${ENVX[@]}" PATH="$PATH" ${TO:+$TO $TETO} claude -p --model "$m" --effort "$e" \
        --strict-mcp-config --disable-slash-commands --no-session-persistence \
        --permission-mode acceptEdits --allowedTools "Read Edit Write Glob Grep Bash(python3:*)" \
        --max-turns 200 --output-format stream-json --verbose -- "$PEDIDO" ) > "$SAI/$id.jsonl" 2> "$SAI/$id.err"
    rc=$?; fim=$(date +%s)
    # a credencial pode ser renovada durante a rodada: se o link virou arquivo, devolve a versão nova ao seu HOME
    if [ $ISOLAR = 1 ] && [ -f "$X/.claude/.credentials.json" ] && [ ! -L "$X/.claude/.credentials.json" ]; then
      cp -p "$X/.claude/.credentials.json" "$CRED" && echo "  (credencial renovada copiada de volta)"
    fi
    python3 "$T/oculto/checar.py" "$X/run/p" > "$SAI/$id.checar.txt" 2>&1
    (cd "$X/run/p" && find . -name __pycache__ -prune -o -type f -print | sort | xargs tar czf "$SAI/$id.projeto.tgz") 2>/dev/null
    python3 "$AQUI/relatorio.py" rodada "$SAI/$id.jsonl" --id "$id" --modelo "$m" --esforco "$e" --rc $rc \
      --parede $((fim-ini)) --checar "$SAI/$id.checar.txt" >> "$SAI/rodadas.jsonl"
    python3 "$AQUI/relatorio.py" linha "$SAI/rodadas.jsonl"
    rm -rf "$X"
  done
 done
done
echo "fim=$(date -Iseconds)" >> "$SAI/config.txt"
python3 "$AQUI/relatorio.py" juntar "$SAI" && cat "$SAI/RESULTADO.md"
