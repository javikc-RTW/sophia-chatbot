from flask import Flask, render_template, request, session
from chatbot import responder

app = Flask(__name__)
app.secret_key = "sophia_secret_key"

@app.before_request
def make_session_permanent():
    session.permanent = True

def formatear_respuesta(texto):
    import re
    texto = re.sub(r"\*(.*?)\*", r"<b>\1</b>", texto)  # Negrita
    texto = texto.replace("\n", "<br>")  # Saltos de línea
    return texto

@app.route("/", methods=["GET", "POST"])
def index():
    if "historial" not in session:
        session["historial"] = []

    if request.method == "POST":
        mensaje = request.form["mensaje"]
        respuesta = responder(mensaje) or "No tengo respuesta para eso."
        respuesta_formateada = formatear_respuesta(respuesta)

        session["historial"].append({"autor": "usuario", "texto": mensaje})
        session["historial"].append({"autor": "bot", "texto": respuesta_formateada})

    return render_template("index.html", historial=session["historial"])

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
