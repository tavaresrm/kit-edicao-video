# Vídeo novo a partir do projeto modelo (criar_modelo.py).
#   result = rodar("novo_video.py", {"NOME": '"Título do vídeo"', "BRUTO": '["/Volumes/SSD/C0001.MP4", "/Volumes/SSD/C0002.MP4"]'})
# Faz: exporta o modelo (.drp), importa uma cópia com o nome do vídeo, importa o bruto na pasta Bruto e cria a
# timeline "Bruto" (cópia da timeline do modelo) com os vídeos em ordem na trilha da câmera e o som na trilha de voz.
# Arquivo só de áudio (gravador) entra na pasta Bruto e fica fora da timeline: sincronizar antes da decupagem.
# Nunca altera projeto existente: recusa se NOME já existe.
import os
# ---- PARAMETROS ----
NOME = None
BRUTO = []
MODELO = "MODELO Canal"
TIMELINE_MODELO = "MODELO - trilhas"
# --------------------
DRP = PASTA + "_modelo_export.drp"     # sobrescrito a cada vídeo novo (sempre o modelo atual)
VIDEO_EXT = (".mp4", ".mov", ".mxf", ".mts", ".m4v", ".braw", ".r3d")

assert NOME, "faltou NOME"
assert BRUTO, "faltou BRUTO"
falta = [b for b in BRUTO if not os.path.exists(b)]
assert not falta, f"arquivo do bruto não existe: {falta}"
pm = resolve.GetProjectManager()
lista = pm.GetProjectListInCurrentFolder() or []
assert MODELO in lista, f"projeto '{MODELO}' não existe: rode criar_modelo.py antes"
assert NOME not in lista, f"projeto '{NOME}' já existe: não mexo"
if pm.GetCurrentProject():
    pm.SaveProject()

# 1. cópia do modelo
assert pm.ExportProject(MODELO, DRP, False), "ExportProject falhou"
assert pm.ImportProject(DRP, NOME), "ImportProject falhou"
p = pm.LoadProject(NOME)
assert p and p.GetName() == NOME, "LoadProject falhou"
project = p
mp = p.GetMediaPool(); raiz = mp.GetRootFolder()
pasta = {f.GetName(): f for f in raiz.GetSubFolderList()}

# 2. bruto
mp.SetCurrentFolder(pasta.get("Bruto", raiz))
itens = mp.ImportMedia(BRUTO) or []
por_arq = {i.GetClipProperty("File Path"): i for i in itens}
videos = [por_arq[b] for b in BRUTO if b in por_arq and b.lower().endswith(VIDEO_EXT)]

# 3. timeline Bruto a partir da timeline do modelo
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
base = timeline(TIMELINE_MODELO)
mp.SetCurrentFolder(pasta.get("Timelines", raiz))
tl = base.DuplicateTimeline("Bruto")
p.SetCurrentTimeline(tl)
assert p.GetCurrentTimeline().GetName() == "Bruto"
preparar(tl)
postos = mp.AppendToTimeline(videos) if videos else []
for c in tl.GetItemListInTrack("video", trilha(tl, "camera")) or []:
    colorir(c, "camera")
for c in tl.GetItemListInTrack("audio", trilha(tl, "voz")) or []:
    colorir(c, "voz")
pm.SaveProject()
result = {
    "projeto": p.GetName(),
    "importados": len(itens), "na_timeline": len(postos or []),
    "fora_da_timeline": [i.GetName() for i in itens if i not in videos],
    "camera": [(c.GetName(), c.GetStart(), c.GetEnd()) for c in tl.GetItemListInTrack("video", 1) or []],
    "trilhas": {k: [tl.GetTrackName(k, i) for i in range(1, tl.GetTrackCount(k) + 1)] for k in ("video", "audio")},
}
