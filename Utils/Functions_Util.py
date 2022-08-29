from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os
from Utils.selenium_locators import locators
from selenium.common.exceptions import NoSuchElementException
from Utils.zephyr import Zephyr
from Utils.Config import Config
from Utils import zephyr_settings
from Utils.slackclient import Slack, BlockMaker

zephyr = Zephyr(zephyr_settings.ZEPHYR_TOKEN)


class function:
    global slack_channel, custome_bot_token, slack

    slack_channel = Config.slack_channel
    custom_bot_token = Config.custom_bot_token
    slack = Slack(slack_channel, token=custom_bot_token)

    @staticmethod
    def header_search(driver, search_string, exp_elem, testcase_key):
        try:
            WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.ID, locators.Header_Search)))
            driver.find_element(By.ID, locators.Header_Search).click()
            time.sleep(1)
            driver.find_element(By.ID, locators.Header_Search).clear()
            driver.find_element(By.ID, locators.Header_Search).send_keys(search_string, Keys.ENTER)
            time.sleep(1)
            WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.XPATH, exp_elem)))
            function.log_capture("Header Search executed")
        except Exception as e:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    "Exception caught while executing header search")
            function.log_capture("Exception caught while executing header search")
            function.log_capture("Python Says:")
            function.log_capture(e)
            driver.fail()

    @staticmethod
    def execute_header_search_and_click_link(driver, search_string, exp_elem, testcase_key):
        try:
            driver.find_element(By.ID, locators.Header_Search).click()
            time.sleep(2)
            driver.find_element(By.ID, locators.Header_Search).clear()
            driver.find_element(By.ID, locators.Header_Search).send_keys(search_string, Keys.ENTER)
            time.sleep(2)
            WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, exp_elem)))
            print("Header Search executed")
            print("-------------------------------------------------------------------------------")
        except Exception as e:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    "Exception caught while executing header search")
            function.log_capture("Exception caught while executing header search")
            function.log_capture("Python Says:")
            function.log_capture(e)
            driver.fail()

        try:
            driver.find_element(By.XPATH, exp_elem).click()
            time.sleep(5)
            function.log_capture(F'{exp_elem} link clicked')
        except Exception as e:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'Exception caught on {exp_elem} link click after header search')
            function.log_capture(f'Exception caught on {exp_elem} link click after header search')
            function.log_capture("Python Says:")
            function.log_capture(e)
            driver.fail()

    @staticmethod
    def assert_elems(cls, driver, elem_name, elem1, elem2, testcase_key):
        try:
            cls.assertEqual(elem1, elem2)
            function.log_capture(f'{elem_name} asserted')
            time.sleep(1)
        except Exception as e:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'Exception caught while asserting {elem_name}')
            function.log_capture(f'Exception in asserting {elem_name}')
            function.log_capture("Python Says:")
            function.log_capture(e)
            cls.fail()

    @staticmethod
    def check_elem(cls, driver, elem, elem_name, testcase_key):
        try:
            driver.find_element(By.XPATH, elem).is_displayed()
            function.log_capture(f'label {elem_name} displayed on page')
        except NoSuchElementException:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'Label {elem_name} not found')
            function.log_capture(f'Label {elem_name} not found')
            cls.fail()

    @staticmethod
    def check_link(cls, driver, link, link_name, testcase_key):
        try:
            driver.find_element(By.XPATH, link).is_displayed()
            function.log_capture(f'{link_name} link present on page as expected')
        except NoSuchElementException:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'{link_name} link not found')
            function.log_capture(f'{link_name} link not found')
            cls.fail()

    @staticmethod
    def check_Table_Header(cls, driver, header_elem, elem_name, testcase_key):
        try:
            driver.find_element(By.XPATH, header_elem).is_displayed()
            function.log_capture(f'{elem_name} table header present on page as expected')
        except NoSuchElementException:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'{elem_name} table header not found')
            function.log_capture(f'{elem_name} table header not found')
            cls.fail()

    @staticmethod
    def check_header(cls, driver, elem, elem_name, testcase_key):
        try:
            driver.find_element(By.XPATH, elem).is_displayed()
            function.log_capture(f'{elem_name} header is displayed on page')
        except NoSuchElementException:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'Header {elem_name} not found')
            function.log_capture(f'Header {elem_name} not found')
            cls.fail()

    @staticmethod
    def load_tab_page(cls, driver, tab_name, tab_link, exp_elem, testcase_key):
        try:
            driver.find_element(By.XPATH, tab_link).click()
            WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, exp_elem)))
            function.log_capture(f'{tab_name} tab loaded')
            time.sleep(3)
        except Exception as e:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'Exception while loading {tab_name} tab')
            function.log_capture("Exception while loading %s tab" % tab_name)
            function.log_capture("Python Says:")
            function.log_capture(e)
            function.log_capture("Failing Test...")
            cls.fail()

    @staticmethod
    def send_keys_to_field(cls, driver, field_name, field_xpath, keys, testcase_key):
        try:
            driver.find_element(By.XPATH, field_xpath).click()
            time.sleep(2)
            driver.find_element(By.XPATH, field_xpath).clear()
            time.sleep(1)
            driver.find_element(By.XPATH, field_xpath).send_keys(keys)
            function.log_capture(f'Data entered in {field_name} field')
        except Exception as e:
            zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                    zephyr_settings.cycle_key, "Fail",
                                    f'Exception in entering data in to {field_name}')
            function.log_capture(f'Exception in entering data in to {field_name}')
            function.log_capture("Python Says:")
            function.log_capture(e)
            function.log_capture("Failing Test...")
            cls.fail()

    @staticmethod
    def get_table_column(driver, rows_locator, col_locator):
        """Function to return all elements of a table column"""
        col = []
        counter = 1
        table_rows = driver.find_elements(By.XPATH, rows_locator)
        for row in table_rows:
            column_elem = driver.find_element(By.XPATH, f'//tr[{counter}]/td[{col_locator}]').text
            counter = counter + 1
            col.append(column_elem)
        return col

    @staticmethod
    def log_capture(log_detail):
        s = str(log_detail) + "\n"
        to_render = s.replace("\n", "<br />")
        print(to_render)
        print("-------------------------------------------------------------------------------")

    @staticmethod
    def check_overlap(self, elem1, elem2, elem1_name, elem2_name):
        try:

            elem1_loc_x = elem1.location.get('x')
            elem1_w = elem1.size.get('width')

            elem2_loc_x = elem2.location.get('x')
            elem2_w = elem2.size.get('width')

            elem1_coordinate_x = elem1_loc_x + elem1_w
            elem2_coordinate_x = elem2_loc_x + elem2_w

            if elem1_coordinate_x < elem2_coordinate_x:
                function.log_capture(f'No overlap between {elem1_name} & {elem2_name}')
            else:
                function.log_capture(f'{elem1_name} and {elem2_name} buttons overlap')
                assert False

        except Exception as e:
            function.log_capture(e)
            function.log_capture("elem1 and elem2 overlap. GUI Test Failed")
            assert False

    def slack_test_start_msg(browser):
        """Posts the completion message once the test cycle is complete."""
        now = datetime.now().strftime('%d-%b-%Y')
        blocks = BlockMaker()
        text_block = blocks.create_text_block(
            f"{now} -> *Running Cross browser testing* for *Edit* application on *{browser}* browser...")
        block_list = [text_block]
        slack.post_blocks(block_list)

    @staticmethod
    def slack_initial_message() -> str:
        """Post the message when the AXE cycle in Zephyr has begun executing.

           Make sure that the 'test bot' is added to your channel you wish
           to post the messages to.

           Returns the message 'ts' to apply threads to.
        """

        message = slack.post_message(
            f"Expand below :point_down: thread to see *testing* report.")
        ts = message.data['ts']
        return ts

    def slack_test_summary_msg(ts):
        blocks = BlockMaker()
        context_block = blocks.create_context_block(
            "*To view the report: double click to expand it or download then open it in your browser.*")
        block_list = [context_block]
        slack.post_blocks(block_list, ts)

    def slack_upload_report(report_path: str, report_name: str, ts: str) -> dict:
        """Upload the report file in to the thread."""
        return slack.upload_file(report_path, report_name, ts)

    def slack_test_complete_msg(ts):
        """Posts the completion message once the test cycle is complete."""
        blocks = BlockMaker()
        text_block = blocks.create_text_block(f"Testing complete on selected browser!")
        block_list = [text_block]
        slack.post_blocks(block_list, ts)

    @staticmethod
    def get_test_report_data(report_file_path='default'):
        """get test report data from pytest_report.html or pytest_report.txt or from user provided file"""
        if report_file_path == 'default':
            # To generate pytest_report.html file use following command e.g. py.test --html = Reports/Edit_cross_browser.html
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Reports',
                                                            'Edit_cross_browser'))  # Change report file name &amp; address here
        else:
            test_report_file = report_file_path
        # check file exist or not
        if not os.path.exists(test_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file" % test_report_file)

        with open(test_report_file, "r") as in_file:
            testdata = ""
            for line in in_file:
                testdata = testdata + '\n' + line
        return testdata
