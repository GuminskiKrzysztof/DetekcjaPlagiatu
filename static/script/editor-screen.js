document.addEventListener("DOMContentLoaded", function() {
    const addFileButton = document.getElementById("add-file-button");
    const filesContainer = document.getElementById("files-container");
    const analyzeFileButton = document.getElementById("analyze-file-button");
    const analyzeProjectButton = document.getElementById("analyze-project-button");
    const codeEditor = document.getElementById("code-editor");

    addFileButton.addEventListener("click", function() {
        const newFile = document.createElement("p");
        newFile.textContent = `plik${filesContainer.children.length + 1}.py`;
        filesContainer.appendChild(newFile);
    });

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