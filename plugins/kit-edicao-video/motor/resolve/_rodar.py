# Roda um script do kit dentro do DaVinci Resolve Studio, trocando só o bloco PARAMETROS.
# Uso (ferramenta run_script_unsafe do conector do Resolve):
#   PASTA = "/caminho/absoluto/da/sua/pasta de edicao/"
#   exec(open(PASTA + "kit/resolve/_rodar.py").read())
#   result = rodar("novo_video.py", {"NOME": '"Meu vídeo"', "BRUTO": '["/Volumes/SSD/C0001.MP4"]'})
# Cada valor do dicionário é texto Python (por isso as aspas dentro das aspas).
import re as _re

assert PASTA.endswith("/"), "PASTA precisa terminar com /"
KIT = PASTA + "kit/"


def rodar(rel, params=None):
    src = open(KIT + "resolve/" + rel, encoding="utf-8").read()
    for k, v in (params or {}).items():
        src, n = _re.subn(rf"^{k} = .*$", f"{k} = {v}", src, count=1, flags=_re.M)
        assert n == 1, f"parâmetro {k} não existe em {rel}"
    g = {"project": project, "resolve": resolve, "PASTA": PASTA, "KIT": KIT, "__name__": "kit"}
    exec(compile(src, rel, "exec"), g)
    return g.get("result")
