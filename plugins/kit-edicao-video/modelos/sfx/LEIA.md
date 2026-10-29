# Sons (SFX) por tipo de animação

Uma pasta por slot. O kit usa o primeiro arquivo de cada pasta (ordem alfabética). Pasta vazia = sem som.
Slots do preset de exemplo: `entra` (texto entra), `item` (item de lista), `destaque` (marca-texto), `cta` (card de CTA).
Seus presets podem criar slots novos: basta criar a pasta com o mesmo nome que o preset usa nos eventos.

- Formato: WAV ou MP3. Som curto e discreto, sempre abaixo da voz.
- Use sons que você tem licença para usar no seu canal. O kit não traz sons.
- Antes de montar, rode `kit/audio/preparar_sfx.py` nesta pasta: corta o silêncio do começo e grava a versão pronta em `<slot>/_pronto/`.
