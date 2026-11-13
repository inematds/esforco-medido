# esfuerzo medido

[![esfuerzo medido](guia/assets/banner-es.jpg)](https://inematds.github.io/esforco-medido/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Esfuerzo medido es un kit gratuito que muestra con números qué cambia realmente el nivel de esfuerzo (`low`, `medium`, `high`, `xhigh`, `max`) en **Claude Fable 5.2** y **Claude Opus 5.5**. Ejecuta la misma tarea en cada nivel con Claude Code de tu suscripción y registra lo que hizo el modelo: cuántas herramientas usó, cuántas veces revisó su propio trabajo, cuánto pensó, cuánto tardó y si acertó, según un verificador oculto que el modelo no puede ver. También incluye 14 consejos sobre esfuerzo, cada uno con su fuente. Necesitas Python 3 y Claude Code; no usa API.

## 📖 Guía de uso

Guía completa (página de presentación + paso a paso): **https://inematds.github.io/esforco-medido/guia/es/**

## Por qué

El esfuerzo no es un cronómetro. Según la documentación de Anthropic, controla cuánto piensa **y actúa** el modelo en cada paso («the level also changes how the model thinks and how many tool calls it makes»). El tiempo es una consecuencia. Y el mismo nombre no significa lo mismo en los dos modelos: en la API, Fable 5.2 viene con `high` y Opus 5.5 con `medium`; además, el `medium` de Opus 5.5 ya supera el `high` de Opus 5. La forma de saber qué nivel te sirve es medirlo en tu propia tarea.

## Lo que medí (12/11/2026)

3 tareas de código, cada una en 5 niveles en los dos modelos: 30 rondas, copia limpia, verificador oculto, una ronda por combinación. **Las 30 obtuvieron la puntuación máxima.** Lo que cambió fue el resto (suma de las 3 tareas):

| | Puntuación | Tiempo | Pensamiento (tokens) | Revisiones | Costo equivalente* |
|---|---|---|---|---|---|
| Fable 5.2 · low | 48/48 | 1 min 05 s | 1.015 | 3 | US$ 0,72 |
| Fable 5.2 · high | 48/48 | 1 min 53 s | 3.174 | 7 | US$ 1,05 |
| Fable 5.2 · max | 48/48 | 26 min 42 s | 132.112 | 25 | US$ 9,78 |
| Opus 5.5 · low | 48/48 | 1 min 04 s | 253 | 5 | US$ 0,30 |
| Opus 5.5 · medium | 48/48 | 1 min 29 s | 760 | 4 | US$ 0,39 |
| Opus 5.5 · max | 48/48 | 18 min 06 s | 92.889 | 16 | US$ 3,77 |

El pensamiento aumentó en cada nivel; las revisiones crecieron poco hasta `high` (Fable 3 → 7; en Opus casi no cambiaron, 5 → 4) y se dispararon en `xhigh` y `max` (Fable 25, Opus 16). Son tareas cortas: no muestran dónde ayuda un esfuerzo alto (trabajo largo, problema abierto). Los cuadros completos, con los 5 niveles, están en `exemplos/`.

Repetición (ruido): Fable 5.2 en la tarea `carrinho` (carrito), `low` y `high` 3 veces cada uno → todas 12/12; `low` 26–33 s, `high` 39–49 s, y el `high` siempre pensó más. En cambio, el número de herramientas varió de 3 a 12 entre rondas iguales: compara el razonamiento y el tiempo, no un recuento aislado de herramientas (`exemplos/carrinho-repeticao/`).

\* Costo que Claude Code calcula según la tabla de la API; con la suscripción, lo que pagas es uso de tu límite.

## Inicio rápido

```bash
git clone https://github.com/inematds/esforco-medido.git
cd esforco-medido
./medir.sh carrinho -m opus -e low,medium        # 2 rodadas rápidas para ver funcionando
./medir.sh calendario                            # fable y opus, low → max (10 rodadas; max demora)
cat dicas/DICAS.md                               # los 14 consejos
```

## Contenido

| Archivo | Qué hace |
|---|---|
| `medir.sh` | Ejecuta la tarea para cada combinación de `modelo × esfuerzo` (`-m fable,opus -e low,…,max -r N`), cada ronda en una copia limpia y con un HOME temporal: el modelo no lee tu CLAUDE.md, hooks, plugins, skills ni MCP. Solo se conecta la credencial de la suscripción. `--sem-isolar` ejecuta con toda tu configuración. |
| `relatorio.py` | Lee el stream-json de cada ronda y cuenta herramientas (por tipo), revisiones (código ejecutado para comprobar, incluida la suite), ediciones, relecturas después de editar, subagentes, errores, tokens de pensamiento, tiempo, costo equivalente y si al final propone continuar en vez de terminar. `sessao <arquivo.jsonl>` hace los mismos conteos en una sesión tuya. |
| `tarefas/` | 3 tareas con verificador oculto (`oculto/checar.py`, puntuación `n/total`): `intervalos` (fácil, 16 casos), `carrinho` (buscar 6 errores según las reglas de un archivo, 12 casos), `calendario` (5 funciones con feriados móviles, 20 casos). |
| `dicas/DICAS.md` | 14 consejos sobre esfuerzo para Fable 5.2 y Opus 5.5, con la fuente de cada uno (en portugués). |
| `dicas/terminar-o-trabalho.es.txt` | El bloque «terminar el trabajo» de Anthropic, para pegar en CLAUDE.md cuando el modelo se detenga antes de tiempo (en portugués; el original está en `.en.txt`). |
| `exemplos/` | Las rondas reales de este kit (12/11/2026): `RESULTADO.md` y `resultado.json` de cada tarea. |
| `tests/` | 18 pruebas sin red: `python3 -m unittest discover tests`. |

## Tu tarea

Crea `tarefas/<nome>/` con `projeto/` (el código que recibe el modelo), `pedido.txt` (la solicitud, igual a la que escribirías) y `oculto/checar.py <pasta>` que imprima `NOTA n/total`. Ejecuta `./medir.sh <nome>`.

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Descargar el kit | `git clone https://github.com/inematds/esforco-medido.git` | 🧠 tú |
| 2 | Elegir o crear la tarea | `ls tarefas/` ou `tarefas/<nome>/` | 🧠 tú |
| 3 | Medir los niveles | `./medir.sh <tarefa> [-m …] [-e …] [-r 3]` | ⚙️ script + 🤖 `claude -p` |
| 4 | Leer el cuadro | `resultados/<tarefa>-<data>/RESULTADO.md` | 🧠 tú |
| 5 | Fijar el nivel | `/effort <nível>` o `effortLevel` / `modelSettings` en settings | 🧠 tú |
| 6 | Si se detiene pronto | pegar `dicas/terminar-o-trabalho.es.txt` en CLAUDE.md | 🧠 tú |

## Precauciones

- Cada ronda consume el límite de tu suscripción. `max` puede tardar mucho; empieza con `-e low,medium,high`.
- Una ronda mide esa tarea en ese día. Antes de convertir el resultado en una regla, repítela (`-r 3`).
- El costo del cuadro es el que Claude Code calcula según la tabla de la API; con la suscripción, lo que pagas es uso de tu límite.
- En macOS, el inicio de sesión queda en Keychain: si el aislamiento no encuentra la credencial, el script avisa y se ejecuta sin aislar.

## Kit hermano

[esfuerzo certo](https://github.com/inematds/esforco-certo): audita con qué modelo y nivel de esfuerzo se ejecuta cada parte de tu proyecto y compara dos niveles en un trabajo tuyo (`ab.sh`).

## Licencia

MIT.