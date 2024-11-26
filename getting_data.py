import os
import json
import pandas as pd


def setup_kaggle_credentials(base_path):
    """
    Przejdź do katalogu zawierającego plik kaggle.json i ustaw środowisko.
    """
    os.chdir(base_path)  # Zmień katalog roboczy
    print(f"Aktualny katalog roboczy: {os.getcwd()}")


def download_kaggle_notebook(author, notebook_title, save_path="./notebooks"):
    """
    Pobierz notebook z Kaggle i zapisz go do folderu.
    """
    os.makedirs(save_path, exist_ok=True)
    command = f"kaggle kernels pull {author}/{notebook_title} -p {save_path}"
    os.system(command)


def extract_code_from_notebook(notebook_path):
    """
    Wyodrębnij kod z komórek notebooka Jupyter (.ipynb).
    """
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
    code_cells = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            code_cells.append("".join(cell.get("source", [])))
    return code_cells


def save_code_to_csv(codes, output_csv_path):
    """
    Zapisz wyodrębniony kod do pliku CSV.
    """
    df = pd.DataFrame({"code": codes})
    df.to_csv(output_csv_path, index=False, encoding="utf-8")


def process_kaggle_projects(project_urls, base_path, output_dir="./output"):
    """
    Pobierz, wyodrębnij kod i zapisz do CSV dla listy projektów.
    """
    setup_kaggle_credentials(base_path)  # Przejdź do katalogu z kaggle.json
    os.makedirs(output_dir, exist_ok=True)

    for url in project_urls:
        # Wyodrębnij autora i nazwę projektu z URL
        parts = url.strip().split("/")[-2:]
        author, notebook_title = parts

        # Pobierz notebook
        print(f"Pobieram projekt: {author}/{notebook_title}")
        download_kaggle_notebook(author, notebook_title)

        # Ścieżka do pobranego notebooka
        notebook_path = f"./notebooks/{notebook_title}.ipynb"

        # Wyodrębnij kod
        if os.path.exists(notebook_path):
            print(f"Wyodrębniam kod z: {notebook_title}")
            code_cells = extract_code_from_notebook(notebook_path)

            # Zapisz kod do CSV
            output_csv_path = os.path.join(output_dir, f"{notebook_title}.csv")
            save_code_to_csv(code_cells, output_csv_path)
            print(f"Zapisano kod do: {output_csv_path}")
        else:
            print(f"Notebook {notebook_title} nie został znaleziony.")


# Ścieżka do katalogu zawierającego plik kaggle.json
base_path = "C:/Users/k.guminski/PycharmProjects/plagiatDet/DetekcjaPlagiatu"  # Zmień na rzeczywistą ścieżkę

# Lista URL projektów Kaggle
project_urls = [
    "https://www.kaggle.com/code/odins0n/video-anomaly-detection",
    "https://www.kaggle.com/code/victorambonati/unsupervised-anomaly-detection",
    "https://www.kaggle.com/code/joshuaswords/time-series-anomaly-detection"
]

# Uruchom proces
process_kaggle_projects(project_urls, base_path)
