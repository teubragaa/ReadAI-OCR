function adicionarCampo() {

    const campos = document.getElementById("campos");

    const campo = document.createElement("div");

    campo.innerHTML = `
        <input
            type="text"
            class="nome-campo"
            placeholder="Nome do campo"
        >

        <select class="tipo-campo">
            <option value="texto">Texto</option>
            <option value="numero">Número</option>
            <option value="data">Data</option>
        </select>

        <button onclick="this.parentElement.remove()">
            Remover
        </button>

        <br><br>
    `;

    campos.appendChild(campo);
}


async function salvarModelo() {

    const nome = document.getElementById("nome-modelo").value;

    const nomesCampos = document.querySelectorAll(".nome-campo");
    const tiposCampos = document.querySelectorAll(".tipo-campo");

    const campos = [];

    for (let i = 0; i < nomesCampos.length; i++) {

        campos.push({
            nome: nomesCampos[i].value,
            tipo: tiposCampos[i].value
        });

    }

    const resposta = await fetch("/api/modelos", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            nome: nome,
            campos: campos
        })

    });

    const resultado = await resposta.json();

    document.getElementById("resultado").innerText =
        resultado.mensagem;
}