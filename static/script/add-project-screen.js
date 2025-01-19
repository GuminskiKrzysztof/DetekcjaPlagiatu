import { toggleVisibility } from "./utils.js";

document.addEventListener("DOMContentLoaded", function() {
    const addProjectScreen = document.getElementById("add-project-screen");
    const editorScreen = document.getElementById("editor-screen");
    const createButton = document.getElementById("create-button");
    const selectFileButton = document.getElementById("select-file-button");
    const fileInput = document.getElementById("file-input");
    const nextButton = document.getElementById("next-button");

    createButton.addEventListener("click", function() {
        toggleVisibility(addProjectScreen);
        toggleVisibility(editorScreen);
    });

    selectFileButton.addEventListener("click", function() {
        fileInput.click();
    });

    fileInput.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            const validExtensions = ["cpp", "py"];
            const fileExtension = file.name.split(".").pop().toLowerCase();

            if (validExtensions.includes(fileExtension)) {
                alert(`Wybrano plik: ${file.name}`);
            } else {
                alert("Nieobsługiwany format pliku. Wybierz plik .cpp lub .py.");
                fileInput.value = "";
            }
        }
    });

    nextButton.addEventListener("click", function() {
        alert("Funkcja przejścia do następnego ekranu nie jest jeszcze dostępna.");
    });

});