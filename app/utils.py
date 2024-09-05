import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import io
import os
from pypdf import PdfReader

def download_pdf(url):
    """
    Downloads a PDF file from the specified URL. This function automates the 
    interaction with a web page to click on a download link, retrieve the PDF,
    and return it as a byte stream.
    """
    # Define the path to the ChromeDriver executable
    chromedriver_path = os.path.join(os.path.dirname(__file__), '../drivers/chromedriver-linux64/chromedriver')
    
    # Set up Chrome options to run in headless mode (no GUI)
    options = Options()
    options.headless = True  # Run Chrome in headless mode (no GUI)
    driver_service = Service(ChromeDriverManager().install())
  
    # Use a context manager to ensure the WebDriver is properly closed after use
    with webdriver.Chrome(service=driver_service, options=options) as driver:
        driver.get(url)

        # Wait until the download button is present and clickable
        wait = WebDriverWait(driver, 20)
        download_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Clique aqui para fazer o download do DOM.")))

        # Click the download button
        download_button.click()
        
        # Wait for the download to complete
        time.sleep(5)

        # Get the current URL, which should now be the PDF URL
        pdf_url = driver.current_url

        # Download the PDF content using requests
        response = requests.get(pdf_url)
        if response.status_code == 200:
            return io.BytesIO(response.content)
        else:
            raise Exception('Failed to download PDF')

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a given PDF file.
    """
    reader = PdfReader(pdf_file)
    text = ""
    
    # Iterate over each page in the PDF and extract the text
    for page in reader.pages:
        text += page.extract_text()
    
    return text
