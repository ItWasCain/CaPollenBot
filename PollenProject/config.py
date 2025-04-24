from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Режим без графического интерфейса
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Инициализация драйвера
driver = webdriver.Chrome(options=options)
