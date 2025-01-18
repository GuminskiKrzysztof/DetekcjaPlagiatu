document.addEventListener("DOMContentLoaded", function() {
    const addFileButton = document.getElementById("add-file-button");
    const filesContainer = document.getElementById("files-container");
    const analyzeFileButton = document.getElementById("analyze-file-button");
    const analyzeProjectButton = document.getElementById("analyze-project-button");
    const codeEditor = document.getElementById("code-editor");

    addFileButton.addEventListener("click", function() {
        const fileElement = createFileElement(`plik${filesContainer.children.length + 1}.py`);
        filesContainer.appendChild(fileElement);
    });

    function createFileElement(fileName) {
        const fileWrapper = document.createElement("div");
        fileWrapper.classList.add("file-wrapper");

        const fileNameElement = document.createElement("p");
        fileNameElement.textContent = fileName;

        const editIcon = document.createElement("span");
        editIcon.innerHTML = "&#9998;";
        editIcon.classList.add("icon", "edit-icon");
        editIcon.addEventListener("click", () => enableFilenameEditing(fileWrapper, fileNameElement));

        const deleteIcon = document.createElement("span");
        deleteIcon.innerHTML = "&#10006;";
        deleteIcon.classList.add("icon", "delete-icon");
        deleteIcon.addEventListener("click", () => fileWrapper.remove());

        
        fileWrapper.appendChild(fileNameElement);
        fileWrapper.appendChild(editIcon);
        fileWrapper.appendChild(deleteIcon);

        return fileWrapper;
    }

    function enableFilenameEditing(fileWrapper, fileNameElement) {
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

        input.addEventListener("blur", function() {
            const newName = input.value || namePart;
            fileNameElement.textContent = newName + extensionPart;
            fileNameElement.style.display = "block";
            inputWrapper.remove();
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