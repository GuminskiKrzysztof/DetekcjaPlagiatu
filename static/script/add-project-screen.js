import { toggleVisibility } from "./utils.js";

// Wait for both DOM and JSZip to be ready
Promise.all([
    new Promise(resolve => document.addEventListener("DOMContentLoaded", resolve)),
    new Promise(resolve => {
        if (window.JSZip) resolve();
        else window.addEventListener('load', resolve);
    })
]).then(() => {
    const addProjectScreen = document.getElementById("add-project-screen");
    const editorScreen = document.getElementById("editor-screen");
    const createButton = document.getElementById("create-button");
    const selectFileButton = document.getElementById("select-file-button");
    const fileInput = document.getElementById("file-input");
    const nextButton = document.getElementById("next-button");
    const fileListDiv = document.getElementById("file-list");

    let files = [];
    let zipFiles = [];

    createButton.addEventListener("click", function() {
        window.location.href = "/edytor";
    });

    selectFileButton.addEventListener("click", function() {
        fileInput.click();
    });

    async function handleZipFile(zipFile) {
        try {
            const zip = await JSZip.loadAsync(zipFile);
            
            const zipNameDiv = document.createElement("div");
            zipNameDiv.textContent = zipFile.name;
            zipNameDiv.classList.add("file-name", "zip-file");

            // Extract files immediately
            for (const filename in zip.files) {
                const file = zip.files[filename];
                if (!file.dir) {
                    const extension = filename.split('.').pop().toLowerCase();
                    if (['cpp', 'py'].includes(extension)) {
                        const content = await file.async('text');
                        const fileObject = {
                            id: `file-${Date.now()}-${filename}`,
                            name: filename,
                            content: content
                        };
                        files.push(fileObject);
                    }
                }
            }
            
            const removeButton = document.createElement("span");
            removeButton.innerHTML = "&#10006;";
            removeButton.classList.add("remove-file");
            removeButton.onclick = () => {
                // Remove all files that came from this zip
                files = files.filter(f => !f.id.includes(zipFile.name));
                zipNameDiv.remove();
            };
            
            zipNameDiv.appendChild(removeButton);
            fileListDiv.appendChild(zipNameDiv);
        } catch (error) {
            alert("Błąd podczas przetwarzania pliku ZIP.");
            console.error(error);
        }
    }

    function handleFile(file) {
        const fileExtension = file.name.split(".").pop().toLowerCase();
        if (fileExtension === 'zip') {
            handleZipFile(file);
        } else if (['cpp', 'py'].includes(fileExtension)) {
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
            alert("Nieobsługiwany format pliku. Wybierz plik .cpp, .py lub .zip");
            fileInput.value = "";
        }
    }

    fileInput.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    nextButton.addEventListener("click", async function() {
        if (files.length > 0) {
            try {
                localStorage.setItem("selectedFiles", JSON.stringify(files));
                window.location.href = "/edytor";
            } catch (error) {
                console.error("Error storing files:", error);
                alert("Błąd podczas zapisywania plików. Spróbuj z mniejszą liczbą plików.");
            }
        }
    });

});