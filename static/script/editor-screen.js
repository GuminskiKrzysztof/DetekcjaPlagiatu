import { toggleVisibility } from "./utils.js";

const DB_NAME = 'fileStorage';
const STORE_NAME = 'files';
const FILE_MODES = {
    'py': 'python',
    'cpp': 'text/x-c++src'
};

async function getStoredFiles() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, 1);
        
        request.onerror = () => reject(request.error);
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                db.createObjectStore(STORE_NAME);
            }
        };
        
        request.onsuccess = () => {
            const db = request.result;
            try {
                const transaction = db.transaction([STORE_NAME], 'readwrite');
                const store = transaction.objectStore(STORE_NAME);
                
                const getRequest = store.get('selectedFiles');
                
                getRequest.onsuccess = () => {
                    store.delete('selectedFiles');
                    resolve(getRequest.result || {});
                };
                
                getRequest.onerror = () => reject(getRequest.error);
            } catch (error) {
                // Fallback to localStorage if IndexedDB fails
                resolve(JSON.parse(localStorage.getItem("selectedFiles") || "[]"));
            }
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
    const noFileMessage = document.getElementById("no-file-message");

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

    // Initialize editor in disabled state
    editor = CodeMirror(codeEditorElement, {
        mode: "python",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true,
        autofocus: false, // Changed from true to false
        matchBrackets: true,
        autoCloseBrackets: true,
        styleActiveLine: true,
        readOnly: true // Start with editor disabled
    });

    await handleStoredFiles();

    // Set initial editor state
    if (!filesContainer.children.length) {
        clearEditor();
    }

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
                const remainingFiles = filesContainer.querySelectorAll('.file-wrapper');
                if (remainingFiles.length > 0) {
                    setActiveFile(remainingFiles[0].dataset.fileId);
                } else {
                    clearEditor();
                }
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
        
        if (editor) {
            editor.setValue(code);
            enableEditor();

            // Set mode based on file extension
            const fileWrapper = filesContainer.querySelector(`[data-file-id="${fileId}"]`);
            if (fileWrapper) {
                const fileName = fileWrapper.dataset.fileName;
                const extension = fileName.split('.').pop().toLowerCase();
                const mode = FILE_MODES[extension] || 'text/plain';
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
            codeEditorElement.classList.remove("active");
            noFileMessage.style.display = "block";
        }
    }

    function enableEditor() {
        if (editor) {
            codeEditorElement.classList.add("active");
            noFileMessage.style.display = "none";
            editor.refresh();
        }
    }

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

        const fileWrapper = filesContainer.querySelector(`[data-file-id="${activeFileName}"]`);
        const fileName = fileWrapper.dataset.fileName;
        const extension = fileName.split('.').pop().toLowerCase();
        let endpoint;
        
        if (extension === 'py') {
            endpoint = '/python_information';
        } else if (extension === 'cpp') {
            endpoint = '/cpp_information';
        } else {
            alert("Nieobsługiwane rozszerzenie pliku.");
            return;
        }

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                body: JSON.stringify({ code: code }), // Changed to send code in correct format
                headers: {
                    "Content-Type": "application/json"
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const info = data["Information: "];
                const isPlagiarism = info[0];
                const similarity = info[1];
                const matchingCode = info[2];
                
                if (isPlagiarism) {
                    alert(`Wykryto plagiat! Podobieństwo: ${(similarity * 100).toFixed(2)}%`);
                } else {
                    alert(`Nie wykryto plagiatu. Podobieństwo: ${(similarity * 100).toFixed(2)}%`);
                }
            } else {
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

        function handleNameChange() {
            const newNamePart = input.value.trim() || namePart;
            const newName = newNamePart + extensionPart;

            // Check for duplicate filename
            const files = filesContainer.querySelectorAll('.file-wrapper');
            const isDuplicate = Array.from(files).some(file => 
                file !== fileWrapper && file.dataset.fileName === newName
            );

            if (isDuplicate) {
                input.classList.add('error');
                let errorMsg = inputWrapper.querySelector('.filename-error');
                if (!errorMsg) {
                    errorMsg = document.createElement('div');
                    errorMsg.classList.add('filename-error');
                    errorMsg.textContent = 'Plik o tej nazwie już istnieje.';
                    inputWrapper.appendChild(errorMsg);
                }
                input.focus();
                return false;
            }

            fileWrapper.dataset.fileName = newName;
            fileNameElement.textContent = newName;

            if (activeFileName === fileWrapper.dataset.fileId) {
                // Aktualizujemy tylko fileId, nie nazwę
                fileNameElement.textContent = newName;
            }

            fileNameElement.style.display = "block";
            inputWrapper.remove();

            toggleVisibility(editIcon);
            toggleVisibility(deleteIcon);
            return true;
        }

        input.addEventListener("blur", handleNameChange);

        input.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                e.preventDefault();
                if (handleNameChange()) {
                    input.blur();
                }
            }
        });

        input.addEventListener("input", function() {
            input.classList.remove('error');
            const errorMsg = inputWrapper.querySelector('.filename-error');
            if (errorMsg) {
                errorMsg.remove();
            }
        });

        fileNameElement.style.display = "none";
        inputWrapper.appendChild(input);
        inputWrapper.appendChild(extensionSpan);
        fileWrapper.insertBefore(inputWrapper, fileNameElement);
        input.focus();

        input.setSelectionRange(0, namePart.length);
    }
});