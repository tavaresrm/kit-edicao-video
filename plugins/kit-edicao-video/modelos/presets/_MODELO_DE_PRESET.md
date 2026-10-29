# <Nome do preset> (v0.1, <dia da semana e data>)

Status: RASCUNHO · PRÉVIA · APROVADO · FINAL

## Para que serve
Uma frase: o que este gráfico mostra e em que momento da fala ele entra.

## Referências (mínimo três, antes de desenhar)
| Canal | Vídeo (link) | Tempo | O que pegar |
|---|---|---|---|
| | | | |

## Regras
- Onde fica no quadro (lado livre, centro, canto).
- Tamanho (escala) e margem.
- Fontes e cores (do `marca.json`; dizer se usa alguma exceção).
- Entrada: duração e movimento. Saída: duração e movimento.
- Tempo de tela: quando entra em relação à fala e quanto fica depois.
- Limite de texto (caracteres).
- Quando entra no vídeo: [sempre], [se couber] ou [sob pedido].
- Som (slot de SFX) de cada evento da animação.

## Código
`presets/codigo/<nome>.py`. Item de exemplo:
```json
{"nome": "<nome>_01", "tipo": "<tipo>", "t0": 0, "t1": 120}
```

## Histórico
| Dia | Versão | O que mudou | Quem decidiu |
|---|---|---|---|
