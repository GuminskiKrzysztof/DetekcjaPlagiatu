import { toggleVisibility } from "./utils.js";

const DB_NAME = 'fileStorage';
const STORE_NAME = 'files';

async function getStoredFiles() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, 1);
        
        request.onerror = () => reject(request.error);
        
        request.onsuccess = () => {
            const db = request.result;
            const transaction = db.transaction([STORE_NAME], 'readwrite');
            const store = transaction.objectStore(STORE_NAME);
            
            const getRequest = store.get('selectedFiles');
            
            getRequest.onsuccess = () => {
                // Clear the data after reading
                store.delete('selectedFiles');
                resolve(getRequest.result || {});
            };
            
            getRequest.onerror = () => reject(getRequest.error);
        };
    });
}

document.addEventListener("DOMContentLoaded", async function() {
    const addFileButton = document.getElementById("add-file-button");
    const filesContainer = document.getElementById("files-container");
    const codeEditorElement = document.getElementById("code-editor");
    const analyzeFileButton = document.getElementById("analyze-file-button");
    const analyzeProjectButton = document.getElementById("analyze-project-button");
    const modal = document.getElementById("file-type-modal");
    const fileTypeMenu = document.getElementById("file-type-menu");

    const fileCodes = new Map();
    let activeFileName = null;
    let fileIdCounter = 0;
    let editor; // Declare editor in wider scope

    function generateFileId() {
        return 'file-' + (fileIdCounter++);
    }

    async function handleStoredFiles() {
        try {
            // Try to get files from IndexedDB first
            const dbFiles = await getStoredFiles();
            const storedFiles = Array.isArray(dbFiles) ? dbFiles : JSON.parse(localStorage.getItem("selectedFiles") || "[]");
            localStorage.removeItem("selectedFiles");

            for (const fileObj of storedFiles) {
                const fileId = fileObj.id || generateFileId();
                fileCodes.set(fileId, fileObj.content);
                const fileElement = createFileElement(fileId, fileObj.name);
                filesContainer.appendChild(fileElement);

                if (filesContainer.children.length === 1) {
                    setActiveFile(fileId);
                }
            }
        } catch (error) {
            console.error("Error handling stored files:", error);
        }
    }

    // Initialize CodeMirror before handling stored files
    editor = CodeMirror(codeEditorElement, {
        mode: "python",
        theme: "dracula",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true,
        autofocus: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        placeholder: "Wpisz kod"
    });

    await handleStoredFiles();

    addFileButton.addEventListener("click", function(e) {
        e.stopPropagation();
        fileTypeMenu.classList.toggle("show");
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function(e) {
        if (!e.target.matches('#add-file-button')) {
            fileTypeMenu.classList.remove("show");
        }
    });

    const fileTypeButtons = document.querySelectorAll(".file-type-button");
    fileTypeButtons.forEach(button => {
        button.addEventListener("click", function(e) {
            e.stopPropagation();
            const extension = this.dataset.extension;
            const fileId = generateFileId();
            const baseName = `plik${filesContainer.children.length + 1}`;
            const newFileName = generateUniqueFileName(baseName + extension);

            fileCodes.set(fileId, "");
            const fileElement = createFileElement(fileId, newFileName);
            filesContainer.appendChild(fileElement);

            setActiveFile(fileId);
            fileTypeMenu.classList.remove("show");
        });
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
        const code = fileCodes.get(fileId) || '';
        
        // Ensure editor exists before using it
        if (editor) {
            editor.setValue(code);

            // Set mode based on file extension
            const fileWrapper = filesContainer.querySelector(`[data-file-id="${fileId}"]`);
            if (fileWrapper) {
                const fileName = fileWrapper.dataset.fileName;
                const extension = fileName.split('.').pop().toLowerCase();
                const mode = extension === 'py' ? 'python' : extension === 'cpp' ? 'text/x-c++src' : 'text/plain';
                editor.setOption('mode', mode);
            }
        }

        const fileWrappers = filesContainer.querySelectorAll(".file-wrapper");
        fileWrappers.forEach((wrapper) => wrapper.classList.remove("active"));
        const activeWrapper = filesContainer.querySelector(`[data-file-id="${fileId}"]`);
        if (activeWrapper) {
            activeWrapper.classList.add("active");
        }
    }

    function clearEditor() {
        activeFileName = null;
        if (editor) {
            editor.setValue("");
        }
    }

    // Attach editor change event handler
    if (editor) {
        editor.on("change", function() {
            if (activeFileName) {
                fileCodes.set(activeFileName, editor.getValue());
            }
        });
    }

    analyzeFileButton.addEventListener("click", async function() {
        const code = editor.getValue().trim();
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