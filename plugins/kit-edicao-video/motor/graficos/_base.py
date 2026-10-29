"""Base dos presets de gráfico do kit. Todo preset é uma página HTML 1920x1080 com fundo transparente e uma função
JavaScript update(t) que desenha o quadro do tempo t (segundos desde o início da timeline). O render abre a página
num navegador sem janela (Chromium + Playwright), chama update(t) quadro a quadro e grava uma sequência PNG.

Saída de render(itens, ...), dentro da pasta de saída:
  <nome>/<nome>_<quadro>.png  sequência numerada pelo quadro da timeline (de t0 a t1)
  montagem.json               lista para o motor/resolve/montar_camadas.py
  eventos.json                quadros de cada evento (entrada, item, destaque...) para o motor/resolve/sfx.py

Cada item precisa de: "nome" (único no vídeo), "t0" e "t1" (primeiro e último quadro na timeline) e "trilha"
(tipo de trilha do trilhas.json; padrão "texto").
"""
import json, os
from fractions import Fraction

W, H = 1920, 1080

BASE_JS = """const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));const prog=(t,t0,d)=>clamp((t-t0)/d);
const eout=x=>1-Math.pow(1-x,3);const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;const $=id=>document.getElementById(id);"""
CSS = (f"html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:transparent}}*{{box-sizing:border-box}}"
       ".abs{position:absolute}.w{display:inline-block;will-change:transform,filter,opacity}")


def carregar_marca(pasta):
    """Lê marca.json da pasta de edição da pessoa e resolve os caminhos das fontes."""
    m = json.load(open(os.path.join(pasta, "marca.json"), encoding="utf-8"))
    m["_pasta"] = os.path.abspath(pasta)
    m["_fps"] = float(Fraction(str(m.get("fps", "24000/1001"))))
    return m


def css_fontes(marca):
    """@font-face de cada fonte do marca.json. Nome no CSS = chave (titulo, texto, detalhe)."""
    out = ""
    for chave, f in marca["fontes"].items():
        arq = f["arquivo"]
        if not os.path.isabs(arq):
            arq = os.path.join(marca["_pasta"], arq)
        if not os.path.exists(arq):
            raise FileNotFoundError(f"fonte '{chave}' não encontrada: {arq}")
        out += f"@font-face{{font-family:{chave};src:url('file://{arq}')}}"
    return out


def fonte(marca, chave, tamanho, peso=None, altura=None):
    f = marca["fontes"][chave]
    p = peso or f.get("peso", 600)
    return f"font:{p} {tamanho}px{'/' + str(altura) if altura else ''} {chave}"


def pagina_html(marca, corpo, js):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css_fontes(marca)}{CSS}</style></head>"
            f"<body>{corpo}<script>{BASE_JS}function update(t){{{js}}}</script></body></html>")


def render(itens, saida, marca, pagina, pasta_no_computador=None, eventos=None, depois_de_abrir=None):
    """Gera as sequências PNG.
    pagina(item, marca) -> html completo.
    eventos(item, marca) -> lista [[quadro dentro da camada, slot], ...] (opcional).
    pasta_no_computador: caminho da pasta de saída como o Resolve vê (quando o render roda em outra máquina ou VM).
    depois_de_abrir: código JS rodado uma vez depois que a página e as fontes carregam (ex.: medir e alinhar)."""
    from playwright.sync_api import sync_playwright
    saida = os.path.abspath(saida); os.makedirs(saida, exist_ok=True)
    fps = marca["_fps"]
    nomes = [it["nome"] for it in itens]
    assert len(nomes) == len(set(nomes)), "nomes repetidos nos itens"
    mont = json.load(open(os.path.join(saida, "montagem.json"))) if os.path.exists(os.path.join(saida, "montagem.json")) else []
    evs = json.load(open(os.path.join(saida, "eventos.json"))) if os.path.exists(os.path.join(saida, "eventos.json")) else {}
    mont = [m for m in mont if m["nome"] not in nomes]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        for it in itens:
            d = os.path.join(saida, it["nome"]); os.makedirs(d, exist_ok=True)
            hp = os.path.join(saida, it["nome"] + ".html")
            open(hp, "w", encoding="utf-8").write(pagina(it, marca))
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            if depois_de_abrir:
                pg.evaluate(depois_de_abrir)
            for n in range(it["t0"], it["t1"] + 1):
                pg.evaluate(f"update({n / fps})")
                pg.screenshot(path=os.path.join(d, f"{it['nome']}_{n:05d}.png"), omit_background=True)
            mont.append({"pasta": pasta_no_computador or saida, "nome": it["nome"], "a": it["t0"], "b": it["t1"],
                         "quadro": it["t0"], "tipo": it.get("trilha", "texto")})
            if eventos:
                evs[it["nome"]] = eventos(it, marca)
            print(it["nome"], it["t0"], it["t1"], flush=True)
        br.close()
    mont.sort(key=lambda m: m["quadro"])
    json.dump(mont, open(os.path.join(saida, "montagem.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(evs, open(os.path.join(saida, "eventos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return mont


def previa(item, marca, pagina, fundo, saida_jpg, quadro=None, depois_de_abrir=None):
    """Um quadro do item sobre uma imagem de fundo (quadro real do vídeo exportado do Resolve), para aprovar antes de gerar."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    import tempfile
    q = quadro if quadro is not None else item["t0"] + int((item["t1"] - item["t0"]) * 0.6)
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        hp = os.path.join(tmp, "p.html"); open(hp, "w", encoding="utf-8").write(pagina(item, marca))
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        if depois_de_abrir:
            pg.evaluate(depois_de_abrir)
        pg.evaluate(f"update({q / marca['_fps']})")
        png = os.path.join(tmp, "c.png"); pg.screenshot(path=png, omit_background=True); br.close()
        base = Image.open(fundo).convert("RGBA").resize((W, H))
        base.alpha_composite(Image.open(png).convert("RGBA"))
        base.convert("RGB").save(saida_jpg, quality=90)
    return saida_jpg
