---
name: editar-video
description: Edita um vídeo no DaVinci Resolve Studio pelo checklist e pelos presets aprovados da pessoa - pauta em marcadores, gráficos, b-roll sinalizado, zoom, SFX e conferência por quadros, cada rodada numa timeline nova. Use quando a pessoa pedir para editar, montar, pôr gráficos, textos, tópicos, CTA, b-roll, zoom ou SFX num vídeo, ou para seguir com a próxima rodada de um vídeo.
---

# Editar um vídeo

Trabalho por rodadas. Em cada rodada: ler o que a pessoa marcou, propor a pauta em marcadores numa timeline nova, esperar a aprovação, montar, conferir por quadros exportados do Resolve. A timeline anterior nunca é alterada.

## Ferramentas
- Conector do DaVinci Resolve Studio: `run_script` para consultas; `run_script_unsafe` para os scripts do kit (eles leem arquivos da pasta de edição).
- Scripts do kit, sempre por `_rodar.py`, que troca só o bloco PARAMETROS:
  ```python
  PASTA = "/caminho/absoluto/da/pasta de edicao/"
  exec(open(PASTA + "kit/resolve/_rodar.py").read())
  result = rodar("marcadores.py", {"MODO": '"ler"', "TL": '"Bruto"'})
  ```
- Presets: `presets/codigo/<nome>.py` (e o exemplo `kit/graficos/texto.py`), rodados com Python onde houver Chromium e Playwright.

## 0. Começo de todo vídeo
1. Ler `LEIA.md`, `REGRAS.md`, `aprendizados.md`, `CHECKLIST.md` e `videos/<video>/notas.md` (se existir). As notas da pessoa valem mais que qualquer preset.
2. Perguntas do começo do `CHECKLIST.md`, numa mensagem só, antes de montar qualquer coisa (formato, corte, oferta, b-roll). Confira o formato também num quadro do bruto.
3. Projeto do vídeo a partir do modelo: `rodar("novo_video.py", {"NOME": '"<nome>"', "BRUTO": '[...]'})`. Projeto existente nunca é alterado.
4. Se a pessoa não cortou o vídeo, a decupagem vem antes (skill decupagem).

## 1. Tempo da fala
Os gráficos entram no tempo exato da fala. Use as legendas da própria timeline (`tl.GetItemListInTrack("subtitle", 1)`; se não houver, peça para a pessoa gerar em Timeline > Create Subtitles from Audio, ou rode `tl.CreateSubtitlesFromAudio()` e espere terminar) ou uma transcrição palavra por palavra feita a partir do áudio. Sempre a partir do corte atual: se a pessoa mexeu na timeline, mapeie os tempos de novo. Nunca confie em tempo anotado numa rodada anterior.

## 2. Pauta antes de montar
1. Leia os marcadores da pessoa, da timeline e de dentro dos clipes (`marcadores.py`, modo "ler"). Marcador dentro de clipe também é pedido. Devolva a lista antes de mexer.
2. A pauta é a edição completa, não só o que foi pedido: os presets que o `CHECKLIST.md` e cada `presets/<nome>.md` mandam usar. O Claude propõe; a pessoa veta.
3. Grave `videos/<video>/pauta_vN.json` (lista de `quadro`, `duracao`, `cor`, `nome`, `nota`, `id`) e `pauta_vN.md`, e escreva na timeline nova: `rodar("marcadores.py", {"MODO": '"pauta"', "TL": '"<base>"', "TL_NOVA": '"Claude - Edicao pauta vN"', "PAUTA_JSON": '"<PASTA>videos/<video>/pauta_vN.json"'})`. Um marcador azul por gráfico: nome = preset, nota = o que entra na tela e por quê.
4. B-roll (se a pessoa tem): marcador amarelo onde cabe imagem de apoio (fala que cita algo que dá para mostrar, trecho longo só de rosto, 2,5 a 8 s, de preferência escondendo uma emenda), com a imagem sugerida na nota. Quem escolhe e insere é a pessoa.
5. Junto da pauta: a lista única do que falta (logos, prints, provas, QR), num pedido só, e a prévia de um quadro de cada tipo de gráfico sobre um quadro real do vídeo.
6. Espere: vermelho = refazer, verde = aprovado ou ajuste, "pode fazer" vale como aprovação.

## 3. Montar
1. Gere as camadas de cada preset numa pasta nova da rodada: `videos/<video>/camadas_vN/` (com `--pasta-no-computador` quando o Claude gera em outra máquina; nesse caso, envie a pasta para o computador antes de montar).
2. Confira antes de gerar: itens da mesma trilha não se sobrepõem; nenhum texto passa do limite.
3. Monte numa timeline nova: `rodar("montar_camadas.py", {"TL": '"<pauta aprovada>"', "TL_NOVA": '"Claude - Edicao vN"', "LISTA_JSON": '"<PASTA>videos/<video>/camadas_vN/montagem.json"'})`.
4. Confira: `conferir_quadros.py` num ponto de cada gráfico, `folha.py`, e olhe a folha antes de responder.

## 4. Zoom (só quando a pessoa pede)
`zoom_1_plano.py` (timeline nova, plano, zoom fixo e marcadores) e, em OUTRO comando, `zoom_2_movimento.py` com o `PLANO_JSON`. Ajuste PROPORCAO, PUNCH e LENTO no preset de zoom da pessoa, se ela tiver.

## 5. SFX (última passada, depois do visual aprovado)
1. `python3 kit/audio/preparar_sfx.py <pasta>/sfx` (precisa de ffmpeg).
2. `rodar("sfx.py", {"MODO": '"pauta"', "TL": '"<aprovada>"', "TL_NOVA": '"Claude - Edicao vN sfx"', "EVENTOS": '["<.../eventos.json>"]'})`.
3. Depois da aprovação: `MODO "montar"` na timeline da pauta. Conferir quantos sons entraram e quais slots estão sem som.

## 6. Fechamento da rodada
- `aprendizados.md`: o que a pessoa aprovou, reprovou ou corrigiu.
- `videos/<video>/notas.md`: uma linha por rodada (timeline, o que mudou).
- Arquivo do preset, quando a versão muda.
- Render só quando a pessoa pedir.

## Cuidados técnicos que já quebraram
- Fusion criado no mesmo comando que coloca o clipe não aparece no render: montar num comando, movimento em outro.
- Imagem parada posta por script entra com duração fixa: use sequência de imagens com o número de quadros certo.
- Sequência de imagens: `startFrame` = número do primeiro arquivo, `endFrame` = último + 1. Confira `GetStart`, `GetEnd` e `GetLeftOffset` depois de cada `AppendToTimeline`.
- O Resolve pode trocar a timeline aberta entre comandos: abra pelo nome e confira antes de qualquer escrita (`timeline(nome)` do `trilhas.py`).
- Exportar quadro: espere uns 2 s depois de mudar o timecode, senão sai o quadro anterior.
- Efeito aplicado à mão no Inspector (ex.: sombra) não passa pela API: ao recriar um clipe, avise a pessoa.
- Mídia de 24 fps numa timeline de 23,976: ao copiar clipe, confira `GetSourceStartTime`, não só o quadro.
- Se a contagem de clipes muda entre duas leituras, a pessoa está editando ao mesmo tempo: pare de escrever e avise.
- Áudio por script: `AppendToTimeline` com `mediaType` 2 e a trilha de SFX; em MP3 a propriedade "Frames" vem vazia (use "Duration").
- O conector pode parar de responder com o Resolve ocupado ou com uma janela aberta: confira o status e peça para a pessoa olhar a tela.
- Código novo de preset é salvo na pasta de edição na mesma rodada. Código que fica só na sessão se perde.

## Nunca
- Alterar timeline ou projeto existente: sempre duplicar.
- Montar sem pauta aprovada, ou gerar o vídeo inteiro sem prévia aprovada.
- Aplicar zoom, renderizar, publicar ou mandar a terceiros sem pedido.
- Inventar número ou texto de fonte; mostrar dado pessoal de terceiro sem desfoque.
- Escolher som ou música pela pessoa, ou baixar arquivo na conta dela.
