import os, re
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
import moderador

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Santiago")
except Exception:
    TZ = None

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-local-de-demostracion")

MAX_STRIKES = 3
comentarios = []   # en memoria: no se guardan datos personales
strikes = {}       # infracciones por usuario (se pierden al reiniciar)


@app.route("/")
def index():
    usuario = session.get("usuario")
    baneado = bool(usuario) and strikes.get(usuario, 0) >= MAX_STRIKES
    return render_template("index.html", usuario=usuario, baneado=baneado,
                           comentarios=comentarios, strikes=strikes,
                           max_strikes=MAX_STRIKES)


@app.route("/entrar", methods=["POST"])
def entrar():
    nombre = (request.form.get("usuario") or "").strip()
    if not re.fullmatch(r"[\w\-]{2,20}", nombre):
        flash("Username must be 2 to 20 characters (letters, numbers, _ or -).", "info")
    else:
        session["usuario"] = nombre
    return redirect(url_for("index"))


@app.route("/salir", methods=["POST"])
def salir():
    session.pop("usuario", None)
    return redirect(url_for("index"))


@app.route("/comentar", methods=["POST"])
def comentar():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("index"))
    if strikes.get(usuario, 0) >= MAX_STRIKES:
        flash(f"🚫 @{usuario} is banned and cannot comment.", "ban")
        return redirect(url_for("index"))

    texto = request.form.get("texto", "")
    try:
        r = moderador.predecir(texto)
    except moderador.ErrorEntrada as e:
        flash(str(e), "info")
        return redirect(url_for("index"))

    mostrado = texto.strip()
    if r["toxico"]:
        n = strikes[usuario] = strikes.get(usuario, 0) + 1
        mostrado = "██████ [Comment censored: potentially toxic content] ██████"
        if n >= MAX_STRIKES:
            flash(f"🚫 @{usuario} reached {n}/{MAX_STRIKES} strikes and has been BANNED.", "ban")
        elif n == MAX_STRIKES - 1:
            flash(f"⚠️ FINAL WARNING: strike {n}/{MAX_STRIKES}. One more toxic comment and you will be banned.", "alerta")
        else:
            flash(f"⚠️ Toxic comment detected (strike {n}/{MAX_STRIKES}). Repeated violations may lead to a ban.", "alerta")
    for adv in r["advertencias"]:
        flash(adv, "info")

    comentarios.append({"usuario": usuario, "mostrado": mostrado, "analisis": r,
                        "toxico": r["toxico"], "hora": datetime.now(TZ).strftime("%H:%M:%S")})
    return redirect(url_for("index"))


if __name__ == "__main__":
    moderador.cargar()                       # carga BERT al arrancar
    app.run(host="0.0.0.0", port=5000)
