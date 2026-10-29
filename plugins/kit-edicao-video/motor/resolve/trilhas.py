# Padrão de trilhas da timeline. Fonte única para todos os scripts de montagem.
# Lê o padrão de PASTA + "trilhas.json" (o seu arquivo; o kit traz um modelo).
# Dentro de um script do kit:
#   exec(open(KIT + "resolve/trilhas.py").read())
#   preparar(tl)               # cria e nomeia as trilhas que faltam; recusa timeline fora do padrão
#   t = trilha(tl, "texto")    # índice da trilha pelo tipo
#   livre(tl, "texto", a, b)   # confere que a trilha está livre de a até b (quadros absolutos, b exclusivo)
#   colorir(item, "texto")     # cor do clipe pelo tipo
import json as _json

_CFG = _json.load(open(PASTA + "trilhas.json", encoding="utf-8"))
VIDEO = [(t["tipo"], i + 1, t["nome"], t.get("cor")) for i, t in enumerate(_CFG["video"])]
AUDIO = [(t["tipo"], i + 1, t["nome"], t.get("cor")) for i, t in enumerate(_CFG["audio"])]
_TAB = {t: ("video", i, n, c) for t, i, n, c in VIDEO}
_TAB.update({t: ("audio", i, n, c) for t, i, n, c in AUDIO})


def preparar(tl):
    """Garante as trilhas do padrão. Trilha vazia ou com nome padrão do Resolve é renomeada.
    Trilha com clipes e outro nome para o script: a timeline está fora do padrão e precisa ser reorganizada antes."""
    feito = []
    for kind, lista in (("video", VIDEO), ("audio", AUDIO)):
        while tl.GetTrackCount(kind) < len(lista):
            tl.AddTrack(kind, "stereo") if kind == "audio" else tl.AddTrack(kind)
        for _, i, nome, _ in lista:
            atual = tl.GetTrackName(kind, i)
            if atual == nome:
                continue
            ocupada = bool(tl.GetItemListInTrack(kind, i))
            nome_padrao = atual in (f"Video {i}", f"Audio {i}", f"V{i}", f"A{i}")
            if i == 1 or not ocupada or nome_padrao:
                tl.SetTrackName(kind, i, nome)
                feito.append([kind, i, atual, nome])
            else:
                raise AssertionError(f"timeline fora do padrão: {kind} {i} chama '{atual}' e tem clipes. Reorganize antes.")
    # clipe sem cor ganha a cor do tipo da trilha (cor posta à mão fica como está)
    for kind, lista in (("video", VIDEO), ("audio", AUDIO)):
        for _, i, _, cor in lista:
            if not cor:
                continue
            for c in tl.GetItemListInTrack(kind, i) or []:
                if not c.GetClipColor():
                    c.SetClipColor(cor)
    return feito


def trilha(tl, tipo):
    kind, i, nome, _ = _TAB[tipo]
    assert tl.GetTrackName(kind, i) == nome, f"{kind} {i} deveria ser '{nome}' e é '{tl.GetTrackName(kind, i)}': rode preparar(tl)"
    return i


def livre(tl, tipo, a, b):
    kind, i, _, _ = _TAB[tipo]
    oc = [x.GetName() for x in tl.GetItemListInTrack(kind, trilha(tl, tipo)) or [] if x.GetStart() < b and x.GetEnd() > a]
    assert not oc, f"trilha {tipo} ocupada entre {a} e {b}: {oc[:3]}"


def colorir(item, tipo):
    cor = _TAB[tipo][3]
    return item.SetClipColor(cor) if cor and item else False


def timeline(nome):
    """Abre a timeline pelo nome e confere que ela ficou aberta (o Resolve pode trocar a timeline entre comandos)."""
    tls = {project.GetTimelineByIndex(i).GetName(): project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1)}
    assert nome in tls, f"timeline '{nome}' não existe"
    project.SetCurrentTimeline(tls[nome])
    assert project.GetCurrentTimeline().GetName() == nome
    return tls[nome]


def duplicar(base, nova):
    """Timeline nova a partir de outra. A base nunca é alterada; recusa se a nova já existe."""
    nomes = [project.GetTimelineByIndex(i).GetName() for i in range(1, project.GetTimelineCount() + 1)]
    assert nova not in nomes, f"timeline '{nova}' já existe: escolha outro nome"
    tl = timeline(base).DuplicateTimeline(nova)
    assert tl, "DuplicateTimeline falhou"
    project.SetCurrentTimeline(tl)
    assert project.GetCurrentTimeline().GetName() == nova
    return tl
