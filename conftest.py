import pytest
import undetected_chromedriver as uc

@pytest.fixture
def driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {
        "profile.default_content_setting_values.ads": 2,
        "profile.default_content_setting_values.popups": 2,
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*ads*", "*doubleclick.net*", "*googlesyndication.com*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    yield driver  # Passa o driver para os testes

    driver.quit()  # Fecha o driver após o teste
