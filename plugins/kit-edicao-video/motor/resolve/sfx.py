# SFX por animação: última passada da edição, depois que a pessoa aprovou o visual.
# Lê a posição de cada camada na timeline e soma o tempo de cada evento dentro dela (arquivo eventos.json que os
# presets gravam ao gerar as camadas). Nunca use só os tempos do JSON: a pessoa pode ter mexido no corte.
# Modo "listar" (padrão, não altera nada): devolve a lista de sons e grava em LISTA_MD, para a pessoa aprovar na conversa.
#   result = rodar("sfx.py", {"MODO": '"listar"', "TL": '"Claude - Edicao v4"', "EVENTOS": '[...]', "LISTA_MD": '"/.../pauta_sfx_v5.md"'})
# Modo "pauta" (só se a pessoa pedir): timeline nova com um marcador azul por som.
#   result = rodar("sfx.py", {"MODO": '"pauta"', "TL": '"Claude - Edicao v4"', "TL_NOVA": '"Claude - Edicao v5 sfx"',
#                             "EVENTOS": '["/.../videos/meu_video/camadas_v1/eventos.json"]'})
# Modo "montar": numa timeline nova (TL_NOVA) ou na da pauta (TL), põe os sons na trilha "sfx" do trilhas.json,
#   um marcador ciano de resumo no começo e um ciano por som descartado por colisão.
#   result = rodar("sfx.py", {"MODO": '"montar"', "TL": '"Claude - Edicao v4"', "TL_NOVA": '"Claude - Edicao v5 sfx"',
#                             "EVENTOS": '[...]', "RODADA": '"v5"'})
# Som de cada slot: o primeiro arquivo de PASTA/sfx/<slot>/ (usa a versão _pronto/ quando existe). Pasta vazia = sem som.
import json, os, glob, re
# ---- PARAMETROS ----
MODO = "listar"
TL = None
TL_NOVA = None
EVENTOS = []            # arquivos eventos.json: {"<nome da camada>": [[quadro dentro da camada, "slot"], ...]}
TIPOS = None            # tipos de trilha onde procurar camadas (None = todas as trilhas de vídeo)
VOL_DB = -12.0
MIN_GAP = 6             # dois sons a menos de MIN_GAP quadros: fica o primeiro
LISTA_MD = None         # modo listar: arquivo .md com a lista
RODADA = ""             # ex.: "v5": começo do nome dos marcadores
APAGAR_HERDADOS = True  # montar com TL_NOVA: tira da timeline nova os marcadores do Claude de rodadas anteriores
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
    final, fora, ult = [], [], -10 ** 9
    for f, slot, nome in lista:
        if f - ult < MIN_GAP:
            fora.append((f, slot, nome)); continue
        final.append((f, slot, nome)); ult = f
    return final, fora


def duracao(mpi):
    d = mpi.GetClipProperty("Frames")
    if d and str(d).isdigit():
        return int(d)
    hh, mm, ss, ff = [int(x) for x in re.split("[:;]", mpi.GetClipProperty("Duration"))]
    fps = float(tl.GetSetting("timelineFrameRate") or 24)
    return int(((hh * 60 + mm) * 60 + ss) * round(fps) + ff)


def tc(f, fps=24):
    s = f // fps
    return f"{s // 60:02d}:{s % 60:02d}+{f % fps:02d}"


if MODO == "listar":
    tl = timeline(TL); evs, fora = coletar(tl); fps = round(float(tl.GetSetting("timelineFrameRate") or 24))
    sem = sorted({s for _, s, _ in evs if not som(s)})
    linhas = [f"| {tc(f, fps)} | {slot} | {nome} |" for f, slot, nome in evs]
    md = (f"# SFX · {TL}\n\n{len(evs)} sons; {len(fora)} descartados por colisão; slots sem som: {', '.join(sem) or 'nenhum'}.\n\n"
          "| Tempo | Slot | Camada |\n|---|---|---|\n" + "\n".join(linhas) + "\n")
    if LISTA_MD:
        open(LISTA_MD, "w", encoding="utf-8").write(md)
    result = {"timeline": TL, "sons": len(evs), "colisoes": [[tc(f, fps), s, n] for f, s, n in fora], "slots_sem_som": sem,
              "lista_md": LISTA_MD}
elif MODO == "pauta":
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
    result = {"timeline": TL_NOVA, "eventos": len(evs), "marcadores": n, "colisoes_descartadas": len(colisoes),
              "slots_sem_som": sorted(sem_som)}
elif MODO == "montar":
    tl = duplicar(TL, TL_NOVA) if TL_NOVA else timeline(TL); preparar(tl); t0 = tl.GetStartFrame(); faixa = trilha(tl, "sfx")
    if TL_NOVA and APAGAR_HERDADOS:   # timeline nova só com os marcadores desta rodada; vermelho da pessoa fica
        for _f, _m in list((tl.GetMarkers() or {}).items()):
            if str(_m.get("customData", "")).startswith("claude:"):
                tl.DeleteMarkerAtFrame(_f)
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
    pre = (RODADA + " · ") if RODADA else ""; ja = set((tl.GetMarkers() or {}).keys())
    def marca(f, nome, nota, cid):
        while f in ja:
            f += 1
        tl.AddMarker(f, "Cyan", pre + nome, nota, 1, cid); ja.add(f)
    marca(0, "SFX", f"Passada de SFX: {len(postos)} sons a {VOL_DB:g} dB na trilha SFX; {len(colisoes)} descartados por colisão.", "claude:sfx")
    for k, (f, slot, nome) in enumerate(colisoes):
        marca(f, f"SFX sem som · {slot}", f"{nome}: som a menos de {MIN_GAP} quadros do anterior; ficou o primeiro.", f"claude:sfxc{k + 1:03d}")
    result = {"timeline": TL_NOVA or TL, "postos": len(postos), "erros": erros, "colisoes_descartadas": len(colisoes)}
else:
    raise AssertionError("MODO deve ser 'listar', 'pauta' ou 'montar'")
