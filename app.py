from flask import Flask, render_template, request
import json
import re

# Cargar archivos JSON
with open('static/data/tags_con_descripciones.json', encoding='utf-8') as f:
    tags_con_descripciones = json.load(f)

with open('static/data/mensajes_con_desc.json', encoding='utf-8') as f:
    mensajes_con_desc = json.load(f)

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

@app.route('/parser', methods=['GET', 'POST'])
def parser():
    parsed_fix = []
    raw_fix = ""
    message_name = None
    message_description = None

    if request.method == 'POST':
        raw_fix = request.form['raw_fix']
        
        # Definir los delimitadores como tabulador (\t) y pipe (|), usando una expresión regular
        delimiters = r'[\t|]'  # Usamos un grupo de caracteres (tabulador y pipe) como delimitadores
        
        # Dividir el mensaje utilizando tabulador o pipe
        fix_pairs = re.split(delimiters, raw_fix.strip())

        for pair in fix_pairs:
            if '=' in pair:
                tag, value = pair.split('=', 1)
                tag_info = tags_con_descripciones.get(tag, {})
                parsed_fix.append({
                    'tag': tag,
                    'value': value,
                    'name': tag_info.get('name', 'Nombre no encontrado'),
                    'description': tag_info.get('description', 'Descripción no encontrada')
                })

                # Buscar nombre del mensaje (tag 35)
                if tag == '35':
                    msg_info = mensajes_con_desc.get(value, {})
                    message_name = msg_info.get('name', 'Mensaje desconocido')
                    message_description = msg_info.get('description', 'Descripción no disponible')

    return render_template('parser.html', parsed_fix=parsed_fix, raw_fix=raw_fix,
                           message_name=message_name, message_description=message_description)

if __name__ == "__main__":
    app.run(debug=True)
