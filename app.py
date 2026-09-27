import json
from flask import Flask, jsonify, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)


@app.get("/")
def inicio():
    return render_template("index.html")


@app.post("/api/modelos")
def criar_modelo():
    
    arquivo = request.files.get("documento")
    if not arquivo:
        return jsonify({"mensagem": "Nenhum arquivo enviado"}), 400

    
    nome = request.form.get("nome", "Documento")
    campos_raw = request.form.get("campos", "[]")
    campos = json.loads(campos_raw)

    if not campos:
        return jsonify({"mensagem": "Adicione pelo menos um campo"}), 400

    try:
        imagem = Image.open(arquivo.stream)
        
        # Pytesseract processa a imagem dentro do container
        texto_bruto = pytesseract.image_to_string(imagem, lang="por")

        if not texto_bruto.strip():
            return jsonify({
                "mensagem": "Não foi possível extrair texto da imagem via OCR local."
            }), 400
    
        linhas = texto_bruto.split("\n")
        dados_extraidos = {}

        for campo in campos:
            nome_campo = campo["nome"]
            valor_encontrado = "Não encontrado"
            
            for linha in linhas:
                if nome_campo.lower() in linha.lower():
                    valor_encontrado = linha.strip()
                    break
            
            dados_extraidos[nome_campo] = valor_encontrado

        return jsonify({
            "mensagem": "Documento processado 100% offline via OCR local!",
            "modelo": {"nome": nome, "campos": campos},
            "texto_bruto_ocr": texto_bruto,
            "dados": dados_extraidos
        })

    except Exception as e:
        return jsonify({"mensagem": f"Erro no processamento interno: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)