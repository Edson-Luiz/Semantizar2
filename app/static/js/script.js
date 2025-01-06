
//Seleciona os itens clicado
var menuItem = document.querySelectorAll('.item-menu')

function selectLink(){
    menuItem.forEach((item)=>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}

menuItem.forEach((item)=>
    item.addEventListener('click', selectLink)
)

//Expandir o menu

var btnExp = document.querySelector('#btn-exp')
var menuSide = document.querySelector('.menu-lateral')

btnExp.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
})




document.addEventListener("DOMContentLoaded", function () {
    const dragArea = document.getElementById("drag-area");
    const fileInput = document.getElementById("file");
    const fileNameDisplay = document.getElementById("file-name-display");

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
        } else {
            fileNameDisplay.innerHTML = `<p style="color: red;">Por favor, envie apenas arquivos PDF.</p>`;
            fileInput.value = ""; // Resetar o input
        }
    });
});




document.getElementById('adicionar-termo').addEventListener('click', function () {
    const termoInput = document.getElementById('termo-input');
    const termo = termoInput.value.trim();

    if (termo !== '') {
        adicionarTermo(termo);
        termoInput.value = '';
        termoInput.focus();
    } else {
        alert('Por favor, insira um termo válido.');
    }
});

function adicionarTermo(termo) {
    const listaTermos = document.getElementById('lista-termos');
    const li = document.createElement('li');
    li.innerHTML = `
        <span>${termo}</span>
        <button onclick="removerTermo(this)">Remover</button>
    `;
    listaTermos.appendChild(li);
}

function removerTermo(button) {
    const li = button.parentElement;
    li.remove();
}





function addAuthor() {
    const container = document.getElementById('authors-container');
    const newAuthorGroup = document.createElement('div');
    newAuthorGroup.classList.add('author-group');

    // Cria um novo campo de entrada para o autor
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'autor[]';
    newInput.placeholder = 'Nome do Autor';
    newInput.required = true;

    // Cria o botão de remover
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.textContent = 'Remover';
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
