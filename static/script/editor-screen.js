document.addEventListener("DOMContentLoaded", function() {
    const addFileButton = document.getElementById("add-file-button");
    const filesContainer = document.getElementById("files-container");
    const analyzeFileButton = document.getElementById("analyze-file-button");
    const analyzeProjectButton = document.getElementById("analyze-project-button");

    addFileButton.addEventListener("click", function() {
        const newFile = document.createElement("p");
        newFile.textContent = `plik${filesContainer.children.length + 1}.py`;
        filesContainer.appendChild(newFile);
    });

    analyzeFileButton.addEventListener("click", function() {
        alert("Analiza wybranego pliku w przygotowaniu...");
    });

    analyzeProjectButton.addEventListener("click", function() {
        alert("Analiza całego projektu w przygotowaniu...");
    });
});