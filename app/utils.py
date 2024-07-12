import requests
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import io
import os
from pypdf import PdfReader
import io

def download_pdf(url):
    chromedriver_path = os.path.join(os.path.dirname(__file__), '../drivers/chromedriver-linux64/chromedriver')
    options = Options()
    options.headless = True  # Executar o Chrome em modo headless
    driver_service = Service(chromedriver_path)

    with webdriver.Chrome(service=driver_service, options=options) as driver:
        driver.get(url)

        # Esperar até que o botão esteja presente e clicável
        wait = WebDriverWait(driver, 20)
        download_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Clique aqui para fazer o download do DOM.")))

        # Clicar no botão de download
        download_button.click()
        time.sleep(5)  # Esperar o download completar

        # Encontrar a URL do PDF baixado
        pdf_url = driver.current_url

        response = requests.get(pdf_url)
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            raise Exception('Failed to download PDF')

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
