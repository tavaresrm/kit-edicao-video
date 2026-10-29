# Pasta de edição (mapa)

Esta pasta é sua. O kit nunca apaga nem sobrescreve nada aqui, com uma exceção: a subpasta `kit/`, que é a cópia do motor e é trocada quando o plugin atualiza.

| O quê | Onde |
|---|---|
| Sua marca: fontes, cores, escala, margens, lado livre do quadro | `marca.json` |
| Trilhas da timeline (nome e cor por tipo) | `trilhas.json` |
| Regras aprovadas por você (o que vale para todo vídeo) | `REGRAS.md` |
| Ordem de trabalho de todo vídeo | `CHECKLIST.md` |
| Suas notas e correções (valem mais que qualquer preset) | `aprendizados.md` |
| Um arquivo por preset, com referências, regras e status | `presets/<nome>.md` |
| Código de cada preset | `presets/codigo/<nome>.py` |
| Fontes e logos | `marca/fontes/`, `marca/logos/` |
| Clipes prontos (inscrever, CTA) que entram no projeto modelo | `biblioteca/<nome>/<nome>_00000.png` |
| Sons por tipo de animação | `sfx/<slot>/` |
| Pauta, camadas e conferências de cada vídeo | `videos/<video>/` |
| Motor do kit (não editar: é trocado na atualização) | `kit/` |

## Ordem de leitura para o Claude
1. Este arquivo.
2. `REGRAS.md` e `aprendizados.md`.
3. `CHECKLIST.md`.
4. O arquivo do preset que vai usar.
