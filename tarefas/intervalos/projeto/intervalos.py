"""Agenda de salas: junta horários que se sobrepõem.

Implemente `juntar(horarios)`.

Entrada: lista de textos "HH:MM-HH:MM" (horário de início e de fim de uma reserva).
Saída: lista de textos "HH:MM-HH:MM" com as reservas que se encostam ou se sobrepõem juntadas,
em ordem de início.

Regras:
- "09:00-10:00" e "10:00-11:00" se encostam: viram "09:00-11:00".
- Uma reserva que passa da meia-noite ("23:00-01:00") termina no dia seguinte; na saída ela fica
  como "23:00-01:00" (ou junta com outras que cruzam ou começam depois dela).
- Espaços em volta são aceitos (" 9:05 - 9:30 " vale "09:05-09:30"); horas de 1 dígito também.
- Início igual ao fim ("10:00-10:00") é inválido.
- Texto fora do formato, hora > 23 ou minuto > 59 → ValueError com o texto ruim na mensagem.
- Lista vazia → lista vazia.
- A saída sempre usa 2 dígitos: "09:05".
"""


def juntar(horarios):
    raise NotImplementedError
