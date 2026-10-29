# 1. Aplicativos

## DaVinci Resolve Studio 21.1 ou mais novo (obrigatório)
- É a versão paga do Resolve, da Blackmagic Design.
- Por que a versão grátis não serve: desde a 21.1, a Blackmagic levou os scripts em Python para o Studio, e o conector de IA (o servidor MCP que liga o Claude ao Resolve) também é só do Studio. Todo o motor do kit é Python rodando dentro do Resolve.
- O Python vem dentro do próprio Resolve. Você não precisa instalar Python para os scripts do Resolve.
- Testado no macOS (Apple Silicon). No Windows deve funcionar igual, mas ainda não foi testado.

## Claude no desktop, com plano pago (obrigatório)
- O kit é um plugin. Plugins funcionam no Cowork e no Claude Code, não no chat comum.
- O Cowork precisa de acesso à pasta de edição no seu computador. Você conecta a pasta quando o Claude pedir.
- Para gerar os gráficos, o Claude usa Python com um navegador sem janela (Chromium e Playwright). Na primeira configuração ele confere e instala o que faltar.

## Canva (opcional)
- Para a skill assets-canva: um design por vídeo com provas, prints, logos e QR.
- Ligue o conector do Canva no Claude (Personalizar > Conectores). Sem o conector, você exporta as páginas à mão.

## ffmpeg (opcional)
- Usado para preparar os sons de SFX e para achar silêncios na decupagem.
- No Mac: instale o Homebrew (brew.sh) e depois, no Terminal, `brew install ffmpeg`.

## Fontes e sons
- O kit não traz fontes nem sons. Use os seus, com licença para uso em vídeo.
- Fontes gratuitas: Google Fonts (fonts.google.com). O exemplo usa Fraunces e Inter.
