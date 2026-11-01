# 3. Como o método funciona

## A ideia
O Claude não edita "do jeito dele". Ele segue as suas regras, os seus presets e o seu checklist, que ficam em arquivos na sua pasta. Cada correção sua vira uma linha em `aprendizados.md`, e a próxima edição já sai certa.

## Rodadas
Toda edição anda em rodadas:
1. O Claude lê os seus marcadores (da timeline e de dentro dos clipes).
2. Propõe a pauta numa timeline nova: um marcador azul por gráfico, com a nota do que entra e por quê.
3. Mostra uma prévia de cada tipo de gráfico sobre um quadro real do vídeo.
4. Você responde nos marcadores (vermelho onde quer mudança) ou na conversa.
5. Ele monta numa timeline nova: o que você pediu e foi feito vira verde, o que ele pôs sem você pedir fica em ciano.
6. Ele revisa o vídeo inteiro atrás de melhoria com fonte e propõe em ciano.
7. Confere por quadros exportados do Resolve antes de te responder.

A timeline anterior nunca é alterada. Se algo der errado, a rodada de antes está lá. Cada timeline leva só os marcadores da rodada dela, então você não precisa caçar o que foi feito.

## Cores dos marcadores
A cor diz o estado de cada item.

| Cor | Quem põe | Significa |
|---|---|---|
| Vermelho | Você | Pedido seu, ainda não feito (escreva na nota o que mudar) |
| Verde | Claude | Pedido seu resolvido nesta rodada: o vermelho vira verde no mesmo quadro, com a nota do que foi feito |
| Ciano | Claude | Mudança nova desta rodada que você não pediu, esperando aprovação |
| Azul | Claude | Proposta antes de montar: ainda não está na tela |
| Amarelo | Claude | Lugar bom para b-roll; quem escolhe e insere é você |

Zoom e SFX não enchem a timeline: um ciano de resumo no começo e um por exceção. No Edit, a lista de marcadores filtra por cor: ciano = falta aprovar, verde = feito do que você pediu, vermelho que sobrou = pendente.

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
- Render. O render é seu, à mão; a conferência dele é por quadros exportados.
- Zoom sem pedido.
- Escolher música ou som por você.
- Pôr número na tela sem fonte, ou sem a fonte no rodapé.
- Pôr foto de pessoa pública baixada da web.
