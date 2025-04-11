from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/que-es-fix")
def que_es_fix():
    return render_template("que_es_fix.html")

@app.route("/como-armar-fix")
def como_armar_fix():
    return render_template("como_armar_fix.html")

@app.route("/simulador", methods=["GET", "POST"])
def simulador():
    fix_message = None
    if request.method == "POST":
        tags = {
            "8": request.form["8"],
            "35": "D",  # Fijo para New Order
            "49": request.form["49"],
            "56": request.form["56"],
            "34": request.form["34"],
            "11": request.form["11"],
            "55": request.form["55"],
            "54": request.form["54"],
            "38": request.form["38"],
            "40": request.form["40"],
        }
        if tags["40"] == "2":  # Solo si es Limit
            tags["44"] = request.form["44"]

        # Armamos el mensaje FIX
        fix_message = "|".join([f"{tag}={value}" for tag, value in tags.items()])

    return render_template("simulador.html", fix_message=fix_message)

@app.route("/errores")
def errores():
    return render_template("errores.html")

@app.route("/logs")
def logs():
    return render_template("logs.html")

if __name__ == "__main__":
    app.run(debug=True)
