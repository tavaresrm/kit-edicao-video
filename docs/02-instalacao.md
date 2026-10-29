# 2. Instalação

Leva uns 20 minutos. Faça na ordem.

## Passo 1. Ligar o Resolve ao Claude
1. Abra o DaVinci Resolve Studio (21.1 ou mais novo).
2. Menu **File > Setup AI Assistants**.
3. Escolha o Claude e confirme.
4. Feche e abra o app do Claude.

## Passo 2. Instalar o plugin
No Claude desktop:
1. **Personalizar > Plugins**.
2. **Adicionar marketplace** e cole: `tavaresrm/kit-edicao-video`.
3. Na lista, ache **kit-edicao-video** e clique em **Instalar**.

No Claude Code (terminal):
```
/plugin marketplace add tavaresrm/kit-edicao-video
/plugin install kit-edicao-video@kit-edicao-video
```

## Passo 3. Configurar
Abra uma conversa nova no Cowork e escreva:

> quero configurar o kit de edição

O Claude vai, uma etapa por vez:
1. Conferir se o Resolve Studio responde.
2. Pedir a pasta de edição (ex.: `Edicao` na sua pasta pessoal) e copiar os arquivos iniciais para ela.
3. Perguntar o nome do canal, as fontes, as cores e o lado livre do seu enquadramento. Tenha os arquivos das fontes à mão.
4. Mostrar as trilhas da timeline e perguntar se quer mudar.
5. Criar o projeto modelo no Resolve. Se você já tem um projeto com a configuração que gosta, abra ele antes: o Claude copia a configuração.
6. Fazer um teste com o preset de exemplo num projeto "TESTE kit". Depois você pode apagar esse projeto.

Ao final, a sua pasta de edição fica assim:
```
Edicao/
  LEIA.md          mapa da pasta
  marca.json       fontes, cores, escala, margem, lado livre
  trilhas.json     trilhas da timeline
  REGRAS.md        regras aprovadas por você
  CHECKLIST.md     ordem de trabalho de todo vídeo
  aprendizados.md  suas correções
  presets/         um arquivo por preset e o código de cada um
  marca/           fontes e logos
  biblioteca/      clipes prontos (inscrever, CTA)
  sfx/             sons por tipo de animação
  videos/          uma pasta por vídeo
  kit/             motor do kit (não editar)
```

## Atualizar
Quando sair versão nova: **Personalizar > Plugins**, no marketplace clique em **Update**. Depois diga ao Claude **"atualiza o kit de edição"**: ele troca só a pasta `kit/`. Seus presets, regras e vídeos não mudam.
