"""Folha de conferência: junta quadros exportados do Resolve numa imagem só, com o nome de cada quadro embaixo.
Uso: python3 folha.py <pasta com os quadros> <saida.jpg> [colunas]"""
import os, sys
from PIL import Image, ImageDraw


def folha(pasta, saida, colunas=3, largura=640):
    arqs = sorted(f for f in os.listdir(pasta) if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff")))
    assert arqs, f"nenhum quadro em {pasta}"
    ims = [Image.open(os.path.join(pasta, f)).convert("RGB") for f in arqs]
    h = int(largura * ims[0].height / ims[0].width); faixa = 28
    linhas = (len(ims) + colunas - 1) // colunas
    out = Image.new("RGB", (colunas * largura, linhas * (h + faixa)), "white"); d = ImageDraw.Draw(out)
    for k, (f, im) in enumerate(zip(arqs, ims)):
        x, y = (k % colunas) * largura, (k // colunas) * (h + faixa)
        out.paste(im.resize((largura, h)), (x, y)); d.text((x + 8, y + h + 6), f, fill="black")
    out.save(saida, quality=88)
    return saida


if __name__ == "__main__":
    print(folha(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3))
