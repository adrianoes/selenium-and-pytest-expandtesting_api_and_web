# selenium-and-pytest-expandtesting_api_and_web

API and web testing in [expandtesting](https://practice.expandtesting.com/notes/api/api-docs/). This project contains basic examples on how to use Pytest to test API and web tests. All the necessary support documentation to develop this project is placed here. Requests library is used to deal with API tests.  

# Pre-requirements:

| Requirement                     | Version        | Note          |
| :------------------------------ |:---------------| :-------------|
| Visual Studio Code              | 1.117.0        | -             |
| Python                          | 3.13.4         | -             |
| Python extension                | 2026.4.0       | -             | 
| Pytest                          | 8.4.1          | -             |
| Faker                           | 37.4.0         | -             |
| requests                        | 2.32.3         | -             |
| pytest-html                     | 4.1.1          | -             |
| python-dotenv                   | 1.2.1          | -             |
          
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
- Open windows prompt as admin and execute ```pip install python-dotenv``` to install python-dotenv.

# Tests:

- Run ```pytest ./tests/api/test_users_api.py -m basic -v --html=./reports/report.html``` to execute all positive tests in a file in verbose mode with HTML report.
- Run ```pytest ./tests/api/test_users_api.py -m negative -v --html=./reports/report.html``` to execute all negative tests in a file in verbose mode with HTML report.
- Run ```pytest ./tests -m basic -v --html=./reports/report.html``` to execute all positive in verbose mode with HTML report.
- Run ```pytest ./tests -m negative -v --html=./reports/report.html``` to execute all negative in verbose mode with HTML report.
- Run `pytest ./tests -v --html=./reports/report.html` to execute all tests in verbose mode and generate an HTML report in the reports folder in verbose mode with HTML report.
- Run `pytest ./tests/api/test_users_api.py -v --html=./reports/report.html` to execute only tests inside test_users_api.py, in verbose mode with HTML report.
- Run `pytest ./tests/api/test_users_api.py -k create_user -v --html=./reports/report.html` to execute only tests containing "create_user" in their name inside test_users_api.py, in verbose mode with HTML report.
- Run `python run_tests_with_jira.py` to execute all tests and automatically create JIRA issues for any failures in a single command. Run `python jira_reporter.py` to manually create JIRA issues for failed tests after reviewing the results.
- In Visual Studio Code, click the :point_right: **Testing** button on the left sidebar and choose the tests to execute.

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

- The `run_tests_with_jira.py` script runs the tests and automatically creates JIRA issues for any failures, using the configuration from your `.env` file.
- The `python-dotenv` package is required to read variables from `.env` and is already listed in requirements.txt.
- Test artifacts (results, logs, screenshots) are saved in `test_artifacts/` and used to provide details in the JIRA issues.
- To create JIRA issues only after a test run, use `python jira_reporter.py`.
