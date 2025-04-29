from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging

def create_driver():
    try:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        
        # Используем Chrome из предустановленного образа
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        logging.error(f"Driver creation failed: {str(e)}")
        return None