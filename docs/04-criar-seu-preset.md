# 4. Criar o seu preset

Esta é a parte mais importante do kit. O objetivo é sair com gráficos que são a cara do seu canal e que o Claude repete igual em todo vídeo.

## Antes de começar
- `marca.json` preenchido (fontes, cores, lado livre). O Claude pergunta isso na configuração.
- Um vídeo seu já gravado, para a prévia e o teste.
- Três vídeos de outros canais com o tipo de gráfico que você quer, com o minuto e o segundo de cada exemplo.

## Como pedir
Numa conversa do Cowork, descreva o gráfico. Exemplos:

> quero um preset de tópico para abrir cada assunto do vídeo, no canto de baixo, com a cor do canal

> quero um card de CTA com QR code que entra da direita quando eu falo da oferta

> quero mostrar prints de notícia em cima do vídeo, com o trecho que eu leio grifado

## O que acontece, etapa por etapa
1. **Perguntas.** O que mostra, quando entra na fala, onde fica no quadro.
2. **Referências.** O Claude olha os três exemplos no tempo que você deu e anota o que pegar de cada um: posição, tamanho, fonte, cor, entrada, saída e tempo de tela. Referência é inspiração: ele não copia logo, arte ou personagem de outro canal.
3. **Regras escritas.** Ele cria `presets/<nome>.md` com tudo isso e te mostra. Você corrige antes de qualquer código.
4. **Código.** Ele cria `presets/codigo/<nome>.py` a partir do exemplo do kit, usando as suas fontes e cores.
5. **Prévia.** Um quadro do gráfico sobre um quadro real do seu vídeo. Quando há escolha (duas posições, dois estilos), as opções vêm lado a lado. Você aprova ou pede ajuste.
6. **Teste de um minuto no Resolve.** Numa timeline nova. Você revisa no próprio Resolve: marcador vermelho para refazer, verde para aprovar (com nota, se tiver ajuste).
7. **Aprovado.** O preset vira FINAL, ganha uma regra em `REGRAS.md` e, se entra em todo vídeo, uma linha no `CHECKLIST.md`.

## Dicas
- **Comece pelo que aparece em todo vídeo:** tópico e frase. Depois CTA. Depois o resto.
- **Um preset por vez.** Só comece o próximo quando o anterior estiver aprovado num vídeo real.
- **Seja específico na correção.** "Menor, mais perto da borda, entra 0,2 s mais rápido" funciona melhor que "não gostei".
- **Rosto nunca coberto.** Se você grava com duas pessoas no quadro, peça a versão de centro (embaixo) dos presets de texto.
- **Menos é mais.** Nos nossos testes, gráfico demais cansou a audiência. Deixe a pessoa falando ser a protagonista.
- **Clipe que nunca muda** (inscrever, vinheta, CTA fixo do produto): peça para gerar uma vez e guardar na `biblioteca/`. Ele entra no projeto modelo e você arrasta quando quiser.

## Anatomia de um preset (para quem quer mexer no código)
- Cada preset gera uma página HTML de 1920x1080 com fundo transparente.
- A página tem uma função `update(t)` que desenha o quadro do segundo `t`. O motor chama `update` quadro a quadro num navegador sem janela e grava um PNG por quadro.
- Fontes, cores, escala e margem vêm do `marca.json`. Assim, trocar a cor do canal muda todos os presets de uma vez.
- `eventos(item, marca)` diz em que quadro cada animação acontece (entrada, item, destaque). O SFX usa isso para pôr o som no quadro certo.
- O exemplo completo está em `kit/graficos/texto.py`, e a base comum em `kit/graficos/_base.py`.

Teste rápido do exemplo, no Terminal:
```
python3 ~/Edicao/kit/graficos/texto.py ~/Edicao ~/Edicao/kit/graficos/exemplo_itens.json ~/Edicao/videos/_teste/camadas
```
