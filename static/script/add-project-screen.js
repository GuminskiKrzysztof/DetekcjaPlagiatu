import { toggleVisibility } from "./utils.js";

document.addEventListener("DOMContentLoaded", function() {
    const addProjectScreen = document.getElementById("add-project-screen");
    const editorScreen = document.getElementById("editor-screen");
    const createButton = document.getElementById("create-button");
    const selectFileButton = document.getElementById("select-file-button");
    const fileInput = document.getElementById("file-input");
    const nextButton = document.getElementById("next-button");
    const fileListDiv = document.getElementById("file-list");

    let files = [];

    createButton.addEventListener("click", function() {
        window.location.href = "/edytor";
    });

    selectFileButton.addEventListener("click", function() {
        fileInput.click();
    });

    function handleFile(file) {
        const validExtensions = ["cpp", "py"];
        const fileExtension = file.name.split(".").pop().toLowerCase();
        if (validExtensions.includes(fileExtension)) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const fileObject = {
                    id: `file-${Date.now()}`, // Dodajemy unikalny identyfikator
                    name: file.name,
                    content: e.target.result
                };
                files.push(fileObject);
                
                const fileNameDiv = document.createElement("div");
                fileNameDiv.textContent = file.name;
                fileNameDiv.classList.add("file-name");
                fileNameDiv.dataset.fileId = fileObject.id;
                
                const removeButton = document.createElement("span");
                removeButton.innerHTML = "&#10006;";
                removeButton.classList.add("remove-file");
                removeButton.onclick = () => {
                    files = files.filter(f => f.id !== fileObject.id);
                    fileNameDiv.remove();
                };
                
                fileNameDiv.appendChild(removeButton);
                fileListDiv.appendChild(fileNameDiv);
            };
            reader.readAsText(file);
        } else {
            alert("Nieobsługiwany format pliku. Wybierz plik .cpp lub .py.");
            fileInput.value = "";
        }
    }

    fileInput.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    nextButton.addEventListener("click", function() {
        if (files.length > 0) {
            localStorage.setItem("selectedFiles", JSON.stringify(files));
            window.location.href = "/edytor";
        }
    });

});