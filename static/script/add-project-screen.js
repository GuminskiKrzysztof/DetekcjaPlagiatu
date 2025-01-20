import { toggleVisibility } from "./utils.js";

// Wait for both DOM and JSZip to be ready
Promise.all([
    new Promise(resolve => document.addEventListener("DOMContentLoaded", resolve)),
    new Promise(resolve => {
        if (window.JSZip) resolve();
        else window.addEventListener('load', resolve);
    })
]).then(() => {
    const MAX_FILES = 10; // Maximum number of files (including files from ZIPs)
    const MAX_TOTAL_SIZE_MB = 10; // Maximum total size in MB

    const addProjectScreen = document.getElementById("add-project-screen");
    const editorScreen = document.getElementById("editor-screen");
    const createButton = document.getElementById("create-button");
    const selectFileButton = document.getElementById("select-file-button");
    const fileInput = document.getElementById("file-input");
    const nextButton = document.getElementById("next-button");
    const fileListDiv = document.getElementById("file-list");
    const dropZone = document.getElementById("drop-zone");

    let files = [];
    let zipFiles = [];
    let totalSize = 0; // Track total size in bytes

    function bytesToMB(bytes) {
        return bytes / (1024 * 1024);
    }

    function validateFileSize(file) {
        if (bytesToMB(totalSize + file.size) > MAX_TOTAL_SIZE_MB) {
            throw new Error(`Przekroczono maksymalny łączny rozmiar plików (${MAX_TOTAL_SIZE_MB}MB).`);
        }
        return true;
    }

    createButton.addEventListener("click", function() {
        window.location.href = "/edytor";
    });

    selectFileButton.addEventListener("click", function() {
        fileInput.click();
    });

    // Create stats div immediately after initialization
    createStatsDiv();
    updateFileStats(); // Show initial stats (0/10 files, 0/10MB)

    async function handleZipFile(zipFile) {
        try {
            validateFileSize(zipFile);
            const zip = await JSZip.loadAsync(zipFile);
            
            let validFiles = [];
            for (const filename in zip.files) {
                const file = zip.files[filename];
                if (!file.dir) {
                    const extension = filename.split('.').pop().toLowerCase();
                    if (['cpp', 'py'].includes(extension)) {
                        validFiles.push(file);
                    }
                }
            }

            if (files.length + validFiles.length > MAX_FILES) {
                throw new Error(`Przekroczono maksymalną liczbę plików (${MAX_FILES}).`);
            }

            const zipFiles = []; // Tablica do przechowywania plików z tego ZIP-a
            
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
                            content: content,
                            fromZip: zipFile.name  // Oznaczamy pliki jako pochodzące z tego ZIP-a
                        };
                        files.push(fileObject);
                        zipFiles.push(fileObject.id);
                    }
                }
            }

            const zipNameDiv = document.createElement("div");
            zipNameDiv.textContent = zipFile.name;
            zipNameDiv.classList.add("file-name", "zip-file");

            const removeButton = document.createElement("span");
            removeButton.innerHTML = "&#10006;";
            removeButton.classList.add("remove-file");
            removeButton.onclick = () => {
                // Usuń wszystkie pliki z tego ZIP-a
                files = files.filter(f => !f.fromZip || f.fromZip !== zipFile.name);
                zipNameDiv.remove();
                totalSize -= zipFile.size;
                updateFileStats();
            };
            
            zipNameDiv.appendChild(removeButton);
            fileListDiv.appendChild(zipNameDiv);

            totalSize += zipFile.size;
            updateFileStats();
        } catch (error) {
            alert(error.message || "Błąd podczas przetwarzania pliku ZIP.");
            console.error(error);
        }
    }

    function handleFile(file) {
        try {
            const fileExtension = file.name.split(".").pop().toLowerCase();
            
            if (files.length >= MAX_FILES) {
                throw new Error(`Przekroczono maksymalną liczbę plików (${MAX_FILES}).`);
            }

            if (fileExtension === 'zip') {
                handleZipFile(file);
            } else if (['cpp', 'py'].includes(fileExtension)) {
                validateFileSize(file);
                
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
                        const fileIndex = files.findIndex(f => f.id === fileObject.id);
                        if (fileIndex !== -1) {
                            totalSize -= file.size;
                            files.splice(fileIndex, 1);
                            fileNameDiv.remove();
                            updateFileStats();
                        }
                    };
                    
                    fileNameDiv.appendChild(removeButton);
                    fileListDiv.appendChild(fileNameDiv);

                    totalSize += file.size;
                    updateFileStats();
                };
                reader.readAsText(file);
            } else {
                throw new Error("Nieobsługiwany format pliku. Wybierz plik .cpp, .py lub .zip");
            }
        } catch (error) {
            alert(error.message);
            fileInput.value = "";
        }
    }

    function updateFileStats() {
        const statsDiv = document.getElementById('file-stats');
        statsDiv.textContent = `Pliki: ${files.length}/${MAX_FILES} | Rozmiar: ${bytesToMB(totalSize).toFixed(2)}MB/${MAX_TOTAL_SIZE_MB}MB`;
    }

    function createStatsDiv() {
        const statsDiv = document.createElement('div');
        statsDiv.id = 'file-stats';
        statsDiv.style.marginTop = '10px';
        statsDiv.style.color = '#aeff8c';
        fileListDiv.parentNode.insertBefore(statsDiv, fileListDiv);
        return statsDiv;
    }

    fileInput.addEventListener("change", function(event) {
        const files = Array.from(event.target.files);
        files.forEach(file => {
            handleFile(file);
        });
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

    // Add drag & drop event listeners
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const droppedFiles = Array.from(e.dataTransfer.files);
        droppedFiles.forEach(file => {
            handleFile(file);
        });
    });

});