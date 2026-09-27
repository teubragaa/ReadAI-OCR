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

   
    texto_ocr = extrair_texto_ocr(arquivo.stream)
    if not texto_ocr:
        return jsonify({"mensagem": "Não foi possível ler o documento"}), 400

    try:
        dados = estruturar_dados_ia(nome, campos, texto_ocr)
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao estruturar com IA: {str(e)}"}), 500

    return jsonify(
        {
            "mensagem": "Documento processado com sucesso",
            "modelo": {"nome": nome, "campos": campos},
            "texto": texto_ocr,
            "dados": dados,
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)