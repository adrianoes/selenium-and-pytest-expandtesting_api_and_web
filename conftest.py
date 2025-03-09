import pytest
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Criação do serviço corretamente com ChromeDriverManager
service = Service(ChromeDriverManager().install())

# Agora o driver recebe o serviço adequado
driver = webdriver.Chrome(service=service)


@pytest.fixture
def driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Desativa o uso de GPU (pode ajudar em alguns casos)
    options.add_argument("--no-sandbox")  # Necessário para o ambiente de CI, como o GitHub Actions
    options.add_argument("--disable-software-rasterizer")  # Desativa o rasterizador de software
    options.add_argument("--remote-debugging-port=9222")  # Pode ajudar a solucionar problemas de comunicação
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    prefs = {
        "profile.default_content_setting_values.ads": 2,
        "profile.default_content_setting_values.popups": 2,
    }
    options.add_experimental_option("prefs", prefs)

    # Inicialize o driver com as opções corretamente configuradas
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*ads*", "*doubleclick.net*", "*googlesyndication.com*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    yield driver
    driver.quit()
