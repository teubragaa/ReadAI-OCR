import json
from flask import Flask, jsonify, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)


@app.get("/")
def inicio():
    return render_template("index.html")


@app.post("/api/modelos")
def processar_documento():
    arquivo = request.files.get("documento")

    if not arquivo:
        return jsonify({"mensagem": "Nenhum arquivo enviado"}), 400

    nome = request.form.get("nome", "Documento")
    campos = json.loads(request.form.get("campos", "[]"))

    if not campos:
        return jsonify({"mensagem": "Adicione pelo menos um campo"}), 400

    imagem = Image.open(arquivo.stream)
    texto = pytesseract.image_to_string(imagem, lang="por")

    if not texto.strip():
        return jsonify({"mensagem": "Não foi possível ler o documento"}), 400

    dados = {}

    for campo in campos:
        nome_campo = campo["nome"]
        dados[nome_campo] = "Não encontrado"

        for linha in texto.splitlines():
            if nome_campo.lower() in linha.lower():
                dados[nome_campo] = linha.strip()
                break

    return jsonify({
        "mensagem": "Documento processado com sucesso",
        "modelo": {
            "nome": nome,
            "campos": campos
        },
        "texto": texto,
        "dados": dados
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)