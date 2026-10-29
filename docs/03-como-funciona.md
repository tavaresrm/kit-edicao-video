# 3. Como o método funciona

## A ideia
O Claude não edita "do jeito dele". Ele segue as suas regras, os seus presets e o seu checklist, que ficam em arquivos na sua pasta. Cada correção sua vira uma linha em `aprendizados.md`, e a próxima edição já sai certa.

## Rodadas
Toda edição anda em rodadas:
1. O Claude lê os seus marcadores (da timeline e de dentro dos clipes).
2. Propõe a pauta numa timeline nova: um marcador azul por gráfico, com a nota do que entra e por quê.
3. Mostra uma prévia de cada tipo de gráfico sobre um quadro real do vídeo.
4. Você responde nos marcadores ou na conversa.
5. Ele monta numa timeline nova e confere por quadros exportados do Resolve.

A timeline anterior nunca é alterada. Se algo der errado, a rodada de antes está lá.

## Cores dos marcadores
| Cor | Quem põe | Significa |
|---|---|---|
| Azul | Claude | Pauta: o que ele vai fazer |
| Vermelho | Você | Refazer (escreva na nota o que mudar) |
| Verde | Você | Aprovado, ou aprovado com ajuste na nota |
| Amarelo | Claude | Lugar bom para b-roll; quem escolhe e insere é você |

## Presets
Um preset é um gráfico que se repete, sempre igual: tópico, frase, lista, card de CTA, prova na tela. Tem duas partes:
- `presets/<nome>.md`: regras escritas (posição, tamanho, fonte, cor, entrada, saída, tempo de tela, quando entra).
- `presets/codigo/<nome>.py`: o código que gera a animação como sequência de PNG transparente.

O kit vem com um preset de exemplo (texto sobre o vídeo) só para você ver funcionando. O seu canal vai ter os seus. Veja [Criar o seu preset](04-criar-seu-preset.md).

## Trilhas
Cada tipo de arquivo tem a sua trilha, com nome e cor fixos (`trilhas.json`). Isso deixa a timeline legível e evita que um gráfico cubra outro. Os scripts acham a trilha pelo tipo, nunca pelo número.

## Projeto modelo
Todo vídeo novo nasce de um projeto modelo no Resolve: mesma configuração, mesmas trilhas, mesmas pastas, clipes prontos e sons já importados.

## O que o Claude não faz (a não ser que você mude as regras)
- Cor, legenda e recorte de fundo.
- Render sem pedido.
- Zoom sem pedido.
- Escolher música ou som por você.
- Pôr número na tela sem prova.
