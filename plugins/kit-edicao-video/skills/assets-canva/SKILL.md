---
name: assets-canva
description: Organiza os assets de um vídeo (provas, prints, logos, QR codes, fotos, ícones) num design do Canva com páginas fixas, baixa cada página para a pasta do vídeo e escreve o que cada uma é e onde entra na edição. Use quando a pessoa falar de assets, provas, prints, logos ou QR de um vídeo, ou disser que subiu as imagens no Canva.
---

# Assets do vídeo no Canva

Cada vídeo tem um design no Canva chamado **"ASSETS - <nome do vídeo>"**, na conta da pessoa. Ali entram as imagens que a edição usa: uma por página, fundo transparente quando der. O Claude acha o design pelo nome, baixa e organiza. Precisa do conector do Canva ligado no Claude; sem ele, a pessoa exporta as páginas à mão para `videos/<video>/assets/`.

## Páginas fixas (padrão do kit)
Ordem e nome de página iguais em todo vídeo, para o Claude saber onde procurar. Página que não se aplica fica vazia (não apagar, não mudar a ordem). A pessoa pode mudar esta tabela: registre a versão dela em `REGRAS.md`.

| Nº | Página | O que vai |
|---|---|---|
| 1 | QR | QR code da oferta ou da comunidade |
| 2 | Logo | Logo da marca citada (fundo transparente) |
| 3 | Prints | Prints de página, post ou vídeo citado (um por página: 3a, 3b...) |
| 4 | Fotos | Fotos de matérias ou lugares citados (4a, 4b...) |
| 5 | Provas | Documentos que provam o que é falado (5a, 5b...) |
| 6 | Ícones | Ícones do vídeo |

## O que a pessoa faz
Cria o design com esse nome e põe uma imagem por página. Só isso. O Claude nunca cria o design por ela.

## O que o Claude faz
1. Procura no Canva o design "ASSETS" + nome do vídeo. Se não existir, pede para a pessoa criar.
2. Exporta todas as páginas em PNG (transparente quando a página permite) e salva em `videos/<video>/assets/` com nome `NN_o_que_e.png`.
3. Olha cada página e escreve `videos/<video>/assets/LEIA.md`: o que é, o que prova, data do documento, o que precisa de desfoque (nome, documento, endereço, conta, código). QR: leia o link (ex.: biblioteca zxing-cpp) e anote.
4. Acha na fala o momento de cada imagem e propõe onde entra, na pauta da skill editar-video.
5. Se o design mudou depois do download (data de atualização mais nova), baixa de novo só as páginas novas ou alteradas e avisa.

## Regras
- Na tela, só o número que está no documento, nunca um número só falado.
- Dado pessoal de terceiro sempre desfocado, com desfoque forte gravado na imagem.
- Logo de outra empresa só quando a marca é assunto da fala.
