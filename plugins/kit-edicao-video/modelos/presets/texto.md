# Texto sobre o vídeo (preset de EXEMPLO do kit)

Status: EXEMPLO. Serve para testar a instalação e como ponto de partida. Troque pelo seu com a skill criar-preset.

## Para que serve
Três tipos de texto branco sobre o vídeo:
- **Tópico**: etiqueta na cor de destaque + título, no canto inferior esquerdo. Abre um assunto.
- **Frase**: a frase que a pessoa fala, palavra por palavra, com marca-texto na cor de destaque nas palavras principais.
- **Lista**: título e itens que entram quando cada um é falado.

## Regras do exemplo
- Fontes, cores, escala, margem e lado livre vêm do `marca.json`.
- `"layout": "centro"` põe tudo no centro, embaixo (vídeo com duas pessoas no quadro).
- Entrada de 0,5 s e saída de 0,4 s (`animacao` no `marca.json`).
- Limites: etiqueta 24, título 34, frase 90, título de lista 36, item 32 caracteres.
- Sons: `entra` na entrada, `destaque` no marca-texto, `item` em cada item da lista.

## Código
`kit/graficos/texto.py`. Itens de exemplo em `kit/graficos/exemplo_itens.json`.
