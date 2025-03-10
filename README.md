# selenium-expandtesting_UI_and_API

UI and API testing in [expandtesting](https://practice.expandtesting.com/notes/app/) note app. This project contains basic examples on how to use Selenium to test UI, API and how to combine UI and API tests writen in Python. Good practices such as hooks, custom commands and tags, among others, are used. All the necessary support documentation to develop this project is placed here. Although custom commands are used, the assertion code to each test is kept in it so we can work independently in each test. Requests library is used to deal with API tests. It creates one .json file for each test so we can share data between different commands in the test. The .json file is excluded after each test execution. 

# Pre-requirements:

| Requirement                     | Version        | Note                                                            |
| :------------------------------ |:---------------| :-------------------------------------------------------------- |
| Python                          | 3.12.5         | -                                                               |
| Visual Studio Code              | 1.89.1         | -                                                               |
| Python extension                | 2024.14.1      | -                                                               | 
| Selenium                        | 4.25.0         | -                                                               |
| Pytest                          | 8.3.3          | -                                                               |
| SelectorsHub                    | 5.3.4          | -                                                               |
| Faker                           | 30.0.0         | -                                                               |
| requests                        | 2.32.3         | -                                                               |
| undetected-chromedriver         | 3.5.5          | -                                                               |
| webdriver-manager               | 4.0.2          | -                                                               |
| pytest-html                     | 4.1.1          | -                                                               |
          
# Installation:

- See [python page](https://www.python.org/downloads/) and download the latest Python stable version. Start the installation and check the checkboxes below: 
  - :white_check_mark: Use admin privileges when installing py.exe 
  - :white_check_mark: Add python.exe to PATH
and keep all the other preferenced options as they are.
- See [Visual Studio Code page](https://code.visualstudio.com/) and install the latest VSC stable version. Keep all the prefereced options as they are until you reach the possibility to check the checkboxes below: 
  - :white_check_mark: Add "Open with code" action to Windows Explorer file context menu. 
  - :white_check_mark: Add "Open with code" action to Windows Explorer directory context menu.
Check then both to add both options in context menu.
- Look for Python in the extensions marketplace and install the one from Microsoft.
- Open windows prompt as admin and execute ```pip install selenium``` to install Selenium.
- Open windows prompt as admin and execute ```pip install pytest``` to install Pytest.
- Open windows prompt as admin and execute ```pip install Faker``` to install Faker library.
- Open windows prompt as admin and execute ```pip install undetected-chromedriver``` to install undetected-chromedriver.
- Open windows prompt as admin and execute ```pip install webdriver-manager``` to install webdriver-manager.
- See [SelectorsHub page](https://chromewebstore.google.com/detail/selectorshub-xpath-helper/ndgimibanhlabgdgjcpbbndiehljcpfh?hl=pt-BR&utm_source=ext_sidebar) and install it. 
- Open windows prompt as admin and execute ```pip install requests``` to install Requests library.
- Open windows prompt as admin and execute ```pip install pytest-html``` to install pytest-html plugin.

# Tests:

- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests in verbose mode and generate a report inside reports folder.
- Execute ```pytest .\tests\ui\notes_ui_test.py -k note_ui_invalid -v --html=./reports/report.html``` to run tests that contains "note_ui_invalid" in its structure inside notes_ui_test.py file in verbose mode and generate a report inside reports folder.

# Support:

- [expandtesting API documentation page](https://practice.expandtesting.com/notes/api/api-docs/)
- [expandtesting API demonstration page](https://www.youtube.com/watch?v=bQYvS6EEBZc)
- [Pytest](https://docs.pytest.org/en/stable/)
- [How to obtain a CSS Selector](https://help.probely.com/en/articles/8480719-how-to-obtain-a-css-selector)
- [Using faker with selenium and python](https://stackoverflow.com/a/27650137/10519428)
- [Faker 30.0.0 documentation](https://faker.readthedocs.io/en/stable/)
- [Working with windows and tabs](https://www.selenium.dev/documentation/webdriver/interactions/windows/)
- [Keeping browser open](https://www.selenium.dev/documentation/webdriver/browsers/chrome/#keeping-browser-open)
- [Selenium: WebDriverException:Chrome failed to start: crashed as google-chrome is no longer running so ChromeDriver is assuming that Chrome has crashed](https://stackoverflow.com/a/53073789/10519428)
- [Implicit waits](https://www.selenium.dev/documentation/webdriver/waits/#implicit-waits)
- [Is Displayed](https://www.selenium.dev/documentation/webdriver/elements/information/#is-displayed)
- [Python For Loops](https://www.w3schools.com/python/python_for_loops.asp)
- [Python – Call function from another file](https://www.geeksforgeeks.org/python-call-function-from-another-file/)
- [Setting Up and Tearing Down](https://www.selenium.dev/documentation/webdriver/getting_started/using_selenium/#setting-up-and-tearing-down)
- [Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it #1653](https://github.com/urllib3/urllib3/issues/1653#issuecomment-512794112)
- [Requests: HTTP for Humans™](https://requests.readthedocs.io/en/latest/)
- [How to get the localStorage with Python and Selenium WebDriver](https://stackoverflow.com/a/46361890/10519428)
- [Python Requests Library Complete Tutorial - Rest API Testing](https://www.youtube.com/watch?v=LP8NlUYHQGg)
- [Python Accessing Nested JSON Data [duplicate]](https://stackoverflow.com/a/23306717/10519428)
- [Session Objects](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects)
- [Headless is Going Away!](https://www.selenium.dev/blog/2023/headless-is-going-away/)
- [Write JSON data to a file in Python](https://sentry.io/answers/write-json-data-to-a-file-in-python/)
- [Read JSON file using Python](https://www.geeksforgeeks.org/read-json-file-using-python/)
- [Python | os.remove() method](https://www.geeksforgeeks.org/python-os-remove-method/)
- [WebDriverWait on finding element by CSS Selector](https://stackoverflow.com/a/53527710/10519428)
- [ImportError: No module named 'support'](https://stackoverflow.com/a/56268774/10519428)
- [Python String strip() Method](https://www.w3schools.com/python/ref_string_strip.asp)
- [StaleElementReferenceException on Python Selenium](https://stackoverflow.com/a/44914767/10519428)
- [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 81](https://stackoverflow.com/a/61412036)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- [distutils](https://docs.python.org/3/library/distutils.html)
- [ChatGPT](https://openai.com/chatgpt/)

# Tips:

- UI and API tests to send password reset link to user's email and API tests to verify a password reset token and reset a user's password must be tested manually as they rely on e-mail verification. 
- To avoid conection problemns, a time.sleep(5) function was implemented between tests.
- Selenium provides no means to intercept network messages. Requests library is used to validate HTTP requests. 
- Features to scroll to element were presenting fail behavior alongside with complications to find the element due to iframes in the screen. Arrow down workaround was used to solve this problem. This solution fits the 1980x1080 and 100% scale screen resolution. 
- Always double check the best selector with the help of SelectorsHub google extension. 
- The undetected-chromedriver library will remove adds from the screen. 
- Python was downgraded in workflow file to 3.11 since is the last version that contains distutils library, needed for undetected-chromedriver.
- delete_note_api was created only with the practice purpose since there is the possibility to delete the user right away. 
- Trust ChatGPT.
