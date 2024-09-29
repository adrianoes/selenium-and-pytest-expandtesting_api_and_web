import  pytest
from    selenium  import  webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
from    selenium.webdriver.common.by  import  By
from    faker import Faker
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver import ActionChains

@pytest.mark.users
def test_create_user():
    user_name = Faker().name()
    user_email = Faker().company_email()
    user_password = Faker().password()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://practice.expandtesting.com/notes/app/register")
    driver.find_element(By.CSS_SELECTOR, "#root > div > div > div").click()    
    assert driver.title == "Notes React Application for Automation Testing Practice"
    driver.find_element(By.CSS_SELECTOR, "#name").send_keys(user_name)
    driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "#confirmPassword").send_keys(user_password)
    driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()

    # driver.get("https://practice.expandtesting.com/notes/app/login")
    # driver.find_element(By.CSS_SELECTOR, "#email").send_keys(user_email)
    # driver.find_element(By.CSS_SELECTOR, "#password").send_keys(user_password)
    # driver.find_element(By.CSS_SELECTOR, "div.form-group > button").click()

    # driver.get("https://practice.expandtesting.com/notes/app/profile")
    # driver.find_element(By.CSS_SELECTOR, "div.row > div > button").click()
    # driver.find_element(By.CSS_SELECTOR, "div.modal-footer > button.btn.btn-danger").click()


# miss scroll to element, assert text, check if can assert api reponse

    #root > div > div > div:nth-child(3) > div > div > div > div > div > div.modal.modal-background.fade.show.bg-black.bg-opacity-75 > div > div > div.modal-footer > button.btn.btn-danger

# if quit command is not commented, detach option to keep browser open after test will not work
    driver.quit()