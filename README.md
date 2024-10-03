# selenium-expandtesting_UI

UI and API testing in [expandtesting](https://practice.expandtesting.com/notes/app/) note app. This project contains basic examples on how to use Selenium for UI tests writen in Python. Good practices such as hooks, custom commands and tags, among others, are used. All the necessary support documentation to develop this project is placed here. Although custom commands are used, the assertion code to each test is kept in it so we can work independently in each test. It creates one .json file for each test so we can share data between different commands in the test. The .json file is excluded after each test execution. 

# Pre-requirements:

| Requirement                     | Version        | Note                                                            |
| :------------------------------ |:---------------| :-------------------------------------------------------------- |
| Python                          | 3.12.5         | -                                                               |
| Visual Studio Code              | 1.89.1         | -                                                               |
| Python extension                | 2024.14.1      | -                                                               | 
| Selenium                        | 4.25.0         | -                                                               |
| Pytest                          | 8.3.3          | -                                                               |
| Copy CSS Selector               | 1.3.4          | -                                                               |
| Faker                           | 30.0.0         | -                                                               |
| requests                        | 2.32.3         | -                                                               |
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
- Open windows propmpt as admin and execute ```pip install selenium``` to install Selenium.
- Open windows propmpt as admin and execute ```pip install pytest``` to install Pytest.
- Open windows propmpt as admin and execute ```pip install Faker``` to install Faker library.
- See [Copy CSS Selector page](https://chromewebstore.google.com/detail/copy-css-selector/bmgbagkoginmbbgjapcacehjdojdnnhf?hl=pt-BR&utm_source=ext_sidebar) and install it. 
- Open windows propmpt as admin and execute ```pip install requests``` to install Requests library.
- Open windows propmpt as admin and execute ```pip install pytest-html``` to install pytest-html plugin.

# Tests:

- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests and generate a report inside reports folder.

# Support:

- [expandtesting API documentation page](https://practice.expandtesting.com/notes/api/api-docs/)
- [expandtesting API demonstration page](https://www.youtube.com/watch?v=bQYvS6EEBZc)
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

# Tips:

- UI and API tests to send password reset link to user's email and API tests to verify a password reset token and reset a user's password must be tested manually as they rely on e-mail verification. 
- To avoid conection problemns, a time.sleep(5) function was implemented between tests.
- Selenium provides no means to intercept network messages. Requests library is used to validate HTTP requests.  
