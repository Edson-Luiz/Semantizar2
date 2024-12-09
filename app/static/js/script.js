
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