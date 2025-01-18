import { toggleVisibility } from "./utils.js";

document.addEventListener("DOMContentLoaded", function() {
    const addProjectScreen = document.getElementById("add-project-screen");
    const editorScreen = document.getElementById("editor-screen");
    const createButton = document.getElementById("create-button");
    const selectFileButton = document.getElementById("select-file-button");
    const nextButton = document.getElementById("next-button");

    createButton.addEventListener("click", function() {
        toggleVisibility(addProjectScreen);
        toggleVisibility(editorScreen);
    });

    selectFileButton.addEventListener("click", function() {
        alert("Funkcja wyboru pliku nie jest jeszcze dostępna.");
    });

    nextButton.addEventListener("click", function() {
        alert("Funkcja przejścia do następnego ekranu nie jest jeszcze dostępna.");
    });

});