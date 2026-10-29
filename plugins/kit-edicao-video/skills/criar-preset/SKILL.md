---
name: criar-preset
description: Cria ou ajusta um preset de gráfico do canal (texto, tópico, lista, card de CTA, prova na tela, selo, qualquer animação sobre o vídeo) a partir de referências reais, com regras escritas, código, prévia sobre um quadro do vídeo e aprovação nos marcadores do DaVinci Resolve. Use quando a pessoa quiser criar um padrão visual, mudar o visual de um gráfico, copiar um estilo que viu em outro canal ou padronizar a edição.
---

# Criar um preset

Preset é um gráfico que se repete nos vídeos, sempre do mesmo jeito: tem um arquivo de regras (`presets/<nome>.md`) e um código (`presets/codigo/<nome>.py`) que gera a animação como sequência PNG transparente. Um preset só vale depois de aprovado pela pessoa num vídeo de verdade.

Antes de começar, leia na pasta de edição: `LEIA.md`, `REGRAS.md`, `aprendizados.md`, `marca.json` e os presets que já existem. Uma etapa por vez; não pule a aprovação.

## 1. Entender o pedido
Pergunte, numa mensagem só:
1. O que o gráfico mostra e em que momento da fala ele entra.
2. Onde fica no quadro (a pessoa nunca pode ser coberta).
3. Se já existe algum vídeo (dela ou de outro canal) com o visual que ela quer.

## 2. Três referências reais
Cada preset começa por no mínimo três exemplos reais de canais que a pessoa admira, com link e tempo exato (minuto e segundo). Se ela não tiver, proponha canais do mesmo nicho e peça para ela escolher. Abra cada vídeo no tempo, olhe o quadro e anote no arquivo do preset o que pegar de cada um: posição, tamanho, fonte, cor, entrada, saída, tempo de tela. Referência é inspiração: nunca copie logo, marca, personagem ou arte de outro canal.

## 3. Regras escritas
Copie `presets/_MODELO_DE_PRESET.md` para `presets/<nome>.md` e preencha: para que serve, referências, posição, escala, fontes e cores (do `marca.json`), entrada e saída (duração e movimento), tempo de tela, limite de texto, quando entra ([sempre], [se couber], [sob pedido]) e o slot de SFX de cada evento. Mostre as regras e espere o ok antes de programar.

## 4. Código
Parta de `kit/graficos/texto.py` (exemplo) e de `kit/graficos/_base.py` (base comum). Copie para `presets/codigo/<nome>.py` e ajuste o caminho de importação para `kit/graficos/`. Padrão de todo preset:
- Uma página HTML 1920x1080 com fundo transparente e uma função JavaScript `update(t)` que desenha o quadro do tempo `t` em segundos.
- Tudo o que é da marca vem do `marca.json` (fontes, cores, escala, margem). Nada de cor ou fonte escrita direto no código, salvo exceção registrada nas regras.
- Entrada e saída por funções de tempo (`prog`, `eout`, `eio` da base): nada depende do relógio do navegador.
- Limite de texto conferido no código (o preset recusa texto grande demais em vez de quebrar o layout).
- `eventos(item, marca)` devolve os quadros de cada animação (entrada, item, destaque) para o SFX.
- `render(...)` da base grava a sequência, o `montagem.json` e o `eventos.json`.
Animação discreta: movimento curto, sem quique, sem exagero. Elemento parado não fica congelado demais: uma flutuação leve ajuda, se a pessoa gostar.

Quando o preset é um clipe que nunca muda (inscrever, vinheta, CTA fixo do produto), gere uma vez e guarde em `biblioteca/<nome>/`, para entrar no projeto modelo.

## 5. Prévia
1. Peça (ou exporte pelo `conferir_quadros.py`) um quadro real de um vídeo dela.
2. Gere a prévia com a função `previa` da base: o gráfico parado no meio da animação sobre esse quadro. Quando houver escolha de linguagem, mostre as opções lado a lado na mesma folha.
3. Prévia de movimento: gere 2 a 3 segundos e monte um MP4 curto (ffmpeg) ou uma folha com 6 quadros da entrada.
4. Mostre e espere o ok. Ajuste e repita até aprovar.

## 6. Teste no Resolve
1. Numa timeline nova (copiada de uma timeline real), monte o preset em um minuto de vídeo com `kit/resolve/montar_camadas.py`.
2. Exporte quadros com `conferir_quadros.py`, junte com `folha.py` e olhe antes de responder.
3. A pessoa revisa no Resolve: marcador vermelho = refazer, verde = aprovado ou ajuste (com nota). Leia os marcadores com `marcadores.py` (modo "ler").

## 7. Aprovado
- Status FINAL no arquivo do preset, com a data e a versão.
- Uma regra nova em `REGRAS.md` e, se o preset entra em todo vídeo, uma linha no `CHECKLIST.md`.
- O que a pessoa disse vai para `aprendizados.md`.
- Slot de SFX novo: crie a pasta `sfx/<slot>/` e avise que ela precisa pôr um som lá.

## Nunca
- Programar antes das regras aprovadas, ou aplicar no vídeo inteiro antes da prévia aprovada.
- Copiar arte, logo ou personagem de outro canal.
- Pôr número ou promessa de resultado na tela sem prova.
