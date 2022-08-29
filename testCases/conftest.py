import time

import requests
import pytest
import os
from selenium import webdriver
from Utils.Config import Config
from Utils.selenium_locators import locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.opera.options import Options
from msedge.selenium_tools import EdgeOptions
from Utils.customLogger import LogGen
from Utils.Functions_Util import function
from datetime import date
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

os.makedirs('./Reports', exist_ok=True)
os.makedirs('./Logs', exist_ok=True)
logger = LogGen.log_gen()
global message_thread, url


@pytest.fixture(scope="session", autouse=True)
def give_me_access(browser):
    requests.get(Config.SSO_GIVEMEACCESS_LINK1)
    requests.get(Config.SSO_GIVEMEACCESS_LINK2)
    function.slack_test_start_msg(browser)
    logger.info(f"Starting Test on {browser} browser...")


@pytest.fixture()
def setup(browser):
    global driver
    env = os.getenv('ENV', "staging")
    if env.casefold() == "internal":
        url = Config.internal_url
    else:
        url = Config.staging_url
    if browser.casefold() == 'chrome':
        if os.getenv('REMOTE', False):  # False is default value
            driver = webdriver.Remote(command_executor="http://selenium__standalone-chrome:4444/wd/hub",
                                      desired_capabilities=DesiredCapabilities.CHROME)
        else:
            driver = webdriver.Chrome(executable_path=Config.CHROME_EXECUTABLE_PATH)

    elif browser.casefold() == 'firefox':
        if os.getenv('REMOTE', False):
            driver = webdriver.Remote(command_executor="http://selenium__standalone-firefox:4444/wd/hub",
                                      desired_capabilities=DesiredCapabilities.FIREFOX)
        else:
            driver = webdriver.Firefox(executable_path=Config.GECKODRIVER_EXECUTABLE_PATH)
    elif browser.casefold() == "edge":
        if os.getenv('REMOTE', False):
            driver = webdriver.Remote(command_executor="http://selenium__standalone-edge:4444/wd/hub",
                                      desired_capabilities=DesiredCapabilities.EDGE)
        else:
            options = EdgeOptions()
            desired_cap = {}
            options.use_chromium = True
            options.binary_location = Config.MSEDGE_BINARY_PATH
            driver = webdriver.Edge(executable_path=Config.MSEDGE_EXECUTABLE_PATH, capabilities=desired_cap)
    elif browser.casefold() == "opera":
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = Config.OPERA_BINARY_PATH
        if os.getenv('REMOTE', False):
            driver = webdriver.Remote(command_executor="http://selenium__standalone-opera:4444/wd/hub",
                                      desired_capabilities=DesiredCapabilities.OPERA)
        else:
            driver = webdriver.Opera(options=options, executable_path=Config.OPERA_EXECUTABLE_PATH)
    elif browser.casefold() == "safari":
        if os.getenv('REMOTE', False):
            driver = webdriver.Remote(command_executor="http://selenium__standalone-safari:4444/wd/hub",
                                      desired_capabilities=DesiredCapabilities.SAFARI)
    driver.implicitly_wait(10)
    driver.get(url)
    driver.implicitly_wait(15)
    driver.maximize_window()
    time.sleep(5)
    WebDriverWait(driver, 120).until(
        ec.visibility_of_element_located((By.XPATH, locators.textbox_email_xpath)))
    yield driver


def pytest_addoption(parser):  # This will get the value from CLI /hooks
    parser.addoption("--browser",
                     action="store",
                     default="chrome")
    parser.addoption("-I", "--slack_integration_flag",
                     dest="slack_integration_flag",
                     default="N",
                     help="Post the test report on slack channel: Y or N")


@pytest.fixture(scope='session')
def browser(request):  # This will return the Browser value to setup method
    return request.config.getoption("--browser")


"""#######################  PyTest HTML Report  ################################# """

# Hook for adding markers and Environment info to HTML Report
"""def pytest_configure(config):
    # :type config: object

    config.addinivalue_line(
        "markers", "regression: mark test to run only regression tests"
    )
    config._metadata['Application Under Test'] = 'Ito Edit'
    config._metadata['Test Name'] = 'Cross Browser Testing'
    config._metadata['Tester'] = 'Meenu Atrey'"""


# Hook for delete/modify environment info to HTML Report
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("PYTHON_HOME", None)
    metadata.pop("Plugins", None)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    message_thread = function.slack_initial_message()
    function.slack_test_summary_msg(message_thread)
    report = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Logs', 'Edit_cross_browser_regression.log'))
    # report = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Reports', 'Edit_cross_browser.html'))
    report_name = f"Edit_cross_browser_testing_report_{date.today()}"
    function.slack_upload_report(report,
                                 report_name,
                                 message_thread)
    function.slack_test_complete_msg(message_thread)
    print("Finished!")
