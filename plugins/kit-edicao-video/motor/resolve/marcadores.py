# Marcadores: ler o que a pessoa marcou e escrever a pauta do Claude.
# Modo "ler" (não altera nada):
#   result = rodar("marcadores.py", {"MODO": '"ler"', "TL": '"Claude - Edicao v1"'})
#   Devolve os marcadores da timeline E os de dentro dos clipes (marcador dentro de clipe também é pedido),
#   com quadro relativo ao início da timeline, cor, nome, nota e customData.
# Modo "pauta" (cria timeline nova a partir da base e escreve um marcador por item):
#   result = rodar("marcadores.py", {"MODO": '"pauta"', "TL": '"Bruto"', "TL_NOVA": '"Claude - Edicao pauta v1"',
#                                    "PAUTA_JSON": '"/.../videos/meu_video/pauta_v1.json"'})
#   PAUTA_JSON: lista de {"quadro", "duracao", "cor", "nome", "nota", "id"} (quadros desde o início da timeline).
import json
# ---- PARAMETROS ----
MODO = "ler"
TL = None
TL_NOVA = None
PAUTA_JSON = None
APAGAR_HERDADOS = True    # no modo pauta, tira da timeline NOVA os marcadores do Claude herdados da base (customData "claude:")
# --------------------
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
assert TL, "faltou TL"

if MODO == "ler":
    tl = timeline(TL); t0 = tl.GetStartFrame()
    mt = [{"onde": "timeline", "quadro": f, "cor": m["color"], "nome": m["name"], "nota": m["note"],
           "duracao": m["duration"], "custom": m.get("customData", "")} for f, m in sorted((tl.GetMarkers() or {}).items())]
    mc = []
    for kind in ("video", "audio"):
        for i in range(1, tl.GetTrackCount(kind) + 1):
            for c in tl.GetItemListInTrack(kind, i) or []:
                for f, m in sorted((c.GetMarkers() or {}).items()):
                    # f é contado a partir do início do clipe na timeline, não do começo da mídia (Resolve Studio 21.1:
                    # AddMarker em f=30 funcionou num clipe com 420 quadros da mídia cortados antes do início).
                    q = c.GetStart() - t0 + int(f)
                    mc.append({"onde": f"clipe {c.GetName()} ({kind} {i})", "quadro": q, "quadro_no_clipe": int(f),
                               "cor": m["color"], "nome": m["name"],
                               "nota": m["note"], "duracao": m["duration"], "custom": m.get("customData", "")})
    result = {"timeline": TL, "da_timeline": mt, "dos_clipes": mc,
              "da_pessoa": [m for m in mt + mc if not str(m["custom"]).startswith("claude:")]}

elif MODO == "pauta":
    assert TL_NOVA and PAUTA_JSON, "faltou TL_NOVA ou PAUTA_JSON"
    pauta = json.load(open(PAUTA_JSON, encoding="utf-8"))
    tl = duplicar(TL, TL_NOVA); t0 = tl.GetStartFrame()
    if APAGAR_HERDADOS:
        for f, m in list((tl.GetMarkers() or {}).items()):
            if str(m.get("customData", "")).startswith("claude:"):
                tl.DeleteMarkerAtFrame(f)
    ja = set((tl.GetMarkers() or {}).keys()); postos, falhou = [], []
    for k, p in enumerate(pauta):
        f = int(p["quadro"])
        while f in ja:
            f += 1                                  # dois marcadores não cabem no mesmo quadro
        ok = tl.AddMarker(f, p.get("cor", "Blue"), p["nome"][:60], p.get("nota", ""), max(1, int(p.get("duracao", 1))),
                          "claude:" + p.get("id", f"p{k + 1:02d}"))
        (postos if ok else falhou).append([p.get("id"), f]); ja.add(f)
    result = {"timeline": TL_NOVA, "postos": len(postos), "falharam": falhou}
else:
    raise AssertionError("MODO deve ser 'ler' ou 'pauta'")
