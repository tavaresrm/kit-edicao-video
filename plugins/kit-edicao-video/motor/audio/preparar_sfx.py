"""Prepara os sons das pastas de SFX antes da montagem. Precisa de ffmpeg e numpy.

Para o primeiro arquivo de áudio de cada pasta sfx/<slot>/ (ordem alfabética):
  1. acha onde o som começa (o atraso do ataque) e corta o silêncio do começo, deixando 10 ms;
  2. se o arquivo tem várias tomadas, fica só a primeira (tomada = som até um silêncio de 0,35 s ou mais);
  3. fade de 5 ms na entrada e 80 ms no fim, sem mudar o volume;
  4. grava em sfx/<slot>/_pronto/<nome>.wav (48 kHz, estéreo). O original não é tocado.
O resolve/sfx.py usa o _pronto quando existe. Rodar de novo sempre que um som novo entrar numa pasta.
Uso: python3 preparar_sfx.py <pasta de edição>/sfx
"""
import os, sys, json, subprocess
import numpy as np
SR = 48000
EXT = (".wav", ".mp3", ".aif", ".aiff", ".m4a")
LIMIAR = 0.08          # fração do pico que conta como som (≈ -22 dB do pico)
SILENCIO = 0.35        # silêncio que separa tomadas, em segundos
PRE, FADE_IN, CAUDA, FADE_OUT, MAXIMO = 0.010, 0.005, 0.12, 0.08, 4.0

def ler(arq):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)

def primeira_tomada(x):
    mono = np.abs(x).max(axis=1); w = int(SR * 0.01)
    env = np.array([mono[i:i + w].max() for i in range(0, len(mono), w)]) if len(mono) else np.zeros(1)
    pk = env.max()
    if pk <= 0: return None
    acima = np.where(env > pk * LIMIAR)[0]
    ini = acima[0]; fim = ini; gap = int(SILENCIO / 0.01)
    for j in acima[1:]:
        if j - fim > gap: break
        fim = j
    a = max(0, int(ini * w - PRE * SR)); b = min(len(x), int((fim + 1) * w + CAUDA * SR), a + int(MAXIMO * SR))
    tomadas = 1 + int(np.sum(np.diff(acima) > gap))
    return a, b, tomadas, float(20 * np.log10(pk))

def preparar(pasta):
    rel = {}
    for slot in sorted(os.listdir(pasta)):
        d = os.path.join(pasta, slot)
        if not os.path.isdir(d) or slot.startswith(("_", ".")): continue
        fs = sorted(f for f in os.listdir(d) if f.lower().endswith(EXT) and not f.startswith("."))
        if not fs: rel[slot] = "pasta vazia"; continue
        x = ler(os.path.join(d, fs[0])); r = primeira_tomada(x)
        if not r: rel[slot] = f"{fs[0]}: sem som"; continue
        a, b, tomadas, pico = r
        y = x[a:b].copy(); n_in, n_out = int(FADE_IN * SR), int(FADE_OUT * SR)
        y[:n_in] *= np.linspace(0, 1, n_in)[:, None]; y[-n_out:] *= np.linspace(1, 0, n_out)[:, None]
        out = os.path.join(d, "_pronto"); os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            if f.endswith(".wav") and f != os.path.splitext(fs[0])[0] + ".wav":
                try: os.remove(os.path.join(out, f))
                except OSError: rel.setdefault("_nao_apagados", []).append(os.path.join(slot, "_pronto", f))
        alvo = os.path.join(out, os.path.splitext(fs[0])[0] + ".wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-c:a", "pcm_s24le", alvo], input=y.astype(np.float32).tobytes(), check=True)
        rel[slot] = dict(arquivo=fs[0], atraso_cortado_s=round(a / SR, 3), duracao_s=round((b - a) / SR, 3),
                         tomadas_no_original=tomadas, pico_db=round(pico, 1), pronto=os.path.relpath(alvo, pasta))
    json.dump(rel, open(os.path.join(pasta, "_preparo.json"), "w"), ensure_ascii=False, indent=1)
    return rel

if __name__ == "__main__":
    print(json.dumps(preparar(sys.argv[1]), ensure_ascii=False, indent=1))
