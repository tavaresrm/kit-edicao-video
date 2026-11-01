# Checklist de edição (v2)

Ordem de trabalho de cada vídeo. Cada etapa: pauta em marcadores numa timeline nova, aprovação sua, montagem, conferência por quadros exportados do Resolve. O render é seu, à mão.
Cores dos marcadores (REGRAS.md, regra 2): vermelho = pedido seu; verde = pedido resolvido na rodada; ciano = mudança nova esperando aprovação; azul = proposta antes de montar; amarelo = b-roll.
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
- [ ] [se couber] Matéria ou notícia na tela com foto, sempre que existir.
- [ ] [se couber] Número, comparação ou evolução falada que tem fonte vira dado na tela (preset de dados, se você tiver um), com a fonte no rodapé.
- [ ] [sempre] Na timeline montada: cada pedido vermelho resolvido vira verde no mesmo quadro; o que entrou sem pedido fica em ciano.
- [ ] [sempre] Revisão do vídeo inteiro atrás de melhoria com fonte (matéria repetida, número falado sem tela, lista que pode virar dado), proposta em ciano.

## Apoio
- [ ] [se couber] B-roll sinalizado em marcadores amarelos junto da pauta; você escolhe e insere.
- [ ] [sob pedido] Zoom na câmera (`kit/resolve/zoom_1_plano.py` e `zoom_2_movimento.py`): um ciano de resumo.

## Última passada
- [ ] [se couber] SFX por animação (`kit/resolve/sfx.py`): lista, aprovação, montagem numa timeline nova, um ciano de resumo. Por último, depois do visual aprovado.

## Fechamento
- [ ] [sempre] Conferência por quadros exportados do Resolve (`kit/resolve/conferir_quadros.py` + `kit/graficos/folha.py`), folha olhada antes de responder: números iguais à fonte, fonte no rodapé, nomes e grafia certos, nada cortado na borda.
- [ ] [sempre] Anotar em `aprendizados.md` o que você corrigiu; atualizar o arquivo do preset e este checklist quando algo muda.
