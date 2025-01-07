from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path="d:/Informatyka/plagiatdet/DetekcjaPlagiatu/msedgedriver.exe")

# Inicjalizacja przeglądarki Edge
driver = webdriver.Edge(service=service)

# Otwieranie strony GitHub
url = 'https://github.com/Talarn/Medical_Segmentation/blob/master/medical_image_segmentation/RenderingView.py'
driver.get(url)

# Poczekaj, aż strona się załaduje
time.sleep(3)  # Czas zależny od szybkości internetu, może być dostosowany

# Pobieranie elementu textarea za pomocą Xpath
textarea = driver.find_element(By.XPATH, '//*[@id="read-only-cursor-text-area"]')

# Wydobycie tekstu z elementu textarea
code_content = textarea.get_attribute('value')

# Wyświetlenie kodu
print(code_content)

# Zamykanie przeglądarki
driver.quit()
