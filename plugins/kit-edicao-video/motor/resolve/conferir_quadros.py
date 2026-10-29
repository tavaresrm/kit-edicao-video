# Exporta quadros da própria timeline do Resolve para conferência (o que o Resolve mostra é o que vai para o render).
#   result = rodar("conferir_quadros.py", {"TL": '"Claude - Edicao v1"', "QUADROS": '[120, 480, 960]',
#                                          "SAIDA": '"/.../videos/meu_video/conferencia_v1/"'})
# Depois, junte os quadros numa folha (graficos/folha.py) e olhe antes de responder.
# Cuidado que já quebrou: sem esperar depois de mudar o timecode, sai o quadro anterior.
import os, time
# ---- PARAMETROS ----
TL = None
QUADROS = []          # quadros desde o início da timeline
SAIDA = None
ESPERA = 2.5          # segundos depois de cada mudança de posição
FORMATO = "png"
# --------------------
exec(open(KIT + "resolve/trilhas.py", encoding="utf-8").read())
assert TL and QUADROS and SAIDA, "faltou TL, QUADROS ou SAIDA"
os.makedirs(SAIDA, exist_ok=True)
tl = timeline(TL)
fps = float(tl.GetSetting("timelineFrameRate") or 24)
pagina = resolve.GetCurrentPage()
resolve.OpenPage("color"); time.sleep(2)


def tc(f):
    f += tl.GetStartFrame(); r = round(fps)
    return f"{f // (3600 * r):02d}:{f // (60 * r) % 60:02d}:{f // r % 60:02d}:{f % r:02d}"


feitos = []
for q in QUADROS:
    tl.SetCurrentTimecode(tc(int(q))); time.sleep(ESPERA)
    arq = os.path.join(SAIDA, f"q{int(q):06d}.{FORMATO}")
    ok = project.ExportCurrentFrameAsStill(arq)
    feitos.append([q, os.path.basename(arq), bool(ok) and os.path.exists(arq)])
if pagina:
    resolve.OpenPage(pagina)
result = {"timeline": TL, "quadros": feitos, "pasta": SAIDA}
