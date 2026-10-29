---
name: decupagem
description: Decupagem (cortes no bruto) de um vídeo falado no DaVinci Resolve Studio - tira silêncio longo, erro, falso começo e take repetido, com pauta em marcadores aprovada antes de cortar. Use quando a pessoa pedir para cortar, decupar, limpar o bruto, tirar os silêncios ou os erros de um vídeo.
---

# Decupagem

A decupagem tira do bruto o que não fica: silêncio longo, respiração longa, erro, falso começo e take repetido (fica o último). Não escolhe entre takes diferentes, não faz ritmo fino, música, efeito, legenda ou cor. Depois dela, a edição segue pela skill editar-video.

Antes: ler `LEIA.md`, `REGRAS.md`, `aprendizados.md` e `videos/<video>/notas.md`. Conferir no Resolve o projeto, a timeline do bruto e onde estão a câmera e a voz (tipos `camera` e `voz` do `trilhas.json`).

## Passo a passo
1. **Timeline nova.** Duplique a timeline do bruto para "Claude - Decupagem pauta". A original nunca é alterada.
2. **Transcrição.** Na timeline duplicada, gere as legendas (`tl.CreateSubtitlesFromAudio()`, ou a pessoa pede em Timeline > Create Subtitles from Audio) e espere terminar. Leia as legendas com tempo (`GetItemListInTrack("subtitle", 1)`). Se precisar de tempo por palavra, extraia o áudio com ffmpeg e transcreva onde houver ferramenta para isso.
3. **Silêncios.** Com ffmpeg: `ffmpeg -i <arquivo da voz> -af silencedetect=noise=-35dB:d=0.3 -f null -`. O limite (0,3 s e -35 dB) é ponto de partida: confirme com a pessoa e anote em `aprendizados.md`. Mantenha 3 quadros antes e 4 depois de cada fala para não cortar sílaba.
4. **Takes repetidos e falsos começos** pela transcrição: frases iguais ou quase iguais em sequência = fica a última; frase interrompida e recomeçada = sai a interrompida. Frases diferentes sobre o mesmo ponto não são take repetido: marque como pergunta.
5. **Pauta.** Grave `videos/<video>/pauta_decupagem.json` e escreva com `marcadores.py` (modo "pauta") um marcador azul por corte, com a duração cobrindo o trecho a tirar; nome = motivo (silêncio, erro, falso começo, take repetido); nota = o texto que sai. Silêncios simples podem ir num marcador só, com a lista.
6. **Aprovação.** Vermelho = não cortar, verde = aprovado ou ajuste. Leia as notas com `marcadores.py` (modo "ler").
7. **Corte.** Timeline nova "Claude - Decupado v1" só com os trechos mantidos, em ordem, por `AppendToTimeline` (vídeo e áudio juntos, mesmos quadros de origem). Confira `GetStart`, `GetEnd` e `GetLeftOffset` de cada trecho.
8. **Conferência.** Duração antes e depois, número de cortes, duração média dos planos, e ouça três emendas ao acaso (render curto de cada emenda) para checar palavra cortada.
9. **Registro.** `aprendizados.md` (limite de silêncio, o que a pessoa devolveu) e `videos/<video>/notas.md`.

## Nunca
- Cortar sem pauta aprovada.
- Alterar a timeline original.
- Decidir entre takes diferentes: marque como pergunta.
