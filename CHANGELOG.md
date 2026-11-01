# Versões

## 0.2.0 (domingo 01/11/2026)
Melhorias que vieram dos últimos vídeos do canal.
- Marcadores por estado: vermelho = pedido seu, verde = pedido resolvido na rodada, ciano = mudança nova esperando aprovação, azul = proposta, amarelo = b-roll. Cada timeline nova leva só os marcadores da rodada. `marcadores.py` troca o vermelho resolvido pelo verde no mesmo quadro (campo "resolve").
- Zoom e SFX sem um marcador por clipe ou por som: um ciano de resumo e um por exceção. `sfx.py` ganhou o modo "listar" (lista para aprovar na conversa) e monta numa timeline nova com `TL_NOVA` e `RODADA`. `zoom_1_plano.py` ganhou `MARCADOR_POR_CLIPE` e `RODADA`.
- Render é seu, à mão: o Claude não renderiza nem pergunta.
- Revisão do vídeo inteiro atrás de melhoria com fonte, proposta em ciano.
- Número na tela com a fonte no rodapé; matéria com foto sempre que existir; foto de pessoa pública baixada da web não entra.
- Conferência por quadros olha números, fonte, grafia e borda.
- Manual: dica de preset de dados e de matéria com foto; transcrição local com whisper.cpp para remapear vídeo regravado; cor de adjustment clip em cópia da câmera.
- Quem já usa o kit: depois do Update, diga "atualiza o kit de edição". O Claude troca o motor e mostra as mudanças em REGRAS e CHECKLIST para você escolher o que entra.

## 0.1.0 (quinta 29/10/2026)
Primeira versão pública: skills comecar, criar-preset, editar-video, decupagem e assets-canva; motor do Resolve (modelo, vídeo novo, marcadores, montagem de camadas, conferência por quadros, zoom, SFX); base de presets e preset de exemplo de texto.
Testado em quinta 29/10/2026 no DaVinci Resolve Studio 21.1.1 (macOS, Apple Silicon): projeto modelo, vídeo novo, pauta e leitura de marcadores (inclusive dentro de clipe), montagem de camadas, conferência por quadros, zoom (fixo e lento) e SFX (pauta e montagem).
