# Checklist de edição (v1)

Ordem de trabalho de cada vídeo. Cada etapa: pauta em marcadores numa timeline nova, aprovação sua, montagem, conferência por quadros exportados do Resolve. Render só quando você pedir.
Legenda: [sempre] entra em todo vídeo · [se couber] entra quando a fala ou o material pede · [sob pedido] só quando você pede.
Edite à vontade: tire, mude ou acrescente etapas. O Claude segue o que estiver aqui.

## Começo
- [ ] [sempre] Perguntas antes de qualquer montagem, numa mensagem só:
  1. Formato: uma pessoa ou duas no quadro (duas = texto no centro, embaixo, para não cobrir rosto).
  2. Corte: você já cortou ou o Claude faz a decupagem.
  3. Oferta do vídeo: o que entra de CTA, link ou QR, e quantas vezes.
  4. B-roll: tem ou não tem.
- [ ] [sempre] Projeto do vídeo a partir do projeto modelo (`kit/resolve/novo_video.py`).

## Antes
- [ ] [sempre] Ler `LEIA.md`, `REGRAS.md`, `aprendizados.md` e as notas do vídeo.
- [ ] [se couber] Assets do vídeo (design "ASSETS - <nome do vídeo>" no Canva) baixados em `videos/<video>/assets/`.

## Corte
- [ ] [se couber] Decupagem (skill decupagem): pauta, aprovação, corte, emendas conferidas.

## Gráficos
- [ ] [sempre] No começo de cada rodada: listar os seus marcadores, da timeline e de dentro dos clipes, e devolver a lista antes de mexer.
- [ ] [sempre] Pauta completa em marcadores azuis numa timeline nova, com a lista do que falta de assets num pedido só.
- [ ] [sempre] Prévia: um quadro de cada tipo de gráfico sobre um quadro real do vídeo. Só depois da prévia aprovada gerar o vídeo inteiro.
- [ ] [sempre] Presets aprovados em `presets/` (cada um diz quando entra).

## Apoio
- [ ] [se couber] B-roll sinalizado em marcadores amarelos junto da pauta; você escolhe e insere.
- [ ] [sob pedido] Zoom na câmera (`kit/resolve/zoom_1_plano.py` e `zoom_2_movimento.py`).

## Última passada
- [ ] [se couber] SFX por animação (`kit/resolve/sfx.py`): pauta, aprovação, montagem. Por último, depois do visual aprovado.

## Fechamento
- [ ] [sempre] Conferência por quadros exportados do Resolve (`kit/resolve/conferir_quadros.py` + `kit/graficos/folha.py`), folha olhada antes de responder.
- [ ] [sempre] Anotar em `aprendizados.md` o que você corrigiu; atualizar o arquivo do preset quando a versão muda.
- [ ] [sob pedido] Render.
