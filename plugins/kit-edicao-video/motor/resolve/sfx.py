# SFX por animação: última passada da edição, depois que a pessoa aprovou o visual.
# Lê a posição de cada camada na timeline e soma o tempo de cada evento dentro dela (arquivo eventos.json que os
# presets gravam ao gerar as camadas). Nunca use só os tempos do JSON: a pessoa pode ter mexido no corte.
# Modo "pauta": timeline nova com um marcador azul por som (para aprovação).
#   result = rodar("sfx.py", {"MODO": '"pauta"', "TL": '"Claude - Edicao v4"', "TL_NOVA": '"Claude - Edicao v5 sfx"',
#                             "EVENTOS": '["/.../videos/meu_video/camadas_v1/eventos.json"]'})
# Modo "montar": põe os sons na timeline da pauta aprovada (trilha "sfx" do trilhas.json).
#   result = rodar("sfx.py", {"MODO": '"montar"', "TL": '"Claude - Edicao v5 sfx"', "EVENTOS": '[...]'})
# Som de cada slot: o primeiro arquivo de PASTA/sfx/<slot>/ (usa a versão _pronto/ quando existe). Pasta vazia = sem som.
import json, os, glob, re
# ---- PARAMETROS ----
MODO = "pauta"
TL = None
TL_NOVA = None
EVENTOS = []            # arquivos eventos.json: {"<nome da camada>": [[quadro dentro da camada, "slot"], ...]}
TIPOS = None            # tipos de trilha onde procurar camadas (None = todas as trilhas de vídeo)
VOL_DB = -12.0
MIN_GAP = 6             # dois sons a menos de MIN_GAP quadros: fica o primeiro
# --------------------
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
assert TL and EVENTOS, "faltou TL ou EVENTOS"
SFX = PASTA + "sfx/"
ev = {}
for arq in EVENTOS:
    ev.update(json.load(open(arq, encoding="utf-8")))


def som(slot):
    d = SFX + slot + "/"
    if not os.path.isdir(d):
        return None
    a = sorted(glob.glob(d + "_pronto/*.wav")) or sorted(
        f for f in glob.glob(d + "*") if os.path.isfile(f) and not os.path.basename(f).startswith("."))
    return a[0] if a else None


def coletar(tl):
    t0 = tl.GetStartFrame(); lista = []
    tipos = TIPOS or [t for t, (k, *_ ) in _TAB.items() if k == "video"]
    for tp in tipos:
        for c in tl.GetItemListInTrack("video", trilha(tl, tp)) or []:
            nome = next((n for n in ev if c.GetName().startswith(n + "_") or c.GetName() == n), None)
            if not nome:
                continue
            s, e, left = c.GetStart() - t0, c.GetEnd() - t0, c.GetLeftOffset()
            for off, slot in ev[nome]:
                f = s + int(off) - left
                if s <= f < e:
                    lista.append((f, slot, nome))
    lista.sort()
    final, ult = [], -10 ** 9
    for f, slot, nome in lista:
        if f - ult < MIN_GAP:
            continue
        final.append((f, slot, nome)); ult = f
    return final, len(lista) - len(final)


def duracao(mpi):
    d = mpi.GetClipProperty("Frames")
    if d and str(d).isdigit():
        return int(d)
    hh, mm, ss, ff = [int(x) for x in re.split("[:;]", mpi.GetClipProperty("Duration"))]
    fps = float(tl.GetSetting("timelineFrameRate") or 24)
    return int(((hh * 60 + mm) * 60 + ss) * round(fps) + ff)


if MODO == "pauta":
    assert TL_NOVA, "faltou TL_NOVA"
    tl = duplicar(TL, TL_NOVA); preparar(tl)
    evs, colisoes = coletar(tl); ja = set((tl.GetMarkers() or {}).keys()); n = 0; sem_som = set()
    for k, (f, slot, nome) in enumerate(evs):
        if not som(slot):
            sem_som.add(slot)
        q = f
        while q in ja:
            q += 1
        if tl.AddMarker(q, "Blue", f"SFX {slot}", f"{nome} · som de sfx/{slot} a {VOL_DB:g} dB", 1, f"claude:sfx{k + 1:03d}"):
            n += 1; ja.add(q)
    result = {"timeline": TL_NOVA, "eventos": len(evs), "marcadores": n, "colisoes_descartadas": colisoes,
              "slots_sem_som": sorted(sem_som)}
elif MODO == "montar":
    tl = timeline(TL); preparar(tl); t0 = tl.GetStartFrame(); faixa = trilha(tl, "sfx")
    mp = project.GetMediaPool(); raiz = mp.GetRootFolder()
    pasta = next((f for f in raiz.GetSubFolderList() if f.GetName() == "SFX"), None) or mp.AddSubFolder(raiz, "SFX")
    mp.SetCurrentFolder(pasta)
    evs, colisoes = coletar(tl); cache = {}; postos, erros = [], []
    for f, slot, nome in evs:
        arq = som(slot)
        if not arq:
            continue
        if arq not in cache:
            m = mp.ImportMedia([arq]); cache[arq] = m[0] if m else None
        mpi = cache[arq]
        if not mpi:
            erros.append([f, slot, "ImportMedia falhou"]); continue
        r = mp.AppendToTimeline([{"mediaPoolItem": mpi, "startFrame": 0, "endFrame": duracao(mpi), "mediaType": 2,
                                  "trackIndex": faixa, "recordFrame": t0 + f}])
        if not r:
            erros.append([f, slot, "AppendToTimeline falhou"]); continue
        it = r[0]; it.SetProperty("AudioVolume", VOL_DB); colorir(it, "sfx")
        postos.append([f, slot, it.GetStart() - t0])
    result = {"timeline": TL, "postos": len(postos), "erros": erros, "colisoes_descartadas": colisoes}
else:
    raise AssertionError("MODO deve ser 'pauta' ou 'montar'")
