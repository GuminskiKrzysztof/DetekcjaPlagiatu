// Wait for both DOM and JSZip to be ready
Promise.all([
    new Promise(resolve => document.addEventListener("DOMContentLoaded", resolve)),
    new Promise(resolve => {
        if (window.JSZip) resolve();
        else window.addEventListener('load', resolve);
    })
]).then(() => {
    const CONFIG = {
        MAX_FILES: 10,
        MAX_TOTAL_SIZE_MB: 10,
        ALLOWED_EXTENSIONS: ['cpp', 'py', 'zip']
    };

    const createButton = document.getElementById("create-button");
    const selectFileButton = document.getElementById("select-file-button");
    const fileInput = document.getElementById("file-input");
    const nextButton = document.getElementById("next-button");
    const fileListDiv = document.getElementById("file-list");
    const dropZone = document.getElementById("drop-zone");

    let files = [];
    let totalSize = 0; // Track total size in bytes

    function bytesToMB(bytes) {
        return bytes / (1024 * 1024);
    }

    function validateFileSize(file) {
        if (bytesToMB(totalSize + file.size) > CONFIG.MAX_TOTAL_SIZE_MB) {
            throw new Error(`Przekroczono maksymalny łączny rozmiar plików (${CONFIG.MAX_TOTAL_SIZE_MB}MB).`);
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
            
            const validFiles = Object.values(zip.files).filter(file => {
                if (file.dir) return false;
                const extension = file.name.split('.').pop().toLowerCase();
                return CONFIG.ALLOWED_EXTENSIONS.includes(extension);
            });

            if (files.length + validFiles.length > CONFIG.MAX_FILES) {
                throw new Error(`Przekroczono maksymalną liczbę plików (${CONFIG.MAX_FILES}).`);
            }

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
                            fromZip: zipFile.name,
                            size: file._data.uncompressedSize  // Zapisujemy rozmiar pliku
                        };
                        files.push(fileObject);
                    }
                }
            }

            const zipItem = createFileElement({
                id: `zip-${Date.now()}`,
                name: zipFile.name,
                isZip: true,
                originalSize: zipFile.size
            }, zipFile);
            fileListDiv.appendChild(zipItem);

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
            
            if (files.length >= CONFIG.MAX_FILES) {
                throw new Error(`Przekroczono maksymalną liczbę plików (${CONFIG.MAX_FILES}).`);
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
                    
                    const fileItem = createFileElement(fileObject, file);
                    fileListDiv.appendChild(fileItem);

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
        statsDiv.textContent = `Pliki: ${files.length}/${CONFIG.MAX_FILES} | Rozmiar: ${bytesToMB(totalSize).toFixed(2)}MB/${CONFIG.MAX_TOTAL_SIZE_MB}MB`;
    }

    function createStatsDiv() {
        const statsDiv = document.createElement('div');
        statsDiv.id = 'file-stats';
        statsDiv.style.color = '#aeff8c';
        // Insert at the bottom of drop-zone instead of before fileListDiv
        dropZone.appendChild(statsDiv);
        return statsDiv;
    }

    function getFileIcon(extension) {
        switch (extension.toLowerCase()) {
            case 'cpp':
                return '/static/img/file_cpp.png';
            case 'py':
                return '/static/img/file_python.png';
            case 'zip':
                return '/static/img/file_zip.png';
            default:
                return '/static/img/file_cpp.png';
        }
    }

    function createFileElement(fileObject, originalFile) {
        const fileExtension = fileObject.name.split('.').pop().toLowerCase();
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        fileItem.dataset.fileId = fileObject.id;

        const icon = document.createElement('img');
        icon.src = getFileIcon(fileExtension);
        icon.classList.add('file-icon');
        
        const fileName = document.createElement('div');
        fileName.classList.add('file-name');
        fileName.textContent = fileObject.name;

        const removeButton = document.createElement('div');
        removeButton.classList.add('remove-file');
        removeButton.innerHTML = '×';
        removeButton.onclick = () => {
            if (fileObject.isZip) {
                // Jeśli to plik ZIP, usuń wszystkie pliki z tego ZIP-a
                files = files.filter(f => !f.fromZip || f.fromZip !== fileObject.name);
                totalSize -= fileObject.originalSize;
            } else {
                const fileIndex = files.findIndex(f => f.id === fileObject.id);
                if (fileIndex !== -1) {
                    if (originalFile) {
                        totalSize -= originalFile.size;
                    } else if (fileObject.size) {
                        totalSize -= fileObject.size;
                    }
                    files.splice(fileIndex, 1);
                }
            }
            fileItem.remove();
            updateFileStats();
        };

        fileItem.appendChild(icon);
        fileItem.appendChild(fileName);
        fileItem.appendChild(removeButton);
        
        return fileItem;
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