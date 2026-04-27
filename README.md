# selenium-and-pytest-expandtesting_api_and_web

API and web testing in [expandtesting](https://practice.expandtesting.com/notes/api/api-docs/). This project contains basic examples on how to use Pytest to test API and web tests. All the necessary support documentation to develop this project is placed here. Requests library is used to deal with API tests.  

# Pre-requirements:

| Requirement                     | Version        | Note                                                            |
| :------------------------------ |:---------------| :-------------------------------------------------------------- |
| Visual Studio Code              | 1.117.0        | -                                                               |
| Python                          | 3.13.4         | -                                                               |
| Python extension                | 2026.4.0       | -                                                               | 
| Pytest                          | 8.4.1          | -                                                               |
| Faker                           | 37.4.0         | -                                                               |
| requests                        | 2.32.3         | -                                                               |
| pytest-html                     | 4.1.1          | -                                                               |
          
# Installation:

- See [Visual Studio Code page](https://code.visualstudio.com/) and install the latest VSC stable version. Keep all the prefereced options as they are until you reach the possibility to check the checkboxes below: 
  - :white_check_mark: Add "Open with code" action to Windows Explorer file context menu. 
  - :white_check_mark: Add "Open with code" action to Windows Explorer directory context menu.
Check then both to add both options in context menu.
- See [python page](https://www.python.org/downloads/) and download the latest Python stable version. Start the installation and check the checkboxes below: 
  - :white_check_mark: Use admin privileges when installing py.exe 
  - :white_check_mark: Add python.exe to PATH
and keep all the other preferenced options as they are.
- Look for Python in the extensions marketplace and install the one from Microsoft.
- Open windows prompt as admin and execute ```pip install pytest``` to install Pytest.
- Open windows prompt as admin and execute ```pip install Faker``` to install Faker library.
- Open windows prompt as admin and execute ```pip install requests``` to install Requests library.
- Open windows prompt as admin and execute ```pip install pytest-html``` to install pytest-html plugin.

# Tests:

- Execute ```pytest ./tests -v --html=./reports/report.html``` to run tests in verbose mode and generate a report inside reports folder.
- Execute ```pytest ./tests/api/users_api_test.py -k create_user_api -v --html=./reports/report.html``` to run tests that contains "create_user_api" in its structure inside users_api_test.py file in verbose mode and generate a report inside reports folder.

# Support:

- [expandtesting API documentation page](https://practice.expandtesting.com/notes/api/api-docs/)
- [expandtesting API demonstration page](https://www.youtube.com/watch?v=bQYvS6EEBZc)
- [Pytest](https://docs.pytest.org/en/stable/)
- [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [How to mark test functions with attributes](https://docs.pytest.org/en/stable/how-to/mark.html)
- [How to parametrize fixtures and test functions](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [Welcome to Faker’s documentation!](https://faker.readthedocs.io/en/stable/)
- [Python For Loops](https://www.w3schools.com/python/python_for_loops.asp)
- [Python – Call function from another file](https://www.geeksforgeeks.org/python-call-function-from-another-file/)
- [Setting Up and Tearing Down](https://www.selenium.dev/documentation/webdriver/getting_started/using_selenium/#setting-up-and-tearing-down)
- [Requests: HTTP for Humans™](https://requests.readthedocs.io/en/latest/)
- [How to get the localStorage with Python and Selenium WebDriver](https://stackoverflow.com/a/46361890/10519428)
- [Python Requests Library Complete Tutorial - Rest API Testing](https://www.youtube.com/watch?v=LP8NlUYHQGg)
- [Python Accessing Nested JSON Data [duplicate]](https://stackoverflow.com/a/23306717/10519428)
- [Write JSON data to a file in Python](https://sentry.io/answers/write-json-data-to-a-file-in-python/)
- [Read JSON file using Python](https://www.geeksforgeeks.org/read-json-file-using-python/)
- [Python | os.remove() method](https://www.geeksforgeeks.org/python-os-remove-method/)
- [ImportError: No module named 'support'](https://stackoverflow.com/a/56268774/10519428)
- [Python String strip() Method](https://www.w3schools.com/python/ref_string_strip.asp)

# Tips:

- API tests to verify a password reset token and reset a user's password must be tested manually as they rely on e-mail verification. 
- delete_note_api was created only with the practice purpose since there is the possibility to delete the user right away. 
