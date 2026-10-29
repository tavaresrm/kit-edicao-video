# Zoom na câmera · passo 1 de 2. Só quando a pessoa pede zoom.
#   result = rodar("zoom_1_plano.py", {"TL": '"Claude - Edicao v3"', "TL_NOVA": '"Claude - Edicao v4 zoom"',
#                                      "PLANO_JSON": '"/.../videos/meu_video/zoom_plano_v4.json"'})
# Duplica a timeline, escolhe os clipes da câmera pelas regras abaixo, aplica o zoom fixo (Zoom do Inspector),
# põe um marcador azul por clipe e grava o plano em JSON. O passo 2 (zoom_2_movimento.py) faz os zooms lentos,
# em OUTRO comando (Fusion criado no mesmo comando que monta o clipe não aparece no render).
# Regras padrão (ajuste no seu preset de zoom):
#   - PROPORCAO dos clipes elegíveis ganha zoom; nunca dois clipes seguidos.
#   - Elegível: clipe da trilha da câmera com MIN_DUR ou mais, menos de COBERTO coberto por trilhas que escondem a câmera,
#     sem zoom posto à mão.
#   - Clipe curto: zoom fixo (disfarça a emenda). Clipe longo: push-in; push-out quando o seguinte começa um tópico,
#     fica coberto ou é o último.
import json, math
# ---- PARAMETROS ----
TL = None
TL_NOVA = None
PLANO_JSON = None
PROPORCAO = 0.50
PUNCH = 1.12            # zoom fixo
LONGO = 4.0             # s: a partir daqui o clipe ganha zoom lento em vez de fixo
MIN_DUR = 1.0           # s: clipe mais curto fica sem zoom
MIX_PUNCH = 0.40        # parte mínima de zoom fixo no total
COBERTO = 0.2           # fração coberta acima da qual o clipe fica sem zoom
COBREM = ["broll", "fundo", "camdesl"]   # tipos de trilha que escondem a câmera
PREFIXO_CAMERA = ""     # ex.: "C0" ou "DJI" para considerar só os arquivos da câmera principal
PREFIXO_TOPICO = "topico"
# --------------------
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
assert TL and TL_NOVA and PLANO_JSON, "faltou TL, TL_NOVA ou PLANO_JSON"
tl = duplicar(TL, TL_NOVA)
preparar(tl); t0 = tl.GetStartFrame(); FPS = float(tl.GetSetting("timelineFrameRate") or 24)
cob = [(c.GetStart() - t0, c.GetEnd() - t0) for tp in COBREM if tp in _TAB
       for c in tl.GetItemListInTrack("video", trilha(tl, tp)) or []]
topicos = sorted(c.GetStart() - t0 for c in tl.GetItemListInTrack("video", trilha(tl, "texto")) or []
                 if c.GetName().startswith(PREFIXO_TOPICO)) if "texto" in _TAB else []
v1 = sorted(tl.GetItemListInTrack("video", trilha(tl, "camera")) or [], key=lambda c: c.GetStart())
clip = []
for c in v1:
    s, e = c.GetStart() - t0, c.GetEnd() - t0; d = e - s
    frac = sum(max(0, min(e, b) - max(s, a)) for a, b in cob) / max(1, d)
    ok = (c.GetName().startswith(PREFIXO_CAMERA) and d >= MIN_DUR * FPS and frac < COBERTO
          and c.GetProperty("ZoomX") in (1.0, None))
    clip.append(dict(s=s, e=e, d=d, ok=ok, it=c))
# escolha: em cada sequência de elegíveis, um sim e um não, começando pelo lado de clipes mais longos
alvo = math.floor(PROPORCAO * sum(1 for c in clip if c["ok"]) + 0.5); esc = []; i = 0
while i < len(clip):
    if not clip[i]["ok"]:
        i += 1; continue
    j = i
    while j < len(clip) and clip[j]["ok"]:
        j += 1
    run = list(range(i, j)); par = run[0::2]; impar = run[1::2]
    esc += par if sum(clip[k]["d"] for k in par) >= sum(clip[k]["d"] for k in impar) else impar
    i = j
esc = sorted(sorted(esc, key=lambda k: -clip[k]["d"])[:alvo])
plano = {}
for k in esc:
    c = clip[k]
    if c["d"] < LONGO * FPS:
        tipo = "punch"
    else:
        prox = clip[k + 1] if k + 1 < len(clip) else None
        fecha = prox is None or not prox["ok"] or any(prox["s"] - 2 <= tp < prox["e"] for tp in topicos)
        tipo = "push_out" if fecha else "push_in"
    plano[c["s"]] = tipo
# equilíbrio: com pouco zoom fixo, zooms lentos alternados viram fixo até chegar em MIX_PUNCH
lentos = [s for s in sorted(plano) if plano[s] != "punch"]
for n, s in enumerate(lentos):
    if sum(1 for t in plano.values() if t == "punch") >= MIX_PUNCH * len(plano):
        break
    if n % 2 == 1:
        plano[s] = "punch"
for k in esc:
    c = clip[k]
    if plano[c["s"]] == "punch":
        c["it"].SetProperty("ZoomX", PUNCH); c["it"].SetProperty("ZoomY", PUNCH)
ja = set((tl.GetMarkers() or {}).keys())
NOTA = {"punch": f"Zoom fixo {PUNCH:.2f}", "push_in": "Zoom lento de entrada", "push_out": "Zoom lento de saída (fecha a ideia)"}
for s, tipo in plano.items():
    c = next(x for x in clip if x["s"] == s); f = s
    while f in ja:
        f += 1
    tl.AddMarker(f, "Blue", f"Zoom · {tipo.replace('_', '-')}", f"{NOTA[tipo]}. {c['d'] / FPS:.1f} s.", max(1, c["e"] - f), f"claude:z{s}")
    ja.add(f)
json.dump({"timeline": TL_NOVA, "plano": plano}, open(PLANO_JSON, "w", encoding="utf-8"), indent=1)
n_ok = sum(1 for c in clip if c["ok"])
result = {"timeline": TL_NOVA, "clipes": len(clip), "elegiveis": n_ok, "com_zoom": len(plano),
          "tipos": {t: list(plano.values()).count(t) for t in NOTA}, "seguidos": sum(1 for k in esc if k + 1 in esc)}
