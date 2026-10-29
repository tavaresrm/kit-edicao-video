# Monta camadas (sequências PNG transparentes geradas pelos presets) numa timeline, cada uma na trilha do seu tipo.
#   result = rodar("montar_camadas.py", {"TL": '"Claude - Edicao v1"', "LISTA_JSON": '"/.../videos/meu_video/camadas_v1/montagem.json"'})
# LISTA_JSON: lista de {"pasta", "nome", "a", "b", "quadro", "tipo"}:
#   pasta  = pasta absoluta que contém a subpasta <nome>/ com <nome>_00000.png...
#   a, b   = primeiro e último número de quadro dos arquivos
#   quadro = onde a camada começa na timeline (quadros desde o início da timeline)
#   tipo   = tipo de trilha do trilhas.json (ex.: "texto")
# Se TL_NOVA for dado, monta numa cópia da TL (a TL nunca é alterada). Sem TL_NOVA, monta na própria TL:
# use isso só numa timeline criada nesta rodada.
import json, os
# ---- PARAMETROS ----
TL = None
TL_NOVA = None
LISTA_JSON = None
PASTA_MP = "Gráficos do vídeo"
# --------------------
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
assert TL and LISTA_JSON, "faltou TL ou LISTA_JSON"
itens = json.load(open(LISTA_JSON, encoding="utf-8"))
tl = duplicar(TL, TL_NOVA) if TL_NOVA else timeline(TL)
preparar(tl)
mp = project.GetMediaPool(); raiz = mp.GetRootFolder()
pasta = next((f for f in raiz.GetSubFolderList() if f.GetName() == PASTA_MP), None) or mp.AddSubFolder(raiz, PASTA_MP)
mp.SetCurrentFolder(pasta)
t0 = tl.GetStartFrame(); log, erros = [], []
for it in itens:
    nome, a, b, tipo = it["nome"], int(it["a"]), int(it["b"]), it["tipo"]
    base = it["pasta"].rstrip("/") + "/"
    rs, re_ = t0 + int(it["quadro"]), t0 + int(it["quadro"]) + (b - a) + 1
    if not os.path.exists(f"{base}{nome}/{nome}_{a:05d}.png"):
        erros.append([nome, "arquivo não existe", f"{base}{nome}/{nome}_{a:05d}.png"]); continue
    try:
        livre(tl, tipo, rs, re_)
    except AssertionError as e:
        erros.append([nome, str(e)]); continue
    m = mp.ImportMedia([{"FilePath": f"{base}{nome}/{nome}_%05d.png", "StartIndex": a, "EndIndex": b}])
    if not m:
        erros.append([nome, "ImportMedia falhou"]); continue
    r = mp.AppendToTimeline([{"mediaPoolItem": m[0], "startFrame": a, "endFrame": b + 1, "trackIndex": trilha(tl, tipo),
                              "recordFrame": rs, "mediaType": 1}])
    if not r:
        erros.append([nome, "AppendToTimeline falhou"]); continue
    c = r[0]
    if (c.GetStart(), c.GetEnd()) != (rs, re_):
        erros.append([nome, "posição diferente", c.GetStart() - t0, c.GetEnd() - t0, rs - t0, re_ - t0])
    colorir(c, tipo); log.append([nome, tipo, c.GetStart() - t0, c.GetEnd() - t0])
result = {"timeline": tl.GetName(), "montados": len(log), "erros": erros, "itens": log}
