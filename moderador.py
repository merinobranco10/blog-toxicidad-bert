import os, re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_ID = os.getenv("MODEL_ID", "bmerino10/vigia-bert-toxicidad")
MAX_LENGTH, UMBRAL = 256, 0.5
MIN_CAR, MAX_CAR = 3, 5000
ID_TOXICO = 1
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

PALABRAS_ES = {"el","la","los","las","de","del","que","y","en","un","una","por","con",
               "para","se","muy","pero","esto","eres","está","como","qué","tú","eso","lo"}

class ErrorEntrada(ValueError):
    pass

_tok = _modelo = None

def cargar():
    """Descarga (1ª vez) y carga el modelo UNA sola vez, en modo eval."""
    global _tok, _modelo
    if _modelo is None:
        _tok = AutoTokenizer.from_pretrained(MODEL_ID)
        _modelo = AutoModelForSequenceClassification.from_pretrained(MODEL_ID).to(DEVICE)
        _modelo.eval()
        for p in _modelo.parameters():
            p.requires_grad_(False)
    return _tok, _modelo

def validar(texto):
    if texto is None:
        raise ErrorEntrada("The comment text is missing.")
    if not isinstance(texto, str):
        raise ErrorEntrada("The comment must be text.")
    t = texto.strip()
    if not t:
        raise ErrorEntrada("The comment is empty.")
    if len(t) < MIN_CAR:
        raise ErrorEntrada(f"Comment too short (minimum {MIN_CAR} characters).")
    if len(t) > MAX_CAR:
        raise ErrorEntrada(f"Comment too long (maximum {MAX_CAR} characters).")
    if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", t):
        raise ErrorEntrada("The comment contains no letters.")
    adv = []
    palabras = re.findall(r"\w+", t.lower())
    if sum(p in PALABRAS_ES for p in palabras) >= 2:
        adv.append("This looks like Spanish; the moderator only works reliably in English.")
    tok, _ = cargar()
    if len(tok(t, truncation=False)["input_ids"]) > MAX_LENGTH:
        adv.append(f"Long text: it will be truncated to {MAX_LENGTH} tokens.")
    return t, adv

@torch.no_grad()
def predecir(texto):
    t, adv = validar(texto)
    tok, modelo = cargar()
    enc = tok(t, truncation=True, max_length=MAX_LENGTH, return_tensors="pt").to(DEVICE)
    p = float(torch.softmax(modelo(**enc).logits, dim=-1)[0][ID_TOXICO])
    tox = p >= UMBRAL
    return {"etiqueta": "Tóxico" if tox else "No tóxico", "toxico": tox,
            "prob_toxico": round(p, 4),
            "confianza": round(p if tox else 1 - p, 4),
            "umbral": UMBRAL, "advertencias": adv}
