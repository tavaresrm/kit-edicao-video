# Zoom na câmera · passo 2 de 2 (em outro comando, DEPOIS do zoom_1_plano.py).
#   result = rodar("zoom_2_movimento.py", {"PLANO_JSON": '"/.../videos/meu_video/zoom_plano_v4.json"'})
# Zoom lento de entrada (100% -> LENTO) e de saída (LENTO -> 100%) no clipe inteiro, por Fusion Transform (Size),
# com entrada e saída suaves.
import json
# ---- PARAMETROS ----
PLANO_JSON = None
LENTO = 1.08
# --------------------
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
assert PLANO_JSON, "faltou PLANO_JSON"
dados = json.load(open(PLANO_JSON, encoding="utf-8"))
tl = timeline(dados["timeline"]); t0 = tl.GetStartFrame()
v1 = {c.GetStart() - t0: c for c in tl.GetItemListInTrack("video", trilha(tl, "camera")) or []}
log, erros = [], []
for s, tipo in sorted((int(k), v) for k, v in dados["plano"].items()):
    if tipo == "punch":
        continue
    if s not in v1:
        erros.append([s, "clipe não achado (o corte mudou?)"]); continue
    z0, z1 = (1.0, LENTO) if tipo == "push_in" else (LENTO, 1.0)
    it = v1[s]
    for nm in list(it.GetFusionCompNameList() or []):
        it.DeleteFusionCompByName(nm)
    comp = it.AddFusionComp(); at = comp.GetAttrs()
    c0, c1 = int(at["COMPN_RenderStart"]), int(at["COMPN_RenderEnd"])
    mi, mo = comp.FindTool("MediaIn1"), comp.FindTool("MediaOut1")
    tr = comp.AddTool("Transform", -32768, -32768); tr.Input = mi.Output; mo.Input = tr.Output
    sz = comp.BezierSpline(); tr.Size = sz; h = (c1 - c0) / 3.0
    sz.SetKeyFrames({c0: {1: z0, "RH": {1: h, 2: 0}}, c1: {1: z1, "LH": {1: -h, 2: 0}}}, True)
    log.append([s, tipo, round(tr.Size[c0], 3), round(tr.Size[c1], 3)])
result = {"timeline": dados["timeline"], "feitos": log, "erros": erros}
