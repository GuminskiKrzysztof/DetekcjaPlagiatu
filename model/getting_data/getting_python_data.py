import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time



def get_urls(url="https://www.kaggle.com/search?q=chatbot+in%3Anotebooks"):
    service = Service(executable_path="C:/Users/k.guminski/PycharmProjects/plagiatDet/DetekcjaPlagiatu/msedge")

    driver = webdriver.Edge(service=service)

    urls = []
    driver.get(url)
    time.sleep(5)

    ul_element = driver.find_element(By.XPATH, '//*[@id="results"]/ul[1]')

    # Znajdź wszystkie linki <a> w <ul>
    a_elements = ul_element.find_elements(By.TAG_NAME, "a")

    for a in a_elements:
        if a.get_attribute("role") == "link":
            href = a.get_attribute("href")
            if href and href.startswith("/"):
                href = "https://www.kaggle.com" + href
            urls.append(href)
    driver.quit()

    return urls



def setup_kaggle_credentials(base_path):
    os.chdir(base_path)
    print(f"Aktualny katalog roboczy: {os.getcwd()}")


def download_kaggle_notebook(author, notebook_title, save_path="./notebooks"):
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
    full_code = "\n".join(code_cells)
    return full_code


def save_code_to_csv(all_codes, output_csv_path):
    """
    Zapisz wszystkie kody do jednego pliku CSV.
    """
    df = pd.DataFrame(all_codes)
    if os.path.exists(output_csv_path):
        df.to_csv(output_csv_path, index=False, encoding="utf-8", mode='a', header=False)
    else:
        df.to_csv(output_csv_path, index=False, encoding="utf-8", mode='w', header=True)


def process_kaggle_projects(project_urls, base_path, output_csv_path):
    """
    Pobierz, wyodrębnij kod i zapisz do jednego pliku CSV dla listy projektów.
    """
    setup_kaggle_credentials(base_path)  # Przejdź do katalogu z

    all_codes = []  # Lista na wszystkie kody i ich kategorie

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
            code = extract_code_from_notebook(notebook_path)

            all_codes.append({"code": code, "category": 'Chatbot'})
        else:
            print(f"Notebook {notebook_title} nie został znaleziony.")

    # Zapisz wszystkie kody do jednego pliku CSV
    save_code_to_csv(all_codes, output_csv_path)
    print(f"Wszystkie kody zapisano do: {output_csv_path}")


# Ścieżka do katalogu zawierającego plik
base_path = "C:/Users/k.guminski/PycharmProjects/plagiatDet/DetekcjaPlagiatu" 

# Lista URL projektów Kaggle
project_urls = get_urls()

# Ścieżka wyjściowego pliku CSV
output_csv_path = "C:/Users/k.guminski/PycharmProjects/plagiatDet/DetekcjaPlagiatu/all_python_codes.csv" 

# Uruchom proces
process_kaggle_projects(project_urls, base_path, output_csv_path)
