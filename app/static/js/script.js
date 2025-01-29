
// CODIGO PARA SELECIONAR O ARQUIVO

document.addEventListener("DOMContentLoaded", function () {
    const dragArea = document.getElementById("drag-area");
    const fileInput = document.getElementById("file");
    const fileNameDisplay = document.getElementById("file-name-display");
    const form = document.querySelector("form"); // Captura o formulário para obter a rota correta

    // Evitar o comportamento padrão ao arrastar/soltar
    ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
        dragArea.addEventListener(eventName, e => e.preventDefault());
    });

    // Adicionar/remover classe para estilizar ao arrastar
    ["dragenter", "dragover"].forEach(eventName => {
        dragArea.addEventListener(eventName, () => dragArea.classList.add("drag-over"));
    });

    ["dragleave", "drop"].forEach(eventName => {
        dragArea.addEventListener(eventName, () => dragArea.classList.remove("drag-over"));
    });

    // Capturar arquivos ao soltar
    dragArea.addEventListener("drop", e => {
        const files = e.dataTransfer.files;

        // Validar o tipo de arquivo
        if (files.length > 0 && files[0].type === "application/pdf") {
            fileInput.files = files; // Transferir arquivos para o input
            fileNameDisplay.innerHTML = `<p>Arquivo selecionado: ${files[0].name}</p>`;
        } else {
            fileNameDisplay.innerHTML = `<p style="color: red;">Por favor, envie apenas arquivos PDF.</p>`;
        }
    });

    // Abrir seletor de arquivo ao clicar na área
    dragArea.addEventListener("click", () => fileInput.click());

    // Mostrar o nome do arquivo selecionado manualmente
    fileInput.addEventListener("change", () => {
        const files = fileInput.files;

        if (files.length > 0 && files[0].type === "application/pdf") {
            fileNameDisplay.innerHTML = `<p>Arquivo selecionado: ${files[0].name}</p>`;
            sendFileToServer(files[0]);  // Chama a função para enviar o arquivo ao servidor
        } else {
            fileNameDisplay.innerHTML = `<p style="color: red;">Por favor, envie apenas arquivos PDF.</p>`;
            fileInput.value = ""; // Resetar o input
        }
    });

    // Função para enviar o arquivo para o servidor
    function sendFileToServer(file) {
        const formData = new FormData();
        formData.append("file", file);  // Adiciona o arquivo no FormData

        // Envia a requisição para o servidor usando fetch
        fetch(form.action, {  // Usa a ação do formulário para a URL da rota correta
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Arquivo enviado com sucesso:", data);
            // Aqui você pode tratar a resposta do servidor, como exibir uma mensagem
        })
        .catch(error => {
            console.error("Erro ao enviar o arquivo:", error);
        });
    }
});


// CÓDIGO PARA ADICIONAR MAIS AUTORES

function addAuthor() {
    const container = document.getElementById('authors-container');
    const newAuthorGroup = document.createElement('div');
    newAuthorGroup.classList.add('author-group');

    // Cria um novo campo de entrada para o autor
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'autor[]';
    newInput.placeholder = 'Digite o nome do autor(a)';
    newInput.required = true;

    // Cria o botão de remover
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.id = 'btn-trash';
    removeButton.innerHTML = '<i class="bi bi-trash-fill"></i>';
    removeButton.classList.add('remove-author');
    removeButton.onclick = function() { removeAuthor(removeButton); };

    // Adiciona os novos elementos no container
    newAuthorGroup.appendChild(newInput);
    newAuthorGroup.appendChild(removeButton);
    container.appendChild(newAuthorGroup);
}

function removeAuthor(button) {
    // Remove o grupo de autor que contém o botão de remoção
    button.parentElement.remove();
}


// CODIGO DE ADICIONAR TERMOS

const termos = []; // Vetor para armazenar os termos adicionados
const termoInput = document.getElementById("termoInput");
const termosLista = document.getElementById("termosLista");
const finalizarBtn = document.getElementById("finalizarBtn");

// Função para adicionar termo
function adicionarTermo() {
    const termo = termoInput.value.trim();

    if (termo && !termos.includes(termo)) {
        termos.push(termo);
        atualizarListaTermos();
        termoInput.value = ""; // Limpar campo de input
        termoInput.focus();
    }
}

// Função para remover um termo
function removerTermo(index) {
    termos.splice(index, 1);
    atualizarListaTermos();
}

// Função para atualizar a lista de termos
function atualizarListaTermos() {
    termosLista.innerHTML = ""; // Limpar a lista antes de atualizar
    termos.forEach((termo, index) => {
        const li = document.createElement("li");
        li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
        li.textContent = termo;

        const excluirBtn = document.createElement("button");
        excluirBtn.classList.add("btn", "btn-danger", "btn-sm");
        excluirBtn.id = 'btn-trash';
        excluirBtn.innerHTML = '<i class="bi bi-trash-fill"></i>';
        excluirBtn.onclick = () => removerTermo(index);

        li.appendChild(excluirBtn);
        termosLista.appendChild(li);
    });

    // Habilitar o botão de finalizar se houver termos
    finalizarBtn.disabled = termos.length === 0;
}

// Função para finalizar o cadastro
function finalizarCadastro() {
    if (termos.length === 0) {
        alert("Adicione ao menos um termo antes de finalizar!");
        return;
    }

    // Envia os termos para o backend usando fetch
    fetch("/salvar_termos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ termos }) // Envia os termos no corpo da requisição
    })
    .then(response => {
        if (response.ok) {
            alert("Termos enviados com sucesso!");
            console.log("Termos enviados:", termos);
        } else {
            alert("Erro ao enviar os termos.");
        }
    })
    .catch(error => {
        console.error("Erro na requisição:", error);
        alert("Erro ao enviar os termos.");
    });
}
