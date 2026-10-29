---
name: comecar
description: Configura o kit de edição pela primeira vez (pasta de edição, marca, trilhas, projeto modelo no DaVinci Resolve Studio e teste) ou atualiza o motor depois de uma atualização do plugin. Use quando a pessoa disser que instalou o kit, pedir para configurar, começar, testar a instalação, mudar a marca ou atualizar o kit.
---

# Começar com o kit de edição

O kit liga o Claude ao DaVinci Resolve Studio para editar vídeos com método: pauta em marcadores, presets de gráfico feitos pela própria pessoa, montagem por script e conferência por quadros. Esta skill deixa tudo pronto. Faça uma etapa por vez e confirme cada uma com a pessoa.

## Onde estão os arquivos do kit
Esta skill está em `<raiz do plugin>/skills/comecar/`. A raiz do plugin tem:
- `motor/`: código (resolve/, graficos/, audio/) e `VERSAO`.
- `modelos/`: arquivos iniciais da pasta de edição da pessoa.

## 1. Conferir o que precisa estar instalado
1. **DaVinci Resolve Studio 21.1 ou mais novo.** A versão grátis não roda scripts em Python desde a 21.1 e não tem o conector de IA. Sem o Studio, pare aqui e explique.
2. **Conector do Resolve ligado no Claude.** Procure as ferramentas do conector do DaVinci Resolve (nomes com `run_script` e `run_script_unsafe`). Se não aparecerem, peça para a pessoa abrir o Resolve Studio, ir em **File > Setup AI Assistants**, escolher o Claude e reiniciar o app do Claude. Depois rode, com `run_script`: `result = {"produto": resolve.GetProductName(), "versao": resolve.GetVersionString()}`.
3. **Navegador sem janela para gerar os gráficos** (onde o Claude roda os scripts de Python): `python3 -c "import playwright"`. Se faltar: `pip install playwright pillow numpy` e `python3 -m playwright install chromium`. Se a rede não deixar instalar, diga o que falta e siga com o resto.
4. **ffmpeg** (opcional, para SFX e decupagem): `which ffmpeg`. No Mac, a pessoa instala com Homebrew (`brew install ffmpeg`). Sem ffmpeg, o kit funciona sem a preparação de SFX.

## 2. Pasta de edição
1. Pergunte onde a pessoa quer a pasta de edição (ex.: `~/Edicao`). Ela precisa estar no computador onde o Resolve roda.
2. Garanta acesso a essa pasta (no Cowork, peça a conexão da pasta). Anote dois caminhos:
   - o caminho que o Claude usa para ler e escrever (pode ser um caminho montado, ex.: `$HOME/mnt/Edicao`);
   - o caminho absoluto no computador, que o Resolve usa (ex.: `/Users/nome/Edicao/`). É o `PASTA` dos scripts.
3. Copie `modelos/*` para a pasta **sem sobrescrever nada que já existe** (`cp -rn` ou equivalente). Se o Claude roda em outra máquina, mande os arquivos para o computador com a ferramenta de envio de arquivos.
4. Copie `motor/` para `<pasta>/kit/` (esta subpasta é do kit e pode ser substituída inteira). Confira que `<pasta>/kit/VERSAO` ficou igual a `motor/VERSAO`.

## 3. Marca (marca.json)
Pergunte, uma coisa por vez, e grave no `marca.json`:
1. Nome do canal.
2. Fontes: título, texto e detalhe. Peça os arquivos .ttf ou .otf em `marca/fontes/` (Google Fonts tem fontes gratuitas). Confira que a licença permite uso em vídeo.
3. Cores: texto, destaque, texto sobre o destaque, sombra.
4. Lado livre do quadro (onde a pessoa NÃO fica no enquadramento): `dir` ou `esq`. Vídeo com duas pessoas no quadro: `"layout": "centro"`.
5. Taxa de quadros dos vídeos (`fps`): `"24000/1001"` para 23,976; `"30000/1001"` para 29,97; `"25"`, `"30"`, `"60"`.
Escala, margem e animação podem ficar no padrão e ser ajustadas depois.

## 4. Trilhas (trilhas.json)
Mostre o padrão do `trilhas.json` (uma trilha por tipo, de baixo para cima) e pergunte se quer mudar nomes, cores ou a ordem. Os tipos `camera`, `voz`, `texto` e `sfx` são usados pelo motor: podem mudar de nome e posição, mas não de tipo.

## 5. Projeto modelo no Resolve
Antes de qualquer script que muda o Resolve: avise a pessoa, porque o Resolve vai trocar de projeto. Peça para salvar o que estiver aberto.
1. Se ela tem um projeto com a configuração preferida (resolução, fps, áudio, cor): peça para abrir esse projeto e rode, com `run_script_unsafe`:
   ```python
   PASTA = "/Users/nome/Edicao/"
   exec(open(PASTA + "kit/resolve/_rodar.py").read())
   result = rodar("exportar_config.py", {})
   ```
2. Crie o modelo: `result = rodar("criar_modelo.py", {"NOME": '"MODELO Canal"'})`. Se já existir um projeto com esse nome, o script recusa: pergunte outro nome.
3. Mostre o resultado: configuração, pastas, trilhas. A cor do cabeçalho das trilhas não tem API: a pessoa pinta à mão uma vez no modelo, se quiser.

## 6. Teste
1. Gere o preset de exemplo: `python3 <pasta>/kit/graficos/texto.py <pasta> <pasta>/kit/graficos/exemplo_itens.json <pasta>/videos/_teste/camadas --pasta-no-computador <PASTA>videos/_teste/camadas`.
2. Peça um projeto de teste: `rodar("novo_video.py", {"NOME": '"TESTE kit"', "BRUTO": '["<um vídeo qualquer>"]'})`.
3. Monte: `rodar("montar_camadas.py", {"TL": '"Bruto"', "TL_NOVA": '"Claude - teste v1"', "LISTA_JSON": '"<PASTA>videos/_teste/camadas/montagem.json"'})`.
4. Confira: `rodar("conferir_quadros.py", {"TL": '"Claude - teste v1"', "QUADROS": '[60, 200, 330]', "SAIDA": '"<PASTA>videos/_teste/conferencia/"'})`, junte com `kit/graficos/folha.py` e olhe a folha antes de responder.
5. Diga à pessoa que o projeto "TESTE kit" pode ser apagado no Resolve por ela.

## Atualizar o kit
Quando `motor/VERSAO` do plugin for mais nova que `<pasta>/kit/VERSAO`: substitua `<pasta>/kit/` pelo `motor/` novo (o resto da pasta não muda) e copie de `modelos/` só os arquivos que ainda não existem na pasta da pessoa. Diga o que mudou.

## Nunca
- Sobrescrever arquivo da pasta da pessoa fora de `kit/`.
- Alterar ou apagar projeto ou timeline que já existe no Resolve.
- Rodar script que muda o Resolve sem avisar antes.
