# Regras do total do carrinho (Loja Exemplo)

1. Subtotal = soma de preço × quantidade de cada item. Itens com quantidade 0 ou negativa não entram (e não contam para nada).
2. Cupom de porcentagem (ex.: `DEZ` = 10%) vale só sobre o subtotal dos produtos, nunca sobre o frete.
3. Frete: R$ 25,00 fixo. Grátis quando o subtotal **já com o cupom** for de R$ 200,00 **ou mais**.
4. Total = subtotal com cupom + frete.
5. Todo valor é arredondado para centavos só no fim, meio centavo para cima (R$ 10,005 → R$ 10,01).
6. Cupom desconhecido: ignora o cupom (não dá erro).
