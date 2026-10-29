# 5. Editar um vídeo

## Começo
Diga ao Claude:

> vamos editar o vídeo "<nome>". O bruto está em <pasta ou SSD>

Ele faz as perguntas do começo numa mensagem só:
1. Uma pessoa ou duas no quadro.
2. Você já cortou ou ele faz a decupagem.
3. Qual a oferta do vídeo (CTA, link, QR) e quantas vezes entra.
4. Tem b-roll ou não.

Depois cria o projeto do vídeo a partir do modelo, com o bruto na timeline "Bruto".

## Decupagem (se você não cortou)
O Claude transcreve, acha silêncios, erros, falsos começos e takes repetidos, e marca cada corte em azul numa timeline nova. Você aprova ou devolve em vermelho. Só depois ele corta, numa timeline nova.

## Rodadas de edição
1. **Seus marcadores primeiro.** Ele lista tudo o que você marcou (na timeline e dentro dos clipes) e confirma.
2. **Pauta.** Marcadores azuis com cada gráfico proposto e amarelos onde cabe b-roll. Junto, a lista do que falta (logo, print, QR) num pedido só, e a prévia de cada tipo de gráfico.
3. **Sua resposta.** Nos marcadores (vermelho, verde) ou na conversa. "Pode fazer" vale como aprovação.
4. **Montagem.** Numa timeline nova "Claude - Edicao vN". Ele exporta quadros do Resolve e confere antes de te responder.
5. **Repete** até ficar como você quer.

## Zoom (só quando você pede)
> aplica zoom

Metade dos clipes da câmera ganha zoom (fixo nos curtos, lento nos longos), nunca dois seguidos. Tudo numa timeline nova, com um marcador por clipe.

## SFX (última passada)
Depois do visual aprovado:
> põe os SFX

O Claude marca onde vai cada som e, depois da sua aprovação, monta na trilha SFX. Os sons vêm das pastas `sfx/<slot>/`: você escolhe e coloca os arquivos.

## Render
Só quando você pedir. Muitas vezes é mais rápido você mesmo renderizar no Resolve.

## Para a próxima edição sair melhor
Cada coisa que você corrige vira uma linha em `aprendizados.md`. Ao final de cada vídeo, peça:
> revisa a sessão e propõe o que mudar no checklist

O Claude sugere mudanças no `CHECKLIST.md` e nas regras. Você aprova o que fizer sentido.
