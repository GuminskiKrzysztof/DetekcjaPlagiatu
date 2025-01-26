import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_code_to_csv(all_codes, output_csv_path):
    """
    Zapisz wszystkie kody do jednego pliku CSV.
    """
    df = pd.DataFrame(all_codes)
    if os.path.exists(output_csv_path):
        df.to_csv(output_csv_path, index=False, encoding="utf-8", mode='a', header=False)
    else:
        df.to_csv(output_csv_path, index=False, encoding="utf-8", mode='w', header=True)

def saving_codes_to_csv(url):
    service = Service(executable_path="D:/Informatyka/plagiatDet/DetekcjaPlagiatu/msedgedriver.exe")

    driver = webdriver.Edge(service=service)

    output_csv_path = "/DetekcjaPlagiatu/backend/data/all_cpp_codes.csv"
    codes = []
    driver.get(url)
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
    )
    consent_button.click()
    print("Kliknięto przycisk zgody!")
    time.sleep(3)


    codes = []
    code_blocks = driver.find_elements(By.CLASS_NAME, "CodeMirror")
    for block in code_blocks:
        # Pobierz wszystkie linie kodu z danego bloku
        code_lines = block.find_elements(By.CLASS_NAME, "CodeMirror-line")
        code = "\n".join([line.text for line in code_lines])
        if code.strip():
            codes.append({"code": code, "category": 'Advanced'})

    save_code_to_csv(codes, output_csv_path)

    # Wyświetl wyodrębniony kod
    print("Wyodrębniony kod:")
    print(codes)
    print(len(codes))
    driver.quit()


def saving_codes_to_csv2(url):
    service = Service(executable_path="D:/Informatyka/plagiatDet/DetekcjaPlagiatu/msedgedriver.exe")

    driver = webdriver.Edge(service=service)

    output_csv_path = "/DetekcjaPlagiatu/backend/data/all_cpp_codes.csv"
    codes = []
    driver.get(url)
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
    )
    consent_button.click()
    print("Kliknięto przycisk zgody!")
    time.sleep(3)


    codes = []
    code_blocks = driver.find_elements(By.CSS_SELECTOR, "td.code div.container")
    for block in code_blocks:
        code_lines = block.find_elements(By.CSS_SELECTOR, "code")
        code = "\n".join([line.text for line in code_lines])
        if code.strip():
            codes.append({"code": code, "category": 'Advanced'})
    save_code_to_csv(codes, output_csv_path)

    print("Pobrano kod źródłowy:")
    print(codes)
    print(len(codes))


saving_codes_to_csv("https://www.geeksforgeeks.org/cc-preprocessors/")