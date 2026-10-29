# Grava a configuração do projeto ABERTO no Resolve em PASTA + "config_projeto.json".
# Use com o projeto que já tem a configuração que você gosta (resolução, fps, áudio, cor).
# O criar_modelo.py copia essa configuração para o projeto modelo. Não altera nada no Resolve.
#   result = rodar("exportar_config.py", {})
import json
# ---- PARAMETROS ----
SAIDA = None   # None = PASTA + "config_projeto.json"
# --------------------
saida = SAIDA or PASTA + "config_projeto.json"
cfg = project.GetSetting()
assert cfg, "não consegui ler a configuração do projeto aberto"
json.dump({"projeto_de_origem": project.GetName(), "settings": cfg}, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
result = {"projeto": project.GetName(), "itens": len(cfg), "arquivo": saida,
          "resumo": {k: cfg.get(k) for k in ("timelineResolutionWidth", "timelineResolutionHeight", "timelineFrameRate", "timelineSampleRate")}}
