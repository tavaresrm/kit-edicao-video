# Kit de edição de vídeo com Claude e DaVinci Resolve

Este é o método que eu uso para editar os vídeos do canal [@ThaiseRoberto](https://www.youtube.com/@ThaiseRoberto) com o Claude, o DaVinci Resolve Studio e o Canva.

O kit não traz os presets do nosso canal. Ele traz o método e as ferramentas para você criar os seus: o Claude entende o seu canal, estuda referências que você escolhe, escreve as regras, programa a animação, mostra uma prévia sobre um quadro do seu vídeo e só aplica depois que você aprova.

## O que o kit faz
- **Pauta em marcadores.** Antes de montar, o Claude marca no Resolve tudo o que pretende fazer. Você aprova, pede para refazer ou ajusta, com cores de marcador.
- **Presets seus.** Tópico, frase, lista, card de CTA, prova na tela: cada gráfico vira um preset com regras e código, sempre igual de um vídeo para o outro.
- **Montagem por script.** Os gráficos entram como camadas transparentes, cada tipo na sua trilha, com cor e nome fixos.
- **Rodadas sem risco.** Cada rodada vira uma timeline nova. A anterior nunca é alterada.
- **Conferência por quadros.** O Claude exporta quadros do próprio Resolve e olha antes de te responder.
- **Extras:** projeto modelo para todo vídeo novo, decupagem (silêncio, erro, take repetido), zoom na câmera, SFX por animação e assets do vídeo organizados no Canva.

## O que você precisa
| Aplicativo | Para quê |
|---|---|
| DaVinci Resolve Studio 21.1 ou mais novo (pago) | Edição. A versão grátis não roda scripts em Python desde a 21.1 e não tem o conector de IA. |
| Claude no desktop, plano pago, com Cowork | O Claude que trabalha no seu computador. Também funciona no Claude Code. |
| Canva (opcional) | Organizar provas, prints, logos e QR de cada vídeo. |
| ffmpeg (opcional) | Preparar os sons de SFX e achar silêncios na decupagem. |

Detalhes em [docs/01-aplicativos.md](docs/01-aplicativos.md).

## Instalação rápida
1. No DaVinci Resolve Studio: **File > Setup AI Assistants** e escolha o Claude.
2. No Claude desktop: **Personalizar > Plugins > Adicionar marketplace**, cole `tavaresrm/kit-edicao-video` e instale o plugin **kit-edicao-video**.
3. Numa conversa nova do Cowork, escreva: **"quero configurar o kit de edição"**.

Passo a passo: [docs/02-instalacao.md](docs/02-instalacao.md).

## Manual
1. [Aplicativos](docs/01-aplicativos.md)
2. [Instalação](docs/02-instalacao.md)
3. [Como o método funciona](docs/03-como-funciona.md)
4. [Criar o seu preset](docs/04-criar-seu-preset.md)
5. [Editar um vídeo](docs/05-editar-um-video.md)
6. [Problemas comuns](docs/06-problemas-comuns.md)

## O que tem aqui
```
.claude-plugin/marketplace.json     lista de plugins deste repositório
plugins/kit-edicao-video/
  skills/                           instruções que o Claude segue
    comecar/                        configuração e atualização
    criar-preset/                   criar ou ajustar um preset
    editar-video/                   editar um vídeo por rodadas
    decupagem/                      cortes no bruto
    assets-canva/                   assets do vídeo no Canva
  motor/                            código
    resolve/                        scripts que rodam dentro do Resolve
    graficos/                       base dos presets e o preset de exemplo
    audio/                          preparo dos sons
  modelos/                          arquivos iniciais da sua pasta de edição
docs/                               manual
```

## Licença
MIT. Use, mude e compartilhe. Fontes, sons e imagens que você puser no seu kit seguem a licença de cada um.

Feito por Roberto Tavares, do canal Thais e Roberto. Dúvida ou melhoria: abra uma issue aqui no GitHub.
