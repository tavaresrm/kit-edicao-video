# 6. Problemas comuns

**O Claude não acha o Resolve.**
Confira se o Resolve Studio está aberto e se o conector foi ligado em File > Setup AI Assistants. Feche e abra o app do Claude. Uma janela aberta no Resolve (salvar, erro, preferências) trava o conector: feche a janela.

**Uso a versão grátis do Resolve.**
O kit não funciona nela. Desde a 21.1 a versão grátis não roda scripts em Python e não tem o conector de IA.

**"timeline fora do padrão".**
A timeline tem uma trilha com clipes e outro nome no lugar de uma trilha do `trilhas.json`. Peça ao Claude para reorganizar numa timeline nova, ou mude o `trilhas.json` para o seu jeito.

**O gráfico aparece no Resolve mas some no render.**
Movimento feito no Fusion no mesmo comando que montou o clipe. O kit separa em dois comandos; se você criou um preset com movimento de câmera, mantenha essa separação.

**O quadro exportado para conferência está errado ou atrasado.**
O Resolve precisa de uns 2 segundos depois de mudar de posição. O `conferir_quadros.py` já espera; aumente `ESPERA` se o seu computador estiver lento.

**Fonte errada no gráfico.**
O arquivo da fonte não está onde o `marca.json` aponta. O render avisa qual fonte faltou.

**Não consigo instalar o Playwright.**
A rede do ambiente do Claude pode estar bloqueando. No Cowork, peça ao administrador para liberar pypi.org e o download do Chromium, ou rode o comando de instalação no seu Terminal.

**O SFX ficou fora do lugar.**
O som está com silêncio no começo. Rode `kit/audio/preparar_sfx.py` na pasta `sfx/` antes de montar. Se ele avisar `_nao_apagados`, apague à mão os arquivos antigos de `_pronto/`.
