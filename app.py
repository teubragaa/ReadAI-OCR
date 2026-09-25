from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.get("/")
def inicio():
    return render_template("index.html")


@app.post("/api/modelos")
def criar_modelo():
    dados = request.json

    nome = dados.get("nome")
    campos = dados.get("campos", [])

    return jsonify({
        "mensagem": "Modelo criado com sucesso",
        "modelo": {
            "nome": nome,
            "campos": campos
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)