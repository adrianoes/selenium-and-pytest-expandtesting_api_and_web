import pytest
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    # Baixa e obtém o caminho correto do ChromeDriver usando webdriver-manager
    chromedriver_path = ChromeDriverManager().install()

    # Configuração das opções do Chrome
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")  # "new" é recomendado para versões recentes do Chrome
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Definição de preferências para bloqueio de anúncios e pop-ups
    prefs = {
        "profile.default_content_setting_values.ads": 2,
        "profile.default_content_setting_values.popups": 2,
    }
    options.add_experimental_option("prefs", prefs)

    # Iniciando o Chrome com undetected-chromedriver e webdriver-manager
    driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options)

    # Bloqueio de URLs indesejadas via CDP (Chrome DevTools Protocol)
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*ads*", "*doubleclick.net*", "*googlesyndication.com*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    yield driver  # Retorna o driver para uso nos testes

    driver.quit()  # Fecha o driver após os testes
