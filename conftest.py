import pytest
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():

    chromedriver_path = ChromeDriverManager().install()

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "profile.default_content_setting_values.ads": 2,
        "profile.default_content_setting_values.popups": 2,
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options)
    driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": ["*ads*", "*doubleclick.net*", "*googlesyndication.com*"]
    })
    driver.execute_cdp_cmd("Network.enable", {})

    yield driver  
    driver.quit()  
