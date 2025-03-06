// CODIGO PARA SELECIONAR O ARQUIVO .PDF

document.addEventListener("DOMContentLoaded", function () {
    const dragArea = document.getElementById("drag-area");
    const fileInput = document.getElementById("file");
    const fileUploadBtn = document.getElementById("file-upload-btn");
    const fileNameDisplay = document.getElementById("file-name-display");
    const sendButton = document.getElementById("send-button"); 
    let selectedFile = null;

    // Evitar o comportamento padrão ao arrastar/soltar
    ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
        dragArea.addEventListener(eventName, e => e.preventDefault());
    });

    // Adicionar/remover classe para estilizar ao arrastar
    dragArea.addEventListener("dragenter", () => dragArea.classList.add("drag-over"));
    dragArea.addEventListener("dragover", () => dragArea.classList.add("drag-over"));
    dragArea.addEventListener("dragleave", () => dragArea.classList.remove("drag-over"));
    dragArea.addEventListener("drop", () => dragArea.classList.remove("drag-over"));

    // Capturar arquivos ao soltar
    dragArea.addEventListener("drop", e => {
        const files = e.dataTransfer.files;

        if (files.length > 0 && files[0].type === "application/pdf") {
            fileInput.files = files;
            fileUploadBtn.files = files;
            selectedFile = files[0];
            fileNameDisplay.innerHTML = `<p>Arquivo selecionado: ${files[0].name}</p>`;
        } else {
            resetFileSelection("Por favor, envie apenas arquivos PDF.");
        }
    });

    // Remover a opção de clicar na área drag
    // Não há mais necessidade do código abaixo, já que não queremos que a área drag funcione como um botão de upload
    // dragArea.addEventListener("click", () => fileInput.click());

    // Mostrar o nome do arquivo selecionado manualmente no input personalizado
    fileInput.addEventListener("change", handleFileSelection);
    fileUploadBtn.addEventListener("change", handleFileSelection);

    function handleFileSelection(event) {
        const files = event.target.files;

        if (files.length > 0 && files[0].type === "application/pdf") {
            selectedFile = files[0];
            fileNameDisplay.innerHTML = `<p>Arquivo selecionado: ${files[0].name}</p>`;
            
            // Sincroniza o outro input file
            if (event.target === fileInput) {
                fileUploadBtn.files = fileInput.files;
            } else {
                fileInput.files = fileUploadBtn.files;
            }
        } else {
            resetFileSelection("Por favor, envie apenas arquivos PDF.");
        }
    }

    function resetFileSelection(message) {
        selectedFile = null;
        fileNameDisplay.innerHTML = `<p style="color: red;">${message}</p>`;
        fileInput.value = "";
        fileUploadBtn.value = "";
    }

    // Enviar apenas quando o botão for clicado
    sendButton.addEventListener("click", () => {
        if (selectedFile) {
            sendFileToServerPDF(selectedFile);
        } else {
            alert("Por favor, selecione um arquivo primeiro.");
        }
    });

    // Função para enviar o arquivo para o servidor
    function sendFileToServerPDF(file) {
        const formData = new FormData();
        formData.append("file", file);

        fetch("/process_file", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Arquivo enviado com sucesso:", data);
        })
        .catch(error => {
            console.error("Erro ao enviar o arquivo:", error);
        });
    }
});


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
        document.getElementById("finalizarBtn").style.display = 'inline-block';
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
        excluirBtn.innerHTML = '<i class="bi bi-trash-fill" style="color: red;"></i>';
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

    // Mostra o indicador de carregamento
    mostrarCarregamento();

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
            console.log("Termos enviados:", termos);
            window.location.href = "/validacaoRelacao";
        } else {
            alert("Erro ao enviar os termos.");
            document.getElementById("loading").style.display = "none"; // Oculta o carregamento em caso de erro
        }
    })
    .catch(error => {
        console.error("Erro na requisição:", error);
        alert("Erro ao enviar os termos.");
        document.getElementById("loading").style.display = "none"; // Oculta o carregamento em caso de erro
    });
}

function mostrarCarregamento() {
    document.getElementById("loading").style.display = "block"; // Mostra o indicador de carregamento
}

// CÓDIGO PARA ADICIONAR O ARQUIVO .TXT

document.addEventListener("DOMContentLoaded", function () {
    const dragArea = document.getElementById("drag-area-txt");
    const fileInput = document.getElementById("file-txt");
    const fileUploadBtn = document.getElementById("file-upload-btn-txt");
    const fileNameDisplay = document.getElementById("file-name-display-txt");
    const sendButton = document.getElementById("send-button"); 
    let selectedFile = null;

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

        if (files.length > 0 && files[0].type === "text/plain") {
            fileInput.files = files;
            fileUploadBtn.files = files;
            selectedFile = files[0];
            fileNameDisplay.innerHTML = `<p>Arquivo selecionado: ${files[0].name}</p>`;
            
            // Mostrar o botão de envio após a seleção de um arquivo válido
            sendButton.style.display = "inline-block"; // Exibir o botão
        } else {
            resetFileSelection("Por favor, envie apenas arquivos TXT.");
        }
    });

    // Abrir seletor de arquivo ao clicar na área
    dragArea.addEventListener("click", () => fileInput.click());

    // Mostrar o nome do arquivo selecionado manualmente no input personalizado
    fileInput.addEventListener("change", handleFileSelection);
    fileUploadBtn.addEventListener("change", handleFileSelection);

    function handleFileSelection(event) {
        const files = event.target.files;

        if (files.length > 0 && files[0].type === "text/plain") {
            selectedFile = files[0];
            fileNameDisplay.innerHTML = `<p>Arquivo selecionado: ${files[0].name}</p>`;

            // Sincroniza o outro input file
            if (event.target === fileInput) {
                fileUploadBtn.files = fileInput.files;
            } else {
                fileInput.files = fileUploadBtn.files;
            }

            // Mostrar o botão de envio após a seleção de um arquivo válido
            sendButton.style.display = "inline-block"; // Exibir o botão
        } else {
            resetFileSelection("Por favor, envie apenas arquivos TXT.");
        }
    }

    function resetFileSelection(message) {
        selectedFile = null;
        fileNameDisplay.innerHTML = `<p style="color: red;">${message}</p>`;
        fileInput.value = "";
        fileUploadBtn.value = "";

        // Ocultar o botão de envio novamente se o arquivo for inválido
        sendButton.style.display = "none";
    }

    // Enviar apenas quando o botão for clicado
    sendButton.addEventListener("click", () => {
        if (selectedFile) {
            sendFileToServerTXT(selectedFile);
        } else {
            alert("Por favor, selecione um arquivo primeiro.");
        }
    });

    // Função para enviar o arquivo para o servidor
    function sendFileToServerTXT(file) {
        const formData = new FormData();
        formData.append("file", file);
    
        fetch("/salvar_termos", {
            method: "POST",
            body: formData
        })
        .then(response => {
            console.log("Status da resposta:", response.status);  // Exibe o status da resposta
            window.location.href = "/validacaoRelacao"; 
            // Se o status de resposta for 3xx, significa que é um redirecionamento
            if (response.status >= 300 && response.status < 400) {
                window.location.href = response.url;  // Faz o redirecionamento para a URL correta
            } else {
                return response.text();  // Caso contrário, processa como texto
            }
        })
        .then(data => {
            console.log("Resposta recebida:", data);
            // Se a resposta for um erro, ele será tratado aqui
            try {
                const jsonData = JSON.parse(data);  // Tenta fazer o parse para JSON se houver dados
                console.log("JSON processado:", jsonData);
                if (jsonData.success) {
                    window.location.href = "/validacaoRelacao";  // Redireciona se tudo estiver certo
                }
            } catch (e) {
                console.error("Erro ao tentar parsear o JSON:", e);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar o arquivo:", error);
        });
    }
});


// CÓDIGO PARA ADICIONAR MAIS AUTORES

function addAuthor() {
    // Obtém o container de autores
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
    const removeButton = document.createElement('span');
    removeButton.id = 'btn-trash';
    removeButton.innerHTML = 'Remover autor(a)';
    removeButton.classList.add('remove-author');
    removeButton.onclick = function() { removeAuthor(newAuthorGroup); };

    // Adiciona os novos elementos no grupo de autores
    newAuthorGroup.appendChild(newInput);
    newAuthorGroup.appendChild(removeButton);

    // Adiciona o novo grupo de autores no container
    container.appendChild(newAuthorGroup);
}

function removeAuthor(authorGroup) {
    // Remove o grupo de autor do DOM
    authorGroup.remove();
}


// FORMULÁRIO DE CADASTRO

function mostrarFormulario(id) {
    // Oculta todos os formulários
    document.getElementById('formLivro').style.display = 'none';
    document.getElementById('formArtigo').style.display = 'none';
    document.getElementById('formDissertacao').style.display = 'none';
    document.getElementById('titulo-autores-ano').style.display = 'none';
    document.getElementById('button-form').style.display = 'none';

    // Exibe apenas o formulário selecionado
    document.getElementById(id).style.display = 'block';
    document.getElementById('titulo-autores-ano').style.display = 'block';
    document.getElementById('button-form').style.display = 'block';
    

    // Remove 'required' de todos os campos
    var allFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    allFields.forEach(function(input) {
        input.removeAttribute('required');
    });

    // Garante que o campo de 'ano' esteja visível
    document.getElementById('ano').style.display = 'block'; // Adicionei isso aqui

    // Adiciona 'required' ao campo 'titulo' do formulário visível
    if (id === 'formLivro') {
        document.getElementById('titulo').setAttribute('required', 'required');
        document.getElementById('editora').setAttribute('required', 'required');
        document.getElementById('ano').setAttribute('required', 'required');
    } else if (id === 'formArtigo') {
        document.getElementById('titulo').setAttribute('required', 'required');
        document.getElementById('revista').setAttribute('required', 'required');
        document.getElementById('ano').setAttribute('required', 'required');
        document.getElementById('volume').setAttribute('required', 'required');
        document.getElementById('numero').setAttribute('required', 'required');
    } else if (id === 'formDissertacao') {
        document.getElementById('titulo').setAttribute('required', 'required');
        document.getElementById('orientador').setAttribute('required', 'required');
        document.getElementById('ano').setAttribute('required', 'required');
        document.getElementById('universidade').setAttribute('required', 'required');
        var tipoDocumentoRadioButtons = document.querySelectorAll('input[name="tipo_documento"]');
        tipoDocumentoRadioButtons.forEach(function(button) {
            button.setAttribute('required', 'required');
        });
    }
}

// Função para remover 'required' antes do envio do formulário
function removerRequiredAntesEnvio() {
    var allFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    allFields.forEach(function(input) {
        input.removeAttribute('required');
    });
}

// Adiciona o evento de submissão ao formulário para remover 'required' antes do envio
document.querySelector('form').addEventListener('submit', function(event) {
    removerRequiredAntesEnvio();
});

function validarRelacao(button, isValid) {
    let termo1 = button.getAttribute("data-termo1");
    let termo2 = button.getAttribute("data-termo2");
    let frase = button.getAttribute("data-frase");

    if (isValid) {
        // Marcar como validado na sessão
        fetch('/validarRelacao', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ termo1, termo2, frase })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redireciona para a página de cadastro, passando os parâmetros
                window.location.href = `/cadastroRelacao?termo1=${encodeURIComponent(termo1)}&termo2=${encodeURIComponent(termo2)}&frase=${encodeURIComponent(frase)}`;
            } else {
                alert('Erro ao validar a relação');
            }
        })
        .catch(error => console.error("Erro ao enviar validação:", error));
    } else {
        let linha = button.closest("tr");
        linha.remove();

        // Envia a validação negativa para o backend
        fetch('/salvar_validacao', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ termo1, termo2, isValid })
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error("Erro ao salvar validação:", error));
    }
}

function moverValidacaoRelacao() {
    mostrarCarregamento(); // Exibe o carregamento
}

//CÓDIGO PARA ADICIONAR AUTORES

const autores = [];
const autorInput = document.getElementById("autorInput");
const autoresLista = document.getElementById("autoresLista");
const finalizarBtnAutores = document.getElementById("finalizarBtnAutores");

// Função para adicionar autor
function addAuthor() {
    const autor = autorInput.value.trim();

    if (autor && !autores.includes(autor)) {
        autores.push(autor);
        atualizarListaAutores();
        document.getElementById("finalizarBtnAutores").style.display = 'inline-block';
        autorInput.value = ""; // Limpar campo de input
        autorInput.focus();
    }
}

// Função para remover um autor
function removerAutor(index) {
    autores.splice(index, 1);
    atualizarListaAutores();
}

// Função para atualizar a lista de autores
function atualizarListaAutores() {
    autoresLista.innerHTML = ""; // Limpar a lista antes de atualizar
    autores.forEach((autor, index) => {
        const li = document.createElement("li");
        li.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
        li.textContent = autor;

        const excluirBtn = document.createElement("button");
        excluirBtn.classList.add("btn", "btn-danger", "btn-sm");
        excluirBtn.id = 'btn-trash';
        excluirBtn.innerHTML = '<i class="bi bi-trash-fill" style="color: red;"></i>';
        excluirBtn.onclick = () => removerAutor(index);

        li.appendChild(excluirBtn);
        autoresLista.appendChild(li);
    });

}

// Função para finalizar o cadastro de autores usando FormData
function finalizarCadastroAutores() {
    console.log("Lista de autores antes da verificação:", autores);

    if (!Array.isArray(autores) || autores.length === 0 || autores.every(a => a.trim() === "")) {
        alert("Adicione ao menos um autor antes de finalizar!");
        return;
    }

    let formData = new FormData();

    // Adicionando os autores ao FormData
    autores.forEach(autor => {
        formData.append("autores[]", autor);
    });

    console.log("Autores enviados:", autores);

    // Envia os autores para o backend usando fetch
    fetch("/salvar_autores", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert("Autores enviados com sucesso!");
        } else {
            alert("Erro ao enviar os autores.");
        }
    })
    .catch(error => {
        console.error("Erro na requisição:", error);
        alert("Erro ao enviar os autores.");
    });
}


// FUNÇÃO PARA CARREGAR AS VISUALIZAÇÕE

function finalizarValidacao() {
    // Redireciona para a página de visualização
    window.location.href = "/visualizacao";
    
}

// Alterei para garantir que o carregamento dos dados ocorre após a página carregar
