# Cria o projeto modelo no Resolve: configuração, pastas do Media Pool, clipes prontos da biblioteca,
# SFX por slot e uma timeline vazia com as trilhas do padrão. Todo vídeo novo nasce dele (novo_video.py).
#   result = rodar("criar_modelo.py", {"NOME": '"MODELO Canal"'})
# Recusa se o projeto já existe: nunca sobrescreve. Para refazer, renomeie ou apague o antigo no Resolve.
import json, os, glob
# ---- PARAMETROS ----
NOME = "MODELO Canal"
TIMELINE = "MODELO - trilhas"
PASTAS = ["Bruto", "Timelines", "Padrões do canal", "SFX", "B-roll", "Música", "Gráficos do vídeo"]
LARGURA, ALTURA, FPS = "1920", "1080", "23.976"   # usados só se não houver config_projeto.json
# --------------------
BIB = PASTA + "biblioteca/"
SFX = PASTA + "sfx/"
CONFIG = PASTA + "config_projeto.json"
PRIMEIRO = ["timelineFrameRate", "timelineResolutionWidth", "timelineResolutionHeight", "timelinePlaybackFrameRate",
            "timelineOutputResMatchTimelineRes", "timelineSampleRate"]

pm = resolve.GetProjectManager()
assert NOME not in (pm.GetProjectListInCurrentFolder() or []), f"projeto '{NOME}' já existe: não sobrescrevo"
if os.path.exists(CONFIG):
    cfg = json.load(open(CONFIG, encoding="utf-8"))["settings"]
else:
    cfg = {"timelineResolutionWidth": LARGURA, "timelineResolutionHeight": ALTURA, "timelineFrameRate": FPS}
atual = pm.GetCurrentProject()
if atual:
    pm.SaveProject()
p = pm.CreateProject(NOME)
assert p, "CreateProject falhou"
project = p
rel = {"projeto": p.GetName(), "config": "config_projeto.json" if os.path.exists(CONFIG) else "padrão do script", "config_falhou": []}

# 1. configuração (taxa de quadros antes de qualquer timeline)
for k in PRIMEIRO:
    if k in cfg and not p.SetSetting(k, str(cfg[k])) and str(p.GetSetting(k)) != str(cfg[k]):
        rel["config_falhou"].append(k)
for k, v in cfg.items():
    if k in PRIMEIRO or str(p.GetSetting(k)) == str(v):
        continue
    if not p.SetSetting(k, str(v)) and str(p.GetSetting(k)) != str(v):
        rel["config_falhou"].append(k)

# 2. pastas do Media Pool
mp = p.GetMediaPool(); raiz = mp.GetRootFolder(); pasta = {}
for n in PASTAS:
    pasta[n] = next((f for f in raiz.GetSubFolderList() if f.GetName() == n), None) or mp.AddSubFolder(raiz, n)

# 3. clipes prontos: cada subpasta de biblioteca/ com uma sequência <nome>_00000.png (ou .jpg)
rel["padroes"] = []
if "Padrões do canal" in pasta and os.path.isdir(BIB):
    mp.SetCurrentFolder(pasta["Padrões do canal"])
    for nome in sorted(d for d in os.listdir(BIB) if os.path.isdir(BIB + d) and not d.startswith(("_", "."))):
        qs = sorted(glob.glob(f"{BIB}{nome}/{nome}_*.png")) or sorted(glob.glob(f"{BIB}{nome}/{nome}_*.jpg"))
        if not qs:
            rel["padroes"].append([nome, "sem sequência"]); continue
        ext = qs[0].rsplit(".", 1)[1]
        nums = [int(q.rsplit("_", 1)[1].split(".")[0]) for q in qs]
        m = mp.ImportMedia([{"FilePath": f"{BIB}{nome}/{nome}_%05d.{ext}", "StartIndex": min(nums), "EndIndex": max(nums)}])
        rel["padroes"].append([nome, len(nums) if m else "FALHOU"])

# 4. SFX: uma subpasta por slot, com a versão preparada (_pronto) do primeiro arquivo
rel["sfx"] = []
if "SFX" in pasta and os.path.isdir(SFX):
    for slot in sorted(d for d in os.listdir(SFX) if os.path.isdir(SFX + d) and not d.startswith(("_", "."))):
        sub = mp.AddSubFolder(pasta["SFX"], slot)
        arqs = sorted(glob.glob(SFX + slot + "/_pronto/*.wav")) or sorted(
            f for f in glob.glob(SFX + slot + "/*") if os.path.isfile(f) and not os.path.basename(f).startswith("."))
        if not arqs:
            rel["sfx"].append([slot, "vazia"]); continue
        mp.SetCurrentFolder(sub)
        m = mp.ImportMedia([arqs[0]])
        rel["sfx"].append([slot, m[0].GetName() if m else "FALHOU"])

# 5. timeline vazia com as trilhas do padrão
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
mp.SetCurrentFolder(pasta.get("Timelines", raiz))
tl = mp.CreateEmptyTimeline(TIMELINE)
p.SetCurrentTimeline(tl)
preparar(tl)
rel["trilhas"] = {k: [tl.GetTrackName(k, i) for i in range(1, tl.GetTrackCount(k) + 1)] for k in ("video", "audio")}
rel["timeline"] = {k: tl.GetSetting(k) for k in ("timelineResolutionWidth", "timelineResolutionHeight", "timelineFrameRate")}
mp.SetCurrentFolder(pasta.get("Bruto", raiz))
pm.SaveProject()
result = rel
