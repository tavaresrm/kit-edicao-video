"""Preset de EXEMPLO do kit: texto sobre o vídeo (tópico, frase e lista).
Serve para ver o kit funcionando e como ponto de partida. Fontes, cores, escala e margens vêm do seu marca.json;
o desenho e a animação são deste arquivo. Para criar o seu preset, use a skill criar-preset: ela copia este arquivo
para presets/codigo/ na sua pasta e muda o que você pedir.

Uso:
  python3 texto.py <pasta de edição> itens.json <pasta de saída> [--pasta-no-computador CAMINHO]
  python3 texto.py <pasta de edição> itens.json --previa quadro_do_video.png previa.jpg

Item (quadros contados desde o início da timeline):
  {"nome": "topico_01", "tipo": "topico", "t0": 120, "t1": 250, "kicker": "CAPÍTULO 1", "titulo": "O começo"}
  {"nome": "frase_01", "tipo": "frase", "t0": 300, "t1": 420, "palavras": [["Ninguém", 306], ["te", 312], ...],
   "destaque": "palavras exatas"}
  {"nome": "lista_01", "tipo": "lista", "t0": 500, "t1": 700, "titulo": "Três coisas", "itens": [["Primeira", 520], ...]}
Opcional em todos: "layout": "lado" | "centro" (centro = embaixo, para vídeo com duas pessoas no quadro),
"lado": "dir" | "esq" (padrão: lado_livre do marca.json), "trilha" (padrão "texto").
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _base import carregar_marca, pagina_html, render, previa, fonte

LIM = dict(kicker=24, titulo=34, frase=90, lista_titulo=36, item=32)


def chk(k, s):
    if len(s) > LIM[k]:
        raise ValueError(f"{k} passa de {LIM[k]} caracteres: {s}")


def _c(m, k, padrao):
    return m.get("cores", {}).get(k, padrao)


def _sombra(m):
    return f"text-shadow:0 2px 18px {_c(m, 'sombra', 'rgba(0,0,0,.55)')},0 1px 3px rgba(0,0,0,.4)"


def _caixa(m, it, inner):
    """Posiciona o bloco: no lado livre (alinhado à margem) ou no centro embaixo. Escala pelo marca.json."""
    k = m.get("escala", 1.0); mg = m.get("margem", 96)
    if it.get("layout", m.get("layout", "lado")) == "centro":
        return (f'<div class="abs" style="left:0;right:0;bottom:{mg}px;display:flex;justify-content:center;'
                f'transform-origin:50% 100%;transform:scale({k})"><div style="text-align:center">{inner}</div></div>')
    lado = it.get("lado", m.get("lado_livre", "dir"))
    pos = f"right:{mg}px;transform-origin:100% 0" if lado == "dir" else f"left:{mg}px;transform-origin:0 0"
    return f'<div class="abs" style="{pos};top:{it.get("top", 260)}px;transform:scale({k})">{inner}</div>'


def _tempos(m, it):
    fps = m["_fps"]; a = m.get("animacao", {})
    return it["t0"] / fps, (it["t1"] + 1) / fps, a.get("entrada_s", 0.5), a.get("saida_s", 0.4)


def topico(it, m):
    chk("kicker", it["kicker"]); chk("titulo", it["titulo"])
    centro = it.get("layout", m.get("layout", "lado")) == "centro"
    k = m.get("escala", 1.0); mg = m.get("margem", 96)
    pos = (f"left:0;right:0;bottom:{mg}px;text-align:center;transform-origin:50% 100%" if centro
           else f"left:{mg}px;bottom:{mg}px;transform-origin:0 100%")
    corpo = (f'<div id="tp" class="abs" style="{pos};transform:scale({k})">'
             f'<div id="et" style="display:inline-block;padding:6px 14px;border-radius:4px;background:{_c(m, "destaque", "#3DDC97")};'
             f'color:{_c(m, "texto_sobre_destaque", "#0B0B0B")};{fonte(m, "detalhe", 20, 700)};letter-spacing:.12em">{it["kicker"]}</div>'
             f'<div id="ti" style="{fonte(m, "titulo", 58, None, 1.05)};color:{_c(m, "texto", "#FFFFFF")};margin-top:12px;'
             f'white-space:nowrap;{_sombra(m)}">{it["titulo"]}</div></div>')
    T0, T1, E, S = _tempos(m, it)
    js = (f"const T0={T0},T1={T1},E={E},S={S};const q=eio(prog(t,T1-S,S));"
          "$('tp').style.opacity=clamp(prog(t,T0,E*.6))*(1-q);"
          "$('et').style.clipPath=`inset(0 ${(1-eout(prog(t,T0,E)))*100}% 0 0)`;"
          "const a=eout(prog(t,T0+.1,E));$('ti').style.transform=`translateY(${(1-a)*18}px)`;$('ti').style.opacity=a;")
    return pagina_html(m, corpo, js)


def _achar(palavras, destaque):
    ws = [w.strip(".,!?;:").lower() for w, _ in palavras]; d = destaque.lower().split()
    for i in range(len(ws) - len(d) + 1):
        if ws[i:i + len(d)] == d:
            return i, i + len(d) - 1
    raise ValueError(f"destaque não achado na frase: {destaque}")


def frase(it, m):
    txt = " ".join(w for w, _ in it["palavras"]); chk("frase", txt)
    i0, i1 = _achar(it["palavras"], it["destaque"]) if it.get("destaque") else (None, None)
    spans = []
    for i, (w, _) in enumerate(it["palavras"]):
        dentro = i0 is not None and i0 <= i <= i1
        fundo = (f'<span id="h{i}" class="abs" style="left:-6px;right:-6px;top:8%;bottom:4%;border-radius:4px;'
                 f'background:{_c(m, "destaque", "#3DDC97")};transform-origin:left;transform:scaleX(0);z-index:-1"></span>') if dentro else ""
        spans.append(f'<span class="w" id="w{i}" style="position:relative;isolation:isolate;opacity:0">{fundo}{w}</span>')
    centro = it.get("layout", m.get("layout", "lado")) == "centro"
    larg = 1200 if centro else 640
    inner = (f'<div id="fr" style="width:{larg}px;{fonte(m, "titulo", 60, None, 1.18)};color:{_c(m, "texto", "#FFFFFF")};'
             f'{"text-align:center;" if centro else ""}{_sombra(m)};isolation:isolate">{" ".join(spans)}</div>')
    T0, T1, E, S = _tempos(m, it)
    tw = [f / m["_fps"] for _, f in it["palavras"]]
    js = (f"const T0={T0},T1={T1},S={S};const TW={json.dumps(tw)};const q=eio(prog(t,T1-S,S));$('fr').style.opacity=1-q;"
          "for(let i=0;i<TW.length;i++){const p=eout(prog(t,TW[i]-0.12,0.45));const e=$('w'+i);e.style.opacity=p;"
          "e.style.transform=`translateY(${(1-p)*14}px)`;}")
    if i0 is not None:
        js += (f"for(let i={i0};i<={i1};i++){{const h=$('h'+i);if(h)h.style.transform=`scaleX(${{eio(prog(t,TW[{i1}]+0.2+(i-{i0})*0.08,0.35))}})`;}}"
               f"for(let i={i0};i<={i1};i++){{const p=prog(t,TW[{i1}]+0.2,0.3);$('w'+i).style.color=p>0.5?'{_c(m, 'texto_sobre_destaque', '#0B0B0B')}':'';"
               f"$('w'+i).style.textShadow=p>0.5?'none':'';}}")
    return pagina_html(m, _caixa(m, it, inner), js)


def lista(it, m):
    chk("lista_titulo", it["titulo"]); [chk("item", s) for s, _ in it["itens"]]
    centro = it.get("layout", m.get("layout", "lado")) == "centro"
    dest = _c(m, "destaque", "#3DDC97"); cor = _c(m, "texto", "#FFFFFF")
    if centro:
        rows = "".join(f'<div id="i{i}" style="display:flex;align-items:center;gap:12px;padding:0 22px;opacity:0;'
                       f'{fonte(m, "texto", 32)};color:{cor};white-space:nowrap;{_sombra(m)}">'
                       f'<span style="width:12px;height:12px;border-radius:2px;background:{dest}"></span>{s}</div>'
                       for i, (s, _) in enumerate(it["itens"]))
        rows = f'<div style="display:flex;justify-content:center">{rows}</div>'
    else:
        rows = "".join(f'<div id="i{i}" style="display:flex;align-items:center;gap:16px;padding:10px 0;opacity:0;'
                       f'{fonte(m, "texto", 34)};color:{cor};white-space:nowrap;{_sombra(m)}">'
                       f'<span style="width:14px;height:14px;border-radius:2px;background:{dest};flex:none"></span>{s}</div>'
                       for i, (s, _) in enumerate(it["itens"]))
    inner = (f'<div id="ls"><div id="lt" style="{fonte(m, "titulo", 50, None, 1.08)};color:{cor};margin-bottom:16px;'
             f'{_sombra(m)}">{it["titulo"]}</div>{rows}</div>')
    T0, T1, E, S = _tempos(m, it)
    ti = [f / m["_fps"] for _, f in it["itens"]]
    js = (f"const T0={T0},T1={T1},E={E},S={S};const TI={json.dumps(ti)};const q=eio(prog(t,T1-S,S));"
          "$('ls').style.opacity=clamp(prog(t,T0,E*.6))*(1-q);const a=eout(prog(t,T0,E));"
          "$('lt').style.transform=`translateY(${(1-a)*16}px)`;"
          "for(let i=0;i<TI.length;i++){const p=eout(prog(t,TI[i]-0.3,0.45));const e=$('i'+i);e.style.opacity=p;"
          "e.style.transform=`translateX(${(1-p)*-16}px)`;}")
    return pagina_html(m, _caixa(m, it, inner), js)


TIPOS = {"topico": topico, "frase": frase, "lista": lista}


def pagina(it, m):
    return TIPOS[it["tipo"]](it, m)


def eventos(it, m):
    """Quadros (dentro da camada) em que cada animação acontece, para o SFX."""
    fps = m["_fps"]; ev = [[0, "entra"]]
    if it["tipo"] == "frase" and it.get("destaque"):
        i0, i1 = _achar(it["palavras"], it["destaque"])
        ev.append([it["palavras"][i1][1] - it["t0"] + int(0.2 * fps), "destaque"])
    if it["tipo"] == "lista":
        ev += [[max(0, f - it["t0"] - int(0.3 * fps)), "item"] for _, f in it["itens"]]
    return ev


if __name__ == "__main__":
    a = sys.argv[1:]
    marca = carregar_marca(a[0]); itens = json.load(open(a[1], encoding="utf-8"))
    if "--previa" in a:
        k = a.index("--previa")
        for it in itens:
            saida = a[k + 2].replace(".jpg", f"_{it['nome']}.jpg") if len(itens) > 1 else a[k + 2]
            print(previa(it, marca, pagina, a[k + 1], saida))
    else:
        pc = a[a.index("--pasta-no-computador") + 1] if "--pasta-no-computador" in a else None
        render(itens, a[2], marca, pagina, pasta_no_computador=pc, eventos=eventos)
