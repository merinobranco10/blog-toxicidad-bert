from datetime import datetime
from flask import Flask, render_template, request
import moderador

app = Flask(__name__)
MAX_STRIKES = 3
comentarios = []   # en memoria (no se guardan datos personales)
strikes = {}

@app.route("/", methods=["GET", "POST"])
def index():
    aviso = error = None
    if request.method == "POST":
        usuario = (request.form.get("usuario") or "anónimo").strip()[:30]
        texto = request.form.get("texto", "")
        if strikes.get(usuario, 0) >= MAX_STRIKES:
            error = f"@{usuario} está baneado (simulado) y no puede comentar."
        else:
            try:
                r = moderador.predecir(texto)
            except moderador.ErrorEntrada as e:
                error = str(e)
            else:
                mostrado = texto.strip()
                if r["toxico"]:
                    strikes[usuario] = strikes.get(usuario, 0) + 1
                    n = strikes[usuario]
                    mostrado = "██████ [Comentario censurado: contenido potencialmente tóxico] ██████"
                    if n >= MAX_STRIKES:
                        aviso = {"ban": True, "texto": f"🚫 @{usuario} alcanzó {n}/{MAX_STRIKES} infracciones: BANEADO (simulado)."}
                    elif n == MAX_STRIKES - 1:
                        aviso = {"ban": False, "texto": f"⚠️ ALERTA: infracción {n}/{MAX_STRIKES}. Un comentario tóxico más y @{usuario} será baneado."}
                    else:
                        aviso = {"ban": False, "texto": f"⚠️ Comentario tóxico detectado (infracción {n}/{MAX_STRIKES}). Las reiteraciones pueden causar baneo."}
                if r["advertencias"]:
                    error = " ".join(r["advertencias"])
                comentarios.append({"usuario": usuario, "mostrado": mostrado, "analisis": r,
                                    "toxico": r["toxico"], "hora": datetime.now().strftime("%H:%M:%S")})
    return render_template("index.html", comentarios=comentarios, aviso=aviso, error=error,
                           strikes=strikes, max_strikes=MAX_STRIKES)

if __name__ == "__main__":
    moderador.cargar()                      # carga el modelo al arrancar
    app.run(host="0.0.0.0", port=5000)
