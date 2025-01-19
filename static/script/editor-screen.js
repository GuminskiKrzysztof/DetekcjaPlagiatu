import { toggleVisibility } from "./utils.js";

document.addEventListener("DOMContentLoaded", function() {
    const addFileButton = document.getElementById("add-file-button");
    const filesContainer = document.getElementById("files-container");
    const codeEditor = document.getElementById("code-editor");
    const analyzeFileButton = document.getElementById("analyze-file-button");
    const analyzeProjectButton = document.getElementById("analyze-project-button");

    const fileCodes = new Map();
    let activeFileName = null;
    let fileIdCounter = 0;

    function generateFileId() {
        return 'file-' + (fileIdCounter++);
    }

    addFileButton.addEventListener("click", function() {
        const fileId = generateFileId();
        const baseName = `plik${filesContainer.children.length + 1}`;
        const extension = ".py";
        const newFileName = generateUniqueFileName(baseName + extension);

        fileCodes.set(fileId, "");
        const fileElement = createFileElement(fileId, newFileName);
        filesContainer.appendChild(fileElement);

        setActiveFile(fileId);
    });

    function generateUniqueFileName(fileName) {
        let uniqueName = fileName;
        let counter = 1;
        while (fileCodes.has(uniqueName)) {
            const lastDotIndex = fileName.lastIndexOf(".");
            const namePart = fileName.substring(0, lastDotIndex);
            const extension = fileName.substring(lastDotIndex);
            uniqueName = `${namePart}_${counter}${extension}`;
            counter++;
        }

        return uniqueName;
    }

    function createFileElement(fileId, fileName) {
        const fileWrapper = document.createElement("div");
        fileWrapper.classList.add("file-wrapper");
        fileWrapper.dataset.fileId = fileId;
        fileWrapper.dataset.fileName = fileName;

        const fileNameElement = document.createElement("p");
        fileNameElement.textContent = fileName;

        fileNameElement.addEventListener("click", () => {
            setActiveFile(fileWrapper.dataset.fileId);
        });

        const editIcon = document.createElement("span");
        editIcon.innerHTML = "&#9998;";
        editIcon.classList.add("icon", "edit-icon");
        editIcon.addEventListener("click", () =>    
            enableFilenameEditing(fileWrapper, fileNameElement, editIcon, deleteIcon)
        );

        const deleteIcon = document.createElement("span");
        deleteIcon.innerHTML = "&#10006;";
        deleteIcon.classList.add("icon", "delete-icon");
        deleteIcon.addEventListener("click", () => {
            fileCodes.delete(fileId);
            fileWrapper.remove();
            if (activeFileName === fileId) {
                clearEditor();
            }
        });

        
        fileWrapper.appendChild(fileNameElement);
        fileWrapper.appendChild(editIcon);
        fileWrapper.appendChild(deleteIcon);

        return fileWrapper;
    }

    function setActiveFile(fileId) {
        activeFileName = fileId;
        const code = fileCodes.get(fileId);
        codeEditor.value = code;

        const fileWrappers = filesContainer.querySelectorAll(".file-wrapper");
        fileWrappers.forEach((wrapper) => wrapper.classList.remove("active"));
        const activeWrapper = filesContainer.querySelector(
            `[data-file-id="${fileId}"]`
        );
        if (activeWrapper) {
            activeWrapper.classList.add("active");
        }
    }

    function clearEditor() {
        activeFileName = null;
        codeEditor.value = "";
    }

    codeEditor.addEventListener("input", function() {
        if (activeFileName) {
            fileCodes.set(activeFileName, codeEditor.value);
        }
    });

    function enableFilenameEditing(fileWrapper, fileNameElement, editIcon, deleteIcon) {
        const currentName = fileNameElement.textContent;
        const lastDotIndex = currentName.lastIndexOf(".");
        const namePart = currentName.substring(0, lastDotIndex);
        const extensionPart = currentName.substring(lastDotIndex);

        const inputWrapper = document.createElement("div");
        inputWrapper.classList.add("input-wrapper");
        
        const input = document.createElement("input");
        input.type = "text";
        input.value = namePart;
        input.classList.add("filename-edit-input");
        
        const extensionSpan = document.createElement("span");
        extensionSpan.textContent = extensionPart;
        extensionSpan.classList.add("file-extension");

        toggleVisibility(editIcon);
        toggleVisibility(deleteIcon);

        input.addEventListener("blur", function() {
            const newNamePart = input.value.trim() || namePart;
            const newName = newNamePart + extensionPart;

            if (newName !== currentName && fileCodes.has(newName)) {
                alert("Plik o tej nazwie już istnieje.");
                input.focus();
                return;
            }

            fileWrapper.dataset.fileName = newName;
            fileNameElement.textContent = newName;

            if (activeFileName === currentName) {
                activeFileName = newName;
            }

            fileNameElement.style.display = "block";
            inputWrapper.remove();

            toggleVisibility(editIcon);
            toggleVisibility(deleteIcon);
        });

        input.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                input.blur();
            }
        });

        fileNameElement.style.display = "none";
        inputWrapper.appendChild(input);
        inputWrapper.appendChild(extensionSpan);
        fileWrapper.insertBefore(inputWrapper, fileNameElement);
        input.focus();

        input.setSelectionRange(0, namePart.length);
    }

    analyzeFileButton.addEventListener("click", async function() {
        const code = codeEditor.value.trim();
        if (!code) {
            alert("Proszę wpisać kod do analizy.");
            return;
        }

        try {
            const response = await fetch("/predict_category_python", {
                method: "POST",
                body: JSON.stringify({ code }),
                headers: {
                    "Content-Type": "application/json"
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                alert(`Przewidywana kategoria: ${data["Predicted Category"]}`);
            }
            else {
                console.error("Błąd podczas analizy kodu:", response.status, response.statusText);
                alert("Wystąpił błąd podczas analizy kodu. Spróbuj ponownie.");
            }
        } catch (error) {
            console.error("Błąd podczas wysyłania żądania:", error);
            alert("Nie udało się połączyć z serwerem.");
        }
    });

    analyzeProjectButton.addEventListener("click", function() {
        alert("Analiza całego projektu w przygotowaniu...");
    });
});